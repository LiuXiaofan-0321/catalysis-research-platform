from __future__ import annotations

import re
import unicodedata
from typing import Any


SPACE_RE = re.compile(r"\s+")
FRAMEWORK_RE = re.compile(r"^[A-Z]{3}(?:-[A-Z])?$")


def compact(value: Any) -> str:
    return SPACE_RE.sub(" ", str(value or "").strip())


def alias_key(value: Any) -> str:
    text = unicodedata.normalize("NFKC", compact(value)).casefold()
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text)


def alias_table(groups: dict[str, list[str]]) -> dict[str, str]:
    table: dict[str, str] = {}
    for canonical, aliases in groups.items():
        for value in [canonical, *aliases]:
            key = alias_key(value)
            previous = table.get(key)
            if previous is not None and previous != canonical:
                raise ValueError(f"Conflicting alias {value!r}: {previous!r} / {canonical!r}")
            table[key] = canonical
    return table


def normalize_alias(value: Any, groups: dict[str, list[str]]) -> str | None:
    return alias_table(groups).get(alias_key(value))


def normalize_framework(value: Any, aliases: dict[str, list[str]]) -> str | None:
    mapped = normalize_alias(value, aliases)
    if mapped:
        return mapped
    candidate = compact(value).upper()
    return candidate if FRAMEWORK_RE.fullmatch(candidate) else None


def normalize_sample(value: Any) -> dict[str, Any] | None:
    raw = compact(value)
    if not raw or alias_key(raw) in {"sample", "catalyst", "unknown", "样品", "催化剂"}:
        return None
    canonical = re.sub(r"\s*-\s*", "-", raw)
    canonical = SPACE_RE.sub(" ", canonical)
    framework = None
    match = re.search(r"\b(?:ZSM-5|MFI)\b", canonical, flags=re.IGNORECASE)
    if match:
        framework = "MFI"
    cation = None
    cation_match = re.search(r"\b(H|Na|K|NH4)-ZSM-5\b", canonical, flags=re.IGNORECASE)
    if cation_match:
        cation = {"H": "H", "NA": "Na", "K": "K", "NH4": "NH4"}[
            cation_match.group(1).upper()
        ]
    metal = None
    metal_match = re.search(
        r"(?:\b\d+(?:\.\d+)?\s*(?:wt|mol)\s*%\s*)?\b(Pt|Pd|Rh|Ru|Ni|Co|Fe|Cu|Zn|Ga|Sn|Mo|W|V)\b(?=[/@-])",
        canonical,
        flags=re.IGNORECASE,
    )
    if metal_match:
        metal = metal_match.group(1).title()
    loading = None
    loading_match = re.search(r"\b\d+(?:\.\d+)?\s*(?:wt|mol)\s*%", canonical, flags=re.IGNORECASE)
    if loading_match:
        loading = compact(loading_match.group(0)).replace("WT", "wt").replace("MOL", "mol")
    si_al = None
    si_al_match = re.search(r"Si\s*/\s*Al\s*[=:]\s*(\d+(?:\.\d+)?)", canonical, flags=re.IGNORECASE)
    if si_al_match:
        si_al = float(si_al_match.group(1))
    treatments = [
        treatment
        for treatment in ("calcined", "steamed", "dealuminated", "desilicated")
        if re.search(rf"\b{treatment}\b", canonical, flags=re.IGNORECASE)
    ]
    return {
        "sample_name": canonical,
        "parent_framework": framework,
        "cation_form": cation,
        "metal": metal,
        "loading": loading,
        "si_al_ratio": si_al,
        "treatments": treatments,
        "identity_level": "catalyst_sample",
    }


def normalize_paper_type(value: Any, groups: dict[str, list[str]]) -> str | None:
    return normalize_alias(value, groups)


def looks_like_si_title(value: Any, patterns: list[str]) -> bool:
    text = compact(value)
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)
