from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from catalysis_research.corpora.stage1 import verify_stage1_corpus
from catalysis_research.provenance.run_manifest import inspect_git_state

from .freeze_stage1 import (
    canonical_hash,
    canonical_json,
    freeze_stage1_archive,
    sha256_file,
    verify_snapshot,
)
from .selection import (
    SELECTION_ALGORITHM_VERSION,
    SELECTION_SCHEMA_VERSION,
    SelectionError,
    build_nested_order,
    prefix_hash,
    selection_order_hash,
)


NESTED_MANIFEST_SCHEMA_VERSION = "nested_kg_manifest.v1"
NESTED_BUILDER_VERSION = "nested_stage1_builder.v1"


class NestedSnapshotError(RuntimeError):
    """Raised when nested KG snapshots cannot be built or verified."""


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise NestedSnapshotError(f"Expected JSON object: {path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for row in rows:
            output.write(canonical_json(row))
            output.write("\n")


def _repository_path(repository_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repository_root / path


def _relative(repository_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repository_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def _load_build_inputs(
    config_path: Path,
    repository_root: Path,
) -> tuple[dict[str, Any], Path, dict[str, Any], list[dict[str, Any]]]:
    config = _read_json(config_path)
    if config.get("schema_version") != "nested_kg_build_config.v1":
        raise NestedSnapshotError("Unsupported nested KG build config")
    corpus_directory = _repository_path(
        repository_root,
        str(config["corpus_directory"]),
    )
    corpus_report = verify_stage1_corpus(corpus_directory)
    if not corpus_report["valid"]:
        raise NestedSnapshotError(
            "Frozen corpus is invalid: "
            + "; ".join(corpus_report["failures"])
        )
    corpus_manifest = _read_json(corpus_directory / "manifest.json")
    papers = _read_jsonl(corpus_directory / "papers.jsonl")
    if corpus_manifest["paper_count"] != len(papers):
        raise NestedSnapshotError("Frozen corpus paper count mismatch")
    if config["corpus_id"] != corpus_manifest["corpus_id"]:
        raise NestedSnapshotError("Configured corpus ID does not match")
    if (
        config["corpus_content_hash"]
        != corpus_manifest["corpus_content_hash"]
    ):
        raise NestedSnapshotError(
            "Configured corpus content hash does not match"
        )
    archive_path = _repository_path(
        repository_root,
        str(config["source_archive"]),
    )
    if not archive_path.is_file():
        raise NestedSnapshotError("Configured source archive does not exist")
    if sha256_file(archive_path) != config["source_archive_sha256"]:
        raise NestedSnapshotError("Configured source archive hash mismatch")
    if (
        corpus_manifest["source_archive"]["sha256"]
        != config["source_archive_sha256"]
    ):
        raise NestedSnapshotError("Corpus/source archive hash mismatch")
    return config, corpus_directory, corpus_manifest, papers


def build_nested_snapshots(
    *,
    config_path: Path,
    repository_root: Path,
    allow_dirty: bool = False,
    frozen_at: str | None = None,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    config_path = config_path.resolve()
    state = inspect_git_state(repository_root)
    if state["dirty"] and not allow_dirty:
        raise NestedSnapshotError(
            "Refusing to build nested snapshots from a dirty Git worktree"
        )
    config, corpus_directory, corpus_manifest, papers = _load_build_inputs(
        config_path,
        repository_root,
    )
    selection_config = config["selection"]
    if selection_config.get("selection_schema_version") != (
        SELECTION_SCHEMA_VERSION
    ):
        raise NestedSnapshotError("Selection schema version mismatch")
    if selection_config.get("algorithm_version") != (
        SELECTION_ALGORITHM_VERSION
    ):
        raise NestedSnapshotError("Selection algorithm version mismatch")
    order = build_nested_order(papers, selection_config)
    order_hash = selection_order_hash(order)

    snapshots_root = _repository_path(
        repository_root,
        str(config["snapshots_root"]),
    )
    nested_manifest_path = _repository_path(
        repository_root,
        str(config["nested_manifest"]),
    )
    order_path = _repository_path(
        repository_root,
        str(config["selection_order_artifact"]),
    )
    destinations = [
        snapshots_root / str(level["snapshot_id"])
        for level in selection_config["levels"]
    ] + [nested_manifest_path, order_path]
    existing = [path for path in destinations if path.exists()]
    if existing:
        raise FileExistsError(
            "Nested KG outputs already exist and will not be overwritten: "
            + ", ".join(str(path) for path in existing)
        )

    timestamp = frozen_at or datetime.now(timezone.utc).isoformat()
    staging_root = Path(
        tempfile.mkdtemp(
            prefix=f".{config['nested_snapshot_id']}-",
            dir=snapshots_root.parent,
        )
    )
    staged_snapshots = staging_root / "snapshots"
    staged_order = staging_root / order_path.name
    staged_manifest = staging_root / nested_manifest_path.name
    moved: list[Path] = []
    try:
        _write_jsonl(staged_order, order)
        level_records: list[dict[str, Any]] = []
        for level in selection_config["levels"]:
            knowledge_level = str(level["knowledge_level"])
            count = int(level["paper_count"])
            prefix = order[:count]
            snapshot_id = str(level["snapshot_id"])
            selection_record = {
                "selection_id": selection_config["selection_id"],
                "selection_schema_version": SELECTION_SCHEMA_VERSION,
                "algorithm_version": SELECTION_ALGORITHM_VERSION,
                "seed": selection_config["seed"],
                "stratification_fields": [
                    "source_topic",
                    "year_bin",
                    "paper_type_group",
                ],
                "full_order_hash": order_hash,
                "prefix_count": count,
                "paper_id_prefix_hash": prefix_hash(
                    order,
                    count,
                    "paper_id",
                ),
                "archive_entry_prefix_hash": prefix_hash(
                    order,
                    count,
                    "archive_entry",
                ),
                "downstream_label_access": "forbidden",
                "performance_based_reordering": "forbidden",
            }
            coverage = {
                "status": "not_measured",
                "reason": (
                    "No eligible public predictive dataset has been frozen"
                ),
            }
            snapshot_manifest = freeze_stage1_archive(
                archive_path=_repository_path(
                    repository_root,
                    str(config["source_archive"]),
                ),
                output_directory=staged_snapshots / snapshot_id,
                snapshot_id=snapshot_id,
                knowledge_level=knowledge_level,
                domain=str(config["domain"]),
                expected_papers=count,
                allowed_systems=set(config["allowed_systems"]),
                repository_root=repository_root,
                ontology_version=str(config["ontology_version"]),
                frozen_at=timestamp,
                selected_entries={
                    str(item["archive_entry"]) for item in prefix
                },
                git_state=state,
                corpus={
                    "corpus_id": corpus_manifest["corpus_id"],
                    "corpus_content_hash": corpus_manifest[
                        "corpus_content_hash"
                    ],
                    "manifest": _relative(
                        repository_root,
                        corpus_directory / "manifest.json",
                    ),
                },
                selection=selection_record,
                coverage=coverage,
            )
            level_records.append(
                {
                    "knowledge_level": knowledge_level,
                    "paper_fraction": level["paper_fraction"],
                    "paper_count": count,
                    "snapshot_id": snapshot_id,
                    "snapshot_path": _relative(
                        repository_root,
                        snapshots_root / snapshot_id,
                    ),
                    "snapshot_content_hash": snapshot_manifest[
                        "snapshot_content_hash"
                    ],
                    "paper_id_prefix_hash": selection_record[
                        "paper_id_prefix_hash"
                    ],
                    "archive_entry_prefix_hash": selection_record[
                        "archive_entry_prefix_hash"
                    ],
                }
            )

        order_artifact = {
            "path": _relative(repository_root, order_path),
            "sha256": sha256_file(staged_order),
            "count": len(order),
            "selection_order_hash": order_hash,
        }
        identity = {
            "nested_snapshot_id": config["nested_snapshot_id"],
            "source_archive_sha256": config["source_archive_sha256"],
            "corpus_content_hash": corpus_manifest["corpus_content_hash"],
            "config_sha256": sha256_file(config_path),
            "selection_order": order_artifact,
            "levels": level_records,
            "builder_version": NESTED_BUILDER_VERSION,
        }
        nested_manifest = {
            "schema_version": NESTED_MANIFEST_SCHEMA_VERSION,
            "nested_snapshot_id": config["nested_snapshot_id"],
            "status": "frozen",
            "frozen_at": timestamp,
            "nested_content_hash": canonical_hash(identity),
            "domain": config["domain"],
            "source_archive": {
                "path": _relative(
                    repository_root,
                    _repository_path(
                        repository_root,
                        str(config["source_archive"]),
                    ),
                ),
                "sha256": config["source_archive_sha256"],
            },
            "corpus": {
                "corpus_id": corpus_manifest["corpus_id"],
                "corpus_content_hash": corpus_manifest[
                    "corpus_content_hash"
                ],
                "manifest": _relative(
                    repository_root,
                    corpus_directory / "manifest.json",
                ),
            },
            "selection": {
                "selection_id": selection_config["selection_id"],
                "selection_schema_version": SELECTION_SCHEMA_VERSION,
                "algorithm_version": SELECTION_ALGORITHM_VERSION,
                "seed": selection_config["seed"],
                "year_bins": selection_config["year_bins"],
                "paper_type_groups": selection_config[
                    "paper_type_groups"
                ],
                "paper_type_fallback": selection_config[
                    "paper_type_fallback"
                ],
                "topic_source_rule": selection_config[
                    "topic_source_rule"
                ],
                "nesting_rule": "exact prefixes of one frozen full order",
                "downstream_label_access": "forbidden",
                "performance_based_reordering": "forbidden",
            },
            "selection_order": order_artifact,
            "levels": level_records,
            "coverage": {
                "status": "not_measured",
                "reason": (
                    "No eligible public predictive dataset has been frozen"
                ),
            },
            "generation": {
                "builder_version": NESTED_BUILDER_VERSION,
                "config": _relative(repository_root, config_path),
                "config_sha256": sha256_file(config_path),
                "code": state,
                "overwrite_policy": "forbidden",
                "private_data_access": "forbidden",
            },
        }
        _write_json(staged_manifest, nested_manifest)

        snapshots_root.mkdir(parents=True, exist_ok=True)
        for level in selection_config["levels"]:
            snapshot_id = str(level["snapshot_id"])
            destination = snapshots_root / snapshot_id
            (staged_snapshots / snapshot_id).replace(destination)
            moved.append(destination)
        order_path.parent.mkdir(parents=True, exist_ok=True)
        staged_order.replace(order_path)
        moved.append(order_path)
        nested_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        staged_manifest.replace(nested_manifest_path)
        moved.append(nested_manifest_path)
        return nested_manifest
    except BaseException:
        for path in reversed(moved):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            elif path.exists():
                path.unlink()
        raise
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)


def verify_nested_snapshots(
    *,
    manifest_path: Path,
    repository_root: Path,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    manifest_path = manifest_path.resolve()
    failures: list[str] = []
    try:
        manifest = _read_json(manifest_path)
    except (OSError, json.JSONDecodeError, NestedSnapshotError) as error:
        return {
            "nested_snapshot_id": manifest_path.stem,
            "valid": False,
            "failures": [str(error)],
        }
    if manifest.get("schema_version") != NESTED_MANIFEST_SCHEMA_VERSION:
        failures.append("Unsupported nested manifest schema version")

    order_record = manifest.get("selection_order") or {}
    order_path = _repository_path(
        repository_root,
        str(order_record.get("path", "")),
    )
    order: list[dict[str, Any]] = []
    if not order_path.is_file():
        failures.append("Selection order artifact is missing")
    else:
        if sha256_file(order_path) != order_record.get("sha256"):
            failures.append("Selection order artifact hash mismatch")
        try:
            order = _read_jsonl(order_path)
        except (OSError, json.JSONDecodeError):
            failures.append("Selection order artifact is invalid")
        if order:
            try:
                actual_order_hash = selection_order_hash(order)
            except (KeyError, TypeError, SelectionError):
                failures.append("Selection order records are malformed")
            else:
                if actual_order_hash != order_record.get(
                    "selection_order_hash"
                ):
                    failures.append("Selection order content hash mismatch")
        if len(order) != order_record.get("count"):
            failures.append("Selection order count mismatch")
        if [item.get("selection_rank") for item in order] != list(
            range(1, len(order) + 1)
        ):
            failures.append("Selection ranks are not contiguous")

    prior_ids: set[str] = set()
    level_reports: list[dict[str, Any]] = []
    for level in manifest.get("levels") or []:
        count = int(level.get("paper_count", 0))
        snapshot_path = _repository_path(
            repository_root,
            str(level.get("snapshot_path", "")),
        )
        try:
            report = verify_snapshot(snapshot_path)
        except (OSError, json.JSONDecodeError, KeyError) as error:
            report = {
                "snapshot_id": level.get("snapshot_id"),
                "valid": False,
                "failures": [str(error)],
            }
        level_reports.append(report)
        if not report["valid"]:
            failures.append(
                f"{level.get('snapshot_id')} failed snapshot verification"
            )
        if report.get("snapshot_content_hash") != level.get(
            "snapshot_content_hash"
        ):
            failures.append(
                f"{level.get('snapshot_id')} content hash mismatch"
            )
        snapshot_manifest_path = snapshot_path / "manifest.json"
        if snapshot_manifest_path.is_file():
            snapshot_manifest = _read_json(snapshot_manifest_path)
            snapshot_selection = snapshot_manifest.get("selection") or {}
            if snapshot_selection.get("full_order_hash") != (
                order_record.get("selection_order_hash")
            ):
                failures.append(
                    f"{level.get('snapshot_id')} selection order mismatch"
                )
            if snapshot_selection.get("prefix_count") != count:
                failures.append(
                    f"{level.get('snapshot_id')} selection count mismatch"
                )
            if snapshot_selection.get("paper_id_prefix_hash") != (
                level.get("paper_id_prefix_hash")
            ):
                failures.append(
                    f"{level.get('snapshot_id')} selection hash mismatch"
                )
        paper_ids_path = snapshot_path / "paper_ids.txt"
        snapshot_ids = (
            {
                line.strip()
                for line in paper_ids_path.read_text(
                    encoding="utf-8"
                ).splitlines()
                if line.strip()
            }
            if paper_ids_path.is_file()
            else set()
        )
        try:
            expected_ids = {
                str(item["paper_id"]) for item in order[:count]
            }
        except (KeyError, TypeError):
            expected_ids = set()
            failures.append("Selection order paper IDs are malformed")
        if snapshot_ids != expected_ids:
            failures.append(
                f"{level.get('snapshot_id')} is not the expected prefix"
            )
        if prior_ids and not prior_ids < snapshot_ids:
            failures.append(
                f"{level.get('snapshot_id')} is not a strict superset"
            )
        prior_ids = snapshot_ids
        if order:
            try:
                paper_prefix_hash = prefix_hash(
                    order,
                    count,
                    "paper_id",
                )
                entry_prefix_hash = prefix_hash(
                    order,
                    count,
                    "archive_entry",
                )
            except (KeyError, TypeError):
                failures.append("Selection order prefixes are malformed")
            else:
                if paper_prefix_hash != level.get(
                    "paper_id_prefix_hash"
                ):
                    failures.append(
                        f"{level.get('snapshot_id')} paper prefix hash "
                        "mismatch"
                    )
                if entry_prefix_hash != level.get(
                    "archive_entry_prefix_hash"
                ):
                    failures.append(
                        f"{level.get('snapshot_id')} entry prefix hash "
                        "mismatch"
                    )

    source = manifest.get("source_archive") or {}
    source_path = _repository_path(
        repository_root,
        str(source.get("path", "")),
    )
    if not source_path.is_file():
        failures.append("Source archive is missing")
    elif sha256_file(source_path) != source.get("sha256"):
        failures.append("Source archive hash mismatch")

    corpus = manifest.get("corpus") or {}
    corpus_manifest_path = _repository_path(
        repository_root,
        str(corpus.get("manifest", "")),
    )
    if not corpus_manifest_path.is_file():
        failures.append("Corpus manifest is missing")
    else:
        corpus_report = verify_stage1_corpus(corpus_manifest_path.parent)
        if not corpus_report["valid"]:
            failures.append("Frozen corpus failed verification")
        if corpus_report.get("corpus_content_hash") != corpus.get(
            "corpus_content_hash"
        ):
            failures.append("Corpus content hash mismatch")

    generation = manifest.get("generation") or {}
    config_path = _repository_path(
        repository_root,
        str(generation.get("config", "")),
    )
    config_hash = (
        sha256_file(config_path) if config_path.is_file() else None
    )
    if config_hash != generation.get("config_sha256"):
        failures.append("Nested build config hash mismatch")
    identity = {
        "nested_snapshot_id": manifest.get("nested_snapshot_id"),
        "source_archive_sha256": source.get("sha256"),
        "corpus_content_hash": corpus.get("corpus_content_hash"),
        "config_sha256": generation.get("config_sha256"),
        "selection_order": order_record,
        "levels": manifest.get("levels"),
        "builder_version": generation.get("builder_version"),
    }
    if canonical_hash(identity) != manifest.get("nested_content_hash"):
        failures.append("Nested manifest content hash mismatch")

    return {
        "nested_snapshot_id": manifest.get("nested_snapshot_id"),
        "valid": not failures,
        "failures": failures,
        "level_count": len(level_reports),
        "levels": level_reports,
        "selection_order_hash": order_record.get("selection_order_hash"),
    }
