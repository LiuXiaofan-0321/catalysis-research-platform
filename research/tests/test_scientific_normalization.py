from __future__ import annotations

import gzip
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "src"))
from catalysis_research.normalization import (  # noqa: E402
    NormalizationError,
    build_normalization_overlay,
    verify_normalization_overlay,
)
from catalysis_research.normalization.units import (  # noqa: E402
    normalize_condition,
    normalize_metric,
)


CONFIG = REPOSITORY_ROOT / "research" / "configs" / "normalization" / "scientific-normalization-v1.1.json"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _evidence(document_id: str, document_type: str) -> list[dict[str, object]]:
    return [{
        "document_id": document_id,
        "document_type": document_type,
        "pdf_page_index": 1,
        "section": "Results",
        "source": "text",
        "source_id": None,
        "quote": "MTO conversion was 0.80 at 400 C and 2 bar.",
        "evidence_validation": "exact",
    }]


def _artifact(document_id: str, document_type: str) -> dict[str, object]:
    evidence = _evidence(document_id, document_type)
    title = "Supplementary Information Figure 1" if document_type == "si" else "MFI catalysis study"
    return {
        "source": {
            "document_id": document_id,
            "document_type": document_type,
            "paper_id": "paper:normalization-test",
            "path": f"/{document_type}.md",
            "source_pdf_sha256": hashlib.sha256(document_id.encode()).hexdigest(),
        },
        "extraction": {
            "schema_version": "catalysis_paper_extraction.v2.1",
            "paper": {
                "id": "paper:normalization-test",
                "title": title,
                "doi": "10.0000/normalization-test",
                "year": 1800,
                "journal": "Test Journal",
                "paper_type": "article",
                "catalysis_system": "thermal_catalysis",
                "reaction_categories": ["MTO"],
                "page_count": 2,
                "source_pdf_sha256": hashlib.sha256(document_id.encode()).hexdigest(),
            },
            "abstract": {"exists": True},
            "summary": {"one_sentence": "Synthetic.", "main_findings": []},
            "keywords": {"extracted": []},
            "entities": [
                {"id": "entity:framework", "type": "zeolite_framework", "canonical_name": "MFI", "evidence": evidence},
                {"id": "entity:sample", "type": "catalyst_sample", "canonical_name": "H-ZSM-5", "evidence": evidence},
            ],
            "experiments": [{
                "id": "experiment:1",
                "experiment_type": "activity_test",
                "sample_entity_ids": ["entity:sample"],
                "material_entity_ids": ["entity:framework"],
                "method_entity_ids": [],
                "conditions": [
                    {"name": "temperature", "value": 400, "unit": "C", "raw_value": "400 C"},
                    {"name": "pressure", "value": 2, "unit": "bar", "raw_value": "2 bar"},
                    {"name": "time", "value": 5, "unit": "min", "raw_value": "5 min"},
                    {"name": "WHSV", "value": 3, "unit": "h^-1", "raw_value": "3 h^-1"},
                    {"name": "flow", "value": 10, "unit": "mL/min", "raw_value": "10 mL/min"},
                ],
                "evidence": evidence,
            }],
            "observations": [
                {"id": "observation:conversion", "experiment_id": "experiment:1", "sample_entity_id": "entity:sample", "metric_name": "conversion rate", "numeric_value": 0.8, "unit": "fraction", "conditions": [], "evidence": evidence},
                {"id": "observation:sty", "experiment_id": "experiment:1", "sample_entity_id": "entity:sample", "metric_name": "STY", "numeric_value": 2.0, "unit": "unknown", "conditions": [], "evidence": evidence},
            ],
            "claims": [],
            "visual_review_items": [],
            "quality": {"extraction_status": "completed", "needs_review_count": 0, "boundary_normalizations": []},
            "extraction_metadata": {"model": "test", "prompt_version": "test-v1", "extracted_at": "2026-09-01T00:00:00Z"},
        },
    }


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _prepare_inputs(root: Path) -> tuple[Path, Path]:
    corpus = root / "corpus"
    corpus.mkdir()
    documents = []
    artifact_rows = []
    for document_type in ("main", "si"):
        document_id = f"document:{document_type}"
        entry = f"documents/{document_type}.json"
        artifact_rows.append((entry, _artifact(document_id, document_type)))
        documents.append({
            "schema_version": "structured_extraction_document.v1",
            "campaign_id": "test",
            "document_id": document_id,
            "paper_id": "paper:normalization-test",
            "document_type": document_type,
            "artifact_entry": entry,
        })
    _write_jsonl(corpus / "documents.jsonl", documents)
    _write_jsonl(corpus / "papers.jsonl", [{"paper_id": "paper:normalization-test", "document_ids": ["document:main", "document:si"], "main_document_ids": ["document:main"], "si_document_ids": ["document:si"]}])
    _write_json(corpus / "quality-summary.json", {"automatic_acceptance": "pass"})
    _write_jsonl(corpus / "review-sample.jsonl", [])
    (corpus / "review-sample.md").write_text("# Review\n", encoding="utf-8")
    with zipfile.ZipFile(corpus / "structured-documents.zip", "w") as archive:
        for entry, artifact in artifact_rows:
            archive.writestr(entry, json.dumps(artifact, sort_keys=True))
    corpus_artifacts = {}
    for name in ("documents.jsonl", "papers.jsonl", "quality-summary.json", "review-sample.jsonl", "review-sample.md", "structured-documents.zip"):
        path = corpus / name
        corpus_artifacts[name] = {"sha256": _hash(path), "bytes": path.stat().st_size}
    _write_json(corpus / "manifest.json", {
        "schema_version": "structured_extraction_corpus.v1",
        "corpus_id": "normalization-test-corpus-v1",
        "document_content_hash": "document-content-test",
        "paper_content_hash": "paper-content-test",
        "artifacts": corpus_artifacts,
    })

    snapshot = root / "snapshot"
    snapshot.mkdir()
    evidence = _evidence("document:main", "main")
    nodes = [
        {"id": "node:framework", "node_type": "entity", "label": "MFI", "canonical_name": "MFI", "data": {"type": "zeolite_framework"}, "evidence": evidence},
        {"id": "node:sample", "node_type": "entity", "label": "H-ZSM-5", "canonical_name": "H-ZSM-5", "data": {"type": "catalyst_sample"}, "evidence": evidence},
        {"id": "node:reaction", "node_type": "reaction", "canonical_name": "MTO", "data": {"reaction_name": "MTO"}, "evidence": evidence},
        {"id": "node:metric-conversion", "node_type": "metric", "canonical_name": "conversion rate", "data": {"metric_name": "conversion rate"}, "evidence": evidence},
        {"id": "node:metric-sty", "node_type": "metric", "canonical_name": "STY", "data": {"metric_name": "STY"}, "evidence": evidence},
        {"id": "node:temperature", "node_type": "condition", "data": {"name": "temperature", "value": 400, "unit": "C", "raw_value": "400 C"}, "evidence": evidence},
        {"id": "node:pressure", "node_type": "condition", "data": {"name": "pressure", "value": 2, "unit": "bar", "raw_value": "2 bar"}, "evidence": evidence},
        {"id": "node:time", "node_type": "condition", "data": {"name": "time", "value": 5, "unit": "min", "raw_value": "5 min"}, "evidence": evidence},
        {"id": "node:whsv", "node_type": "condition", "data": {"name": "WHSV", "value": 3, "unit": "h^-1", "raw_value": "3 h^-1"}, "evidence": evidence},
        {"id": "node:flow", "node_type": "condition", "data": {"name": "flow", "value": 10, "unit": "mL/min", "raw_value": "10 mL/min"}, "evidence": evidence},
        {"id": "node:conversion", "node_type": "observation", "data": {"metric_name": "conversion rate", "numeric_value": 0.8, "unit": "fraction"}, "evidence": evidence},
        {"id": "node:sty", "node_type": "observation", "data": {"metric_name": "STY", "numeric_value": 2.0, "unit": "unknown"}, "evidence": evidence},
        {"id": "node:paper", "node_type": "paper", "data": {"year": 1800, "paper_type": "article"}, "evidence": evidence},
    ]
    nodes_path = snapshot / "nodes.jsonl.gz"
    with gzip.open(nodes_path, "wt", encoding="utf-8") as target:
        for node in nodes:
            target.write(json.dumps(node, sort_keys=True) + "\n")
    _write_json(snapshot / "manifest.json", {
        "schema_version": "kg_snapshot.v1",
        "snapshot_id": "Small-KG-normalization-test-v1",
        "snapshot_content_hash": "snapshot-content-test",
        "artifacts": {"nodes": {"path": "nodes.jsonl.gz", "sha256": _hash(nodes_path), "count": len(nodes)}},
    })
    return snapshot, corpus


