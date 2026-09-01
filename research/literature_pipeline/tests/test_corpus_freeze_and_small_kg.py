from __future__ import annotations

import gzip
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "literature_pipeline" / "scripts"))
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "src"))

from build_small_kg_from_corpus import build_aggregated_archive  # noqa: E402
from freeze_structured_corpus import freeze_structured_corpus  # noqa: E402
from catalysis_research.kg.freeze_stage1 import (  # noqa: E402
    freeze_stage1_archive,
    verify_snapshot,
)


def _evidence(document_id: str, document_type: str) -> list[dict[str, object]]:
    return [
        {
            "document_id": document_id,
            "document_type": document_type,
            "pdf_page_index": 1,
            "section": "Results",
            "source": "text",
            "source_id": None,
            "quote": "Methanol conversion reached 80 percent at 673 K.",
            "evidence_validation": "exact",
        }
    ]


def _artifact(document_id: str, document_type: str) -> dict[str, object]:
    evidence = _evidence(document_id, document_type)
    return {
        "source": {
            "document_id": document_id,
            "document_type": document_type,
            "paper_id": "paper:test",
            "path": f"/{document_type}.md",
            "source_pdf_sha256": hashlib.sha256(document_id.encode()).hexdigest(),
        },
        "extraction": {
            "schema_version": "catalysis_paper_extraction.v2.1",
            "paper": {
                "id": "paper:test",
                "title": "Synthetic zeolite paper",
                "doi": "10.0000/test",
                "year": 2026,
                "journal": "Test Journal",
                "paper_type": "research_article",
                "catalysis_system": "thermal_catalysis",
                "reaction_categories": ["Methanol conversion"],
                "page_count": 2,
                "source_pdf_sha256": hashlib.sha256(document_id.encode()).hexdigest(),
            },
            "abstract": {"exists": True},
            "summary": {
                "one_sentence": "Synthetic summary.",
                "main_findings": [{"statement": "Active.", "evidence": evidence}],
            },
            "keywords": {
                "extracted": [
                    {
                        "id": "keyword:k1",
                        "raw_term": "MFI",
                        "normalized_term": "MFI",
                        "category": "material",
                        "evidence": evidence,
                    }
                ]
            },
            "entities": [
                {
                    "id": "entity:e1",
                    "type": "zeolite_framework",
                    "canonical_name": "MFI",
                    "zh_name": "MFI",
                    "evidence": evidence,
                },
                {
                    "id": "entity:e2",
                    "type": "catalyst_sample",
                    "canonical_name": "H-ZSM-5",
                    "evidence": evidence,
                },
            ],
            "experiments": [
                {
                    "id": "experiment:x1",
                    "experiment_type": "activity_test",
                    "sample_entity_ids": ["entity:e2"],
                    "material_entity_ids": ["entity:e1"],
                    "method_entity_ids": [],
                    "conditions": [
                        {"name": "temperature", "value": 673, "unit": "K", "raw_value": "673 K"}
                    ],
                    "evidence": evidence,
                }
            ],
            "observations": [
                {
                    "id": "observation:o1",
                    "experiment_id": "experiment:x1",
                    "sample_entity_id": "entity:e2",
                    "metric_name": "conversion",
                    "numeric_value": 80.0,
                    "unit": "%",
                    "conditions": [],
                    "evidence": evidence,
                }
            ],
            "claims": [
                {
                    "id": "claim:c1",
                    "claim_type": "reported_result",
                    "statement": "The catalyst was active.",
                    "evidence": evidence,
                }
            ],
            "visual_review_items": (
                [{"reason": "table"}] if document_type == "si" else []
            ),
            "quality": {
                "extraction_status": "completed",
                "needs_review_count": int(document_type == "si"),
                "boundary_normalizations": (
                    [{"action": "normalized"}] if document_type == "si" else []
                ),
            },
            "extraction_metadata": {
                "model": "glm-5.3-flash",
                "prompt_version": "test-v1",
                "extracted_at": "2026-09-01T00:00:00Z",
            },
        },
    }


