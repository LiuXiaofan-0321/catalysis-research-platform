from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from catalysis_research.datasets.themecat import (
    ALLOWED_INPUT_COLUMNS,
    OOD_FOLDS,
    TARGET_COLUMN,
    audit_rows,
    load_themecat,
)
from catalysis_research.models.deepseek import DeepSeekClient


EPSILON = 1e-12
ALPHA_GRID = (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)
HUMAN_HEURISTIC_IDS = (
    "temperature_k",
    "pressure_bar",
    "h2_co2_ratio",
    "ghsv",
    "catalyst_load",
    "active_percent",
    "h2_partial_pressure",
    "co2_partial_pressure",
    "inverse_ghsv",
    "active_mass_proxy",
)


@dataclass(frozen=True)
class Descriptor:
    descriptor_id: str
    formula: str
    units: str
    rationale: str
    compute: Callable[[dict[str, str]], float]

    def prompt_record(self) -> dict[str, str]:
        return {
            "descriptor_id": self.descriptor_id,
            "formula": self.formula,
            "units": self.units,
            "scientific_rationale": self.rationale,
        }


def _number(row: dict[str, str], column: str) -> float:
    try:
        value = float(row.get(column, ""))
    except (TypeError, ValueError):
        return float("nan")
    return value if math.isfinite(value) else float("nan")


def _safe_log10(value: float) -> float:
    return math.log10(max(value, EPSILON)) if math.isfinite(value) else value


def _safe_divide(numerator: float, denominator: float) -> float:
    if not math.isfinite(numerator) or not math.isfinite(denominator):
        return float("nan")
    return numerator / max(abs(denominator), EPSILON)


