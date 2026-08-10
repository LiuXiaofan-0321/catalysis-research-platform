from __future__ import annotations

import copy
import hashlib
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import traceback
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


RUN_MANIFEST_SCHEMA_VERSION = "run_manifest.v1"
RUN_FINALIZATION_SCHEMA_VERSION = "run_finalization.v1"

OUTPUT_FIELDS = {
    "retrieved_evidence": "retrieved_evidence.json",
    "hypothesis": "hypothesis.json",
    "descriptors": "descriptors.json",
    "raw_model_output": "raw_model_output.json",
    "structured_output": "structured_output.json",
}

REQUIRED_SPEC_FIELDS = (
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
    "dataset",
    "split",
    "downstream_model",
    "hyperparameters",
)

COMPLETED_OUTPUT_FIELDS = tuple(OUTPUT_FIELDS)


class RunManifestError(RuntimeError):
    """Raised when a run violates the manifest lifecycle."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _run_git(repository_root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def inspect_git_state(repository_root: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    return {
        "commit": _run_git(repository_root, "rev-parse", "HEAD"),
        "tree": _run_git(repository_root, "rev-parse", "HEAD^{tree}"),
        "branch": _run_git(repository_root, "branch", "--show-current"),
        "dirty": bool(_run_git(repository_root, "status", "--porcelain")),
    }


def _validate_nonempty_string(spec: dict[str, Any], field: str) -> None:
    value = spec.get(field)
    if not isinstance(value, str) or not value.strip():
        raise RunManifestError(f"{field} must be a non-empty string")


def validate_run_spec(spec: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_SPEC_FIELDS if field not in spec]
    if missing:
        raise RunManifestError(
            f"Run spec is missing required fields: {', '.join(missing)}"
        )
    for field in (
        "model_provider",
        "model_name",
        "model_version",
        "prompt_version",
        "kg_snapshot",
        "kg_hash",
        "retrieval_mode",
    ):
        _validate_nonempty_string(spec, field)
    if isinstance(spec["seed"], bool) or not isinstance(spec["seed"], int):
        raise RunManifestError("seed must be an integer")
    if isinstance(spec["temperature"], bool) or not isinstance(
        spec["temperature"],
        (int, float),
    ):
        raise RunManifestError("temperature must be numeric")
    if spec["reasoning_budget"] is None:
        raise RunManifestError("reasoning_budget must not be null")
    if not re.fullmatch(r"[0-9a-f]{64}", str(spec["kg_hash"])):
        raise RunManifestError("kg_hash must be a full SHA256 hash")
    for field in ("dataset", "split", "downstream_model", "hyperparameters"):
        if not isinstance(spec[field], dict):
            raise RunManifestError(f"{field} must be an object")
    if not spec["dataset"]:
        raise RunManifestError("dataset must not be empty")
    if not spec["split"]:
        raise RunManifestError("split must not be empty")
    if not spec["downstream_model"]:
        raise RunManifestError("downstream_model must not be empty")


def _manifest_hash(manifest: dict[str, Any]) -> str:
    value = copy.deepcopy(manifest)
    value.pop("manifest_content_hash", None)
    return content_hash(value)


def _atomic_write_bytes(path: Path, value: bytes, *, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise RunManifestError(f"Artifact already exists: {path}")
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(handle, "wb") as output:
            output.write(value)
            output.flush()
            os.fsync(output.fileno())
        if path.exists() and not overwrite:
            raise RunManifestError(f"Artifact already exists: {path}")
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _atomic_write_json(path: Path, value: Any, *, overwrite: bool) -> None:
    serialized = (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    _atomic_write_bytes(
        path,
        serialized.encode("utf-8"),
        overwrite=overwrite,
    )


def load_manifest(run_directory: Path) -> dict[str, Any]:
    path = run_directory.resolve() / "manifest.json"
    if not path.is_file():
        raise RunManifestError(f"Run manifest does not exist: {path}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise RunManifestError(f"Run manifest must be a JSON object: {path}")
    return manifest


def _write_manifest(
    run_directory: Path,
    manifest: dict[str, Any],
    *,
    timestamp: str | None = None,
) -> dict[str, Any]:
    manifest["updated_at"] = timestamp or utc_now()
    manifest["manifest_content_hash"] = _manifest_hash(manifest)
    _atomic_write_json(
        run_directory / "manifest.json",
        manifest,
        overwrite=True,
    )
    return manifest


@contextmanager
def _run_lock(run_directory: Path) -> Iterator[None]:
    lock_path = run_directory / ".run.lock"
    try:
        descriptor = os.open(
            lock_path,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
        )
    except FileExistsError as error:
        raise RunManifestError(f"Run is locked: {run_directory}") from error
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as lock:
            lock.write(f"{os.getpid()}\n")
        yield
    finally:
        lock_path.unlink(missing_ok=True)


def _ensure_mutable(run_directory: Path, manifest: dict[str, Any]) -> None:
    if (run_directory / "FINALIZED.json").exists():
        raise RunManifestError(f"Run is finalized: {run_directory.name}")
    if manifest.get("status") != "running":
        raise RunManifestError(
            f"Run is not mutable in status {manifest.get('status')}"
        )


def _generate_run_id(spec: dict[str, Any], timestamp: str) -> str:
    compact_timestamp = re.sub(r"[^0-9]", "", timestamp)[:20]
    spec_hash = content_hash(spec)[:10]
    unique = uuid.uuid4().hex[:10]
    return f"run-{compact_timestamp}-{spec_hash}-{unique}"


def create_run(
    *,
    runs_root: Path,
    spec: dict[str, Any],
    repository_root: Path,
    allow_dirty: bool = False,
    run_id: str | None = None,
    timestamp: str | None = None,
    git_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_run_spec(spec)
    started_at = timestamp or utc_now()
    state = git_state or inspect_git_state(repository_root)
    if state.get("dirty") and not allow_dirty:
        raise RunManifestError(
            "Refusing to create an outcome-bearing run from a dirty Git tree"
        )

    resolved_run_id = run_id or _generate_run_id(spec, started_at)
    if (
        resolved_run_id in {".", ".."}
        or not re.fullmatch(r"[A-Za-z0-9._-]+", resolved_run_id)
    ):
        raise RunManifestError(
            "run_id may contain only letters, numbers, dot, underscore, and dash"
        )
    if not re.fullmatch(r"[0-9a-f]{40}", str(state.get("commit", ""))):
        raise RunManifestError("Git state must contain a full commit hash")
    tree = state.get("tree")
    if tree is not None and not re.fullmatch(r"[0-9a-f]{40}", str(tree)):
        raise RunManifestError("Git state tree must be a full hash or null")
    run_directory = runs_root.resolve() / resolved_run_id
    try:
        run_directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError as error:
        raise RunManifestError(
            f"Run directory already exists: {run_directory}"
        ) from error

    manifest = {
        "schema_version": RUN_MANIFEST_SCHEMA_VERSION,
        "run_id": resolved_run_id,
        "status": "running",
        "created_at": started_at,
        "updated_at": started_at,
        "experiment_id": spec.get("experiment_id"),
        "condition_id": spec.get("condition_id"),
        "task_id": spec.get("task_id"),
        "protocol": copy.deepcopy(spec.get("protocol") or {}),
        "git_commit": state["commit"],
        "git_tree": state.get("tree"),
        "git_branch": state.get("branch"),
        "git_dirty": bool(state.get("dirty")),
        "model_provider": spec["model_provider"],
        "model_name": spec["model_name"],
        "model_version": spec["model_version"],
        "temperature": spec["temperature"],
        "seed": spec["seed"],
        "reasoning_budget": copy.deepcopy(spec["reasoning_budget"]),
        "prompt_version": spec["prompt_version"],
        "prompt_hash": spec.get("prompt_hash"),
        "kg_snapshot": spec["kg_snapshot"],
        "kg_hash": spec["kg_hash"],
        "retrieval_mode": spec["retrieval_mode"],
        "retrieval_configuration": copy.deepcopy(
            spec.get("retrieval_configuration") or {}
        ),
        "retrieved_evidence": None,
        "hypothesis": None,
        "descriptors": None,
        "raw_model_output": None,
        "structured_output": None,
        "dataset": copy.deepcopy(spec["dataset"]),
        "split": copy.deepcopy(spec["split"]),
        "downstream_model": copy.deepcopy(spec["downstream_model"]),
        "hyperparameters": copy.deepcopy(spec["hyperparameters"]),
        "metrics": {},
        "errors": [],
        "manual_interventions": [],
        "runtime": {
            "started_at": started_at,
            "finished_at": None,
            "duration_seconds": None,
            "host": socket.gethostname(),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "process_id": os.getpid(),
            "stages": {},
        },
        "artifacts": {},
        "manifest_content_hash": "",
    }
    try:
        _write_manifest(run_directory, manifest, timestamp=started_at)
    except BaseException:
        shutil.rmtree(run_directory, ignore_errors=True)
        raise
    return {
        "run_id": resolved_run_id,
        "run_directory": str(run_directory),
        "manifest": manifest,
    }


def record_artifact(
    *,
    run_directory: Path,
    field: str,
    value: Any,
    media_type: str = "application/json",
) -> dict[str, Any]:
    if field not in OUTPUT_FIELDS:
        raise RunManifestError(
            f"Unsupported run artifact field: {field}"
        )
    run_directory = run_directory.resolve()
    with _run_lock(run_directory):
        manifest = load_manifest(run_directory)
        _ensure_mutable(run_directory, manifest)
        if manifest.get(field) is not None:
            raise RunManifestError(f"Run field already recorded: {field}")

        default_name = OUTPUT_FIELDS[field]
        if media_type == "application/json":
            serialized = (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
            filename = default_name
        elif media_type == "text/plain":
            serialized = str(value).encode("utf-8")
            filename = default_name.removesuffix(".json") + ".txt"
        else:
            raise RunManifestError(
                f"Unsupported artifact media type: {media_type}"
            )

        artifact_path = run_directory / filename
        _atomic_write_bytes(artifact_path, serialized, overwrite=False)
        artifact = {
            "path": filename,
            "sha256": sha256_bytes(serialized),
            "bytes": len(serialized),
            "media_type": media_type,
        }
        manifest[field] = copy.deepcopy(artifact)
        manifest["artifacts"][field] = copy.deepcopy(artifact)
        try:
            _write_manifest(run_directory, manifest)
        except BaseException:
            try:
                artifact_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise
        return artifact


def record_runtime_stage(
    *,
    run_directory: Path,
    stage: str,
    duration_seconds: float,
    metadata: dict[str, Any] | None = None,
) -> None:
    if duration_seconds < 0:
        raise RunManifestError("Runtime duration must be non-negative")
    run_directory = run_directory.resolve()
    with _run_lock(run_directory):
        manifest = load_manifest(run_directory)
        _ensure_mutable(run_directory, manifest)
        if stage in manifest["runtime"]["stages"]:
            raise RunManifestError(f"Runtime stage already recorded: {stage}")
        manifest["runtime"]["stages"][stage] = {
            "duration_seconds": float(duration_seconds),
            "metadata": copy.deepcopy(metadata or {}),
        }
        _write_manifest(run_directory, manifest)


def record_manual_intervention(
    *,
    run_directory: Path,
    actor: str,
    reason: str,
    action: str,
    timestamp: str | None = None,
) -> None:
    if not actor.strip() or not reason.strip() or not action.strip():
        raise RunManifestError(
            "Manual intervention requires actor, reason, and action"
        )
    run_directory = run_directory.resolve()
    with _run_lock(run_directory):
        manifest = load_manifest(run_directory)
        _ensure_mutable(run_directory, manifest)
        manifest["manual_interventions"].append(
            {
                "timestamp": timestamp or utc_now(),
                "actor": actor,
                "reason": reason,
                "action": action,
            }
        )
        _write_manifest(run_directory, manifest)


def _error_record(
    *,
    stage: str,
    error_type: str,
    message: str,
    traceback_text: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    return {
        "timestamp": timestamp or utc_now(),
        "stage": stage,
        "type": error_type,
        "message": message,
        "traceback": traceback_text,
    }


def record_error(
    *,
    run_directory: Path,
    stage: str,
    error: BaseException | None = None,
    error_type: str | None = None,
    message: str | None = None,
) -> dict[str, Any]:
    if error is None and not message:
        raise RunManifestError("An exception or error message is required")
    record = _error_record(
        stage=stage,
        error_type=error_type or (
            type(error).__name__ if error is not None else "RunError"
        ),
        message=message or str(error),
        traceback_text=(
            "".join(traceback.format_exception(error))
            if error is not None
            else None
        ),
    )
    run_directory = run_directory.resolve()
    with _run_lock(run_directory):
        manifest = load_manifest(run_directory)
        _ensure_mutable(run_directory, manifest)
        manifest["errors"].append(record)
        _write_manifest(run_directory, manifest)
    return record


def _finished_runtime(
    runtime: dict[str, Any],
    finished_at: str,
) -> dict[str, Any]:
    result = copy.deepcopy(runtime)
    started_at = datetime.fromisoformat(result["started_at"])
    ended_at = datetime.fromisoformat(finished_at)
    result["finished_at"] = finished_at
    result["duration_seconds"] = max(
        0.0,
        (ended_at - started_at).total_seconds(),
    )
    return result


def _finalize(
    *,
    run_directory: Path,
    manifest: dict[str, Any],
    status: str,
    finished_at: str,
) -> dict[str, Any]:
    manifest["status"] = status
    manifest["runtime"] = _finished_runtime(
        manifest["runtime"],
        finished_at,
    )
    _write_manifest(run_directory, manifest, timestamp=finished_at)
    finalization = {
        "schema_version": RUN_FINALIZATION_SCHEMA_VERSION,
        "run_id": manifest["run_id"],
        "status": status,
        "finalized_at": finished_at,
        "manifest_content_hash": manifest["manifest_content_hash"],
    }
    _atomic_write_json(
        run_directory / "FINALIZED.json",
        finalization,
        overwrite=False,
    )
    return manifest


def complete_run(
    *,
    run_directory: Path,
    metrics: dict[str, Any],
    finished_at: str | None = None,
) -> dict[str, Any]:
    if not isinstance(metrics, dict) or not metrics:
        raise RunManifestError("Completed runs require non-empty metrics")
    run_directory = run_directory.resolve()
    with _run_lock(run_directory):
        manifest = load_manifest(run_directory)
        _ensure_mutable(run_directory, manifest)
        missing_outputs = [
            field
            for field in COMPLETED_OUTPUT_FIELDS
            if manifest.get(field) is None
        ]
        if missing_outputs:
            raise RunManifestError(
                "Completed run is missing artifacts: "
                + ", ".join(missing_outputs)
            )
        manifest["metrics"] = copy.deepcopy(metrics)
        return _finalize(
            run_directory=run_directory,
            manifest=manifest,
            status="completed",
            finished_at=finished_at or utc_now(),
        )


def fail_run(
    *,
    run_directory: Path,
    stage: str,
    error: BaseException | None = None,
    error_type: str | None = None,
    message: str | None = None,
    finished_at: str | None = None,
) -> dict[str, Any]:
    if error is None and not message:
        raise RunManifestError("An exception or error message is required")
    run_directory = run_directory.resolve()
    with _run_lock(run_directory):
        manifest = load_manifest(run_directory)
        _ensure_mutable(run_directory, manifest)
        manifest["errors"].append(
            _error_record(
                stage=stage,
                error_type=error_type or (
                    type(error).__name__
                    if error is not None
                    else "RunError"
                ),
                message=message or str(error),
                traceback_text=(
                    "".join(traceback.format_exception(error))
                    if error is not None
                    else None
                ),
            )
        )
        return _finalize(
            run_directory=run_directory,
            manifest=manifest,
            status="failed",
            finished_at=finished_at or utc_now(),
        )


def verify_run(run_directory: Path) -> dict[str, Any]:
    run_directory = run_directory.resolve()
    failures: list[str] = []
    warnings: list[str] = []
    try:
        manifest = load_manifest(run_directory)
    except (RunManifestError, json.JSONDecodeError) as error:
        return {
            "run_id": run_directory.name,
            "valid": False,
            "failures": [str(error)],
            "warnings": [],
        }

    for field in (
        "schema_version",
        "run_id",
        "status",
        "git_commit",
        *REQUIRED_SPEC_FIELDS,
        "retrieved_evidence",
        "hypothesis",
        "descriptors",
        "raw_model_output",
        "structured_output",
        "metrics",
        "errors",
        "runtime",
        "artifacts",
        "manifest_content_hash",
    ):
        if field not in manifest:
            failures.append(f"Missing manifest field: {field}")

    if manifest.get("schema_version") != RUN_MANIFEST_SCHEMA_VERSION:
        failures.append("Unsupported run manifest schema version")
    if manifest.get("run_id") != run_directory.name:
        failures.append("run_id does not match directory name")
    try:
        validate_run_spec(manifest)
    except RunManifestError as error:
        failures.append(f"Invalid run configuration: {error}")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("git_commit", ""))):
        failures.append("git_commit must be a full 40-character hash")
    if _manifest_hash(manifest) != manifest.get("manifest_content_hash"):
        failures.append("Manifest content hash mismatch")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        failures.append("artifacts must be an object")
        artifacts = {}
    registered_paths: set[str] = set()
    for field, artifact in artifacts.items():
        if field not in OUTPUT_FIELDS:
            failures.append(f"Unknown artifact field: {field}")
            continue
        if not isinstance(artifact, dict):
            failures.append(f"Artifact reference must be an object: {field}")
            continue
        if manifest.get(field) != artifact:
            failures.append(f"Artifact reference mismatch: {field}")
        relative_path = str(artifact.get("path", ""))
        candidate = Path(relative_path)
        allowed_paths = {
            OUTPUT_FIELDS[field],
            OUTPUT_FIELDS[field].removesuffix(".json") + ".txt",
        }
        if (
            relative_path not in allowed_paths
            or candidate.is_absolute()
            or ".." in candidate.parts
        ):
            failures.append(f"Unsafe artifact path: {field}")
            continue
        registered_paths.add(relative_path)
        path = run_directory / candidate
        if not path.is_file():
            failures.append(f"Missing artifact file: {field}")
            continue
        if sha256_file(path) != artifact.get("sha256"):
            failures.append(f"Artifact hash mismatch: {field}")
        if path.stat().st_size != artifact.get("bytes"):
            failures.append(f"Artifact size mismatch: {field}")

    status = manifest.get("status")
    finalization_path = run_directory / "FINALIZED.json"
    if status == "running":
        if finalization_path.exists():
            failures.append("Running run must not have FINALIZED.json")
        warnings.append("Run is still running")
    elif status in {"completed", "failed"}:
        if not finalization_path.is_file():
            failures.append("Finalized run is missing FINALIZED.json")
        else:
            try:
                finalization = json.loads(
                    finalization_path.read_text(encoding="utf-8")
                )
            except json.JSONDecodeError:
                failures.append("FINALIZED.json is invalid JSON")
            else:
                if not isinstance(finalization, dict):
                    failures.append("FINALIZED.json must be an object")
                else:
                    manifest_runtime = manifest.get("runtime")
                    if not isinstance(manifest_runtime, dict):
                        manifest_runtime = {}
                    expected_finalization = {
                        "schema_version": RUN_FINALIZATION_SCHEMA_VERSION,
                        "run_id": manifest.get("run_id"),
                        "status": status,
                        "finalized_at": manifest_runtime.get("finished_at"),
                        "manifest_content_hash": manifest.get(
                            "manifest_content_hash"
                        ),
                    }
                    if finalization != expected_finalization:
                        failures.append("Finalization record mismatch")
    else:
        failures.append(f"Unsupported run status: {status}")

    if status == "completed":
        for field in COMPLETED_OUTPUT_FIELDS:
            if manifest.get(field) is None:
                failures.append(f"Completed run missing output: {field}")
        if not manifest.get("metrics"):
            failures.append("Completed run has no metrics")
    if status == "failed" and not manifest.get("errors"):
        failures.append("Failed run has no errors")

    expected_files = {
        "manifest.json",
        *registered_paths,
    }
    if status in {"completed", "failed"}:
        expected_files.add("FINALIZED.json")
    actual_files = {
        str(path.relative_to(run_directory)).replace("\\", "/")
        for path in run_directory.rglob("*")
        if path.is_file() and path.name != ".run.lock"
    }
    unexpected_files = sorted(actual_files - expected_files)
    missing_registered_files = sorted(expected_files - actual_files)
    if unexpected_files:
        failures.append(
            "Unregistered run files: " + ", ".join(unexpected_files)
        )
    if missing_registered_files:
        failures.append(
            "Registered run files are missing: "
            + ", ".join(missing_registered_files)
        )

    runtime = manifest.get("runtime")
    if not isinstance(runtime, dict):
        failures.append("runtime must be an object")
        runtime = {}
    if status in {"completed", "failed"}:
        if runtime.get("finished_at") is None:
            failures.append("Finalized run has no runtime.finished_at")
        if runtime.get("duration_seconds") is None:
            failures.append("Finalized run has no runtime.duration_seconds")

    return {
        "run_id": manifest.get("run_id"),
        "status": status,
        "valid": not failures,
        "failures": failures,
        "warnings": warnings,
        "manifest_content_hash": manifest.get("manifest_content_hash"),
        "git_commit": manifest.get("git_commit"),
        "artifact_count": len(artifacts),
        "error_count": len(manifest.get("errors") or []),
    }