def _write_campaign(root: Path) -> Path:
    campaign = root / "campaign"
    campaign.mkdir()
    rows = []
    for document_type in ("main", "si"):
        document_id = f"document:{document_type}"
        artifact_path = campaign / f"{document_type}.json"
        raw = (json.dumps(_artifact(document_id, document_type)) + "\n").encode()
        artifact_path.write_bytes(raw)
        rows.append(
            {
                "status": "completed",
                "document_id": document_id,
                "paper_id": "paper:test",
                "document_type": document_type,
                "extraction_artifact_path": str(artifact_path),
                "extraction_artifact_sha256": hashlib.sha256(raw).hexdigest(),
                "source_document_sha256": hashlib.sha256(document_id.encode()).hexdigest(),
                "source_path": f"/{document_type}.md",
                "source_metadata": {"source_collection": "ACS"},
            }
        )
    (campaign / "completed-results.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )
    (campaign / "campaign-summary.json").write_text(
        json.dumps(
            {
                "campaign_id": "batch-test",
                "complete": True,
                "failed": 0,
                "missing": 0,
                "completed": 2,
                "paper_count": 1,
                "document_count": 2,
                "selection_hash": "selection-test",
                "result_content_hash": "result-test",
                "usage": {},
            }
        ),
        encoding="utf-8",
    )
    return campaign


class CorpusAndSmallKgTests(unittest.TestCase):
    def test_merges_main_si_and_builds_strict_grounded_kg(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            corpus = root / "corpus"
            freeze_structured_corpus(
                campaign_directories=[_write_campaign(root)],
                output_directory=corpus,
                corpus_id="test-corpus-v1",
                expected_documents=2,
                review_sample_size=2,
            )
            quality = json.loads((corpus / "quality-summary.json").read_text())
            self.assertEqual(quality["record_counts"]["entities"], 4)
            self.assertEqual(quality["review_sample_count"], 2)
            self.assertEqual(quality["boundary_normalized_document_count"], 1)
            self.assertEqual(quality["visual_review_document_count"], 1)

            stage1 = root / "stage1.zip"
            build_aggregated_archive(
                corpus_directory=corpus,
                output_archive=stage1,
                expected_documents=2,
                expected_papers=1,
            )
            snapshot = root / "snapshot"
            manifest = freeze_stage1_archive(
                archive_path=stage1,
                output_directory=snapshot,
                snapshot_id="Small-KG-test-v1",
                knowledge_level="Small/Local",
                domain="zeolite_catalysis",
                expected_papers=1,
                allowed_systems={"thermal_catalysis"},
                repository_root=REPOSITORY_ROOT,
                ontology_version="catalysis_evidence_graph.v2",
                strict_grounded_edges=True,
                normalize_science_concepts=True,
                frozen_at="2026-09-01T00:00:00+00:00",
                git_state={"commit": "test", "tree": "test", "branch": "test", "dirty": False},
            )
            self.assertEqual(manifest["paper_count"], 1)
            self.assertEqual(manifest["graph"]["grounded_edge_rate"], 1.0)
            for node_type in ("reaction", "condition", "metric"):
                self.assertGreater(manifest["graph"]["node_type_distribution"][node_type], 0)
            self.assertTrue(verify_snapshot(snapshot)["valid"])

            with gzip.open(snapshot / "edges.jsonl.gz", "rt", encoding="utf-8") as source:
                edges = [json.loads(line) for line in source]
            self.assertTrue(any(len(edge["source_document_ids"]) == 2 for edge in edges))
            for edge in edges:
                self.assertEqual(edge["source_paper_id"], "paper:test")
                self.assertTrue(edge["evidence"])
                for item in edge["evidence"]:
                    self.assertTrue(item["document_id"])
                    self.assertGreaterEqual(item["pdf_page_index"], 1)
                    self.assertTrue(item["quote"])

    def test_rejects_duplicate_document_ids_across_campaigns(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            campaign = _write_campaign(root)
            with self.assertRaisesRegex(ValueError, "Duplicate document_id"):
                freeze_structured_corpus(
                    campaign_directories=[campaign, campaign],
                    output_directory=root / "corpus",
                    corpus_id="test-corpus-v1",
                )

    def test_small_kg_accepts_preselected_corpus_with_missing_system(self) -> None:
        artifact = _artifact("document:main", "main")
        artifact["extraction"]["paper"]["catalysis_system"] = ""
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive_path = root / "dataset.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("dataset-manifest.json", json.dumps({}))
                archive.writestr("json/test.json", json.dumps(artifact))
            result = freeze_stage1_archive(
                archive_path=archive_path,
                output_directory=root / "snapshot",
                snapshot_id="Small-KG-test-missing-system",
                knowledge_level="Small/Local",
                domain="zeolite_catalysis",
                expected_papers=1,
                allowed_systems=set(),
                repository_root=REPOSITORY_ROOT,
                frozen_at="2026-09-01T00:00:00+00:00",
                git_state={
                    "commit": "test",
                    "tree": "test",
                    "branch": "test",
                    "dirty": False,
                },
            )
            self.assertEqual(result["paper_count"], 1)
            self.assertEqual(
                result["paper_distributions"]["reaction_category"],
                {"Methanol conversion": 1},
            )


if __name__ == "__main__":
    unittest.main()