def descriptor_catalog() -> dict[str, Descriptor]:
    n = _number
    definitions = (
        Descriptor("temperature_k", "T", "K", "Absolute reaction temperature.", lambda r: n(r, "temperature_k")),
        Descriptor("inverse_temperature", "1/T", "K^-1", "Arrhenius-like temperature coordinate.", lambda r: _safe_divide(1.0, n(r, "temperature_k"))),
        Descriptor("temperature_squared", "T^2", "K^2", "Captures smooth temperature curvature.", lambda r: n(r, "temperature_k") ** 2),
        Descriptor("pressure_bar", "P", "bar", "Total reactor pressure.", lambda r: n(r, "pressure_bar")),
        Descriptor("log_pressure", "log10(P)", "unitless", "Compressed pressure scale.", lambda r: _safe_log10(n(r, "pressure_bar"))),
        Descriptor("h2_co2_ratio", "R=H2/CO2", "unitless", "Feed stoichiometry proxy.", lambda r: n(r, "pH2_pCO2_ratio")),
        Descriptor("log_h2_co2_ratio", "log10(R)", "unitless", "Compressed feed-ratio scale.", lambda r: _safe_log10(n(r, "pH2_pCO2_ratio"))),
        Descriptor("h2_partial_pressure", "P*R/(1+R)", "bar", "Approximate hydrogen partial pressure.", lambda r: n(r, "pressure_bar") * _safe_divide(n(r, "pH2_pCO2_ratio"), 1.0 + n(r, "pH2_pCO2_ratio"))),
        Descriptor("co2_partial_pressure", "P/(1+R)", "bar", "Approximate carbon-dioxide partial pressure.", lambda r: _safe_divide(n(r, "pressure_bar"), 1.0 + n(r, "pH2_pCO2_ratio"))),
        Descriptor("partial_pressure_product", "pH2*pCO2", "bar^2", "Bimolecular pressure interaction proxy.", lambda r: (n(r, "pressure_bar") * _safe_divide(n(r, "pH2_pCO2_ratio"), 1.0 + n(r, "pH2_pCO2_ratio"))) * _safe_divide(n(r, "pressure_bar"), 1.0 + n(r, "pH2_pCO2_ratio"))),
        Descriptor("ghsv", "GHSV", "NL h^-1 gcat^-1", "Gas hourly space velocity.", lambda r: n(r, "GHSV_nlph_gcat")),
        Descriptor("log_ghsv", "log10(GHSV)", "unitless", "Compressed flow scale.", lambda r: _safe_log10(n(r, "GHSV_nlph_gcat"))),
        Descriptor("inverse_ghsv", "1/GHSV", "gcat h NL^-1", "Residence-time proxy.", lambda r: _safe_divide(1.0, n(r, "GHSV_nlph_gcat"))),
        Descriptor("pressure_over_ghsv", "P/GHSV", "bar gcat h NL^-1", "Pressure-weighted residence proxy.", lambda r: _safe_divide(n(r, "pressure_bar"), n(r, "GHSV_nlph_gcat"))),
        Descriptor(
            "h2_pressure_over_ghsv",
            "pH2/GHSV",
            "bar gcat h NL^-1",
            "Hydrogen exposure proxy.",
            lambda r: _safe_divide(
                n(r, "pressure_bar")
                * _safe_divide(
                    n(r, "pH2_pCO2_ratio"),
                    1.0 + n(r, "pH2_pCO2_ratio"),
                ),
                n(r, "GHSV_nlph_gcat"),
            ),
        ),
        Descriptor(
            "co2_pressure_over_ghsv",
            "pCO2/GHSV",
            "bar gcat h NL^-1",
            "Carbon-dioxide exposure proxy.",
            lambda r: _safe_divide(
                _safe_divide(
                    n(r, "pressure_bar"),
                    1.0 + n(r, "pH2_pCO2_ratio"),
                ),
                n(r, "GHSV_nlph_gcat"),
            ),
        ),
        Descriptor("temperature_pressure", "T*P", "K bar", "Temperature-pressure interaction.", lambda r: n(r, "temperature_k") * n(r, "pressure_bar")),
        Descriptor("pressure_over_temperature", "P/T", "bar K^-1", "Pressure relative to thermal scale.", lambda r: _safe_divide(n(r, "pressure_bar"), n(r, "temperature_k"))),
        Descriptor("temperature_over_ghsv", "T/GHSV", "K gcat h NL^-1", "Thermal residence proxy.", lambda r: _safe_divide(n(r, "temperature_k"), n(r, "GHSV_nlph_gcat"))),
        Descriptor("catalyst_load", "m_cat", "g", "Catalyst mass in the reactor.", lambda r: n(r, "catalyst_load_g")),
        Descriptor("log_catalyst_load", "log10(m_cat)", "unitless", "Compressed catalyst-mass scale.", lambda r: _safe_log10(n(r, "catalyst_load_g"))),
        Descriptor("active_percent", "w_active", "%", "Reported primary active-component loading.", lambda r: n(r, "active_1_percent")),
        Descriptor("active_fraction", "w_active/100", "unitless", "Primary active-component mass fraction.", lambda r: n(r, "active_1_percent") / 100.0),
        Descriptor("active_mass_proxy", "m_cat*w_active/100", "g", "Approximate primary active-component mass.", lambda r: n(r, "catalyst_load_g") * n(r, "active_1_percent") / 100.0),
        Descriptor("ghsv_times_load", "GHSV*m_cat", "NL h^-1", "Approximate total normalized feed rate.", lambda r: n(r, "GHSV_nlph_gcat") * n(r, "catalyst_load_g")),
        Descriptor("feed_per_active_mass", "GHSV/(w_active/100)", "NL h^-1 gactive^-1", "Flow normalized by active fraction.", lambda r: _safe_divide(n(r, "GHSV_nlph_gcat"), n(r, "active_1_percent") / 100.0)),
        Descriptor("temperature_active_fraction", "T*w_active/100", "K", "Thermal-loading interaction.", lambda r: n(r, "temperature_k") * n(r, "active_1_percent") / 100.0),
        Descriptor("pressure_active_fraction", "P*w_active/100", "bar", "Pressure-loading interaction.", lambda r: n(r, "pressure_bar") * n(r, "active_1_percent") / 100.0),
        Descriptor("co2_exposure_active", "pCO2*w_active/(100*GHSV)", "bar gcat h NL^-1", "CO2 exposure normalized by primary active fraction.", lambda r: _safe_divide(_safe_divide(n(r, "pressure_bar"), 1.0 + n(r, "pH2_pCO2_ratio")) * n(r, "active_1_percent") / 100.0, n(r, "GHSV_nlph_gcat"))),
        Descriptor("h2_exposure_active", "pH2*w_active/(100*GHSV)", "bar gcat h NL^-1", "H2 exposure normalized by primary active fraction.", lambda r: _safe_divide(n(r, "pressure_bar") * _safe_divide(n(r, "pH2_pCO2_ratio"), 1.0 + n(r, "pH2_pCO2_ratio")) * n(r, "active_1_percent") / 100.0, n(r, "GHSV_nlph_gcat"))),
    )
    return {item.descriptor_id: item for item in definitions}


