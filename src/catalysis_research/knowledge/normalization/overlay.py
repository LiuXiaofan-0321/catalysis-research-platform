from __future__ import annotations

import gzip
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from .schema import canonical_json
from .verifier import verify_normalization_overlay


_IGNORED_CANONICAL_FIELDS = {
    "cation_form",
    "identity_level",
    "loading",
    "metal",
    "parent_framework",
    "si_al_ratio",
    "treatments",
}


def _jsonl_gzip(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as source:
        for line in source:
            if line.strip():
                yield json.loads(line)


def _searchable_values(value: Any, *, field: str | None = None) -> list[str]:
    if field in _IGNORED_CANONICAL_FIELDS:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    if isinstance(value, dict):
        return [
            item
            for key, nested in value.items()
            for item in _searchable_values(nested, field=str(key))
        ]
    if isinstance(value, list):
        return [
            item
            for nested in value
            for item in _searchable_values(nested, field=field)
        ]
    return []


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def _contains(query: str, term: str) -> bool:
    query_normalized = _normalized(query)
    term_normalized = _normalized(term).strip()
    if not term_normalized:
        return False
    if re.search(r"[\u3400-\u9fff]", term_normalized):
        return term_normalized in query_normalized
    pattern = rf"(?<![a-z0-9]){re.escape(term_normalized)}(?![a-z0-9])"
    return re.search(pattern, query_normalized) is not None


class ScientificNormalizationOverlay:
    """Read-only high-confidence query and node mappings from a frozen overlay."""

    def __init__(self, overlay_directory: Path, *, minimum_confidence: float = 0.9):
        self.overlay_directory = overlay_directory.resolve()
        report = verify_normalization_overlay(self.overlay_directory)
        if not report["valid"]:
            raise ValueError(
                "Invalid scientific normalization overlay: "
                + "; ".join(report["failures"])
            )
        self.manifest = json.loads(
            (self.overlay_directory / "manifest.json").read_text(encoding="utf-8")
        )
        concept_artifact = self.manifest["artifacts"]["concept_mappings"]
        accepted_concepts = [
            row
            for row in _jsonl_gzip(
                self.overlay_directory / concept_artifact["path"]
            )
            if float(row.get("confidence", 0.0)) >= minimum_confidence
            and row.get("review_status") == "normalized"
        ]
        accepted_by_artifact = {"concept_mappings": accepted_concepts}
        for artifact_name in ("value_mappings", "metadata_repairs"):
            artifact = self.manifest["artifacts"][artifact_name]
            accepted_by_artifact[artifact_name] = [
                row
                for row in _jsonl_gzip(self.overlay_directory / artifact["path"])
                if float(row.get("confidence", 0.0)) >= minimum_confidence
                and row.get("review_status") == "normalized"
            ]
        grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
        self._by_node_id: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for artifact_name, rows in accepted_by_artifact.items():
            for row in rows:
                if row.get("source_node_id"):
                    node_id = str(row["source_node_id"])
                    self._by_node_id[node_id].append(
                        {**row, "mapping_artifact": artifact_name}
                    )
        for row in accepted_concepts:
            key = (
                str(row["category"]),
                canonical_json(row.get("raw_value")),
                canonical_json(row.get("canonical_value")),
            )
            summary = grouped.setdefault(
                key,
                {
                    "category": row["category"],
                    "raw_value": row.get("raw_value"),
                    "canonical_value": row.get("canonical_value"),
                    "mapping_ids": [],
                    "source_node_ids": [],
                },
            )
            summary["mapping_ids"].append(str(row["mapping_id"]))
            if row.get("source_node_id"):
                node_id = str(row["source_node_id"])
                summary["source_node_ids"].append(node_id)
        self.mapping_groups = []
        for summary in grouped.values():
            summary["mapping_ids"] = sorted(set(summary["mapping_ids"]))
            summary["source_node_ids"] = sorted(set(summary["source_node_ids"]))
            summary["search_terms"] = sorted(
                set(
                    _searchable_values(summary["raw_value"])
                    + _searchable_values(summary["canonical_value"])
                ),
                key=lambda value: (-len(value), value.casefold()),
            )
            self.mapping_groups.append(summary)
        self.mapping_groups.sort(
            key=lambda row: (
                str(row["category"]),
                canonical_json(row["raw_value"]),
                canonical_json(row["canonical_value"]),
            )
        )

    @property
    def identity(self) -> dict[str, Any]:
        return {
            "overlay_id": self.manifest["overlay_id"],
            "overlay_content_hash": self.manifest["overlay_content_hash"],
            "rule_version": self.manifest["rule_version"],
        }

    def expand_query(
        self,
        query: str,
        *,
        maximum_mapping_groups: int = 8,
        maximum_added_terms: int = 12,
    ) -> dict[str, Any]:
        matched: list[dict[str, Any]] = []
        additions: list[str] = []
        seen_terms = {_normalized(query)}
        for group in self.mapping_groups:
            if len(matched) >= maximum_mapping_groups:
                break
            if not any(_contains(query, term) for term in group["search_terms"]):
                continue
            matched.append(
                {
                    key: group[key]
                    for key in (
                        "category",
                        "raw_value",
                        "canonical_value",
                        "mapping_ids",
                        "source_node_ids",
                    )
                }
            )
            for term in group["search_terms"]:
                normalized = _normalized(term)
                if normalized in seen_terms or _contains(query, term):
                    continue
                additions.append(term)
                seen_terms.add(normalized)
                if len(additions) >= maximum_added_terms:
                    break
            if len(additions) >= maximum_added_terms:
                break
        expanded = " ".join([query.strip(), *additions]).strip()
        return {
            **self.identity,
            "original_query": query,
            "expanded_query": expanded,
            "added_terms": additions,
            "matched_mappings": matched,
        }

    def mappings_for_nodes(
        self,
        node_ids: Iterable[str],
        *,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        mappings: dict[str, dict[str, Any]] = {}
        for node_id in node_ids:
            for row in self._by_node_id.get(str(node_id), []):
                mappings[str(row["mapping_id"])] = {
                    "mapping_id": str(row["mapping_id"]),
                    "category": row["category"],
                    "field": row["field"],
                    "raw_value": row.get("raw_value"),
                    "canonical_value": row.get("canonical_value"),
                    "rule_id": row["rule_id"],
                    "confidence": float(row["confidence"]),
                    "mapping_artifact": row["mapping_artifact"],
                }
        return [mappings[key] for key in sorted(mappings)[:limit]]
