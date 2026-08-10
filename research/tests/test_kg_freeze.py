from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = RESEARCH_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_research.kg.freeze_stage1 import (
    freeze_stage1_archive,
    verify_snapshot,
)


def evidence() -> list[dict[str, object]]:
    return [
        {
            "pdf_page_index": 1,
            "section": "Results",
            "quote": "Synthetic evidence.",
            "evidence_validation": "exact",
        }
    ]


class KnowledgeSnapshotTests(unittest.TestCase):
    def test_freezes_and_verifies_stage1_archive(self) -> None:
        artifact = {
            "source": {
                "path": "paper.pdf",
                "source_pdf_sha256": "a" * 64,
                "model_requested": "model-test",
                "extracted_text_sha256": "b" * 64,
            },
            "extraction": {
                "schema_version": "zeolite_paper_extraction.v1",
                "paper": {
                    "id": "paper:test",
                    "title": "Synthetic paper",
                    "doi": "10.0000/test",
                    "year": 2026,
                    "paper_type": "research_article",
                    "catalysis_system": "photocatalysis",
                    "source_pdf_sha256": "a" * 64,
                },
                "keywords": {
                    "extracted": [
                        {
                            "id": "keyword:k1",
                            "raw_term": "zeolite",
                            "normalized_term": "zeolite",
                            "category": "material",
                            "evidence": evidence(),
                        }
                    ]
                },
                "entities": [
                    {
                        "id": "entity:e1",
                        "type": "material",
                        "canonical_name": "Zeolite",
                        "zh_name": "Zeolite",
                        "evidence": evidence(),
                    }
                ],
                "experiments": [
                    {
                        "id": "experiment:x1",
                        "experiment_type": "activity_test",
                        "objective": "Test activity",
                        "sample_entity_ids": ["entity:e1"],
                        "material_entity_ids": [],
                        "method_entity_ids": [],
                        "evidence": evidence(),
                    }
                ],
                "observations": [
                    {
                        "id": "observation:o1",
                        "experiment_id": "experiment:x1",
                        "sample_entity_id": "entity:e1",
                        "property_entity_id": "entity:e1",
                        "method_entity_id": "entity:e1",
                        "metric_name": "conversion",
                        "numeric_value": 1.0,
                        "unit": "%",
                        "evidence": evidence(),
                    }
                ],
                "claims": [
                    {
                        "id": "claim:c1",
                        "claim_type": "reported_result",
                        "statement": "The catalyst was active.",
                        "evidence": evidence(),
                    }
                ],
                "extraction_metadata": {
                    "model": "model-test",
                    "prompt_version": "prompt-test-v1",
                    "extracted_at": "2026-08-10T00:00:00Z",
                    "extracted_text_sha256": "b" * 64,
                },
            },
        }
        manifest = {
            "schema": "catalysis_research_dataset.v1",
            "generatedAt": "2026-08-10T00:00:00Z",
            "counts": {"documents": 1},
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive_path = root / "dataset.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr(
                    "dataset-manifest.json",
                    json.dumps(manifest),
                )
                archive.writestr(
                    "json/0001.json",
                    json.dumps(artifact),
                )
            output = root / "snapshot"
            result = freeze_stage1_archive(
                archive_path=archive_path,
                output_directory=output,
                snapshot_id="K1-test-v1",
                knowledge_level="K1",
                domain="photocatalysis",
                expected_papers=1,
                allowed_systems={"photocatalysis"},
                repository_root=Path(__file__).resolve().parents[2],
                frozen_at="2026-08-10T00:00:00+00:00",
            )

            self.assertEqual(result["paper_count"], 1)
            self.assertEqual(result["graph"]["node_count"], 6)
            self.assertEqual(
                result["graph"]["relation_distribution"][
                    "PAPER_ASSERTS_CLAIM"
                ],
                1,
            )
            self.assertTrue(verify_snapshot(output)["valid"])

    def test_refuses_to_overwrite_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = root / "snapshot"
            output.mkdir()

            with self.assertRaises(FileExistsError):
                freeze_stage1_archive(
                    archive_path=root / "missing.zip",
                    output_directory=output,
                    snapshot_id="K1-test-v1",
                    knowledge_level="K1",
                    domain="photocatalysis",
                    expected_papers=1,
                    allowed_systems={"photocatalysis"},
                    repository_root=Path(__file__).resolve().parents[2],
                )
