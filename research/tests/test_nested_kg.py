from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = RESEARCH_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_research.cli import main
from catalysis_research.corpora.stage1 import (
    CorpusError,
    freeze_stage1_corpus,
    verify_stage1_corpus,
)
from catalysis_research.kg.freeze_stage1 import sha256_file
from catalysis_research.kg.nested import (
    build_nested_snapshots,
    verify_nested_snapshots,
)
from catalysis_research.kg.selection import (
    SelectionError,
    build_nested_order,
    selection_order_hash,
)


def _run_git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )


def _artifact(index: int, duplicate_doi: str | None = None) -> dict:
    topic = ("Alkylation", "Toluene_disproportionation")[
        index % 2
    ]
    paper_type = (
        "research_article"
        if index < 7
        else ("review" if index < 9 else "conference")
    )
    pdf_hash = f"{index + 1:064x}"
    return {
        "source": {
            "path": f"Reaction/{topic}/paper-{index}.pdf",
            "source_pdf_sha256": pdf_hash,
            "model_requested": "synthetic-model",
            "extracted_text_sha256": f"{index + 101:064x}",
        },
        "extraction": {
            "schema_version": "zeolite_paper_extraction.v1",
            "paper": {
                "id": f"paper:{index:03d}",
                "title": f"Synthetic paper {index}",
                "doi": duplicate_doi or f"10.0000/synthetic.{index}",
                "year": None if index == 9 else 1975 + index * 5,
                "paper_type": paper_type,
                "catalysis_system": "thermal_catalysis",
                "source_pdf_sha256": pdf_hash,
                "source_path": (
                    f"Reaction/{topic}/paper-{index}.pdf"
                ),
                "reaction_categories": [topic],
            },
            "keywords": {"extracted": []},
            "entities": [
                {
                    "id": f"entity:{index}",
                    "type": "material",
                    "canonical_name": f"Catalyst {index}",
                    "evidence": [],
                }
            ],
            "experiments": [],
            "observations": [],
            "claims": [],
            "extraction_metadata": {
                "model": "synthetic-model",
                "prompt_version": "synthetic-prompt-v1",
                "extracted_at": "2026-08-11T00:00:00Z",
                "extracted_text_sha256": f"{index + 101:064x}",
            },
        },
    }


def _write_archive(
    path: Path,
    paper_count: int = 10,
    duplicate_doi: bool = False,
) -> None:
    manifest = {
        "schema": "catalysis_research_dataset.v1",
        "generatedAt": "2026-08-11T00:00:00Z",
        "counts": {"documents": paper_count},
    }
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "dataset-manifest.json",
            json.dumps(manifest),
        )
        for index in range(paper_count):
            duplicate = (
                "10.0000/duplicate"
                if duplicate_doi and index in {0, 1}
                else None
            )
            archive.writestr(
                f"json/{index:04d}.json",
                json.dumps(_artifact(index, duplicate)),
            )


def _selection_config() -> dict:
    return {
        "selection_id": "synthetic-selection-v1",
        "selection_schema_version": "nested_kg_selection.v1",
        "algorithm_version": "proportional_stratified_hash_order.v1",
        "seed": 20260810,
        "year_bins": [
            {"id": "unknown", "unknown": True},
            {"id": "pre-1990", "minimum": None, "maximum": 1989},
            {"id": "1990-present", "minimum": 1990, "maximum": None},
        ],
        "paper_type_groups": {
            "research_article": ["research_article"],
            "review": ["review"],
            "other": ["conference", "unknown"],
        },
        "paper_type_fallback": "other",
        "topic_source_rule": (
            "first directory after Reaction in source_path"
        ),
        "levels": [
            {
                "knowledge_level": "K20",
                "paper_fraction": 0.2,
                "paper_count": 2,
                "snapshot_id": "K20-synthetic-v1",
            },
            {
                "knowledge_level": "K40",
                "paper_fraction": 0.4,
                "paper_count": 4,
                "snapshot_id": "K40-synthetic-v1",
            },
            {
                "knowledge_level": "K60",
                "paper_fraction": 0.6,
                "paper_count": 6,
                "snapshot_id": "K60-synthetic-v1",
            },
            {
                "knowledge_level": "K80",
                "paper_fraction": 0.8,
                "paper_count": 8,
                "snapshot_id": "K80-synthetic-v1",
            },
            {
                "knowledge_level": "K100",
                "paper_fraction": 1.0,
                "paper_count": 10,
                "snapshot_id": "K100-synthetic-v1",
            },
        ],
        "downstream_label_access": "forbidden",
    }


