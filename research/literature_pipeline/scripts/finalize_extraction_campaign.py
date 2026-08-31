#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_literature.hashing import atomic_write_json, canonical_json, content_hash  # noqa: E402
from catalysis_literature.manifest import utc_now, verify_manifest  # noqa: E402


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def finalize_campaign(
    *, summary_path: Path, workspace: Path, output_directory: Path
) -> dict[str, Any]:
    selection = json.loads(summary_path.read_text(encoding="utf-8"))
    campaign_id = str(selection["campaign_id"])
    expected_document_ids: set[str] = set()
    results_by_document: dict[str, dict[str, Any]] = {}
    shard_reports: list[dict[str, Any]] = []
    for shard in selection["shards"]:
        shard_id = str(shard["shard_id"])
        expected = _load_jsonl(Path(shard["manifest_path"]))
        shard_expected_ids = {str(row["document_id"]) for row in expected}
        overlap = expected_document_ids & shard_expected_ids
        if overlap:
            raise ValueError(f"Documents occur in multiple shards: {sorted(overlap)[:3]}")
        expected_document_ids.update(shard_expected_ids)
        run_id = f"{campaign_id}-{shard_id}"
        run_directory = workspace.resolve() / "runs" / run_id
        verification = verify_manifest(run_directory)
        if not verification["valid"]:
            raise ValueError(f"Invalid shard run {run_id}: {verification['failures']}")
        rows = _load_jsonl(run_directory / "paper-results.jsonl")
        shard_results: dict[str, dict[str, Any]] = {}
        for row in rows:
            document_id = str(row["document_id"])
            if document_id in shard_results:
                raise ValueError(f"Duplicate result for {document_id} in {run_id}")
            shard_results[document_id] = row
        extra = sorted(set(shard_results) - shard_expected_ids)
        if extra:
            raise ValueError(f"Shard {run_id} has unexpected results: {extra[:3]}")
        results_by_document.update(shard_results)
        completed_count = sum(
            row.get("status") == "completed" for row in shard_results.values()
        )
        shard_reports.append(
            {
                "shard_id": shard_id,
                "run_id": run_id,
                "expected": len(shard_expected_ids),
                "completed": completed_count,
                "failed": len(shard_results) - completed_count,
                "missing": len(shard_expected_ids - set(shard_results)),
                "valid": True,
            }
        )

    output_directory.mkdir(parents=True, exist_ok=True)
    results = [results_by_document[key] for key in sorted(results_by_document)]
    completed_results = [row for row in results if row.get("status") == "completed"]
    failed_results = [row for row in results if row.get("status") != "completed"]
    for name, rows in (
        ("paper-results.jsonl", results),
        ("completed-results.jsonl", completed_results),
        ("failed-results.jsonl", failed_results),
    ):
        (output_directory / name).write_text(
            "".join(canonical_json(row) + "\n" for row in rows),
            encoding="utf-8",
            newline="\n",
        )
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for row in results:
        for key in usage:
            usage[key] += int((row.get("usage") or {}).get(key) or 0)
    report = {
        "schema_version": "extraction_campaign_result.v1",
        "campaign_id": campaign_id,
        "finalized_at": utc_now(),
        "selection_hash": selection["selection_hash"],
        "paper_count": selection["paper_count"],
        "document_count": len(expected_document_ids),
        "main_document_count": selection.get("main_document_count"),
        "si_document_count": selection.get("si_document_count"),
        "expected": len(expected_document_ids),
        "completed": len(completed_results),
        "failed": len(failed_results),
        "missing": len(expected_document_ids - set(results_by_document)),
        "success_rate": len(completed_results) / max(1, len(expected_document_ids)),
        "complete": len(completed_results) == len(expected_document_ids),
        "usage": usage,
        "result_content_hash": content_hash(results),
        "shards": shard_reports,
    }
    atomic_write_json(output_directory / "campaign-summary.json", report)
    atomic_write_json(
        output_directory / "FINALIZED.json",
        {
            "campaign_id": campaign_id,
            "valid": True,
            "complete": report["complete"],
            "expected": report["expected"],
            "completed": report["completed"],
            "failed": report["failed"],
            "missing": report["missing"],
        },
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify and merge an extraction campaign.")
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    report = finalize_campaign(
        summary_path=args.summary.resolve(),
        workspace=args.workspace.resolve(),
        output_directory=args.output_directory.resolve(),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
