"""AdsZeo evidence-to-descriptor benchmark."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from catalysis_research.datasets.adszeo import AdsZeoDataset, TARGET_COLUMN, load_adszeo
from catalysis_research.experiments.discovery_loop import (
    DEFAULT_MODEL,
    DISCOVERY_SCHEMA_VERSION,
    _canonical_hash,
    _label_evidence_context,
    build_discovery_prompt,
    validate_discovery_output,
)
from catalysis_research.experiments.themecat_pilot import Descriptor
from catalysis_research.models.glm import GlmClient, GlmResponse
from catalysis_research.retrieval import EXPERIMENT_KNOWLEDGE_MODES, KnowledgeModeRetriever, RetrievalBudget


RUN_SCHEMA_VERSION = "glm_scientific_discovery_adszeo.v1"
MODEL_CANDIDATES = (
    {"learning_rate": 0.05, "max_leaf_nodes": 15, "l2_regularization": 0.1},
    {"learning_rate": 0.05, "max_leaf_nodes": 31, "l2_regularization": 1.0},
    {"learning_rate": 0.10, "max_leaf_nodes": 15, "l2_regularization": 1.0},
    {"learning_rate": 0.10, "max_leaf_nodes": 31, "l2_regularization": 10.0},
)
D0_DESCRIPTOR_IDS = (
    "log_pressure",
    "framework_density",
    "al_fraction",
    "helium_void_fraction",
    "cell_volume_per_t",
    "cell_length_anisotropy",
)


def _number(row: dict[str, Any], key: str) -> float:
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")
    return value if math.isfinite(value) else float("nan")


def _safe_divide(numerator: float, denominator: float) -> float:
    if not math.isfinite(numerator) or not math.isfinite(denominator) or abs(denominator) < 1e-12:
        return float("nan")
    return numerator / denominator


def adszeo_descriptor_catalog() -> dict[str, Descriptor]:
    n = _number
    t_count = lambda r: n(r, "si_count") + n(r, "al_count_cif")
    al_fraction = lambda r: _safe_divide(n(r, "al_count_cif"), t_count(r))
    definitions = (
        Descriptor("log_pressure", "log10(P_bar)", "unitless", "Adsorption pressure coordinate.", lambda r: math.log10(max(n(r, "pressure_bar"), 1e-12))),
        Descriptor("framework_density", "1000*N_T/V_cell", "T/1000 A^3", "Framework packing density.", lambda r: 1000.0 * _safe_divide(t_count(r), n(r, "cell_volume"))),
        Descriptor("al_fraction", "N_Al/N_T", "unitless", "Framework aluminium fraction.", al_fraction),
        Descriptor("helium_void_fraction", "phi_He", "unitless", "Independent helium-accessible void fraction.", lambda r: n(r, "helium_void_fraction")),
        Descriptor("cell_volume_per_t", "V_cell/N_T", "A^3/T", "Framework volume per tetrahedral atom.", lambda r: _safe_divide(n(r, "cell_volume"), t_count(r))),
        Descriptor("cell_length_anisotropy", "std(a,b,c)/mean(a,b,c)", "unitless", "Unit-cell shape anisotropy.", lambda r: float(np.std([n(r, "cell_a"), n(r, "cell_b"), n(r, "cell_c")]) / max(np.mean([n(r, "cell_a"), n(r, "cell_b"), n(r, "cell_c")]), 1e-12))),
        Descriptor("pressure_bar", "P", "bar", "Uncompressed pressure coordinate for nonlinear saturation.", lambda r: n(r, "pressure_bar")),
        Descriptor("al_count", "N_Al", "count", "Number of framework aluminium atoms in the simulation cell.", lambda r: n(r, "al_count_cif")),
        Descriptor("t_count", "N_Si+N_Al", "count", "Framework size in tetrahedral atoms.", t_count),
        Descriptor("al_number_density", "N_Al/V_cell", "A^-3", "Charge-site number density before adsorption.", lambda r: _safe_divide(n(r, "al_count_cif"), n(r, "cell_volume"))),
        Descriptor("al_per_void_volume", "N_Al/(V_cell*phi_He)", "A^-3", "Al/Na charge density normalized by accessible void volume.", lambda r: _safe_divide(n(r, "al_count_cif"), n(r, "cell_volume") * n(r, "helium_void_fraction"))),
        Descriptor("void_volume_per_t", "V_cell*phi_He/N_T", "A^3/T", "Accessible pore volume per tetrahedral atom.", lambda r: _safe_divide(n(r, "cell_volume") * n(r, "helium_void_fraction"), t_count(r))),
        Descriptor("cell_angle_deviation", "mean(|alpha,beta,gamma-90|)", "degree", "Deviation of the simulation cell from orthogonality.", lambda r: float(np.mean(np.abs(np.asarray([n(r, "cell_alpha"), n(r, "cell_beta"), n(r, "cell_gamma")]) - 90.0)))),
        Descriptor("al_nn_mean", "mean nearest periodic Al-Al distance", "A", "Typical separation between framework charge sites.", lambda r: n(r, "al_nn_mean_a")),
        Descriptor("al_nn_std", "std nearest periodic Al-Al distance", "A", "Heterogeneity of nearest charge-site separation.", lambda r: n(r, "al_nn_std_a")),
        Descriptor("al_nn_min", "min nearest periodic Al-Al distance", "A", "Closest framework charge-site pair.", lambda r: n(r, "al_nn_min_a")),
        Descriptor("al_pair_mean", "mean periodic Al-Al pair distance", "A", "Global dispersion of framework aluminium sites.", lambda r: n(r, "al_pair_mean_a")),
        Descriptor("al_pair_std", "std periodic Al-Al pair distance", "A", "Width of the Al-Al distance distribution.", lambda r: n(r, "al_pair_std_a")),
        Descriptor("al_pair_distance_cv", "std(d_AlAl)/mean(d_AlAl)", "unitless", "Scale-normalized Al-pair heterogeneity.", lambda r: _safe_divide(n(r, "al_pair_std_a"), n(r, "al_pair_mean_a"))),
        Descriptor("al_close_pair_fraction_5a", "fraction(d_AlAl<5 A)", "unitless", "Short-range Al-pair prevalence.", lambda r: n(r, "al_close_pair_fraction_5a")),
        Descriptor("al_close_pair_fraction_8a", "fraction(d_AlAl<8 A)", "unitless", "Medium-range Al-pair prevalence.", lambda r: n(r, "al_close_pair_fraction_8a")),
        Descriptor("al_clustering_index", "mean(NN_AlAl)/(V_cell/N_Al)^(1/3)", "unitless", "Al clustering normalized by charge-site density.", lambda r: n(r, "al_clustering_index")),
        Descriptor("pressure_al_fraction", "log10(P)*N_Al/N_T", "unitless", "Pressure-dependent aluminium-site contribution.", lambda r: math.log10(max(n(r, "pressure_bar"), 1e-12)) * al_fraction(r)),
        Descriptor("pressure_void_fraction", "log10(P)*phi_He", "unitless", "Pressure-dependent accessible-volume contribution.", lambda r: math.log10(max(n(r, "pressure_bar"), 1e-12)) * n(r, "helium_void_fraction")),
        Descriptor("pressure_al_clustering", "log10(P)*Al_clustering", "unitless", "Pressure-dependent sensitivity to Al spatial organization.", lambda r: math.log10(max(n(r, "pressure_bar"), 1e-12)) * n(r, "al_clustering_index")),
    )
    return {item.descriptor_id: item for item in definitions}


def _feature_matrix(rows: list[dict[str, Any]], ids: Iterable[str], catalog: dict[str, Descriptor]) -> np.ndarray:
    return np.asarray([[catalog[item].compute(row) for item in ids] for row in rows], dtype=float)


def _metrics(rows: list[dict[str, Any]], target: np.ndarray, prediction: np.ndarray) -> dict[str, float]:
    topology_errors: dict[str, list[float]] = {}
    for row, truth, predicted in zip(rows, target, prediction):
        topology_errors.setdefault(str(row["framework_code"]), []).append(float(truth - predicted))
    topology_mae = [float(np.mean(np.abs(values))) for values in topology_errors.values()]
    topology_rmse = [float(np.sqrt(np.mean(np.square(values)))) for values in topology_errors.values()]
    return {
        "row_mae_mol_kg": float(mean_absolute_error(target, prediction)),
        "row_rmse_mol_kg": float(mean_squared_error(target, prediction) ** 0.5),
        "row_r2": float(r2_score(target, prediction)),
        "topology_macro_mae_mol_kg": float(np.mean(topology_mae)),
        "topology_macro_rmse_mol_kg": float(np.mean(topology_rmse)),
        "negative_prediction_fraction": float(np.mean(prediction < 0.0)),
    }


def evaluate_adszeo(
    dataset: AdsZeoDataset,
    descriptor_ids: tuple[str, ...] | list[str],
    catalog: dict[str, Descriptor],
    *,
    fixed_parameters: dict[str, float | int] | None = None,
    random_state: int = 20260902,
    evaluate_test: bool = True,
) -> dict[str, Any]:
    partitions = {
        name: [row for row in dataset.rows if row["split"] == name]
        for name in ("train", "validation", "test")
    }
    if any(not rows for rows in partitions.values()):
        raise ValueError("AdsZeo split contains an empty partition")

    def fit(parameters: dict[str, float | int], rows: list[dict[str, Any]]) -> Pipeline:
        model = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
                ("regressor", HistGradientBoostingRegressor(max_iter=250, random_state=random_state, **parameters)),
            ]
        )
        model.fit(_feature_matrix(rows, descriptor_ids, catalog), np.log1p([float(row[TARGET_COLUMN]) for row in rows]))
        return model

    candidates = (fixed_parameters,) if fixed_parameters is not None else MODEL_CANDIDATES
    validation_rows = partitions["validation"]
    validation_target = np.asarray([float(row[TARGET_COLUMN]) for row in validation_rows])
    scored = []
    for parameters in candidates:
        model = fit(dict(parameters), partitions["train"])
        prediction = np.maximum(np.expm1(model.predict(_feature_matrix(validation_rows, descriptor_ids, catalog))), 0.0)
        score = _metrics(validation_rows, validation_target, prediction)["topology_macro_mae_mol_kg"]
        scored.append((score, dict(parameters)))
    validation_score, selected = min(scored, key=lambda item: (item[0], json.dumps(item[1], sort_keys=True)))
    result = {
        "descriptor_ids": list(descriptor_ids),
        "split": {name: len(rows) for name, rows in partitions.items()},
        "selected_parameters": selected,
        "validation_topology_macro_mae_mol_kg": validation_score,
    }
    if evaluate_test:
        final_rows = partitions["train"] + partitions["validation"]
        model = fit(selected, final_rows)
        test_rows = partitions["test"]
        target = np.asarray([float(row[TARGET_COLUMN]) for row in test_rows])
        prediction = np.maximum(np.expm1(model.predict(_feature_matrix(test_rows, descriptor_ids, catalog))), 0.0)
        result["test"] = _metrics(test_rows, target, prediction)
    return result


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_adszeo_loop(
    *,
    service: KnowledgeModeRetriever,
    database_path: Path,
    output_path: Path,
    task: str,
    query: str,
    budget: RetrievalBudget,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4500,
    thinking: str = "enabled",
    reasoning_effort: str = "low",
    replicate_id: int | None = None,
    modes: Iterable[str] = EXPERIMENT_KNOWLEDGE_MODES,
    selected_descriptor_count: int = 3,
    strict_dataset: bool = True,
    database_sha256: str | None = None,
    client: GlmClient | None = None,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    dataset = load_adszeo(database_path, strict=strict_dataset)
    catalog = adszeo_descriptor_catalog()
    allowed_inputs = sorted({key for row in dataset.rows for key in row} - {TARGET_COLUMN, "run_id", "structure_id", "framework_code", "split"})
    prompt_system, _ = build_discovery_prompt(
        task=task, query=query, knowledge_mode="agent", evidence_context="", catalog=catalog,
        selected_descriptor_count=selected_descriptor_count, benchmark_name="AdsZeo v1",
        benchmark_target="298 K methane absolute loading (mol/kg framework)",
        benchmark_role="primary zeolite scientific-descriptor benchmark",
        allowed_inputs=allowed_inputs, baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
    )
    baseline = evaluate_adszeo(dataset, D0_DESCRIPTOR_IDS, catalog)
    api_client = client or GlmClient()
    mode_results: dict[str, Any] = {}
    for mode in modes:
        try:
            bundle = service.retrieve(query=query, experiment_mode=mode, budget=budget)
            system, user = build_discovery_prompt(
                task=task, query=query, knowledge_mode=mode,
                evidence_context=_label_evidence_context(bundle), catalog=catalog,
                selected_descriptor_count=selected_descriptor_count, benchmark_name="AdsZeo v1",
                benchmark_target="298 K methane absolute loading (mol/kg framework)",
                benchmark_role="primary zeolite scientific-descriptor benchmark",
                allowed_inputs=allowed_inputs, baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
            )
            response: GlmResponse = api_client.chat_json(
                model=model, system=system, user=user, temperature=temperature,
                max_tokens=max_tokens, thinking=thinking, reasoning_effort=reasoning_effort,
            )
            generation = validate_discovery_output(
                response.structured, catalog, selected_descriptor_count=selected_descriptor_count,
                allowed_evidence_ids={f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)},
                require_empty_evidence=mode == "agent", baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
            )
            d1 = evaluate_adszeo(
                dataset, (*D0_DESCRIPTOR_IDS, *generation["selected_descriptor_ids"]), catalog,
                fixed_parameters=baseline["selected_parameters"],
            )
            d0_mae = baseline["test"]["topology_macro_mae_mol_kg"]
            d1_mae = d1["test"]["topology_macro_mae_mol_kg"]
            mode_results[mode] = {
                "status": "completed", "bundle": bundle,
                "prompt": {"system_sha256": _canonical_hash(system), "user_sha256": _canonical_hash(user), "row_level_data_included": False, "row_level_labels_included": False},
                "model": {"provider": response.provider, "model": response.model, "requested_model": model, "usage": response.usage, "response_id": response.raw.get("id"), "temperature": temperature, "max_tokens": max_tokens, "thinking": thinking, "reasoning_effort": reasoning_effort},
                "generation": generation,
                "downstream": {
                    "model": "sklearn.HistGradientBoostingRegressor",
                    "target_transform": "log1p",
                    "D0": baseline,
                    "D0_plus_X": d1,
                    "topology_macro_mae_relative_improvement": (d0_mae - d1_mae) / max(d0_mae, 1e-12),
                },
            }
        except Exception as error:
            mode_results[mode] = {"status": "failed", "error_type": type(error).__name__, "error": str(error)}
    finished = datetime.now(timezone.utc)
    result = {
        "schema_version": RUN_SCHEMA_VERSION,
        "run_classification": "EXPLORATORY_BENCHMARK_V1",
        "protocol_status": "FROZEN_BEFORE_OUTCOME_RUN",
        "replicate_id": replicate_id,
        "started_at": started.isoformat(), "finished_at": finished.isoformat(),
        "duration_seconds": (finished - started).total_seconds(),
        "task": task, "query": query,
        "warnings": [
            "Only pre-adsorption framework fields and scalar GCMC targets are loaded; positions and cycle_stats are forbidden features.",
            "Splits are topology-level, so all structures and pressures from a topology remain in one partition.",
            "AdsZeo is a methane-adsorption benchmark and does not by itself establish thermocatalysis transfer.",
        ],
        "dataset": {
            **dataset.metadata,
            "database_sha256": database_sha256 or _sha256_file(database_path),
            "database_sha256_source": "supplied_after_staging" if database_sha256 else "computed_during_run",
        },
        "retrieval": {"budget": budget.__dict__, "source_identities": service.source_identities},
        "prompt": {"system_sha256": _canonical_hash(prompt_system), "schema_version": DISCOVERY_SCHEMA_VERSION, "selected_descriptor_count": selected_descriptor_count},
        "baseline_D0": baseline,
        "modes": mode_results,
        "environment": {"python": sys.version, "platform": platform.platform()},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output_path)
    return result
