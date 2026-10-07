from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .hashing import atomic_write_json, canonical_json, content_hash, sha256_file
from .ledger import PipelineLedger, utc_now


INVENTORY_SCHEMA_VERSION = "literature_inventory.v2"


def _paths_from_manifest(path: Path) -> Iterable[tuple[Path, dict[str, Any]]]:
    if path.suffix.lower() == ".jsonl":
        payload: Any = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = payload.get("papers") or payload.get("documents") or []
    else:
        raise ValueError("Source manifest must contain a list of papers")
    if not isinstance(records, list):
        raise ValueError("Source manifest paper records must be a list")
    for record in records:
        if not isinstance(record, dict):
            continue
        raw_path = record.get("local_path") or record.get("path") or record.get("source_path")
        if not raw_path:
            continue
        candidate = Path(str(raw_path))
        if not candidate.is_absolute():
            candidate = (path.parent / candidate).resolve()
        yield candidate, record


def source_paths(source: Path) -> Iterable[tuple[Path, dict[str, Any]]]:
    source = source.resolve()
    if source.is_dir():
        for path in sorted(
            source.rglob("*.pdf"),
            key=lambda item: str(item).casefold(),
        ):
            yield path.resolve(), {}
        return
    if source.is_file() and source.suffix.lower() in {".pdf", ".md"}:
        yield source, {}
        return
    if source.is_file() and source.suffix.lower() in {".json", ".jsonl"}:
        yield from _paths_from_manifest(source)
        return
    raise FileNotFoundError(f"Unsupported literature source: {source}")


def build_inventory(
    *,
    source: Path,
    output_path: Path,
    ledger: PipelineLedger,
) -> dict[str, Any]:
    records_by_hash: dict[str, dict[str, Any]] = {}
    document_ids: dict[str, str] = {}
    missing: list[str] = []
    for path, metadata in source_paths(source):
        if not path.is_file():
            missing.append(str(path))
            continue
        digest = sha256_file(path)
        if digest in records_by_hash:
            records_by_hash[digest]["duplicate_paths"].append(str(path))
            continue
        canonical_paper_id = str(metadata.get("paper_id") or f"sha256:{digest}")
        document_id = str(metadata.get("document_id") or canonical_paper_id)
        prior_hash = document_ids.get(document_id)
        if prior_hash is not None and prior_hash != digest:
            raise ValueError(f"document_id maps to multiple files: {document_id}")
        document_ids[document_id] = digest
        document_type = str(metadata.get("document_type") or "paper").lower()
        if document_type not in {"paper", "main", "si"}:
            raise ValueError(f"Unsupported document_type: {document_type}")
        record = {
            "paper_id": canonical_paper_id,
            "document_id": document_id,
            "document_type": document_type,
            "source_path": str(path),
            "source_pdf_sha256": digest,
            "source_document_sha256": digest,
            "source_media_type": (
                "text/markdown"
                if path.suffix.lower() == ".md"
                else "application/pdf"
            ),
            "size_bytes": path.stat().st_size,
            "source_metadata": metadata,
            "duplicate_paths": [],
        }
        records_by_hash[digest] = record
        ledger.register_paper(
            paper_id=record["document_id"],
            source_path=record["source_path"],
            source_sha256=digest,
            size_bytes=record["size_bytes"],
            metadata=metadata,
        )
    records = [records_by_hash[key] for key in sorted(records_by_hash)]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(f"{canonical_json(record)}\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "created_at": utc_now(),
        "source": str(source.resolve()),
        "paper_count": len({record["paper_id"] for record in records}),
        "document_count": len(records),
        "document_type_counts": {
            name: sum(record["document_type"] == name for record in records)
            for name in ("paper", "main", "si")
        },
        "missing_count": len(missing),
        "missing_paths": missing,
        "inventory_path": str(output_path.resolve()),
        "inventory_hash": content_hash(records),
    }
    atomic_write_json(output_path.with_suffix(".manifest.json"), manifest)
    return manifest


def load_inventory(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Inventory line {line_number} is not an object")
            records.append(value)
    return records