def build_prompt(catalog: dict[str, Descriptor]) -> tuple[str, str]:
    system = (
        "You are selecting physically interpretable descriptors for a catalysis "
        "regression benchmark. You never receive row-level target values. Return "
        "only one valid JSON object and do not invent formulas outside the catalog."
    )
    task = {
        "run_classification": "exploratory_pilot_not_confirmatory",
        "domain": "thermocatalytic CO2 hydrogenation to methanol",
        "target": {
            "name": "methanol space-time yield",
            "column": TARGET_COLUMN,
            "units": "g_CH3OH g_cat^-1 h^-1",
        },
        "allowed_inputs": list(ALLOWED_INPUT_COLUMNS),
        "forbidden_outcome_proxies": [
            "CO2_conversion", "selectivity_CH3OH", "yield_CH3OH"
        ],
        "candidate_budget": 30,
        "selected_budget": 10,
        "catalog": [item.prompt_record() for item in catalog.values()],
        "output_schema": {
            "hypothesis": "string",
            "candidates": [
                {
                    "rank": "integer 1..30",
                    "descriptor_id": "catalog ID",
                    "rationale": "string",
                }
            ],
            "selected_descriptor_ids": "exactly 10 unique catalog IDs in rank order",
        },
        "instructions": [
            "Rank all 30 catalog descriptors exactly once.",
            "Select exactly 10 descriptors without using any labels or outcomes.",
            "Favor complementary mechanisms and avoid algebraic redundancy.",
        ],
    }
    return system, json.dumps(task, ensure_ascii=False, sort_keys=True)


def validate_selection(value: dict[str, Any], catalog: dict[str, Descriptor]) -> list[str]:
    candidates = value.get("candidates")
    selected = value.get("selected_descriptor_ids")
    if not isinstance(value.get("hypothesis"), str) or not value["hypothesis"].strip():
        raise ValueError("Missing descriptor hypothesis")
    if not isinstance(candidates, list) or len(candidates) != 30:
        raise ValueError("DeepSeek must rank exactly 30 candidates")
    candidate_ids = [item.get("descriptor_id") for item in candidates if isinstance(item, dict)]
    if len(candidate_ids) != 30 or set(candidate_ids) != set(catalog):
        raise ValueError("Candidate ranking must contain each catalog ID exactly once")
    ranks = [item.get("rank") for item in candidates]
    if sorted(ranks) != list(range(1, 31)):
        raise ValueError("Candidate ranks must be the integers 1 through 30")
    if not isinstance(selected, list) or len(selected) != 10:
        raise ValueError("DeepSeek must select exactly 10 descriptors")
    if len(set(selected)) != 10 or any(item not in catalog for item in selected):
        raise ValueError("Selected descriptor IDs must be unique catalog members")
    ranked_ids = [item for _, item in sorted(zip(ranks, candidate_ids))]
    if selected != ranked_ids[:10]:
        raise ValueError("Selected descriptors must equal the first 10 ranked candidates")
    return selected


