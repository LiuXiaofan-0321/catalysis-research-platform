from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA_VERSION = "scientific_normalization_overlay.v1.1"


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def mapping_id(*parts: Any) -> str:
    return "norm:" + canonical_hash(list(parts))[:32]


def overlay_hash_identity(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": manifest["schema_version"],
        "overlay_id": manifest["overlay_id"],
        "rule_version": manifest["rule_version"],
        "source_kg": manifest["source_kg"],
        "source_corpus": manifest["source_corpus"],
        "artifacts": manifest["artifacts"],
        "record_counts": manifest["record_counts"],
    }
