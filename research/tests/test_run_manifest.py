from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = RESEARCH_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_research.provenance.run_manifest import (
    RunManifestError,
    complete_run,
    create_run,
    fail_run,
    load_manifest,
    record_artifact,
    record_error,
    record_runtime_stage,
    verify_run,
)


def run_git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def run_spec() -> dict[str, object]:
    return {
        "experiment_id": "pilot-v1",
        "condition_id": "M1-K247-seed17",
        "task_id": "task-1",
        "protocol": {
            "protocol_id": "catalysis-model-knowledge-scaling.v1",
            "hash": "protocol-hash",
        },
        "model_provider": "provider-test",
        "model_name": "model-test",
        "model_version": "model-test-v1",
        "temperature": 0.2,
        "seed": 17,
        "reasoning_budget": {"class": "standard"},
        "prompt_version": "descriptor-v1",
        "prompt_hash": "prompt-hash",
        "kg_snapshot": "K247-photocatalysis-v1",
        "kg_hash": (
            "df414e70e4b2ca6ad999e6fa69c1c26a60316b3b7c2eb9d01ee3f6df4f1246b6"
        ),
        "retrieval_mode": "evidence_kg",
        "retrieval_configuration": {"top_k": 30},
        "dataset": {
            "dataset_id": "dataset-test",
            "version": "v1",
            "hash": "dataset-hash",
        },
        "split": {
            "split_id": "ood-v1",
            "hash": "split-hash",
        },
        "downstream_model": {
            "name": "Ridge",
            "version": "test",
        },
        "hyperparameters": {
            "alpha": 1.0,
        },
    }


class RunManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repository = self.root / "repository"
        self.runs_root = self.root / "runs"
        self.repository.mkdir()
        run_git(self.repository, "init")
        run_git(self.repository, "config", "user.email", "test@example.com")
        run_git(self.repository, "config", "user.name", "Test User")
        (self.repository / "README.md").write_text(
            "test\n",
            encoding="utf-8",
        )
        run_git(self.repository, "add", "README.md")
        run_git(self.repository, "commit", "-m", "initial")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def create(self, run_id: str = "run-test") -> Path:
        result = create_run(
            runs_root=self.runs_root,
            spec=run_spec(),
            repository_root=self.repository,
            run_id=run_id,
            timestamp="2026-08-10T00:00:00+00:00",
        )
        return Path(result["run_directory"])

    def record_all_outputs(self, run_directory: Path) -> None:
        record_artifact(
            run_directory=run_directory,
            field="retrieved_evidence",
            value=[{"evidence_id": "E01"}],
        )
        record_artifact(
            run_directory=run_directory,
            field="hypothesis",
            value={"hypothesis_id": "H01", "statement": "Test hypothesis"},
        )
        record_artifact(
            run_directory=run_directory,
            field="descriptors",
            value=[{"descriptor_id": "D01", "name": "Test descriptor"}],
        )
        record_artifact(
            run_directory=run_directory,
            field="raw_model_output",
            value='{"raw":true}',
            media_type="text/plain",
        )
        record_artifact(
            run_directory=run_directory,
            field="structured_output",
            value={"descriptors": [{"descriptor_id": "D01"}]},
        )

    def test_completed_run_is_traceable_and_immutable(self) -> None:
        run_directory = self.create()
        self.record_all_outputs(run_directory)
        record_runtime_stage(
            run_directory=run_directory,
            stage="model_generation",
            duration_seconds=2.5,
            metadata={"attempts": 1},
        )
        completed = complete_run(
            run_directory=run_directory,
            metrics={"rmse": 0.42, "q_primary": 0.08},
            finished_at="2026-08-10T00:00:10+00:00",
        )

        report = verify_run(run_directory)
        self.assertTrue(report["valid"], report["failures"])
        self.assertEqual(completed["status"], "completed")
        self.assertEqual(completed["run_id"], "run-test")
        self.assertEqual(completed["runtime"]["duration_seconds"], 10.0)
        self.assertEqual(
            completed["git_commit"],
            run_git(self.repository, "rev-parse", "HEAD"),
        )
        self.assertTrue((run_directory / "FINALIZED.json").is_file())

        with self.assertRaises(RunManifestError):
            record_error(
                run_directory=run_directory,
                stage="late-change",
                message="Must not mutate a finalized run",
            )

    def test_artifact_tampering_is_detected(self) -> None:
        run_directory = self.create()
        self.record_all_outputs(run_directory)
        complete_run(
            run_directory=run_directory,
            metrics={"rmse": 0.42},
            finished_at="2026-08-10T00:00:10+00:00",
        )
        (run_directory / "descriptors.json").write_text(
            "tampered\n",
            encoding="utf-8",
        )

        report = verify_run(run_directory)
        self.assertFalse(report["valid"])
        self.assertIn(
            "Artifact hash mismatch: descriptors",
            report["failures"],
        )

    def test_finalization_tampering_is_detected(self) -> None:
        run_directory = self.create()
        self.record_all_outputs(run_directory)
        complete_run(
            run_directory=run_directory,
            metrics={"rmse": 0.42},
            finished_at="2026-08-10T00:00:10+00:00",
        )
        finalization_path = run_directory / "FINALIZED.json"
        finalization = json.loads(
            finalization_path.read_text(encoding="utf-8")
        )
        finalization["finalized_at"] = "2026-08-10T00:00:11+00:00"
        finalization_path.write_text(
            json.dumps(finalization),
            encoding="utf-8",
        )

        report = verify_run(run_directory)

        self.assertFalse(report["valid"])
        self.assertIn(
            "Finalization record mismatch",
            report["failures"],
        )

    def test_unsafe_artifact_path_is_rejected_without_external_read(self) -> None:
        run_directory = self.create()
        manifest_path = run_directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        artifact = {
            "path": "../outside.json",
            "sha256": "0" * 64,
            "bytes": 0,
            "media_type": "application/json",
        }
        manifest["descriptors"] = artifact
        manifest["artifacts"]["descriptors"] = artifact
        manifest_path.write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        report = verify_run(run_directory)

        self.assertFalse(report["valid"])
        self.assertIn(
            "Unsafe artifact path: descriptors",
            report["failures"],
        )

    def test_failed_run_retains_error_and_finalizes(self) -> None:
        run_directory = self.create()
        failed = fail_run(
            run_directory=run_directory,
            stage="retrieval",
            error_type="RetrievalFailure",
            message="No evidence returned",
            finished_at="2026-08-10T00:00:05+00:00",
        )

        report = verify_run(run_directory)
        self.assertTrue(report["valid"], report["failures"])
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(failed["errors"][0]["stage"], "retrieval")
        self.assertEqual(report["error_count"], 1)

    def test_completed_run_requires_every_scientific_output(self) -> None:
        run_directory = self.create()

        with self.assertRaises(RunManifestError):
            complete_run(
                run_directory=run_directory,
                metrics={"rmse": 0.42},
            )

    def test_artifact_field_cannot_be_overwritten(self) -> None:
        run_directory = self.create()
        record_artifact(
            run_directory=run_directory,
            field="hypothesis",
            value={"hypothesis_id": "H01"},
        )

        with self.assertRaises(RunManifestError):
            record_artifact(
                run_directory=run_directory,
                field="hypothesis",
                value={"hypothesis_id": "H02"},
            )

    def test_dirty_repository_is_rejected_by_default(self) -> None:
        (self.repository / "README.md").write_text(
            "dirty\n",
            encoding="utf-8",
        )

        with self.assertRaises(RunManifestError):
            create_run(
                runs_root=self.runs_root,
                spec=run_spec(),
                repository_root=self.repository,
            )

    def test_invalid_relative_run_id_is_rejected(self) -> None:
        with self.assertRaises(RunManifestError):
            create_run(
                runs_root=self.runs_root,
                spec=run_spec(),
                repository_root=self.repository,
                run_id="..",
            )

    def test_create_failure_removes_partial_run_directory(self) -> None:
        run_directory = self.runs_root / "run-write-failure"

        with patch(
            "catalysis_research.provenance.run_manifest._write_manifest",
            side_effect=OSError("simulated write failure"),
        ):
            with self.assertRaises(OSError):
                create_run(
                    runs_root=self.runs_root,
                    spec=run_spec(),
                    repository_root=self.repository,
                    run_id=run_directory.name,
                )

        self.assertFalse(run_directory.exists())

    def test_schema_lists_required_traceability_fields(self) -> None:
        schema = json.loads(
            (
                RESEARCH_ROOT
                / "manifests"
                / "schemas"
                / "run-manifest.schema.json"
            ).read_text(encoding="utf-8")
        )
        required = set(schema["required"])

        self.assertTrue(
            {
                "run_id",
                "git_commit",
                "model_provider",
                "model_name",
                "model_version",
                "temperature",
                "seed",
                "reasoning_budget",
                "prompt_version",
                "kg_snapshot",
                "kg_hash",
                "retrieval_mode",
                "retrieved_evidence",
                "hypothesis",
                "descriptors",
                "raw_model_output",
                "structured_output",
                "dataset",
                "split",
                "downstream_model",
                "hyperparameters",
                "metrics",
                "errors",
                "runtime",
            }.issubset(required)
        )

    def test_running_manifest_verifies_with_warning(self) -> None:
        run_directory = self.create()
        manifest = load_manifest(run_directory)
        report = verify_run(run_directory)

        self.assertEqual(manifest["status"], "running")
        self.assertTrue(report["valid"])
        self.assertIn("Run is still running", report["warnings"])

    def test_unregistered_file_is_detected(self) -> None:
        run_directory = self.create()
        (run_directory / "manual-result.csv").write_text(
            "metric,value\nrmse,0.1\n",
            encoding="utf-8",
        )

        report = verify_run(run_directory)
        self.assertFalse(report["valid"])
        self.assertTrue(
            any(
                failure.startswith("Unregistered run files:")
                for failure in report["failures"]
            )
        )

    def test_cli_creates_and_verifies_running_manifest(self) -> None:
        config_path = self.root / "run-spec.json"
        config_path.write_text(
            json.dumps(run_spec()),
            encoding="utf-8",
        )
        script = RESEARCH_ROOT / "scripts" / "research.py"
        created = subprocess.run(
            [
                sys.executable,
                str(script),
                "run",
                "create",
                "--config",
                str(config_path),
                "--runs-root",
                str(self.runs_root),
                "--repository-root",
                str(self.repository),
                "--run-id",
                "run-cli-test",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(json.loads(created.stdout)["run_id"], "run-cli-test")

        verified = subprocess.run(
            [
                sys.executable,
                str(script),
                "run",
                "verify",
                "--run",
                str(self.runs_root / "run-cli-test"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertTrue(json.loads(verified.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
