from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from fractions import Fraction
from typing import Any

from .freeze_stage1 import canonical_hash, canonical_json, compact_text


SELECTION_SCHEMA_VERSION = "nested_kg_selection.v1"
SELECTION_ALGORITHM_VERSION = "proportional_stratified_hash_order.v1"


class SelectionError(RuntimeError):
    """Raised when a nested knowledge selection violates frozen rules."""


def _year_bin(year: Any, bins: list[dict[str, Any]]) -> str:
    if year in (None, ""):
        matches = [item for item in bins if item.get("unknown")]
    else:
        try:
            numeric_year = int(year)
        except (TypeError, ValueError) as error:
            raise SelectionError(f"Invalid paper year: {year!r}") from error
        matches = [
            item
            for item in bins
            if not item.get("unknown")
            and (
                item.get("minimum") is None
                or numeric_year >= int(item["minimum"])
            )
            and (
                item.get("maximum") is None
                or numeric_year <= int(item["maximum"])
            )
        ]
    if len(matches) != 1:
        raise SelectionError(
            f"Paper year {year!r} must match exactly one year bin"
        )
    return str(matches[0]["id"])


def _paper_type_group(
    paper_type: Any,
    groups: dict[str, list[str]],
    fallback: str,
) -> str:
    normalized = compact_text(paper_type, 80).lower() or "unknown"
    matches = [
        group
        for group, values in groups.items()
        if normalized in {str(value).lower() for value in values}
    ]
    if len(matches) > 1:
        raise SelectionError(
            f"Paper type {normalized!r} belongs to multiple groups"
        )
    return matches[0] if matches else fallback


def _selection_digest(seed: int, paper: dict[str, Any]) -> str:
    identity = {
        "seed": seed,
        "paper_id": paper["paper_id"],
        "archive_entry": paper["archive_entry"],
        "raw_pdf_sha256": paper["raw_pdf_sha256"],
        "structured_json_sha256": paper["structured_json_sha256"],
    }
    return hashlib.sha256(
        canonical_json(identity).encode("utf-8")
    ).hexdigest()


def validate_selection_config(
    config: dict[str, Any],
    paper_count: int,
) -> None:
    required = {
        "selection_id",
        "selection_schema_version",
        "algorithm_version",
        "seed",
        "year_bins",
        "paper_type_groups",
        "paper_type_fallback",
        "topic_source_rule",
        "levels",
        "downstream_label_access",
    }
    missing = sorted(required - set(config))
    if missing:
        raise SelectionError(
            "Selection config is missing fields: " + ", ".join(missing)
        )
    forbidden = {
        "dataset",
        "labels",
        "target",
        "metrics",
        "descriptor_performance",
        "model_performance",
    }
    present_forbidden = sorted(forbidden & set(config))
    if present_forbidden:
        raise SelectionError(
            "Selection config references forbidden outcome fields: "
            + ", ".join(present_forbidden)
        )
    if config["selection_schema_version"] != SELECTION_SCHEMA_VERSION:
        raise SelectionError("Unsupported selection schema version")
    if config["algorithm_version"] != SELECTION_ALGORITHM_VERSION:
        raise SelectionError("Unsupported selection algorithm version")
    if config["downstream_label_access"] != "forbidden":
        raise SelectionError("Downstream label access must be forbidden")
    if config["topic_source_rule"] != (
        "first directory after Reaction in source_path"
    ):
        raise SelectionError("Unsupported source-topic rule")
    if not isinstance(config["seed"], int):
        raise SelectionError("Selection seed must be an integer")
    bins = config["year_bins"]
    if not isinstance(bins, list) or not bins:
        raise SelectionError("At least one year bin is required")
    bin_ids = [str(item.get("id", "")) for item in bins]
    if any(not value for value in bin_ids) or len(bin_ids) != len(set(bin_ids)):
        raise SelectionError("Year bin IDs must be non-empty and unique")
    if sum(bool(item.get("unknown")) for item in bins) != 1:
        raise SelectionError("Exactly one unknown year bin is required")
    levels = config["levels"]
    if not isinstance(levels, list) or not levels:
        raise SelectionError("Knowledge levels must be a non-empty list")
    counts = [int(level["paper_count"]) for level in levels]
    if counts != sorted(set(counts)):
        raise SelectionError("Knowledge level counts must strictly increase")
    if counts[-1] != paper_count:
        raise SelectionError("Final knowledge level must include every paper")
    for level in levels:
        count = int(level["paper_count"])
        fraction = float(level["paper_fraction"])
        if count <= 0 or count > paper_count:
            raise SelectionError("Knowledge level count is out of range")
        if not 0 < fraction <= 1:
            raise SelectionError("Knowledge level fraction is out of range")
        expected_count = math.floor(fraction * paper_count + 0.5)
        if count != expected_count:
            raise SelectionError(
                f"{level['knowledge_level']} count does not match its "
                "registered corpus fraction"
            )