def _matrix(rows: list[dict[str, str]], descriptor_ids: tuple[str, ...] | list[str], catalog: dict[str, Descriptor]) -> np.ndarray:
    return np.asarray(
        [[catalog[item].compute(row) for item in descriptor_ids] for row in rows],
        dtype=float,
    )


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "rmse": float(mean_squared_error(y_true, y_pred) ** 0.5),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def evaluate_descriptor_set(rows: list[dict[str, str]], descriptor_ids: tuple[str, ...] | list[str], catalog: dict[str, Descriptor]) -> dict[str, Any]:
    fold_results = []
    for fold in OOD_FOLDS:
        validation_groups = set(fold["validation_groups"])
        test_groups = set(fold["test_groups"])
        train = [row for row in rows if row["catalyst_family"] not in validation_groups | test_groups]
        validation = [row for row in rows if row["catalyst_family"] in validation_groups]
        test = [row for row in rows if row["catalyst_family"] in test_groups]
        x_train = _matrix(train, descriptor_ids, catalog)
        x_validation = _matrix(validation, descriptor_ids, catalog)
        x_test = _matrix(test, descriptor_ids, catalog)
        y_train = np.asarray([float(row[TARGET_COLUMN]) for row in train])
        y_validation = np.asarray([float(row[TARGET_COLUMN]) for row in validation])
        y_test = np.asarray([float(row[TARGET_COLUMN]) for row in test])
        candidates = []
        for alpha in ALPHA_GRID:
            pipeline = Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
                    ("scaler", StandardScaler()),
                    ("ridge", Ridge(alpha=alpha)),
                ]
            )
            pipeline.fit(x_train, y_train)
            prediction = pipeline.predict(x_validation)
            candidates.append((float(mean_squared_error(y_validation, prediction) ** 0.5), alpha, pipeline))
        validation_rmse, alpha, pipeline = min(candidates, key=lambda item: (item[0], item[1]))
        predictions = pipeline.predict(x_test)
        fold_results.append(
            {
                "fold_id": fold["fold_id"],
                "train_rows": len(train),
                "validation_rows": len(validation),
                "test_rows": len(test),
                "selected_alpha": alpha,
                "validation_rmse": validation_rmse,
                "test": _metrics(y_test, predictions),
            }
        )
    return {
        "folds": fold_results,
        "macro_test_rmse": float(np.mean([fold["test"]["rmse"] for fold in fold_results])),
        "macro_test_mae": float(np.mean([fold["test"]["mae"] for fold in fold_results])),
        "macro_test_r2": float(np.mean([fold["test"]["r2"] for fold in fold_results])),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_pilot(*, raw_path: Path, output_path: Path, model: str = "deepseek-v4-flash") -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    rows = load_themecat(raw_path)
    audit = audit_rows(rows)
    catalog = descriptor_catalog()
    system, user = build_prompt(catalog)
    prompt_hash = hashlib.sha256(f"{system}\n{user}".encode("utf-8")).hexdigest()
    client = DeepSeekClient()
    available_models = client.list_models()
    if model not in available_models:
        raise RuntimeError(
            f"Requested model {model!r} is unavailable; provider returned {available_models}"
        )
    response = client.chat_json(
        model=model,
        system=system,
        user=user,
        temperature=0.2,
        max_tokens=8000,
    )
    selected = validate_selection(response["structured"], catalog)
    baseline = evaluate_descriptor_set(rows, HUMAN_HEURISTIC_IDS, catalog)
    generated = evaluate_descriptor_set(rows, selected, catalog)
    baseline_rmse = baseline["macro_test_rmse"]
    q_exploratory = (baseline_rmse - generated["macro_test_rmse"]) / baseline_rmse
    finished = datetime.now(timezone.utc)
    result = {
        "schema_version": "themecat_deepseek_exploratory_pilot.v1",
        "run_classification": "EXPLORATORY_NOT_CONFIRMATORY",
        "protocol_status": "ACTIVATION_BLOCKED",
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "duration_seconds": (finished - started).total_seconds(),
        "warnings": [
            "The dataset, human descriptors, model registry, prompt and Ridge grid are not frozen.",
            "This model post-dates TheMeCat publication; benchmark contamination is not ruled out.",
            "The source paper reports 822 entries, while the downloaded CSV contains 821 populated records and 712 numeric STY records.",
            "The baseline is a fixed heuristic sanity baseline, not the protocol's expert-frozen human baseline.",
        ],
        "dataset": {
            "name": "TheMeCat v1",
            "raw_sha256": sha256_file(raw_path),
            "target": TARGET_COLUMN,
            "audit": audit,
        },
        "split": {
            "strategy": "material-family OOD",
            "folds": list(OOD_FOLDS),
        },
        "model": {
            "provider": "DeepSeek",
            "requested_model": model,
            "provider_model": response["provider_model"],
            "provider_response_id": response["provider_response_id"],
            "available_models_at_run": available_models,
            "mode": "non-thinking",
            "temperature": 0.2,
            "usage": response["usage"],
        },
        "prompt": {
            "version": "themecat-descriptor-catalog-v1",
            "sha256": prompt_hash,
            "row_level_data_included": False,
            "row_level_labels_included": False,
        },
        "generation": {
            "hypothesis": response["structured"]["hypothesis"],
            "candidates": response["structured"]["candidates"],
            "selected_descriptor_ids": selected,
            "raw_model_output": response["raw_content"],
        },
        "downstream": {
            "model": "sklearn.linear_model.Ridge",
            "alpha_grid": list(ALPHA_GRID),
            "preprocessing": "train-only median imputation with missing indicators, then standard scaling",
            "baseline_descriptor_ids": list(HUMAN_HEURISTIC_IDS),
            "baseline": baseline,
            "deepseek_descriptors": generated,
            "exploratory_normalized_rmse_improvement": q_exploratory,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(output_path)
    return result
