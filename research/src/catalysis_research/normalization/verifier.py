from __future__ import annotations

import hashlib
import gzip
import json
from pathlib import Path
from typing import Any

from ..kg.freeze_stage1 import verify_snapshot
from .schema import canonical_hash, overlay_hash_identity


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_normalization_overlay(overlay_directory: Path, snapshot_directory: Path | None = None, corpus_directory: Path | None = None) -> dict[str, Any]:
    overlay = overlay_directory.resolve()
    manifest = json.loads((overlay / "manifest.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    for name, artifact in manifest.get("artifacts", {}).items():
        path = overlay / artifact["path"]
        if not path.is_file():
            failures.append(f"Missing artifact: {name}")
        elif _sha256(path) != artifact["sha256"]:
            failures.append(f"Artifact hash mismatch: {name}")
        elif "count" in artifact:
            try:
                with gzip.open(path, "rt", encoding="utf-8") as source:
                    count = sum(bool(line.strip()) for line in source)
                if count != artifact["count"]:
                    failures.append(f"Artifact record count mismatch: {name}")
            except (gzip.BadGzipFile, OSError, UnicodeDecodeError):
                failures.append(f"Invalid gzip JSONL artifact: {name}")
    if canonical_hash(overlay_hash_identity(manifest)) != manifest.get("overlay_content_hash"):
        failures.append("Overlay content hash mismatch")
    if snapshot_directory is not None:
        source_manifest = snapshot_directory.resolve() / "manifest.json"
        if not source_manifest.is_file() or _sha256(source_manifest) != manifest["source_kg"]["manifest_sha256"]:
            failures.append("Source KG manifest hash mismatch")
        else:
            report = verify_snapshot(snapshot_directory)
            if not report["valid"]:
                failures.append("Source KG snapshot verification failed")
    if corpus_directory is not None:
        corpus = corpus_directory.resolve()
        source_manifest = corpus / "manifest.json"
        if not source_manifest.is_file() or _sha256(source_manifest) != manifest["source_corpus"]["manifest_sha256"]:
            failures.append("Source corpus manifest hash mismatch")
        else:
            corpus_manifest = json.loads(source_manifest.read_text(encoding="utf-8"))
            for name, artifact in corpus_manifest.get("artifacts", {}).items():
                path = corpus / name
                if not path.is_file() or _sha256(path) != artifact.get("sha256"):
                    failures.append(f"Source corpus artifact verification failed: {name}")
    return {"valid": not failures, "failures": failures, "overlay_id": manifest.get("overlay_id"), "overlay_content_hash": manifest.get("overlay_content_hash")}
