from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .hashing import atomic_write_json, content_hash, sha256_file
from .manifest import utc_now


def _load_results(run_directory: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with (run_directory / "paper-results.jsonl").open(
        "r",
        encoding="utf-8",
    ) as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def export_stage1(*, run_directory: Path, output_directory: Path) -> dict[str, Any]:
    run_directory = run_directory.resolve()
    output_directory = output_directory.resolve()
    if output_directory.exists():
        raise FileExistsError(f"Export directory already exists: {output_directory}")
    json_directory = output_directory / "json"
    json_directory.mkdir(parents=True)
    exported: list[dict[str, Any]] = []
    counts = {
        "documents": 0,
        "keywords": 0,
        "entities": 0,
        "experiments": 0,
        "observations": 0,
        "claims": 0,
    }
    for index, result in enumerate(
        sorted(_load_results(run_directory), key=lambda row: row["paper_id"]),
        start=1,
    ):
        source = result.get("extraction_artifact_path")
        if result.get("status") != "completed" or not source:
            continue
        source_path = Path(source)
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        extraction = payload["extraction"]
        destination = json_directory / (
            f"{index:06d}_{result['source_pdf_sha256'][:16]}.json"
        )
        shutil.copy2(source_path, destination)
        counts["documents"] += 1
        counts["keywords"] += len(
            (extraction.get("keywords") or {}).get("extracted") or []
        )
        for field in ("entities", "experiments", "observations", "claims"):
            counts[field] += len(extraction.get(field) or [])
        exported.append(
            {
                "paper_id": extraction["paper"]["id"],
                "source_pdf_sha256": result["source_pdf_sha256"],
                "path": str(destination.relative_to(output_directory)).replace(
                    "\\",
                    "/",
                ),
                "sha256": sha256_file(destination),
            }
        )
    manifest = {
        "schema": "catalysis_research_dataset.v2",
        "generated_at": utc_now(),
        "source_run_id": run_directory.name,
        "counts": counts,
        "documents": exported,
        "corpus_fingerprint": content_hash(
            [record["paper_id"] for record in exported]
        ),
    }
    atomic_write_json(output_directory / "dataset-manifest.json", manifest)
    return manifest
