from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


TARGET_COLUMN = "STY_g_per_gcath"
LEAKY_OUTCOME_COLUMNS = (
    "CO2_conversion",
    "selectivity_CH3OH",
    "yield_CH3OH",
)
ALLOWED_INPUT_COLUMNS = (
    "active_comp_1",
    "active_1_percent",
    "support_comp_1",
    "temperature_k",
    "pressure_bar",
    "pH2_pCO2_ratio",
    "GHSV_nlph_gcat",
    "catalyst_load_g",
)
OOD_FOLDS = (
    {
        "fold_id": "active-cu",
        "validation_groups": ("indium_oxide",),
        "test_groups": ("copper",),
    },
    {
        "fold_id": "active-in2o3",
        "validation_groups": ("palladium",),
        "test_groups": ("indium_oxide",),
    },
    {
        "fold_id": "active-pd",
        "validation_groups": ("copper",),
        "test_groups": ("palladium",),
    },
)


class TheMeCatError(RuntimeError):
    """Raised when the fixed TheMeCat v1 adapter contract is violated."""


def _clean(value: Any) -> str:
    text = "" if value is None else str(value).strip()
    return "" if text.upper() == "NA" else text


def _finite_float(value: Any) -> float | None:
    text = _clean(value)
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def catalyst_family(active_component: Any) -> str:
    value = _clean(active_component).lower().replace(" ", "")
    exact = {
        "cu": "copper",
        "in2o3": "indium_oxide",
        "pd": "palladium",
        "zn": "zinc",
        "inni3o0.5": "indium_nickel_oxide",
        "ir": "iridium",
        "au": "gold",
        "cdo": "cadmium_oxide",
        "pt": "platinum",
        "cogaalo4": "cobalt_gallium_aluminate",
    }
    if not value:
        return "unknown"
    if value in exact:
        return exact[value]
    if value.startswith("lamn"):
        return "lanthanum_manganite"
    return "other"


def _canonical_doi(row: dict[str, str]) -> str:
    value = _clean(row.get("doi_link")).lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    return value.rstrip("/.") or "unknown-source"


def _duplicate_record_id(row: dict[str, str]) -> str:
    fields = (
        _canonical_doi(row),
        _clean(row.get("catalyst_name")).lower(),
        _clean(row.get("active_comp_1")).lower(),
        _clean(row.get("active_comp_2")).lower(),
        _clean(row.get("support_comp_1")).lower(),
        _clean(row.get("support_comp_2")).lower(),
        _clean(row.get("temperature_k")),
        _clean(row.get("pressure_bar")),
        _clean(row.get("pH2_pCO2_ratio")),
        _clean(row.get("GHSV_nlph_gcat")),
        _clean(row.get("catalyst_load_g")),
    )
    payload = json.dumps(fields, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def adapt_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    adapted: list[dict[str, str]] = []
    for physical_index, source in enumerate(rows, start=2):
        if not _clean(source.get("reference")):
            continue
        if _finite_float(source.get(TARGET_COLUMN)) is None:
            continue
        row = {key: _clean(value) for key, value in source.items() if key}
        row["sample_id"] = f"themecat-v1-row-{physical_index:04d}"
        row["source_group"] = _canonical_doi(source)
        row["catalyst_family"] = catalyst_family(source.get("active_comp_1"))
        row["duplicate_record_id"] = _duplicate_record_id(source)
        adapted.append(row)
    if not adapted:
        raise TheMeCatError("No populated rows with a numeric STY target were found")
    identifiers = [row["sample_id"] for row in adapted]
    if len(identifiers) != len(set(identifiers)):
        raise TheMeCatError("The adapted sample IDs are not unique")
    return adapted


def load_themecat(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        return adapt_rows(csv.DictReader(source))


def audit_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    families = Counter(row["catalyst_family"] for row in rows)
    missingness = {
        column: sum(not _clean(row.get(column)) for row in rows) / len(rows)
        for column in ALLOWED_INPUT_COLUMNS
    }
    duplicate_families: dict[str, set[str]] = {}
    duplicate_counts: Counter[str] = Counter()
    for row in rows:
        duplicate_id = row["duplicate_record_id"]
        duplicate_counts[duplicate_id] += 1
        duplicate_families.setdefault(duplicate_id, set()).add(
            row["catalyst_family"]
        )
    crossing = sorted(
        key for key, values in duplicate_families.items() if len(values) > 1
    )
    if crossing:
        raise TheMeCatError(
            f"{len(crossing)} duplicate identities cross catalyst families"
        )
    known_families = set(families)
    for fold in OOD_FOLDS:
        configured = set(fold["validation_groups"]) | set(fold["test_groups"])
        missing = sorted(configured - known_families)
        if missing:
            raise TheMeCatError(
                f"OOD fold {fold['fold_id']} has unknown groups: {', '.join(missing)}"
            )
    return {
        "adapted_row_count": len(rows),
        "allowed_input_missing_fractions": missingness,
        "catalyst_family_counts": dict(sorted(families.items())),
        "duplicate_group_count": sum(count > 1 for count in duplicate_counts.values()),
        "duplicate_row_count": sum(
            count for count in duplicate_counts.values() if count > 1
        ),
        "duplicate_groups_cross_families": 0,
        "leaky_outcomes_excluded": list(LEAKY_OUTCOME_COLUMNS),
    }


def write_adapted_csv(source_path: Path, output_path: Path) -> dict[str, Any]:
    rows = load_themecat(source_path)
    fieldnames = [
        "sample_id",
        "source_group",
        "catalyst_family",
        "duplicate_record_id",
        *[key for key in rows[0] if key not in {
            "sample_id", "source_group", "catalyst_family", "duplicate_record_id"
        }],
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(output_path)
    return audit_rows(rows)
