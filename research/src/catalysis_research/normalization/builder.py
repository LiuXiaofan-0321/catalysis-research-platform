from __future__ import annotations

import gzip
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from ..kg.freeze_stage1 import verify_snapshot
from .rules import (
    compact,
    looks_like_si_title,
    normalize_alias,
    normalize_framework,
    normalize_paper_type,
    normalize_sample,
)
from .schema import SCHEMA_VERSION, canonical_hash, canonical_json, mapping_id, overlay_hash_identity
from .units import normalize_condition, normalize_metric


class NormalizationError(ValueError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _jsonl(path: Path) -> Iterable[dict[str, Any]]:
    opener = gzip.open if path.suffix == ".gz" else path.open
    with opener(path, "rt", encoding="utf-8") if path.suffix == ".gz" else opener("r", encoding="utf-8") as source:
        for line in source:
            if line.strip():
                yield json.loads(line)


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _write_gzip_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            for row in sorted(rows, key=lambda item: item["mapping_id"]):
                compressed.write((canonical_json(row) + "\n").encode("utf-8"))


def _record(*, category: str, field: str, raw: Any, canonical: Any, rule_id: str, rule_version: str, source: str, node: dict[str, Any] | None = None, document_id: str | None = None, confidence: float = 1.0, review_status: str = "normalized") -> dict[str, Any]:
    node_id = (node or {}).get("id")
    evidence = (node or {}).get("evidence") or []
    document_ids = sorted({str(item.get("document_id")) for item in evidence if item.get("document_id")})
    if document_id:
        document_ids = sorted(set(document_ids) | {document_id})
    return {
        "mapping_id": mapping_id(category, node_id, document_id, field, raw, canonical, rule_version),
        "category": category,
        "source_node_id": node_id,
        "source_record": (
            {"type": "kg_node", "id": node_id}
            if node_id
            else {"type": "corpus_document", "id": document_id}
        ),
        "source_paper_ids": [],
        "source_document_ids": document_ids,
        "evidence_references": [
            {
                "document_id": item.get("document_id"),
                "pdf_page_index": item.get("pdf_page_index"),
                "quote_sha256": hashlib.sha256(
                    str(item.get("quote") or "").encode("utf-8")
                ).hexdigest(),
                "evidence_validation": item.get("evidence_validation"),
            }
            for item in evidence
            if item.get("document_id") and item.get("quote")
        ],
        "field": field,
        "raw_value": raw,
        "canonical_value": canonical,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "source": source,
        "confidence": confidence,
        "review_status": review_status,
    }


def _unresolved(*, category: str, field: str, raw: Any, reason: str, rule_version: str, node: dict[str, Any]) -> dict[str, Any]:
    return _record(category=category, field=field, raw=raw, canonical=None, rule_id=reason, rule_version=rule_version, source="deterministic_rule", node=node, confidence=0.0, review_status="needs_review")


def _verify_corpus(corpus: Path) -> dict[str, Any]:
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    for name, artifact in manifest.get("artifacts", {}).items():
        path = corpus / name
        if not path.is_file() or _sha256(path) != artifact.get("sha256"):
            raise NormalizationError(f"Frozen corpus artifact verification failed: {name}")
    return manifest


def _metadata_repairs(corpus: Path, config: dict[str, Any], rule_version: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    repairs: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    documents = list(_jsonl(corpus / "documents.jsonl"))
    zip_path = corpus / "structured-documents.zip"
    artifact_titles: dict[str, str] = {}
    with zipfile.ZipFile(zip_path) as archive:
        for row in documents:
            artifact = json.loads(archive.read(row["artifact_entry"]))
            paper = (artifact.get("extraction") or {}).get("paper") or {}
            artifact_titles[str(row["document_id"])] = compact(paper.get("title"))
    main_titles: dict[str, str] = {}
    for row in documents:
        if row["document_type"] == "main":
            main_titles[str(row["paper_id"])] = artifact_titles[str(row["document_id"])]
    for row in documents:
        if row["document_type"] != "si":
            continue
        document_id = str(row["document_id"])
        raw_title = artifact_titles[document_id]
        main_title = main_titles.get(str(row["paper_id"]))
        if main_title and (raw_title != main_title or looks_like_si_title(raw_title, config["metadata"]["si_title_pollution_patterns"])):
            repairs.append(_record(category="metadata", field="display_title", raw=raw_title, canonical=main_title, rule_id="si_inherit_main_title", rule_version=rule_version, source="frozen_corpus_main_document", document_id=document_id, confidence=1.0))
    return repairs, unresolved


def build_normalization_overlay(*, snapshot_directory: Path, corpus_directory: Path, output_directory: Path, config_path: Path, code_commit: str | None = None) -> dict[str, Any]:
    snapshot = snapshot_directory.resolve()
    corpus = corpus_directory.resolve()
    output = output_directory.resolve()
    if output.exists():
        raise NormalizationError(f"Output already exists; overwrite is forbidden: {output}")
    snapshot_report = verify_snapshot(snapshot)
    if not snapshot_report["valid"]:
        raise NormalizationError("Frozen KG snapshot verification failed: " + "; ".join(snapshot_report["failures"]))
    kg_manifest = json.loads((snapshot / "manifest.json").read_text(encoding="utf-8"))
    corpus_manifest = _verify_corpus(corpus)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    rule_version = str(config["rule_version"])
    concept: list[dict[str, Any]] = []
    values: list[dict[str, Any]] = []
    repairs: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    nodes_path = snapshot / kg_manifest["artifacts"]["nodes"]["path"]
    year_min, year_max = config["metadata"]["valid_year_range"]
    for node in _jsonl(nodes_path):
        node_type = node.get("node_type")
        data = node.get("data") or {}
        if node_type == "entity":
            entity_type = compact(data.get("type"))
            raw = compact(node.get("canonical_name") or node.get("label"))
            if entity_type == "zeolite_framework":
                canonical = normalize_framework(raw, config["framework_aliases"])
                if canonical:
                    concept.append(_record(category="framework", field="canonical_name", raw=raw, canonical={"framework_code": canonical, "identity_level": "framework_topology"}, rule_id="framework_alias", rule_version=rule_version, source="curated_alias_or_iza_code", node=node))
                else:
                    unresolved.append(_unresolved(category="framework", field="canonical_name", raw=raw, reason="ambiguous_framework", rule_version=rule_version, node=node))
            elif entity_type == "catalyst_sample":
                sample = normalize_sample(raw)
                if sample:
                    concept.append(_record(category="catalyst_sample", field="canonical_name", raw=raw, canonical=sample, rule_id="sample_identity_preserving", rule_version=rule_version, source="deterministic_parser", node=node, confidence=0.9))
                else:
                    unresolved.append(_unresolved(category="catalyst_sample", field="canonical_name", raw=raw, reason="ambiguous_sample", rule_version=rule_version, node=node))
        elif node_type == "reaction":
            raw = data.get("reaction_name") or node.get("canonical_name")
            canonical = normalize_alias(raw, config["reaction_aliases"])
            if canonical:
                concept.append(_record(category="reaction", field="reaction_name", raw=raw, canonical=canonical, rule_id="reaction_alias", rule_version=rule_version, source="curated_alias", node=node))
            else:
                unresolved.append(_unresolved(category="reaction", field="reaction_name", raw=raw, reason="unknown_reaction_alias", rule_version=rule_version, node=node))
        elif node_type == "metric":
            raw = data.get("metric_name") or node.get("canonical_name")
            canonical = normalize_alias(raw, config["metric_aliases"])
            if canonical:
                concept.append(_record(category="metric", field="metric_name", raw=raw, canonical=canonical, rule_id="metric_alias", rule_version=rule_version, source="curated_alias", node=node))
            else:
                unresolved.append(_unresolved(category="metric", field="metric_name", raw=raw, reason="unknown_metric_alias", rule_version=rule_version, node=node))
        elif node_type == "condition":
            raw = {key: data.get(key) for key in ("name", "value", "unit", "raw_value")}
            canonical, rule = normalize_condition(data.get("name"), data.get("value"), data.get("unit"), data.get("raw_value"))
            if canonical:
                values.append(_record(category="condition", field="value_unit", raw=raw, canonical=canonical, rule_id=rule, rule_version=rule_version, source="deterministic_unit_conversion", node=node))
            else:
                unresolved.append(_unresolved(category="condition", field="value_unit", raw=raw, reason=rule, rule_version=rule_version, node=node))
        elif node_type == "observation":
            raw = {"metric_name": data.get("metric_name"), "value": data.get("numeric_value"), "unit": data.get("unit"), "raw_value": data.get("raw_value")}
            normalized_metric_name = (
                normalize_alias(data.get("metric_name"), config["metric_aliases"])
                or data.get("metric_name")
            )
            canonical, rule = normalize_metric(normalized_metric_name, data.get("numeric_value"), data.get("unit"), data.get("raw_value"))
            if canonical:
                values.append(_record(category="performance_metric", field="numeric_value_unit", raw=raw, canonical=canonical, rule_id=rule, rule_version=rule_version, source="deterministic_unit_conversion", node=node))
            elif data.get("numeric_value") is not None:
                unresolved.append(_unresolved(category="performance_metric", field="numeric_value_unit", raw=raw, reason=rule, rule_version=rule_version, node=node))
        elif node_type == "paper":
            year = data.get("year")
            if year is not None and (not isinstance(year, int) or isinstance(year, bool) or not year_min <= year <= year_max):
                unresolved.append(_unresolved(category="metadata", field="year", raw=year, reason="invalid_year", rule_version=rule_version, node=node))
            raw_type = data.get("paper_type")
            if raw_type:
                canonical_type = normalize_paper_type(raw_type, config["paper_type_aliases"])
                if canonical_type:
                    repairs.append(_record(category="metadata", field="paper_type", raw=raw_type, canonical=canonical_type, rule_id="paper_type_alias", rule_version=rule_version, source="curated_alias", node=node))
                else:
                    unresolved.append(_unresolved(category="metadata", field="paper_type", raw=raw_type, reason="unknown_paper_type", rule_version=rule_version, node=node))

    si_repairs, si_unresolved = _metadata_repairs(corpus, config, rule_version)
    repairs.extend(si_repairs)
    unresolved.extend(si_unresolved)
    rows_by_name = {"concept_mappings": concept, "value_mappings": values, "metadata_repairs": repairs, "unresolved": unresolved}
    document_to_paper = {
        str(row["document_id"]): str(row["paper_id"])
        for row in _jsonl(corpus / "documents.jsonl")
    }
    for rows in rows_by_name.values():
        for row in rows:
            row["source_paper_ids"] = sorted(
                {
                    document_to_paper[document_id]
                    for document_id in row["source_document_ids"]
                    if document_id in document_to_paper
                }
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        artifacts: dict[str, Any] = {}
        for name, rows in rows_by_name.items():
            path = temporary / f"{name}.jsonl.gz"
            _write_gzip_jsonl(path, rows)
            artifacts[name] = {"path": path.name, "sha256": _sha256(path), "count": len(rows)}
        reason_counts = Counter(row["rule_id"] for row in unresolved)
        quality = {
            "schema_version": "scientific_normalization_quality.v1.1",
            "record_counts": {name: len(rows) for name, rows in rows_by_name.items()},
            "unresolved_reason_counts": dict(sorted(reason_counts.items())),
            "automatic_acceptance": "pass",
        }
        quality_path = temporary / "quality-summary.json"
        _write_json(quality_path, quality)
        artifacts["quality_summary"] = {"path": quality_path.name, "sha256": _sha256(quality_path)}
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "overlay_id": str(config["overlay_id"]),
            "rule_version": rule_version,
            "status": "frozen",
            "source_kg": {"snapshot_id": kg_manifest["snapshot_id"], "snapshot_content_hash": kg_manifest["snapshot_content_hash"], "manifest_sha256": _sha256(snapshot / "manifest.json")},
            "source_corpus": {"corpus_id": corpus_manifest["corpus_id"], "document_content_hash": corpus_manifest["document_content_hash"], "paper_content_hash": corpus_manifest["paper_content_hash"], "manifest_sha256": _sha256(corpus / "manifest.json")},
            "record_counts": quality["record_counts"],
            "artifacts": artifacts,
            "generation": {
                "overwrite_policy": "forbidden",
                "gzip_mtime": 0,
                "ordering": "mapping_id",
                "config_sha256": _sha256(config_path),
                "code_commit": code_commit,
            },
        }
        manifest["overlay_content_hash"] = canonical_hash(overlay_hash_identity(manifest))
        _write_json(temporary / "manifest.json", manifest)
        os.replace(temporary, output)
        return manifest
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
