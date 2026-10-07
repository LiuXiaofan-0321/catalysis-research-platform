#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_literature.hashing import atomic_write_json, canonical_json, content_hash


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select main text and targeted SI documents for an extraction pilot."
    )
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--paper-id", action="append", required=True)
    parser.add_argument("--si-document-id", action="append", default=[])
    parser.add_argument("--max-si-per-paper", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    args = parse_args()
    if args.max_si_per_paper < 0:
        raise ValueError("--max-si-per-paper must be non-negative")
    requested_papers = list(dict.fromkeys(str(value) for value in args.paper_id))
    requested_si = set(str(value) for value in args.si_document_id)
    documents = load_jsonl(args.index.resolve() / "documents.jsonl")
    selected: list[dict[str, object]] = []
    missing_papers: list[str] = []
    for paper_id in requested_papers:
        paper_documents = [
            row for row in documents if str(row.get("paper_id")) == paper_id
        ]
        if not paper_documents:
            missing_papers.append(paper_id)
            continue
        main_documents = [
            row for row in paper_documents if row.get("document_type") == "main"
        ]
        if not main_documents:
            raise ValueError(f"Pilot paper has no main document: {paper_id}")
        si_documents = [
            row for row in paper_documents if row.get("document_type") == "si"
        ]
        explicit_si = [
            row for row in si_documents if str(row.get("document_id")) in requested_si
        ]
        remaining_si = sorted(
            (row for row in si_documents if row not in explicit_si),
            key=lambda row: (
                -int(row.get("chunk_count") or 0),
                str(row.get("document_id")),
            ),
        )
        si_limit = max(args.max_si_per_paper, len(explicit_si))
        selected.extend(main_documents)
        selected.extend((explicit_si + remaining_si)[:si_limit])
    if missing_papers:
        raise ValueError("Unknown paper ids: " + ", ".join(missing_papers))
    unmatched_si = requested_si - {
        str(row.get("document_id")) for row in selected
    }
    if unmatched_si:
        raise ValueError("Unknown or mismatched SI ids: " + ", ".join(sorted(unmatched_si)))

    records: list[dict[str, object]] = []
    for row in sorted(
        selected,
        key=lambda value: (
            requested_papers.index(str(value["paper_id"])),
            0 if value.get("document_type") == "main" else 1,
            str(value.get("document_id")),
        ),
    ):
        metadata = json.loads(str(row.get("metadata_json") or "{}"))
        records.append(
            {
                **metadata,
                "path": row["source_path"],
                "paper_id": row["paper_id"],
                "document_id": row["document_id"],
                "document_type": row["document_type"],
                "source_document_sha256": row["source_document_sha256"],
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(canonical_json(record) + "\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )
    summary = {
        "schema_version": "extraction_pilot_selection.v1",
        "index": str(args.index.resolve()),
        "paper_ids": requested_papers,
        "paper_count": len(requested_papers),
        "document_count": len(records),
        "main_document_count": sum(
            record["document_type"] == "main" for record in records
        ),
        "si_document_count": sum(record["document_type"] == "si" for record in records),
        "selection_hash": content_hash(records),
    }
    atomic_write_json(args.output.with_suffix(".summary.json"), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