def build_nested_order(
    papers: list[dict[str, Any]],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    validate_selection_config(config, len(papers))
    paper_ids = [str(paper.get("paper_id", "")) for paper in papers]
    archive_entries = [
        str(paper.get("archive_entry", "")) for paper in papers
    ]
    if any(not value for value in paper_ids + archive_entries):
        raise SelectionError(
            "Every paper needs a paper ID and archive entry"
        )
    if len(paper_ids) != len(set(paper_ids)):
        raise SelectionError("Paper IDs must be unique")
    if len(archive_entries) != len(set(archive_entries)):
        raise SelectionError("Archive entries must be unique")

    groups = config["paper_type_groups"]
    fallback = str(config["paper_type_fallback"])
    if fallback not in groups:
        raise SelectionError(
            "Paper type fallback must name a configured group"
        )
    strata: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(
        list
    )
    for paper in papers:
        stratum = (
            compact_text(paper.get("source_topic"), 200) or "unknown",
            _year_bin(paper.get("year"), config["year_bins"]),
            _paper_type_group(
                paper.get("paper_type"),
                groups,
                fallback,
            ),
        )
        enriched = dict(paper)
        enriched["selection_hash"] = _selection_digest(
            int(config["seed"]),
            paper,
        )
        enriched["selection_stratum"] = {
            "source_topic": stratum[0],
            "year_bin": stratum[1],
            "paper_type_group": stratum[2],
        }
        strata[stratum].append(enriched)

    candidates: list[
        tuple[Fraction, tuple[str, str, str], str, str, dict[str, Any]]
    ] = []
    for stratum, members in strata.items():
        members.sort(
            key=lambda paper: (
                paper["selection_hash"],
                paper["paper_id"],
                paper["archive_entry"],
            )
        )
        size = len(members)
        for rank, paper in enumerate(members):
            candidates.append(
                (
                    Fraction(2 * rank + 1, 2 * size),
                    stratum,
                    paper["selection_hash"],
                    paper["paper_id"],
                    paper,
                )
            )
    candidates.sort(key=lambda item: item[:4])

    ordered: list[dict[str, Any]] = []
    for index, (_, _, _, _, paper) in enumerate(candidates, start=1):
        ordered.append(
            {
                "selection_rank": index,
                "paper_id": paper["paper_id"],
                "archive_entry": paper["archive_entry"],
                "raw_pdf_sha256": paper["raw_pdf_sha256"],
                "structured_json_sha256": paper[
                    "structured_json_sha256"
                ],
                "selection_hash": paper["selection_hash"],
                "selection_stratum": paper["selection_stratum"],
            }
        )
    return ordered


def selection_order_hash(order: list[dict[str, Any]]) -> str:
    return canonical_hash(
        [
            {
                "selection_rank": item["selection_rank"],
                "paper_id": item["paper_id"],
                "archive_entry": item["archive_entry"],
                "selection_hash": item["selection_hash"],
                "selection_stratum": item["selection_stratum"],
            }
            for item in order
        ]
    )


def prefix_hash(
    order: list[dict[str, Any]],
    count: int,
    field: str,
) -> str:
    return canonical_hash([item[field] for item in order[:count]])