class NestedKnowledgeTests(unittest.TestCase):
    def _prepare_repository(
        self,
        root: Path,
    ) -> tuple[Path, Path, dict]:
        _run_git(root, "init")
        _run_git(root, "config", "user.email", "tests@example.com")
        _run_git(root, "config", "user.name", "Research Tests")
        archive_path = root / "data" / "stage1.zip"
        archive_path.parent.mkdir()
        _write_archive(archive_path)
        _run_git(root, "add", "data/stage1.zip")
        _run_git(root, "commit", "-m", "Add synthetic archive")

        corpus_directory = root / "research" / "corpora" / "synthetic-v1"
        manifest = freeze_stage1_corpus(
            archive_path=archive_path,
            output_directory=corpus_directory,
            corpus_id="synthetic-v1",
            domain="thermal_catalysis",
            expected_papers=10,
            allowed_systems={"thermal_catalysis"},
            repository_root=root,
            expected_archive_sha256=sha256_file(archive_path),
            frozen_at="2026-08-11T00:00:00+00:00",
        )
        return archive_path, corpus_directory, manifest

    def _write_build_config(
        self,
        root: Path,
        archive_path: Path,
        corpus_manifest: dict,
    ) -> Path:
        config = {
            "schema_version": "nested_kg_build_config.v1",
            "nested_snapshot_id": "synthetic-nested-v1",
            "corpus_id": "synthetic-v1",
            "corpus_content_hash": corpus_manifest[
                "corpus_content_hash"
            ],
            "corpus_directory": "research/corpora/synthetic-v1",
            "source_archive": "data/stage1.zip",
            "source_archive_sha256": sha256_file(archive_path),
            "domain": "thermal_catalysis",
            "allowed_systems": ["thermal_catalysis"],
            "ontology_version": "catalysis_evidence_graph.v1",
            "snapshots_root": "research/kg_snapshots",
            "nested_manifest": (
                "research/manifests/kg/synthetic-nested-v1.json"
            ),
            "selection_order_artifact": (
                "research/manifests/kg/synthetic-nested-v1.order.jsonl"
            ),
            "selection": _selection_config(),
        }
        config_path = root / "research" / "configs" / "kg" / "nested.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(
            json.dumps(config, indent=2),
            encoding="utf-8",
        )
        return config_path

    def test_selection_is_deterministic_and_rejects_labels(self) -> None:
        papers = [
            {
                "paper_id": f"paper:{index}",
                "archive_entry": f"json/{index:04d}.json",
                "raw_pdf_sha256": f"{index + 1:064x}",
                "structured_json_sha256": f"{index + 101:064x}",
                "source_topic": ("A", "B")[index % 2],
                "year": None if index == 9 else 1975 + index * 5,
                "paper_type": (
                    "research_article" if index < 7 else "review"
                ),
            }
            for index in range(10)
        ]
        config = _selection_config()
        first = build_nested_order(papers, config)
        second = build_nested_order(list(reversed(papers)), config)
        self.assertEqual(first, second)
        self.assertEqual(
            selection_order_hash(first),
            selection_order_hash(second),
        )
        forbidden = dict(config)
        forbidden["target"] = "conversion"
        with self.assertRaises(SelectionError):
            build_nested_order(papers, forbidden)

    def test_freezes_verifies_and_detects_nested_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive, _, corpus_manifest = self._prepare_repository(root)
            config_path = self._write_build_config(
                root,
                archive,
                corpus_manifest,
            )
            manifest = build_nested_snapshots(
                config_path=config_path,
                repository_root=root,
                allow_dirty=True,
                frozen_at="2026-08-11T00:00:00+00:00",
            )
            manifest_path = (
                root
                / "research"
                / "manifests"
                / "kg"
                / "synthetic-nested-v1.json"
            )
            report = verify_nested_snapshots(
                manifest_path=manifest_path,
                repository_root=root,
            )
            self.assertTrue(report["valid"], report["failures"])
            self.assertEqual(report["level_count"], 5)
            self.assertEqual(
                [level["paper_count"] for level in manifest["levels"]],
                [2, 4, 6, 8, 10],
            )

            k20_papers = (
                root
                / "research"
                / "kg_snapshots"
                / "K20-synthetic-v1"
                / "papers.jsonl"
            ).read_text(encoding="utf-8")
            self.assertEqual(len(k20_papers.splitlines()), 2)
            self.assertNotIn("paper:009", k20_papers)

            order_path = (
                root
                / "research"
                / "manifests"
                / "kg"
                / "synthetic-nested-v1.order.jsonl"
            )
            order_path.write_text(
                order_path.read_text(encoding="utf-8") + "{}\n",
                encoding="utf-8",
            )
            tampered = verify_nested_snapshots(
                manifest_path=manifest_path,
                repository_root=root,
            )
            self.assertFalse(tampered["valid"])
            self.assertIn(
                "Selection order artifact hash mismatch",
                tampered["failures"],
            )

    def test_duplicate_corpus_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _run_git(root, "init")
            _run_git(root, "config", "user.email", "tests@example.com")
            _run_git(root, "config", "user.name", "Research Tests")
            archive = root / "duplicate.zip"
            _write_archive(archive, paper_count=2, duplicate_doi=True)
            _run_git(root, "add", "duplicate.zip")
            _run_git(root, "commit", "-m", "Add duplicate archive")
            with self.assertRaisesRegex(CorpusError, "Duplicate DOI"):
                freeze_stage1_corpus(
                    archive_path=archive,
                    output_directory=root / "corpus",
                    corpus_id="duplicate",
                    domain="thermal_catalysis",
                    expected_papers=2,
                    allowed_systems={"thermal_catalysis"},
                    repository_root=root,
                )

    def test_corpus_and_nested_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            archive, corpus_directory, corpus_manifest = (
                self._prepare_repository(root)
            )
            config_path = self._write_build_config(
                root,
                archive,
                corpus_manifest,
            )
            self.assertEqual(
                main(
                    [
                        "corpus",
                        "verify",
                        "--corpus",
                        str(corpus_directory),
                    ]
                ),
                0,
            )
            self.assertEqual(
                main(
                    [
                        "kg",
                        "build-nested",
                        "--config",
                        str(config_path),
                        "--repository-root",
                        str(root),
                        "--allow-dirty",
                    ]
                ),
                0,
            )
            self.assertEqual(
                main(
                    [
                        "kg",
                        "verify-nested",
                        "--manifest",
                        str(
                            root
                            / "research"
                            / "manifests"
                            / "kg"
                            / "synthetic-nested-v1.json"
                        ),
                        "--repository-root",
                        str(root),
                    ]
                ),
                0,
            )

    def test_corpus_verification_detects_inventory_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _, corpus_directory, _ = self._prepare_repository(root)
            self.assertTrue(verify_stage1_corpus(corpus_directory)["valid"])
            papers_path = corpus_directory / "papers.jsonl"
            papers_path.write_text(
                papers_path.read_text(encoding="utf-8") + "{}\n",
                encoding="utf-8",
            )
            report = verify_stage1_corpus(corpus_directory)
            self.assertFalse(report["valid"])
            self.assertIn(
                "Corpus artifact hash mismatch: papers",
                report["failures"],
            )


if __name__ == "__main__":
    unittest.main()
