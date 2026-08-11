from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from catalysis_research.provenance.run_manifest import inspect_git_state

from .loader import index_rows, is_missing, load_manifest_rows
from .registry import (
    load_dataset_manifest,
    require_tracked_file,
    verify_dataset_manifest,
)
from .schema import (
    IID_SPLIT_RATIOS,
    SPLIT_MANIFEST_SCHEMA_VERSION,
    DatasetError,
    content_hash,
    manifest_hash,
    split_hash,
)


SPLIT_ALGORITHM_VERSION = "fixed_split.v1"
PARTITION_ORDER = ("train", "validation", "test")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise DatasetError(f"Frozen split manifest already exists: {path}")
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as output:
            json.dump(
                value,
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            raise DatasetError(f"Frozen split manifest already exists: {path}")
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def load_split_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise DatasetError(f"Split manifest does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise DatasetError(f"Invalid split manifest JSON: {path}") from error
    if not isinstance(value, dict):
        raise DatasetError("Split manifest must be a JSON object")
    return value


def _stable_hash(seed: int, stratum: str, key: str) -> str:
    payload = f"{seed}|{stratum}|{key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _duplicate_key(
    row: dict[str, Any],
    duplicate_columns: list[str],
) -> str:
    values = [row.get(column) for column in duplicate_columns]
    if any(is_missing(value) for value in values):
        raise DatasetError(
            "Cannot split rows with missing duplicate-key values"
        )
    return content_hash([str(value).strip() for value in values])


def _target_value(row: dict[str, Any], manifest: dict[str, Any]) -> Any:
    column = manifest["target"]["column"]
    value = row.get(column)
    if is_missing(value):
        raise DatasetError(f"Missing split target in column {column}")
    if manifest["target"]["task_type"] == "classification":
        return str(value).strip()
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise DatasetError("Regression target must be numeric") from error
    if not math.isfinite(number):
        raise DatasetError("Regression target must be finite")
    return number


def _atomic_units(
    rows: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    sample_column = manifest["sample_id_column"]
    duplicate_columns = list(manifest["duplicate_key_columns"])
    indexed = index_rows(rows, sample_column)
    units: dict[str, dict[str, Any]] = {}
    for identifier, row in indexed.items():
        key = _duplicate_key(row, duplicate_columns)
        unit = units.setdefault(
            key,
            {
                "key": key,
                "sample_ids": [],
                "targets": [],
            },
        )
        unit["sample_ids"].append(identifier)
        unit["targets"].append(_target_value(row, manifest))
    for unit in units.values():
        unit["sample_ids"].sort()
        if manifest["target"]["task_type"] == "classification":
            labels = set(unit["targets"])
            if len(labels) != 1:
                raise DatasetError(
                    "Duplicate group contains conflicting class labels"
                )
            unit["stratify_value"] = next(iter(labels))
        else:
            unit["stratify_value"] = sum(unit["targets"]) / len(
                unit["targets"]
            )
    return sorted(units.values(), key=lambda item: item["key"])


def _allocate_count(total: int) -> dict[str, int]:
    raw = {
        partition: total * IID_SPLIT_RATIOS[partition]
        for partition in PARTITION_ORDER
    }
    counts = {
        partition: math.floor(raw[partition])
        for partition in PARTITION_ORDER
    }
    remaining = total - sum(counts.values())
    ranked = sorted(
        PARTITION_ORDER,
        key=lambda partition: (
            -(raw[partition] - counts[partition]),
            PARTITION_ORDER.index(partition),
        ),
    )
    for partition in ranked[:remaining]:
        counts[partition] += 1
    return counts


def _stratified_units(
    units: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    if manifest["target"]["task_type"] == "classification":
        strata: dict[str, list[dict[str, Any]]] = {}
        for unit in units:
            strata.setdefault(
                f"class:{unit['stratify_value']}",
                [],
            ).append(unit)
        return strata

    quantiles = manifest["iid_split"].get(
        "stratify_target_quantiles"
    )
    if quantiles is None:
        return {"all": units}
    ordered = sorted(
        units,
        key=lambda item: (item["stratify_value"], item["key"]),
    )
    strata = {f"quantile:{index}": [] for index in range(quantiles)}
    for index, unit in enumerate(ordered):
        bucket = min(quantiles - 1, index * quantiles // len(ordered))
        strata[f"quantile:{bucket}"].append(unit)
    return {key: value for key, value in strata.items() if value}


def _ensure_nonempty_partitions(
    assignments: dict[str, list[dict[str, Any]]],
) -> None:
    if sum(len(values) for values in assignments.values()) < 3:
        raise DatasetError(
            "At least three duplicate-safe units are required for IID splitting"
        )
    for empty_partition in PARTITION_ORDER:
        if assignments[empty_partition]:
            continue
        donor = max(
            PARTITION_ORDER,
            key=lambda partition: len(assignments[partition]),
        )
        if len(assignments[donor]) <= 1:
            raise DatasetError("Cannot create non-empty IID partitions")
        assignments[empty_partition].append(assignments[donor].pop())


def _iid_membership(
    rows: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> dict[str, list[str]]:
    units = _atomic_units(rows, manifest)
    seed = manifest["iid_split"]["seed"]
    assignments = {partition: [] for partition in PARTITION_ORDER}
    for stratum, values in sorted(
        _stratified_units(units, manifest).items()
    ):
        ordered = sorted(
            values,
            key=lambda item: _stable_hash(seed, stratum, item["key"]),
        )
        counts = _allocate_count(len(ordered))
        cursor = 0
        for partition in PARTITION_ORDER:
            next_cursor = cursor + counts[partition]
            assignments[partition].extend(ordered[cursor:next_cursor])
            cursor = next_cursor
    _ensure_nonempty_partitions(assignments)
    return {
        partition: sorted(
            sample_id
            for unit in assignments[partition]
            for sample_id in unit["sample_ids"]
        )
        for partition in PARTITION_ORDER
    }


def _ood_folds(
    rows: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    sample_column = manifest["sample_id_column"]
    group_column = manifest["ood_split"]["group_column"]
    duplicate_columns = list(manifest["duplicate_key_columns"])
    indexed = index_rows(rows, sample_column)
    result: list[dict[str, Any]] = []
    for fold_config in manifest["ood_split"]["folds"]:
        test_groups = {str(value) for value in fold_config["test_groups"]}
        validation_groups = {
            str(value) for value in fold_config["validation_groups"]
        }
        partitions = {partition: [] for partition in PARTITION_ORDER}
        duplicate_partitions: dict[str, set[str]] = {}
        for identifier, row in indexed.items():
            group = str(row[group_column]).strip()
            if group in test_groups:
                partition = "test"
            elif group in validation_groups:
                partition = "validation"
            else:
                partition = "train"
            partitions[partition].append(identifier)
            key = _duplicate_key(row, duplicate_columns)
            duplicate_partitions.setdefault(key, set()).add(partition)
        crossing = [
            key
            for key, memberships in duplicate_partitions.items()
            if len(memberships) > 1
        ]
        if crossing:
            raise DatasetError(
                f"OOD fold {fold_config['fold_id']} separates duplicate rows"
            )
        if any(not partitions[partition] for partition in PARTITION_ORDER):
            raise DatasetError(
                f"OOD fold {fold_config['fold_id']} has an empty partition"
            )
        result.append(
            {
                "fold_id": fold_config["fold_id"],
                "test_groups": sorted(test_groups),
                "validation_groups": sorted(validation_groups),
                "partitions": {
                    partition: sorted(partitions[partition])
                    for partition in PARTITION_ORDER
                },
                "counts": {
                    partition: len(partitions[partition])
                    for partition in PARTITION_ORDER
                },
                "observed_ratios": {
                    partition: len(partitions[partition]) / len(indexed)
                    for partition in PARTITION_ORDER
                },
            }
        )
    return result


def _build_split_manifest(
    *,
    dataset_manifest: dict[str, Any],
    rows: list[dict[str, Any]],
    strategy: str,
    git_state: dict[str, Any],
    created_at: str,
) -> dict[str, Any]:
    if strategy not in {"iid", "ood"}:
        raise DatasetError("Split strategy must be iid or ood")
    split_id = (
        f"{dataset_manifest['dataset_id']}-{strategy}-"
        f"{dataset_manifest['version']}"
    )
    manifest: dict[str, Any] = {
        "schema_version": SPLIT_MANIFEST_SCHEMA_VERSION,
        "split_id": split_id,
        "dataset_id": dataset_manifest["dataset_id"],
        "dataset_version": dataset_manifest["version"],
        "dataset_content_hash": dataset_manifest["dataset_content_hash"],
        "strategy": strategy,
        "algorithm_version": SPLIT_ALGORITHM_VERSION,
        "created_at": created_at,
        "git_commit": git_state.get("commit"),
        "git_tree": git_state.get("tree"),
        "git_branch": git_state.get("branch"),
        "git_dirty": bool(git_state.get("dirty")),
        "configuration": copy.deepcopy(
            dataset_manifest[
                "iid_split" if strategy == "iid" else "ood_split"
            ]
        ),
        "sample_id_hash": dataset_manifest["sample_id_hash"],
        "row_count": dataset_manifest["row_count"],
        "partitions": None,
        "folds": None,
        "observed_ratios": None,
        "split_hash": "",
        "manifest_content_hash": "",
    }
    if strategy == "iid":
        partitions = _iid_membership(rows, dataset_manifest)
        manifest["partitions"] = partitions
        manifest["counts"] = {
            partition: len(partitions[partition])
            for partition in PARTITION_ORDER
        }
        manifest["observed_ratios"] = {
            partition: len(partitions[partition]) / len(rows)
            for partition in PARTITION_ORDER
        }
    else:
        manifest["folds"] = _ood_folds(rows, dataset_manifest)
        manifest["counts"] = None
    manifest["split_hash"] = split_hash(manifest)
    manifest["manifest_content_hash"] = manifest_hash(manifest)
    return manifest


def create_split(
    *,
    dataset_manifest_path: Path,
    strategy: str,
    output_root: Path,
    repository_root: Path,
    allow_dirty: bool = False,
    timestamp: str | None = None,
    git_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    dataset_manifest_path = require_tracked_file(
        repository_root=repository_root,
        path=dataset_manifest_path,
        required_directory="research/manifests/datasets",
        artifact_name="Dataset manifest",
    )
    dataset_report = verify_dataset_manifest(
        dataset_manifest_path,
        repository_root,
    )
    if not dataset_report["valid"]:
        raise DatasetError(
            "Dataset manifest failed verification: "
            + "; ".join(dataset_report["failures"])
        )
    dataset_manifest = load_dataset_manifest(dataset_manifest_path)
    state = git_state or inspect_git_state(repository_root)
    if state.get("dirty") and not allow_dirty:
        raise DatasetError(
            "Refusing to freeze a split from a dirty Git worktree"
        )
    if len(str(state.get("commit", ""))) != 40:
        raise DatasetError("Git state must contain a full commit hash")
    rows = load_manifest_rows(dataset_manifest, repository_root)
    manifest = _build_split_manifest(
        dataset_manifest=dataset_manifest,
        rows=rows,
        strategy=strategy,
        git_state=state,
        created_at=timestamp or utc_now(),
    )
    output_path = output_root.resolve() / f"{manifest['split_id']}.json"
    _atomic_write_json(output_path, manifest)
    return {
        "split_id": manifest["split_id"],
        "split_path": str(output_path),
        "manifest": manifest,
    }


def verify_split_manifest(
    *,
    split_manifest_path: Path,
    dataset_manifest_path: Path,
    repository_root: Path,
) -> dict[str, Any]:
    failures: list[str] = []
    try:
        split_manifest = load_split_manifest(split_manifest_path)
        dataset_manifest = load_dataset_manifest(dataset_manifest_path)
    except DatasetError as error:
        return {
            "split_id": split_manifest_path.stem,
            "valid": False,
            "failures": [str(error)],
        }

    if split_manifest.get("schema_version") != SPLIT_MANIFEST_SCHEMA_VERSION:
        failures.append("Unsupported split manifest schema version")
    if split_manifest_path.name != f"{split_manifest.get('split_id')}.json":
        failures.append("Split manifest filename does not match split_id")
    if manifest_hash(split_manifest) != split_manifest.get(
        "manifest_content_hash"
    ):
        failures.append("Split manifest content hash mismatch")
    if split_hash(split_manifest) != split_manifest.get("split_hash"):
        failures.append("Split content hash mismatch")
    if split_manifest.get("dataset_id") != dataset_manifest.get("dataset_id"):
        failures.append("Split dataset_id mismatch")
    if split_manifest.get(
        "dataset_content_hash"
    ) != dataset_manifest.get("dataset_content_hash"):
        failures.append("Split dataset content hash mismatch")

    dataset_report = verify_dataset_manifest(
        dataset_manifest_path,
        repository_root,
    )
    if not dataset_report["valid"]:
        failures.extend(
            f"Dataset verification: {failure}"
            for failure in dataset_report["failures"]
        )
    else:
        try:
            rows = load_manifest_rows(
                dataset_manifest,
                repository_root.resolve(),
            )
            rebuilt = _build_split_manifest(
                dataset_manifest=dataset_manifest,
                rows=rows,
                strategy=str(split_manifest.get("strategy")),
                git_state={
                    "commit": split_manifest.get("git_commit"),
                    "tree": split_manifest.get("git_tree"),
                    "branch": split_manifest.get("git_branch"),
                    "dirty": split_manifest.get("git_dirty"),
                },
                created_at=str(split_manifest.get("created_at")),
            )
        except DatasetError as error:
            failures.append(str(error))
        else:
            for field in (
                "split_id",
                "dataset_id",
                "dataset_version",
                "dataset_content_hash",
                "strategy",
                "algorithm_version",
                "configuration",
                "sample_id_hash",
                "row_count",
                "partitions",
                "folds",
                "counts",
                "observed_ratios",
                "split_hash",
            ):
                if split_manifest.get(field) != rebuilt.get(field):
                    failures.append(f"Split manifest mismatch: {field}")

    return {
        "split_id": split_manifest.get("split_id"),
        "strategy": split_manifest.get("strategy"),
        "valid": not failures,
        "failures": failures,
        "split_hash": split_manifest.get("split_hash"),
        "dataset_content_hash": split_manifest.get(
            "dataset_content_hash"
        ),
    }
