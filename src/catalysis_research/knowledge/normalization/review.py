from __future__ import annotations

import gzip
import hashlib
import json
import os
import shutil
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .schema import canonical_hash, canonical_json


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize_unresolved(
    *,
    overlay_directory: Path,
    output_directory: Path,
    top_n: int = 50,
    sample_per_reason: int = 20,
) -> dict[str, Any]:
    if top_n < 1 or sample_per_reason < 1:
        raise ValueError("top_n and sample_per_reason must be at least 1")
    overlay = overlay_directory.resolve()
    output = output_directory.resolve()
    if output.exists():
        raise ValueError(f"Output already exists; overwrite is forbidden: {output}")
    manifest_path = overlay / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifact = manifest["artifacts"]["unresolved"]
    unresolved_path = overlay / artifact["path"]
    if _sha256(unresolved_path) != artifact["sha256"]:
        raise ValueError("Unresolved artifact hash mismatch")

    reasons: Counter[str] = Counter()
    categories: Counter[str] = Counter()
    fields: Counter[str] = Counter()
    raw_counts: dict[str, Counter[str]] = defaultdict(Counter)
    raw_values: dict[str, dict[str, Any]] = defaultdict(dict)
    samples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    record_count = 0
    with gzip.open(unresolved_path, "rt", encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            row = json.loads(line)
            record_count += 1
            reason = str(row["rule_id"])
            reasons[reason] += 1
            categories[str(row["category"])] += 1
            fields[str(row["field"])] += 1
            raw_key = canonical_json(row.get("raw_value"))
            raw_counts[reason][raw_key] += 1
            raw_values[reason][raw_key] = row.get("raw_value")
            bucket = samples[reason]
            bucket.append(row)
            bucket.sort(key=lambda item: item["mapping_id"])
            if len(bucket) > sample_per_reason:
                bucket.pop()

    top_raw_values = {}
    for reason in sorted(raw_counts):
        ranked = sorted(
            raw_counts[reason].items(),
            key=lambda item: (-item[1], item[0]),
        )[:top_n]
        top_raw_values[reason] = [
            {"raw_value": raw_values[reason][raw_key], "count": count}
            for raw_key, count in ranked
        ]
    sample_rows = [
        row
        for reason in sorted(samples)
        for row in samples[reason]
    ]
    summary = {
        "schema_version": "scientific_normalization_review.v1",
        "source_overlay_id": manifest["overlay_id"],
        "source_overlay_content_hash": manifest["overlay_content_hash"],
        "source_manifest_sha256": _sha256(manifest_path),
        "unresolved_artifact_sha256": artifact["sha256"],
        "unresolved_record_count": record_count,
        "reason_counts": dict(sorted(reasons.items())),
        "category_counts": dict(sorted(categories.items())),
        "field_counts": dict(sorted(fields.items())),
        "top_raw_values": top_raw_values,
        "sample_per_reason": sample_per_reason,
        "sample_count": len(sample_rows),
        "scientific_review_status": "required",
    }
    summary["review_content_hash"] = canonical_hash(summary)

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        summary_path = temporary / "unresolved-review-summary.json"
        summary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        sample_path = temporary / "unresolved-review-sample.jsonl.gz"
        with sample_path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                for row in sample_rows:
                    compressed.write((canonical_json(row) + "\n").encode("utf-8"))
        review_manifest = {
            "schema_version": "scientific_normalization_review_manifest.v1",
            "source_overlay_content_hash": manifest["overlay_content_hash"],
            "review_content_hash": summary["review_content_hash"],
            "artifacts": {
                "summary": {"path": summary_path.name, "sha256": _sha256(summary_path)},
                "sample": {"path": sample_path.name, "sha256": _sha256(sample_path), "count": len(sample_rows)},
            },
            "status": "frozen",
        }
        (temporary / "manifest.json").write_text(
            json.dumps(review_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        os.replace(temporary, output)
        return review_manifest
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
