#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
import sys

sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_literature.hashing import canonical_json, content_hash, sha256_file  # noqa: E402
from catalysis_literature.models import PaperArtifactV2  # noqa: E402


CORPUS_SCHEMA_VERSION = "structured_extraction_corpus.v1"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.write_text(
        "".join(canonical_json(row) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def _zip_write(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _evidence_containers(extraction: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for finding in (extraction.get("summary") or {}).get("main_findings") or []:
        if isinstance(finding, dict):
            yield finding
    for keyword in (extraction.get("keywords") or {}).get("extracted") or []:
        if isinstance(keyword, dict):
            yield keyword
    for field in ("entities", "experiments", "observations", "claims"):
        for item in extraction.get(field) or []:
            if isinstance(item, dict):
                yield item


def _quality_record(
    *, result: dict[str, Any], extraction: dict[str, Any], campaign_id: str
) -> dict[str, Any]:
    validation_counts: Counter[str] = Counter()
    evidence_sources: Counter[str] = Counter()
    evidence_count = 0
    review_records = 0
    visual_review_records = 0
    quotes: list[str] = []
    for container in _evidence_containers(extraction):
        review_records += int(container.get("review_status") == "needs_review")
        visual_review_records += int(bool(container.get("needs_visual_review")))
        for evidence in container.get("evidence") or []:
            if not isinstance(evidence, dict):
                continue
            evidence_count += 1
            validation_counts[str(evidence.get("evidence_validation") or "unverified")] += 1
            evidence_sources[str(evidence.get("source") or "text")] += 1
            quote = str(evidence.get("quote") or "").strip()
            if quote and len(quotes) < 2:
                quotes.append(quote[:500])
    quality = extraction.get("quality") or {}
    boundary = quality.get("boundary_normalizations") or []
    if validation_counts.get("unverified"):
        risk = "unverified"
    elif boundary:
        risk = "normalized"
    elif review_records or int(quality.get("needs_review_count") or 0):
        risk = "review"
    else:
        risk = "clean"
    paper = extraction.get("paper") or {}
    return {
        "campaign_id": campaign_id,
        "document_id": str(result["document_id"]),
        "paper_id": str(result["paper_id"]),
        "document_type": str(result["document_type"]),
        "source_collection": str(
            (result.get("source_metadata") or {}).get("source_collection")
            or "unknown"
        ),
        "title": str(paper.get("title") or ""),
        "doi": paper.get("doi"),
        "record_counts": {
            field: len(extraction.get(field) or [])
            for field in ("entities", "experiments", "observations", "claims")
        },
        "evidence_count": evidence_count,
        "evidence_validation_counts": dict(validation_counts),
        "evidence_source_counts": dict(evidence_sources),
        "review_record_count": review_records,
        "visual_review_record_count": visual_review_records,
        "visual_review_item_count": len(extraction.get("visual_review_items") or []),
        "needs_review_count": int(quality.get("needs_review_count") or 0),
        "boundary_normalization_count": len(boundary),
        "risk_tier": risk,
        "quotes": quotes,
        "artifact_path": str(result["extraction_artifact_path"]),
    }


def _review_sample(rows: list[dict[str, Any]], size: int) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row["campaign_id"], row["document_type"], row["risk_tier"])
        buckets[key].append(row)
    selected: dict[str, dict[str, Any]] = {}
    for key in sorted(buckets):
        candidate = min(
            buckets[key],
            key=lambda row: hashlib.sha256(
                f"small-kg-review-v1|{row['document_id']}".encode("utf-8")
            ).hexdigest(),
        )
        selected[candidate["document_id"]] = candidate
    if len(selected) < size:
        remaining = sorted(
            (row for row in rows if row["document_id"] not in selected),
            key=lambda row: hashlib.sha256(
                f"small-kg-review-fill-v1|{row['document_id']}".encode("utf-8")
            ).hexdigest(),
        )
        for row in remaining[: size - len(selected)]:
            selected[row["document_id"]] = row
    return sorted(selected.values(), key=lambda row: row["document_id"])[:size]


def _render_review(sample: list[dict[str, Any]]) -> str:
    lines = [
        "# Small KG 结构化抽取快速复核样本",
        "",
        "样本按 campaign、主文/SI 和风险层分层确定性抽取。重点检查数值、条件、实体对应关系与 quote 支持性。",
        "",
        "| 文档 | 批次 | 类型 | 风险层 | 实体 | 实验 | 观测 | Claim | 证据 |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in sample:
        counts = row["record_counts"]
        lines.append(
            f"| `{row['document_id']}` | {row['campaign_id']} | {row['document_type']} | "
            f"{row['risk_tier']} | {counts['entities']} | {counts['experiments']} | "
            f"{counts['observations']} | {counts['claims']} | {row['evidence_count']} |"
        )
    for index, row in enumerate(sample, start=1):
        lines.extend(
            [
                "",
                f"## {index}. {row['doi'] or row['paper_id']} ({row['document_type']})",
                "",
                f"- 标题：{row['title'] or '未提供'}",
                f"- 风险层：`{row['risk_tier']}`；边界修复 "
                f"{row['boundary_normalization_count']}；待复核记录 "
                f"{row['review_record_count']}",
                f"- Artifact：`{row['artifact_path']}`",
                "- 证据摘录：",
            ]
        )
        if row["quotes"]:
            lines.extend(f"  - {quote}" for quote in row["quotes"])
        else:
            lines.append("  - 无证据摘录")
    lines.append("")
    return "\n".join(lines)


def freeze_structured_corpus(
    *,
    campaign_directories: list[Path],
    output_directory: Path,
    corpus_id: str,
    expected_documents: int | None = None,
    review_sample_size: int = 24,
) -> dict[str, Any]:
    output_directory = output_directory.resolve()
    if output_directory.exists():
        raise FileExistsError(output_directory)
    campaign_reports: list[dict[str, Any]] = []
    results: list[tuple[str, dict[str, Any]]] = []
    for directory in campaign_directories:
        directory = directory.resolve()
        summary = json.loads((directory / "campaign-summary.json").read_text(encoding="utf-8"))
        if not summary.get("complete") or summary.get("failed") or summary.get("missing"):
            raise ValueError(f"Campaign is not complete: {summary.get('campaign_id')}")
        rows = _load_jsonl(directory / "completed-results.jsonl")
        if len(rows) != int(summary["completed"]):
            raise ValueError(f"Campaign result count mismatch: {summary['campaign_id']}")
        campaign_reports.append(
            {
                "campaign_id": summary["campaign_id"],
                "paper_count": summary["paper_count"],
                "document_count": summary["document_count"],
                "selection_hash": summary["selection_hash"],
                "result_content_hash": summary["result_content_hash"],
                "usage": summary["usage"],
            }
        )
        results.extend((str(summary["campaign_id"]), row) for row in rows)

    results.sort(key=lambda pair: (str(pair[1]["paper_id"]), str(pair[1]["document_id"])))
    document_ids = [str(row["document_id"]) for _, row in results]
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("Duplicate document_id across campaigns")
    if expected_documents is not None and len(results) != expected_documents:
        raise ValueError(f"Expected {expected_documents} documents, found {len(results)}")

    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{output_directory.name}-", dir=output_directory.parent)
    )
    try:
        document_rows: list[dict[str, Any]] = []
        quality_rows: list[dict[str, Any]] = []
        papers: dict[str, dict[str, Any]] = {}
        record_counts: Counter[str] = Counter()
        validation_counts: Counter[str] = Counter()
        evidence_sources: Counter[str] = Counter()
        risk_counts: Counter[str] = Counter()
        schema_versions: Counter[str] = Counter()
        models: Counter[str] = Counter()
        boundary_documents = 0
        boundary_actions = 0
        review_documents = 0
        visual_review_documents = 0
        visual_review_records = 0
        visual_review_items = 0
        unverified_documents = 0
        archive_path = temporary / "structured-documents.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            for campaign_id, result in results:
                if result.get("status") != "completed":
                    raise ValueError(f"Non-completed result: {result.get('document_id')}")
                artifact_path = Path(str(result["extraction_artifact_path"]))
                raw = artifact_path.read_bytes()
                actual_hash = hashlib.sha256(raw).hexdigest()
                if actual_hash != result["extraction_artifact_sha256"]:
                    raise ValueError(f"Artifact hash mismatch: {result['document_id']}")
                artifact = json.loads(raw)
                validated = PaperArtifactV2.model_validate(artifact["extraction"])
                extraction = validated.model_dump(mode="json")
                if str(result["document_id"]) != str(artifact["source"]["document_id"]):
                    raise ValueError(f"Artifact document mismatch: {result['document_id']}")
                entry_hash = hashlib.sha256(
                    str(result["document_id"]).encode()
                ).hexdigest()[:24]
                entry = f"json/{entry_hash}.json"
                _zip_write(archive, entry, raw)
                quality_row = _quality_record(
                    result=result, extraction=extraction, campaign_id=campaign_id
                )
                quality_rows.append(quality_row)
                for field, count in quality_row["record_counts"].items():
                    record_counts[field] += int(count)
                validation_counts.update(quality_row["evidence_validation_counts"])
                evidence_sources.update(quality_row["evidence_source_counts"])
                risk_counts[quality_row["risk_tier"]] += 1
                boundary_documents += int(quality_row["boundary_normalization_count"] > 0)
                boundary_actions += quality_row["boundary_normalization_count"]
                review_documents += int(quality_row["needs_review_count"] > 0)
                visual_review_documents += int(
                    quality_row["visual_review_record_count"] > 0
                    or quality_row["visual_review_item_count"] > 0
                )
                visual_review_records += quality_row["visual_review_record_count"]
                visual_review_items += quality_row["visual_review_item_count"]
                unverified_documents += int(
                    quality_row["evidence_validation_counts"].get("unverified", 0) > 0
                )
                metadata = extraction.get("extraction_metadata") or {}
                schema_versions[str(extraction.get("schema_version") or "unknown")] += 1
                models[str(metadata.get("model") or "unknown")] += 1
                document_row = {
                    "schema_version": "structured_extraction_document.v1",
                    "campaign_id": campaign_id,
                    "document_id": result["document_id"],
                    "paper_id": result["paper_id"],
                    "document_type": result["document_type"],
                    "artifact_entry": entry,
                    "artifact_sha256": actual_hash,
                    "source_document_sha256": result["source_document_sha256"],
                    "source_path": result["source_path"],
                    "source_collection": quality_row["source_collection"],
                    "extraction_schema_version": extraction.get("schema_version"),
                    "model": metadata.get("model"),
                    "prompt_version": metadata.get("prompt_version"),
                }
                document_rows.append(document_row)
                paper = papers.setdefault(
                    str(result["paper_id"]),
                    {
                        "paper_id": str(result["paper_id"]),
                        "document_ids": [],
                        "main_document_ids": [],
                        "si_document_ids": [],
                        "source_collections": set(),
                    },
                )
                paper["document_ids"].append(str(result["document_id"]))
                paper[f"{result['document_type']}_document_ids"].append(str(result["document_id"]))
                paper["source_collections"].add(quality_row["source_collection"])

            paper_rows = []
            for paper_id in sorted(papers):
                paper = papers[paper_id]
                if len(paper["main_document_ids"]) != 1:
                    raise ValueError(f"Paper must have exactly one main document: {paper_id}")
                paper["source_collections"] = sorted(paper["source_collections"])
                paper_rows.append(paper)
            summary = {
                "schema_version": CORPUS_SCHEMA_VERSION,
                "corpus_id": corpus_id,
                "status": "frozen",
                "frozen_at": datetime.now(timezone.utc).isoformat(),
                "paper_count": len(paper_rows),
                "document_count": len(document_rows),
                "main_document_count": sum(row["document_type"] == "main" for row in document_rows),
                "si_document_count": sum(row["document_type"] == "si" for row in document_rows),
                "document_content_hash": content_hash(document_rows),
                "paper_content_hash": content_hash(paper_rows),
                "campaigns": campaign_reports,
                "artifacts": {},
            }
            _zip_write(
                archive,
                "dataset-manifest.json",
                (
                    json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
                    + "\n"
                ).encode("utf-8"),
            )

        _write_jsonl(temporary / "documents.jsonl", document_rows)
        _write_jsonl(temporary / "papers.jsonl", paper_rows)
        sample = _review_sample(quality_rows, review_sample_size)
        _write_jsonl(temporary / "review-sample.jsonl", sample)
        (temporary / "review-sample.md").write_text(
            _render_review(sample), encoding="utf-8", newline="\n"
        )
        evidence_total = sum(validation_counts.values())
        quality_summary = {
            "schema_version": "structured_extraction_quality.v1",
            "corpus_id": corpus_id,
            "automated_acceptance": "pass",
            "validated_document_count": len(document_rows),
            "record_counts": dict(sorted(record_counts.items())),
            "evidence_count": evidence_total,
            "evidence_validation_counts": dict(sorted(validation_counts.items())),
            "evidence_validation_rates": {
                key: value / max(1, evidence_total)
                for key, value in sorted(validation_counts.items())
            },
            "evidence_source_counts": dict(sorted(evidence_sources.items())),
            "risk_tier_document_counts": dict(sorted(risk_counts.items())),
            "boundary_normalized_document_count": boundary_documents,
            "boundary_normalized_document_rate": boundary_documents / max(1, len(document_rows)),
            "boundary_normalization_action_count": boundary_actions,
            "unverified_evidence_count": validation_counts.get("unverified", 0),
            "unverified_evidence_rate": validation_counts.get("unverified", 0)
            / max(1, evidence_total),
            "unverified_evidence_document_count": unverified_documents,
            "unverified_evidence_document_rate": unverified_documents
            / max(1, len(document_rows)),
            "needs_review_document_count": review_documents,
            "needs_review_document_rate": review_documents / max(1, len(document_rows)),
            "visual_review_document_count": visual_review_documents,
            "visual_review_document_rate": visual_review_documents
            / max(1, len(document_rows)),
            "visual_review_record_count": visual_review_records,
            "visual_review_item_count": visual_review_items,
            "review_sample_count": len(sample),
            "schema_versions": dict(sorted(schema_versions.items())),
            "models": dict(sorted(models.items())),
            "acceptance_checks": {
                "campaigns_complete": True,
                "document_ids_unique": True,
                "artifact_hashes_valid": True,
                "strict_schema_valid": True,
                "one_main_document_per_paper": True,
            },
        }
        _write_json(temporary / "quality-summary.json", quality_summary)
        for name in (
            "documents.jsonl",
            "papers.jsonl",
            "quality-summary.json",
            "review-sample.jsonl",
            "review-sample.md",
            "structured-documents.zip",
        ):
            path = temporary / name
            summary["artifacts"][name] = {
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        _write_json(temporary / "manifest.json", summary)
        temporary.replace(output_directory)
        return summary
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze merged structured extraction campaigns.")
    parser.add_argument("--campaign-directory", type=Path, action="append", required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--corpus-id", required=True)
    parser.add_argument("--expected-documents", type=int)
    parser.add_argument("--review-sample-size", type=int, default=24)
    args = parser.parse_args()
    report = freeze_structured_corpus(
        campaign_directories=args.campaign_directory,
        output_directory=args.output_directory,
        corpus_id=args.corpus_id,
        expected_documents=args.expected_documents,
        review_sample_size=args.review_sample_size,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
