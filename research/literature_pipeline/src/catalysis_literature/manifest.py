from __future__ import annotations

import copy
import json
import platform
import re
import socket
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .hashing import atomic_write_json, content_hash, sha256_file
from .models import RUN_SCHEMA_VERSION


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_state(repository_root: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    status = run("status", "--porcelain")
    return {
        "commit": run("rev-parse", "HEAD"),
        "tree": run("rev-parse", "HEAD^{tree}"),
        "branch": run("branch", "--show-current") or None,
        "dirty": bool(status),
    }


def _manifest_hash(manifest: dict[str, Any]) -> str:
    payload = copy.deepcopy(manifest)
    payload["manifest_content_hash"] = ""
    return content_hash(payload)


def generate_run_id(config_hash: str) -> str:
    stamp = re.sub(r"\D", "", utc_now())[:14]
    return f"lit-{stamp}-{config_hash[:10]}-{uuid.uuid4().hex[:8]}"


def create_run_manifest(
    *,
    run_directory: Path,
    run_id: str,
    config: dict[str, Any],
    config_hash: str,
    repository_root: Path,
) -> dict[str, Any]:
    run_directory.mkdir(parents=True, exist_ok=False)
    timestamp = utc_now()
    manifest: dict[str, Any] = {
        "schema_version": RUN_SCHEMA_VERSION,
        "run_id": run_id,
        "status": "running",
        "created_at": timestamp,
        "updated_at": timestamp,
        "git": git_state(repository_root),
        "config": config,
        "config_hash": config_hash,
        "inventory": None,
        "stages": {
            "parse": {"completed": 0, "cached": 0, "failed": 0},
            "extract": {"completed": 0, "cached": 0, "failed": 0},
            "index": {"completed": 0, "failed": 0},
        },
        "model": {
            "provider": (config.get("extraction") or {}).get("provider"),
            "name": (config.get("extraction") or {}).get("model"),
            "temperature": (config.get("extraction") or {}).get("temperature"),
            "seed": (config.get("extraction") or {}).get("seed"),
            "prompt_version": (config.get("extraction") or {}).get(
                "prompt_version"
            ),
        },
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "model_calls": 0,
            "cache_hits": 0,
        },
        "errors": [],
        "artifacts": {},
        "runtime": {
            "host": socket.gethostname(),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "finished_at": None,
            "duration_seconds": None,
        },
        "manifest_content_hash": "",
    }
    manifest["manifest_content_hash"] = _manifest_hash(manifest)
    atomic_write_json(run_directory / "manifest.json", manifest)
    return manifest


def load_manifest(run_directory: Path) -> dict[str, Any]:
    value = json.loads((run_directory / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Run manifest must be an object")
    return value


def update_manifest(run_directory: Path, mutator: Any) -> dict[str, Any]:
    if (run_directory / "FINALIZED.json").exists():
        raise RuntimeError(f"Run is finalized: {run_directory.name}")
    manifest = load_manifest(run_directory)
    mutator(manifest)
    manifest["updated_at"] = utc_now()
    manifest["manifest_content_hash"] = _manifest_hash(manifest)
    atomic_write_json(run_directory / "manifest.json", manifest)
    return manifest


def register_artifact(
    run_directory: Path,
    *,
    name: str,
    path: Path,
    media_type: str,
) -> dict[str, Any]:
    run_directory = run_directory.resolve()
    resolved = path.resolve()
    reference = {
        "path": str(resolved.relative_to(run_directory)).replace("\\", "/")
        if resolved.is_relative_to(run_directory)
        else str(resolved),
        "sha256": sha256_file(resolved),
        "bytes": resolved.stat().st_size,
        "media_type": media_type,
    }
    update_manifest(
        run_directory,
        lambda manifest: manifest["artifacts"].__setitem__(name, reference),
    )
    return reference


def finalize_manifest(run_directory: Path, *, status: str) -> dict[str, Any]:
    if status not in {"completed", "failed", "partial"}:
        raise ValueError("Final status must be completed, failed, or partial")
    manifest = load_manifest(run_directory)
    if (run_directory / "FINALIZED.json").exists():
        return manifest
    finished_at = utc_now()
    started_at = datetime.fromisoformat(manifest["created_at"])
    finished = datetime.fromisoformat(finished_at)
    manifest["status"] = status
    manifest["updated_at"] = finished_at
    manifest["runtime"]["finished_at"] = finished_at
    manifest["runtime"]["duration_seconds"] = max(
        0.0,
        (finished - started_at).total_seconds(),
    )
    manifest["manifest_content_hash"] = _manifest_hash(manifest)
    atomic_write_json(run_directory / "manifest.json", manifest)
    atomic_write_json(
        run_directory / "FINALIZED.json",
        {
            "schema_version": "literature_run_finalization.v1",
            "run_id": manifest["run_id"],
            "status": status,
            "finalized_at": finished_at,
            "manifest_content_hash": manifest["manifest_content_hash"],
        },
        overwrite=False,
    )
    return manifest


def verify_manifest(run_directory: Path) -> dict[str, Any]:
    failures: list[str] = []
    try:
        manifest = load_manifest(run_directory)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return {"valid": False, "failures": [str(error)]}
    if manifest.get("schema_version") != RUN_SCHEMA_VERSION:
        failures.append("Unsupported run schema")
    if manifest.get("run_id") != run_directory.name:
        failures.append("run_id does not match directory")
    if _manifest_hash(manifest) != manifest.get("manifest_content_hash"):
        failures.append("Manifest content hash mismatch")
    for name, artifact in (manifest.get("artifacts") or {}).items():
        path = Path(str(artifact.get("path", "")))
        if not path.is_absolute():
            path = run_directory / path
        if not path.is_file():
            failures.append(f"Missing artifact: {name}")
        elif sha256_file(path) != artifact.get("sha256"):
            failures.append(f"Artifact hash mismatch: {name}")
    finalized = run_directory / "FINALIZED.json"
    if manifest.get("status") in {"completed", "failed"} and not finalized.is_file():
        failures.append("Finalized run is missing FINALIZED.json")
    return {
        "run_id": manifest.get("run_id"),
        "status": manifest.get("status"),
        "valid": not failures,
        "failures": failures,
        "finalized": finalized.is_file(),
        "manifest_content_hash": manifest.get("manifest_content_hash"),
    }