def _read_gzip_jsonl(path: Path) -> list[dict[str, object]]:
    with gzip.open(path, "rt", encoding="utf-8") as source:
        return [json.loads(line) for line in source]


class ScientificNormalizationTests(unittest.TestCase):
    def test_unit_rules_are_conservative(self) -> None:
        self.assertEqual(normalize_condition("temperature", 400, "C", None)[0]["value"], 673.15)
        self.assertEqual(normalize_condition("pressure", 2, "bar", None)[0]["value"], 200.0)
        self.assertEqual(normalize_condition("time", 5, "min", None)[0]["value"], 300.0)
        self.assertEqual(normalize_condition("GHSV", 3, "h^-1", None)[0]["basis"], "GHSV")
        self.assertEqual(normalize_condition("flow", 10, "mL/min", None)[0]["basis"], "reported_volumetric")
        self.assertIsNone(normalize_condition("flow", 10, "unknown", None)[0])
        self.assertEqual(normalize_metric("conversion", 0.8, "fraction", None)[0]["value"], 80.0)
        self.assertEqual(normalize_metric("conversion", 80, "%", None)[0]["value"], 80.0)
        self.assertIsNone(normalize_metric("STY", 2, "unknown", None)[0])

    def test_builds_deterministic_immutable_overlay_and_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            snapshot, corpus = _prepare_inputs(root)
            source_hashes = {_hash(snapshot / "nodes.jsonl.gz"), _hash(corpus / "manifest.json")}
            first = root / "overlay-first"
            second = root / "overlay-second"
            with patch("catalysis_research.normalization.builder.verify_snapshot", return_value={"valid": True, "failures": []}):
                manifest = build_normalization_overlay(snapshot_directory=snapshot, corpus_directory=corpus, output_directory=first, config_path=CONFIG)
                second_manifest = build_normalization_overlay(snapshot_directory=snapshot, corpus_directory=corpus, output_directory=second, config_path=CONFIG)

            self.assertEqual(manifest["overlay_content_hash"], second_manifest["overlay_content_hash"])
            self.assertEqual(manifest["artifacts"], second_manifest["artifacts"])
            self.assertEqual(manifest["generation"]["config_sha256"], _hash(CONFIG))
            with patch("catalysis_research.normalization.verifier.verify_snapshot", return_value={"valid": True, "failures": []}):
                self.assertTrue(verify_normalization_overlay(first, snapshot, corpus)["valid"])
            self.assertEqual(source_hashes, {_hash(snapshot / "nodes.jsonl.gz"), _hash(corpus / "manifest.json")})

            concepts = _read_gzip_jsonl(first / "concept_mappings.jsonl.gz")
            framework = next(row for row in concepts if row["category"] == "framework")
            sample = next(row for row in concepts if row["category"] == "catalyst_sample")
            self.assertEqual(framework["canonical_value"]["identity_level"], "framework_topology")
            self.assertEqual(framework["source_paper_ids"], ["paper:normalization-test"])
            self.assertTrue(framework["evidence_references"])
            self.assertEqual(sample["canonical_value"]["identity_level"], "catalyst_sample")
            self.assertEqual(sample["canonical_value"]["parent_framework"], "MFI")
            self.assertNotEqual(framework["canonical_value"], sample["canonical_value"])
            self.assertTrue(any(row["canonical_value"] == "methanol-to-olefins" for row in concepts))

            values = _read_gzip_jsonl(first / "value_mappings.jsonl.gz")
            self.assertTrue(any(row["canonical_value"].get("value") == 673.15 for row in values))
            self.assertTrue(any(row["canonical_value"].get("value") == 80.0 and row["category"] == "performance_metric" for row in values))
            self.assertTrue(any(row["canonical_value"].get("basis") == "reported_volumetric" for row in values))
            unresolved = _read_gzip_jsonl(first / "unresolved.jsonl.gz")
            reasons = {row["rule_id"] for row in unresolved}
            self.assertIn("invalid_year", reasons)
            self.assertNotIn("ambiguous_flow_unit_or_basis", reasons)
            self.assertIn("unsupported_or_basis_sensitive_metric", reasons)
            repairs = _read_gzip_jsonl(first / "metadata_repairs.jsonl.gz")
            self.assertTrue(any(row["field"] == "paper_type" and row["canonical_value"] == "research_article" for row in repairs))
            self.assertTrue(any(row["field"] == "display_title" and row["canonical_value"] == "MFI catalysis study" for row in repairs))

            with self.assertRaises(NormalizationError):
                with patch("catalysis_research.normalization.builder.verify_snapshot", return_value={"valid": True, "failures": []}):
                    build_normalization_overlay(snapshot_directory=snapshot, corpus_directory=corpus, output_directory=first, config_path=CONFIG)
            with (first / "concept_mappings.jsonl.gz").open("ab") as target:
                target.write(b"tamper")
            with patch("catalysis_research.normalization.verifier.verify_snapshot", return_value={"valid": True, "failures": []}):
                report = verify_normalization_overlay(first, snapshot, corpus)
            self.assertFalse(report["valid"])
            self.assertIn("Artifact hash mismatch: concept_mappings", report["failures"])


if __name__ == "__main__":
    unittest.main()
