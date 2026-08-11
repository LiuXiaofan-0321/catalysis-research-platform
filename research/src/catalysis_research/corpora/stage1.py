from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from catalysis_research.kg.freeze_stage1 import (
    canonical_hash,
    canonical_json,
    compact_text,
    document_key_for,
    sha256_bytes,
    sha256_file,
    source_topic_for,
)
from catalysis_research.provenance.run_manifest import inspect_git_state


CORPUS_SCHEMA_VERSION = "stage1_corpus.v1"
CORPUS_FREEZER_VERSION = "stage1_corpus_freezer.v1"


class CorpusError(RuntimeError):
    """Raised when a literature corpus cannot be frozen or verified."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for row in rows:
            output.write(canonical_json(row))
            output.write("\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def _require_tracked_archive(
    archive_path: Path,
    repository_root: Path,
) -> None:
    repository_root = repository_root.resolve()
    archive_path = archive_path.resolve()
    try:
        relative_path = archive_path.relative_to(repository_root)
    except ValueError as error:
        raise CorpusError("Corpus archive must be inside the repository") from error
    tracked = subprocess.run(
        [
            "git",
            "ls-files",
            "--error-unmatch",
            "--",
            relative_path.as_posix(),
        ],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if tracked.returncode != 0:
        raise CorpusError("Corpus archive must be committed before freezing")


def _normalize_title(value: Any) -> str:
    return re.sub(r"\W+", "", str(value or "").lower(), flags=re.UNICODE)


def _paper_inventory(
    *,
    archive_path: Path,
    allowed_systems: set[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with zipfile.ZipFile(archive_path) as archive:
        try:
            dataset_manifest = json.loads(
                archive.read("dataset-manifest.json").decode("utf-8")
            )
        except KeyError as error:
            raise CorpusError(
                "Stage 1 archive is missing dataset-manifest.json"
            ) from error
        entries = sorted(
            (
                entry
                for entry in archive.infolist()
                if entry.filename.startswith("json/")
                and entry.filename.lower().endswith(".json")
            ),
            key=lambda entry: entry.filename,
        )
        papers: list[dict[str, Any]] = []
        for entry in entries:
            raw_json = archive.read(entry)
            try:
                artifact = json.loads(raw_json.decode("utf-8"))
            except json.JSONDecodeError as error:
                raise CorpusError(
                    f"Invalid Stage 1 JSON: {entry.filename}"
                ) from error
            extraction = artifact.get("extraction") or {}
            paper = extraction.get("paper") or {}
            source = artifact.get("source") or {}
            system = compact_text(
                paper.get("catalysis_system"),
                80,
            ).lower()
            if system not in allowed_systems:
                continue
            paper_id = compact_text(paper.get("id"), 400) or document_key_for(
                paper,
                source,
            )
            source_path = compact_text(
                paper.get("source_path") or source.get("path"),
                900,
            )
            metadata = extraction.get("extraction_metadata") or {}
            papers.append(
                {
                    "paper_id": paper_id,
                    "archive_entry": entry.filename,
                    "title": compact_text(paper.get("title"), 600),
                    "doi": compact_text(paper.get("doi"), 240) or None,
                    "year": paper.get("year"),
                    "journal": compact_text(
                        paper.get("journal"),
                        300,
                    )
                    or None,
                    "paper_type": compact_text(
                        paper.get("paper_type"),
                        80,
                    )
                    or "unknown",
                    "catalysis_system": system,
                    "reaction_categories": paper.get(
                        "reaction_categories"
                    )
                    or [],
                    "source_topic": source_topic_for(source_path),
                    "source_path": source_path,
                    "raw_pdf_sha256": compact_text(
                        paper.get("source_pdf_sha256")
                        or source.get("source_pdf_sha256"),
                        128,
                    ),
                    "structured_json_sha256": sha256_bytes(raw_json),
                    "extracted_text_sha256": compact_text(
                        metadata.get("extracted_text_sha256")
                        or source.get("extracted_text_sha256"),
                        128,
                    ),
                    "extraction_schema_version": compact_text(
                        extraction.get("schema_version"),
                        160,
                    ),
                    "extraction_prompt_version": compact_text(
                        metadata.get("prompt_version"),
                        240,
                    ),
                    "extraction_model": compact_text(
                        metadata.get("model"),
                        240,
                    ),
                    "extracted_at": compact_text(
                        metadata.get("extracted_at"),
                        100,
                    ),
                }
            )
    return papers, dataset_manifest


def _validate_paper_inventory(
    papers: list[dict[str, Any]],
    expected_papers: int,
) -> None:
    if len(papers) != expected_papers:
        raise CorpusError(
            f"Expected {expected_papers} papers, found {len(papers)}"
        )
    identity_fields = {
        "paper_id": lambda paper: paper["paper_id"],
        "raw PDF SHA256": lambda paper: paper["raw_pdf_sha256"],
        "DOI": lambda paper: str(paper.get("doi") or "").lower(),
        "title-year": lambda paper: (
            f"{_normalize_title(paper.get('title'))}|{paper.get('year') or ''}"
        ),
    }
    for label, identity in identity_fields.items():
        values = [identity(paper) for paper in papers]
        if label == "DOI":
            values = [value for value in values if value]
        if len(values) != len(set(values)):
            raise CorpusError(f"Duplicate {label} detected")
    if any(not paper["raw_pdf_sha256"] for paper in papers):
        raise CorpusError("Every paper must have a raw PDF SHA256")


def _corpus_identity(
    *,
    corpus_id: str,
    archive_sha256: str,
    artifact_files: dict[str, Any],
) -> dict[str, Any]:
    return {
        "corpus_id": corpus_id,
        "archive_sha256": archive_sha256,
        "artifact_files": artifact_files,
        "freezer_version": CORPUS_FREEZER_VERSION,
    }


def freeze_stage1_corpus(
    *,
    archive_path: Path,
    output_directory: Path,
    corpus_id: str,
    domain: str,
    expected_papers: int,
    allowed_systems: set[str],
    repository_root: Path,
    expected_archive_sha256: str | None = None,
    frozen_at: str | None = None,
    allow_dirty: bool = False,
    git_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    archive_path = archive_path.resolve()
    output_directory = output_directory.resolve()
    repository_root = repository_root.resolve()
    if output_directory.exists():
        raise FileExistsError(
            "Corpus directory already exists and will not be overwritten: "
            f"{output_directory}"
        )
    _require_tracked_archive(archive_path, repository_root)
    state = git_state or inspect_git_state(repository_root)
    if state.get("dirty") and not allow_dirty:
        raise CorpusError(
            "Refusing to freeze a corpus from a dirty Git worktree"
        )
    archive_sha256 = sha256_file(archive_path)
    if (
        expected_archive_sha256 is not None
        and archive_sha256 != expected_archive_sha256.lower()
    ):
        raise CorpusError("Corpus archive SHA256 does not match configuration")

    papers, dataset_manifest = _paper_inventory(
        archive_path=archive_path,
        allowed_systems=allowed_systems,
    )
    _validate_paper_inventory(papers, expected_papers)
    paper_ids = [paper["paper_id"] for paper in papers]
    distributions = {
        "year": dict(
            sorted(
                Counter(
                    str(paper.get("year") or "unknown")
                    for paper in papers
                ).items()
            )
        ),
        "source_topic": dict(
            sorted(
                Counter(paper["source_topic"] for paper in papers).items()
            )
        ),
        "paper_type": dict(
            sorted(
                Counter(paper["paper_type"] for paper in papers).items()
            )
        ),
    }

    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(
            prefix=f".{output_directory.name}-",
            dir=output_directory.parent,
        )
    )
    try:
        paper_ids_path = temporary_root / "paper_ids.txt"
        papers_path = temporary_root / "papers.jsonl"
        paper_ids_path.write_text(
            "".join(f"{paper_id}\n" for paper_id in paper_ids),
            encoding="utf-8",
            newline="\n",
        )
        _write_jsonl(papers_path, papers)
        artifacts = {
            "paper_ids": {
                "path": "paper_ids.txt",
                "sha256": sha256_file(paper_ids_path),
                "count": len(paper_ids),
            },
            "papers": {
                "path": "papers.jsonl",
                "sha256": sha256_file(papers_path),
                "count": len(papers),
            },
        }
        try:
            source_path = archive_path.relative_to(repository_root).as_posix()
        except ValueError:
            source_path = str(archive_path).replace("\\", "/")
        manifest = {
            "schema_version": CORPUS_SCHEMA_VERSION,
            "corpus_id": corpus_id,
            "domain": domain,
            "status": "frozen",
            "frozen_at": frozen_at or utc_now(),
            "corpus_content_hash": canonical_hash(
                _corpus_identity(
                    corpus_id=corpus_id,
                    archive_sha256=archive_sha256,
                    artifact_files=artifacts,
                )
            ),
            "source_archive": {
                "path": source_path,
                "sha256": archive_sha256,
                "bytes": archive_path.stat().st_size,
                "dataset_manifest": dataset_manifest,
            },
            "paper_count": len(papers),
            "paper_id_hash": canonical_hash(paper_ids),
            "raw_pdf_hash_count": len(
                {paper["raw_pdf_sha256"] for paper in papers}
            ),
            "structured_json_hash_count": len(
                {paper["structured_json_sha256"] for paper in papers}
            ),
            "distributions": distributions,
            "artifacts": artifacts,
            "generation": {
                "freezer_version": CORPUS_FREEZER_VERSION,
                "code": state,
                "allowed_systems": sorted(allowed_systems),
                "paper_ordering": "lexicographic ZIP entry path",
                "deduplication_identity": [
                    "paper_id",
                    "doi",
                    "raw_pdf_sha256",
                    "normalized_title_year",
                ],
                "downstream_label_access": "forbidden",
                "overwrite_policy": "forbidden",
            },
        }
        _write_json(temporary_root / "manifest.json", manifest)
        temporary_root.replace(output_directory)
        return manifest
    except BaseException:
        shutil.rmtree(temporary_root, ignore_errors=True)
        raise


def verify_stage1_corpus(corpus_directory: Path) -> dict[str, Any]:
    corpus_directory = corpus_directory.resolve()
    failures: list[str] = []
    manifest_path = corpus_directory / "manifest.json"
    if not manifest_path.is_file():
        return {
            "corpus_id": corpus_directory.name,
            "valid": False,
            "failures": ["Corpus manifest does not exist"],
        }
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "corpus_id": corpus_directory.name,
            "valid": False,
            "failures": ["Corpus manifest is invalid JSON"],
        }
    if not isinstance(manifest, dict):
        return {
            "corpus_id": corpus_directory.name,
            "valid": False,
            "failures": ["Corpus manifest must be an object"],
        }
    if manifest.get("schema_version") != CORPUS_SCHEMA_VERSION:
        failures.append("Unsupported corpus schema version")
    if manifest.get("corpus_id") != corpus_directory.name:
        failures.append("Corpus ID does not match directory name")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        failures.append("Corpus artifacts must be an object")
        artifacts = {}
    for name, artifact in artifacts.items():
        if not isinstance(artifact, dict):
            failures.append(f"Invalid corpus artifact: {name}")
            continue
        path = corpus_directory / str(artifact.get("path", ""))
        if not path.is_file():
            failures.append(f"Missing corpus artifact: {name}")
            continue
        if sha256_file(path) != artifact.get("sha256"):
            failures.append(f"Corpus artifact hash mismatch: {name}")

    expected_content_hash = canonical_hash(
        _corpus_identity(
            corpus_id=str(manifest.get("corpus_id")),
            archive_sha256=str(
                (manifest.get("source_archive") or {}).get("sha256")
            ),
            artifact_files=artifacts,
        )
    )
    if expected_content_hash != manifest.get("corpus_content_hash"):
        failures.append("Corpus content hash mismatch")

    papers_path = corpus_directory / str(
        (artifacts.get("papers") or {}).get("path", "papers.jsonl")
    )
    paper_ids_path = corpus_directory / str(
        (artifacts.get("paper_ids") or {}).get(
            "path",
            "paper_ids.txt",
        )
    )
    papers = _read_jsonl(papers_path) if papers_path.is_file() else []
    paper_ids = (
        [
            line.strip()
            for line in paper_ids_path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]
        if paper_ids_path.is_file()
        else []
    )
    if len(papers) != manifest.get("paper_count"):
        failures.append("Corpus paper count mismatch")
    if paper_ids != [paper.get("paper_id") for paper in papers]:
        failures.append("Corpus paper ID ordering mismatch")
    if canonical_hash(paper_ids) != manifest.get("paper_id_hash"):
        failures.append("Corpus paper ID hash mismatch")
    try:
        _validate_paper_inventory(papers, int(manifest.get("paper_count", 0)))
    except CorpusError as error:
        failures.append(str(error))

    repository_root = next(
        (
            parent
            for parent in (corpus_directory, *corpus_directory.parents)
            if (parent / ".git").exists()
        ),
        None,
    )
    source_archive_valid: bool | None = None
    if repository_root is not None:
        source_record = manifest.get("source_archive") or {}
        source_path = repository_root / str(source_record.get("path", ""))
        if source_path.is_file():
            source_archive_valid = (
                sha256_file(source_path) == source_record.get("sha256")
            )
            if not source_archive_valid:
                failures.append("Corpus source archive hash mismatch")

    return {
        "corpus_id": manifest.get("corpus_id"),
        "valid": not failures,
        "failures": failures,
        "corpus_content_hash": manifest.get("corpus_content_hash"),
        "paper_count": manifest.get("paper_count"),
        "source_archive_valid": source_archive_valid,
    }
