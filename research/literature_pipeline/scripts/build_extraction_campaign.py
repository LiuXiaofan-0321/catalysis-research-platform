#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_literature.hashing import (  # noqa: E402
    atomic_write_json,
    canonical_json,
    content_hash,
    sha256_file,
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(canonical_json(record) + "\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )


def _excluded_papers(paths: list[Path]) -> set[str]:
    excluded: set[str] = set()
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        paper_ids = payload.get("paper_ids")
        if not isinstance(paper_ids, list):
            raise ValueError(f"Excluded summary has no paper_ids list: {path}")
        excluded.update(str(value) for value in paper_ids)
    return excluded


def _manifest_record(row: dict[str, Any]) -> dict[str, Any]:
    metadata = json.loads(str(row.get("metadata_json") or "{}"))
    return {
        **metadata,
        "path": row["source_path"],
        "paper_id": row["paper_id"],
        "document_id": row["document_id"],
        "document_type": row["document_type"],
        "source_document_sha256": row["source_document_sha256"],
    }


def build_campaign(
    *,
    index_directory: Path,
    output_directory: Path,
    campaign_id: str,
    paper_count: int,
    shard_size: int,
    excluded_summaries: list[Path],
    config_template: Path,
    workspace: Path,
) -> dict[str, Any]:
    index_directory = index_directory.resolve()
    output_directory = output_directory.resolve()
    documents_path = index_directory / "documents.jsonl"
    manifest_path = index_directory / "manifest.json"
    if not documents_path.is_file() or not manifest_path.is_file():
        raise FileNotFoundError(f"Invalid index directory: {index_directory}")
    if paper_count < 1:
        raise ValueError("paper_count must be at least 1")
    if shard_size < 1:
        raise ValueError("shard_size must be at least 1")

    rows_by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in load_jsonl(documents_path):
        rows_by_paper[str(row["paper_id"])].append(row)
    excluded = _excluded_papers(excluded_summaries)
    available = sorted(set(rows_by_paper) - excluded)
    selected_papers = available[:paper_count]
    if not selected_papers:
        raise ValueError("No unprocessed papers remain in the source index")

    records_by_paper: dict[str, list[dict[str, Any]]] = {}
    for paper_id in selected_papers:
        rows = sorted(
            rows_by_paper[paper_id],
            key=lambda row: (
                0 if row.get("document_type") == "main" else 1,
                str(row.get("document_id")),
            ),
        )
        if not any(row.get("document_type") == "main" for row in rows):
            raise ValueError(f"Selected paper has no main document: {paper_id}")
        records_by_paper[paper_id] = [_manifest_record(row) for row in rows]

    output_directory.mkdir(parents=True, exist_ok=False)
    configs_directory = output_directory / "configs"
    configs_directory.mkdir()
    template = yaml.safe_load(config_template.read_text(encoding="utf-8"))
    shards: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    for start in range(0, len(selected_papers), shard_size):
        shard_number = len(shards) + 1
        shard_id = f"shard-{shard_number:04d}"
        shard_papers = selected_papers[start : start + shard_size]
        shard_records = [
            record for paper_id in shard_papers for record in records_by_paper[paper_id]
        ]
        all_records.extend(shard_records)
        shard_path = output_directory / "shards" / f"{shard_id}.jsonl"
        _write_jsonl(shard_path, shard_records)
        config = dict(template)
        config["source"] = str(shard_path)
        config["workspace"] = str(workspace.resolve())
        config_path = configs_directory / f"{shard_id}.yaml"
        config_path.write_text(
            yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
            newline="\n",
        )
        shards.append(
            {
                "shard_id": shard_id,
                "paper_ids": shard_papers,
                "paper_count": len(shard_papers),
                "document_count": len(shard_records),
                "main_document_count": sum(
                    row["document_type"] == "main" for row in shard_records
                ),
                "si_document_count": sum(
                    row["document_type"] == "si" for row in shard_records
                ),
                "manifest_path": str(shard_path),
                "config_path": str(config_path),
                "content_hash": content_hash(shard_records),
            }
        )

    _write_jsonl(output_directory / "master.jsonl", all_records)
    summary = {
        "schema_version": "extraction_campaign_selection.v1",
        "campaign_id": campaign_id,
        "source_index": str(index_directory),
        "source_index_manifest_sha256": sha256_file(manifest_path),
        "selection_policy": "paper_id_ascending_excluding_prior_campaigns",
        "requested_paper_count": paper_count,
        "paper_count": len(selected_papers),
        "paper_ids": selected_papers,
        "excluded_paper_count": len(excluded),
        "excluded_summary_paths": [str(path.resolve()) for path in excluded_summaries],
        "document_count": len(all_records),
        "main_document_count": sum(
            row["document_type"] == "main" for row in all_records
        ),
        "si_document_count": sum(row["document_type"] == "si" for row in all_records),
        "shard_paper_count": shard_size,
        "shard_count": len(shards),
        "workspace": str(workspace.resolve()),
        "selection_hash": content_hash(all_records),
        "shards": shards,
    }
    atomic_write_json(output_directory / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Freeze an incremental, resumable structured-extraction campaign."
    )
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--paper-count", type=int, default=500)
    parser.add_argument("--shard-size", type=int, default=50)
    parser.add_argument("--exclude-summary", type=Path, action="append", default=[])
    parser.add_argument("--config-template", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    output = args.output_directory.resolve()
    if output.exists():
        if not args.overwrite:
            raise FileExistsError(output)
        shutil.rmtree(output)
    summary = build_campaign(
        index_directory=args.index,
        output_directory=output,
        campaign_id=args.campaign_id,
        paper_count=args.paper_count,
        shard_size=args.shard_size,
        excluded_summaries=args.exclude_summary,
        config_template=args.config_template,
        workspace=args.workspace,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
