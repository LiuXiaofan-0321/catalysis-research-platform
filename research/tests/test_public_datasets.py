from __future__ import annotations

import copy
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = RESEARCH_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_research.datasets.leakage import leakage_audit
from catalysis_research.datasets.loader import (
    generation_context,
    load_partition_rows,
)
from catalysis_research.datasets.registry import (
    load_dataset_manifest,
    register_dataset,
    verify_dataset_manifest,
)
from catalysis_research.datasets.schema import (
    DatasetError,
    manifest_hash,
    split_hash,
    validate_registration_config,
)
from catalysis_research.datasets.split import (
    create_split,
    load_split_manifest,
    verify_split_manifest,
)


def run_git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def registration_config() -> dict[str, object]:
    return {
        "schema_version": "dataset_registration.v1",
        "dataset_id": "public-catalysis-test",
        "version": "v1",
        "status": "frozen",
        "study_role": "primary",
        "domain": "thermal_catalysis",
        "data_classification": "public",
        "contains_private_data": False,
        "source": {
            "name": "Synthetic public test fixture",
            "url": "https://example.test/dataset",
            "citation": "Test Fixture et al. (2026)",
            "accessed_at": "2026-08-11",
        },
        "license": {
            "name": "CC BY 4.0",
            "url": "https://creativecommons.org/licenses/by/4.0/",
            "allows_research": True,
            "allows_publication": True,
            "allows_redistribution": True,
        },
        "files": [
            {
                "path": "research/datasets/raw/public-test.csv",
                "format": "csv",
                "role": "primary_table",
            }
        ],
        "sample_id_column": "sample_id",
        "target": {
            "name": "conversion",
            "column": "target_value",
            "definition": "Synthetic conversion used only by tests.",
            "units": "%",
            "task_type": "regression",
        },
        "allowed_inputs": [
            {
                "name": "temperature_k",
                "description": "Reaction temperature.",
                "dtype": "number",
                "units": "K",
            },
            {
                "name": "catalyst_composition",
                "description": "Catalyst composition string.",
                "dtype": "string",
                "units": None,
            },
        ],
        "forbidden_inputs": [
            {
                "name": "target_value",
                "reason": "Primary label.",
            },
            {
                "name": "post_reaction_measurement",
                "reason": "Post-outcome measurement.",
            },
        ],
        "group_columns": [
            {
                "name": "catalyst_family",
                "priority": 1,
                "rationale": "Material-family OOD test.",
            },
            {
                "name": "reaction_family",
                "priority": 2,
                "rationale": "Reaction-family metadata.",
            },
        ],
        "duplicate_key_columns": ["source_record_id"],
        "missing_data_policy": {
            "strategy": "reject in test fixture",
            "maximum_allowed_fraction": 0.0,
        },
        "duplicate_policy": {
            "action": "keep_together",
            "rationale": "Source-identical records must share a partition.",
        },
        "label_access_policy": {
            "descriptor_generation": "metadata only",
            "descriptor_computation": "inputs without labels",
            "downstream_training": "train and validation labels only",
            "evaluation": "test labels only",
        },
        "iid_split": {
            "seed": 20260810,
            "ratios": {
                "train": 0.6,
                "validation": 0.2,
                "test": 0.2,
            },
            "stratify_target_quantiles": 5,
        },
        "ood_split": {
            "group_column": "catalyst_family",
            "folds": [
                {
                    "fold_id": "fold-1",
                    "test_groups": ["E"],
                    "validation_groups": ["D"],
                }
            ],
        },
    }


class PublicDatasetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repository = self.root / "repository"
        self.raw_root = (
            self.repository / "research" / "datasets" / "raw"
        )
        self.config_root = (
            self.repository / "research" / "configs" / "datasets"
        )
        self.dataset_manifest_root = (
            self.repository / "research" / "manifests" / "datasets"
        )
        self.split_manifest_root = (
            self.repository / "research" / "manifests" / "splits"
        )
        self.raw_root.mkdir(parents=True)
        self.config_root.mkdir(parents=True)
        self.dataset_path = self.raw_root / "public-test.csv"
        self.config_path = self.config_root / "public-test.json"
        self._write_dataset()
        self.config_path.write_text(
            json.dumps(registration_config(), indent=2),
            encoding="utf-8",
        )
        run_git(self.repository, "init")
        run_git(self.repository, "config", "user.email", "test@example.com")
        run_git(self.repository, "config", "user.name", "Test User")
        run_git(self.repository, "add", ".")
        run_git(self.repository, "commit", "-m", "fixture")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _write_dataset(self) -> None:
        fieldnames = [
            "sample_id",
            "source_record_id",
            "temperature_k",
            "catalyst_composition",
            "catalyst_family",
            "reaction_family",
            "post_reaction_measurement",
            "target_value",
        ]
        families = ["A", "B", "C", "D", "E"]
        with self.dataset_path.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for index in range(30):
                duplicate = index in {0, 1}
                family = "A" if duplicate else families[index % 5]
                writer.writerow(
                    {
                        "sample_id": f"S{index:03d}",
                        "source_record_id": (
                            "SOURCE-DUP"
                            if duplicate
                            else f"SOURCE-{index:03d}"
                        ),
                        "temperature_k": 500 + index,
                        "catalyst_composition": f"CAT-{family}-{index % 3}",
                        "catalyst_family": family,
                        "reaction_family": f"R{index % 3}",
                        "post_reaction_measurement": 1000 + index,
                        "target_value": 10.0 if duplicate else 20 + index,
                    }
                )

    def register(self) -> Path:
        result = register_dataset(
            config_path=self.config_path,
            output_root=self.dataset_manifest_root,
            repository_root=self.repository,
            timestamp="2026-08-11T00:00:00+00:00",
        )
        return Path(result["manifest_path"])

    def commit_dataset_manifest(self, manifest_path: Path) -> None:
        run_git(self.repository, "add", str(manifest_path))
        run_git(self.repository, "commit", "-m", "freeze dataset")

    def split(self, strategy: str) -> tuple[Path, Path]:
        dataset_manifest_path = self.register()
        self.commit_dataset_manifest(dataset_manifest_path)
        result = create_split(
            dataset_manifest_path=dataset_manifest_path,
            strategy=strategy,
            output_root=self.split_manifest_root,
            repository_root=self.repository,
            timestamp="2026-08-11T00:01:00+00:00",
        )
        return dataset_manifest_path, Path(result["split_path"])

    def test_registration_is_traceable_and_verifiable(self) -> None:
        manifest_path = self.register()
        manifest = load_dataset_manifest(manifest_path)
        report = verify_dataset_manifest(
            manifest_path,
            self.repository,
        )

        self.assertTrue(report["valid"], report["failures"])
        self.assertEqual(manifest["row_count"], 30)
        self.assertEqual(manifest["data_classification"], "public")
        self.assertFalse(manifest["contains_private_data"])
        self.assertRegex(manifest["dataset_content_hash"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["duplicate_group_count"], 1)
        schema = json.loads(
            (
                RESEARCH_ROOT
                / "manifests"
                / "schemas"
                / "dataset-manifest.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(set(schema["required"]).issubset(manifest))
        self.assertTrue(set(manifest).issubset(schema["properties"]))

    def test_private_data_cannot_enter_public_registry(self) -> None:
        config = registration_config()
        config["data_classification"] = "private"
        config["contains_private_data"] = True

        with self.assertRaises(DatasetError):
            validate_registration_config(config)

    def test_dirty_repository_is_rejected(self) -> None:
        self.dataset_path.write_text("dirty\n", encoding="utf-8")

        with self.assertRaises(DatasetError):
            register_dataset(
                config_path=self.config_path,
                output_root=self.dataset_manifest_root,
                repository_root=self.repository,
            )

    def test_dataset_file_tampering_is_detected(self) -> None:
        manifest_path = self.register()
        with self.dataset_path.open("a", encoding="utf-8") as output:
            output.write("tampered\n")

        report = verify_dataset_manifest(
            manifest_path,
            self.repository,
        )

        self.assertFalse(report["valid"])
        self.assertTrue(report["failures"])

    def test_dataset_semantic_tampering_survives_no_rehash_bypass(self) -> None:
        manifest_path = self.register()
        manifest = load_dataset_manifest(manifest_path)
        manifest["target"]["name"] = "rewritten-after-freeze"
        manifest["manifest_content_hash"] = manifest_hash(manifest)
        manifest_path.write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        report = verify_dataset_manifest(
            manifest_path,
            self.repository,
        )

        self.assertFalse(report["valid"])
        self.assertIn(
            "Dataset registration mismatch: target",
            report["failures"],
        )

    def test_malformed_dataset_manifest_returns_invalid_report(self) -> None:
        manifest_path = self.register()
        manifest = load_dataset_manifest(manifest_path)
        manifest["registration"] = {}
        manifest["manifest_content_hash"] = manifest_hash(manifest)
        manifest_path.write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        report = verify_dataset_manifest(
            manifest_path,
            self.repository,
        )

        self.assertFalse(report["valid"])
        self.assertTrue(
            any(
                failure.startswith("Invalid registration config:")
                for failure in report["failures"]
            )
        )

    def test_iid_split_is_deterministic_and_duplicate_safe(self) -> None:
        dataset_manifest_path, split_path = self.split("iid")
        first = load_split_manifest(split_path)
        second_result = create_split(
            dataset_manifest_path=dataset_manifest_path,
            strategy="iid",
            output_root=self.root / "second-splits",
            repository_root=self.repository,
            allow_dirty=True,
            timestamp="2026-08-11T00:02:00+00:00",
        )
        second = second_result["manifest"]

        self.assertEqual(first["split_hash"], second["split_hash"])
        self.assertEqual(first["partitions"], second["partitions"])
        self.assertAlmostEqual(
            sum(first["observed_ratios"].values()),
            1.0,
        )
        schema = json.loads(
            (
                RESEARCH_ROOT
                / "manifests"
                / "schemas"
                / "split-manifest.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(set(schema["required"]).issubset(first))
        self.assertTrue(set(first).issubset(schema["properties"]))
        memberships = {
            identifier: partition
            for partition, identifiers in first["partitions"].items()
            for identifier in identifiers
        }
        self.assertEqual(memberships["S000"], memberships["S001"])
        self.assertTrue(
            all(first["partitions"][partition] for partition in (
                "train",
                "validation",
                "test",
            ))
        )

    def test_ood_split_holds_out_complete_groups(self) -> None:
        dataset_manifest_path, split_path = self.split("ood")
        split_manifest = load_split_manifest(split_path)
        dataset_manifest = load_dataset_manifest(dataset_manifest_path)
        fold = split_manifest["folds"][0]
        test_rows = load_partition_rows(
            dataset_manifest=dataset_manifest,
            split_manifest=split_manifest,
            repository_root=self.repository,
            partition="test",
            access_role="audit",
            fold_id="fold-1",
        )
        validation_rows = load_partition_rows(
            dataset_manifest=dataset_manifest,
            split_manifest=split_manifest,
            repository_root=self.repository,
            partition="validation",
            access_role="audit",
            fold_id="fold-1",
        )

        self.assertEqual(
            {row["catalyst_family"] for row in test_rows},
            {"E"},
        )
        self.assertEqual(
            {row["catalyst_family"] for row in validation_rows},
            {"D"},
        )
        self.assertEqual(fold["test_groups"], ["E"])

    def test_split_tampering_is_detected(self) -> None:
        dataset_manifest_path, split_path = self.split("iid")
        split_manifest = load_split_manifest(split_path)
        moved = split_manifest["partitions"]["train"].pop()
        split_manifest["partitions"]["test"].append(moved)
        split_path.write_text(
            json.dumps(split_manifest),
            encoding="utf-8",
        )

        report = verify_split_manifest(
            split_manifest_path=split_path,
            dataset_manifest_path=dataset_manifest_path,
            repository_root=self.repository,
        )

        self.assertFalse(report["valid"])
        self.assertIn(
            "Split manifest content hash mismatch",
            report["failures"],
        )

    def test_split_identity_tampering_survives_no_rehash_bypass(self) -> None:
        dataset_manifest_path, split_path = self.split("iid")
        split_manifest = load_split_manifest(split_path)
        split_manifest["split_id"] = "rewritten-split-id"
        split_manifest["split_hash"] = split_hash(split_manifest)
        split_manifest["manifest_content_hash"] = manifest_hash(
            split_manifest
        )
        split_path.write_text(
            json.dumps(split_manifest),
            encoding="utf-8",
        )

        report = verify_split_manifest(
            split_manifest_path=split_path,
            dataset_manifest_path=dataset_manifest_path,
            repository_root=self.repository,
        )

        self.assertFalse(report["valid"])
        self.assertIn(
            "Split manifest filename does not match split_id",
            report["failures"],
        )
        self.assertIn(
            "Split manifest mismatch: split_id",
            report["failures"],
        )

    def test_label_access_policy_blocks_test_labels(self) -> None:
        dataset_manifest_path, split_path = self.split("iid")
        dataset_manifest = load_dataset_manifest(dataset_manifest_path)
        split_manifest = load_split_manifest(split_path)
        context = generation_context(dataset_manifest)

        self.assertFalse(context["row_data_included"])
        self.assertNotIn(
            dataset_manifest["target"]["column"],
            json.dumps(context),
        )
        descriptor_rows = load_partition_rows(
            dataset_manifest=dataset_manifest,
            split_manifest=split_manifest,
            repository_root=self.repository,
            partition="test",
            access_role="descriptor_computation",
        )
        self.assertNotIn("target_value", descriptor_rows[0])

        with self.assertRaises(DatasetError):
            load_partition_rows(
                dataset_manifest=dataset_manifest,
                split_manifest=split_manifest,
                repository_root=self.repository,
                partition="test",
                access_role="downstream_training",
            )

        evaluator_rows = load_partition_rows(
            dataset_manifest=dataset_manifest,
            split_manifest=split_manifest,
            repository_root=self.repository,
            partition="test",
            access_role="evaluation",
        )
        self.assertIn("target_value", evaluator_rows[0])

    def test_leakage_audit_passes_for_generated_splits(self) -> None:
        dataset_manifest_path, split_path = self.split("ood")

        report = leakage_audit(
            dataset_manifest_path=dataset_manifest_path,
            repository_root=self.repository,
            split_manifest_path=split_path,
        )

        self.assertTrue(report["valid"], report["failures"])
        self.assertTrue(report["manual_review_required"])

    def test_target_cannot_be_an_allowed_input(self) -> None:
        config = registration_config()
        config["allowed_inputs"] = [
            *config["allowed_inputs"],
            {
                "name": "target_value",
                "description": "Leak",
                "dtype": "number",
                "units": "%",
            },
        ]

        with self.assertRaises(DatasetError):
            validate_registration_config(config)

    def test_cli_register_and_verify(self) -> None:
        script = RESEARCH_ROOT / "scripts" / "research.py"
        registered = subprocess.run(
            [
                sys.executable,
                str(script),
                "dataset",
                "register",
                "--config",
                str(self.config_path),
                "--output-root",
                str(self.dataset_manifest_root),
                "--repository-root",
                str(self.repository),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(registered.returncode, 0, registered.stdout)
        manifest_path = Path(json.loads(registered.stdout)["manifest_path"])

        verified = subprocess.run(
            [
                sys.executable,
                str(script),
                "dataset",
                "verify",
                "--manifest",
                str(manifest_path),
                "--repository-root",
                str(self.repository),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(verified.returncode, 0, verified.stdout)
        self.assertTrue(json.loads(verified.stdout)["valid"])

        self.commit_dataset_manifest(manifest_path)
        split = subprocess.run(
            [
                sys.executable,
                str(script),
                "dataset",
                "split",
                "--dataset",
                "public-catalysis-test",
                "--strategy",
                "iid",
                "--dataset-manifests-root",
                str(self.dataset_manifest_root),
                "--output-root",
                str(self.split_manifest_root),
                "--repository-root",
                str(self.repository),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(split.returncode, 0, split.stdout)
        split_path = Path(json.loads(split.stdout)["split_path"])

        split_verified = subprocess.run(
            [
                sys.executable,
                str(script),
                "dataset",
                "verify-split",
                "--dataset-manifest",
                str(manifest_path),
                "--split",
                str(split_path),
                "--repository-root",
                str(self.repository),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            split_verified.returncode,
            0,
            split_verified.stdout,
        )
        self.assertTrue(json.loads(split_verified.stdout)["valid"])

    def test_manifest_schemas_include_frozen_hashes(self) -> None:
        dataset_schema = json.loads(
            (
                RESEARCH_ROOT
                / "manifests"
                / "schemas"
                / "dataset-manifest.schema.json"
            ).read_text(encoding="utf-8")
        )
        split_schema = json.loads(
            (
                RESEARCH_ROOT
                / "manifests"
                / "schemas"
                / "split-manifest.schema.json"
            ).read_text(encoding="utf-8")
        )

        self.assertTrue(
            {
                "dataset_id",
                "files",
                "sample_id_hash",
                "dataset_content_hash",
                "target",
                "allowed_inputs",
                "label_access_policy",
            }.issubset(set(dataset_schema["required"]))
        )
        self.assertTrue(
            {
                "split_id",
                "dataset_content_hash",
                "configuration",
                "split_hash",
            }.issubset(set(split_schema["required"]))
        )
        registry = json.loads(
            (
                RESEARCH_ROOT
                / "configs"
                / "datasets"
                / "public-registry.v1.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(registry["status"], "ACTIVATION_BLOCKED")
        self.assertEqual(registry["datasets"], [])
        example = json.loads(
            (
                RESEARCH_ROOT
                / "configs"
                / "datasets"
                / "example-dataset-registration.json"
            ).read_text(encoding="utf-8")
        )
        validate_registration_config(example)


if __name__ == "__main__":
    unittest.main()
