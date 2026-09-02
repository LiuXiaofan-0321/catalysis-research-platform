"""Materials Cloud Zeolite Atlas GLM comparison and exploratory ML diagnostic."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from catalysis_research.datasets.materialscloud import ZeoliteAtlasDataset, load_zeolite_atlas
from catalysis_research.experiments.discovery_loop import (
    DISCOVERY_SCHEMA_VERSION,
    DEFAULT_MODEL,
    _canonical_hash,
    _label_evidence_context,
    build_discovery_prompt,
    validate_discovery_output,
)
from catalysis_research.models.glm import GlmClient, GlmResponse
from catalysis_research.retrieval import EXPERIMENT_KNOWLEDGE_MODES, KnowledgeModeRetriever, RetrievalBudget
from catalysis_research.experiments.themecat_pilot import ALPHA_GRID, Descriptor


RUN_SCHEMA_VERSION = "glm_scientific_discovery_zeolite_atlas_exploratory.v1"
D0_DESCRIPTOR_IDS = tuple(
    [f"angles_mean_{index}" for index in range(4)]
    + [f"distances_mean_{index}" for index in range(4)]
    + [f"ring_mean_{index}" for index in range(20)]
)


def _number(row: dict[str, str], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")


def atlas_descriptor_catalog() -> dict[str, Descriptor]:
    n = _number
    definitions = [
        *[
            Descriptor(
                f"angles_mean_{index}",
                f"mean(angle_descriptor_{index})",
                "descriptor units",
                "Source classical angular descriptor baseline.",
                lambda r, index=index: n(r, f"angles_mean_{index}"),
            )
            for index in range(4)
        ],
        *[
            Descriptor(
                f"distances_mean_{index}",
                f"mean(distance_descriptor_{index})",
                "descriptor units",
                "Source classical distance descriptor baseline.",
                lambda r, index=index: n(r, f"distances_mean_{index}"),
            )
            for index in range(4)
        ],
        *[
            Descriptor(
                f"ring_mean_{index}",
                f"mean(ring_descriptor_{index})",
                "count",
                "Source King ring-distribution descriptor baseline.",
                lambda r, index=index: n(r, f"ring_mean_{index}"),
            )
            for index in range(20)
        ],
        Descriptor("angles_std_mean", "mean(std(angle descriptor))", "descriptor units", "Local angular heterogeneity.", lambda r: float(np.mean([n(r, f"angles_std_{i}") for i in range(4)]))),
        Descriptor("distances_std_mean", "mean(std(distance descriptor))", "descriptor units", "Local distance heterogeneity.", lambda r: float(np.mean([n(r, f"distances_std_{i}") for i in range(4)]))),
        Descriptor("ring_entropy", "H(ring distribution)", "unitless", "Topology distribution diversity.", lambda r: n(r, "ring_entropy")),
        Descriptor("ring_nonzero_fraction", "fraction(ring_mean > 0)", "unitless", "Fraction of represented ring sizes.", lambda r: n(r, "ring_nonzero_fraction")),
        Descriptor("soap6_pc1_mean", "mean(SOAP-KPCA PC1)", "source-defined", "Long-range local-environment coordinate.", lambda r: n(r, "soap6_pc1_mean")),
        Descriptor("soap6_pc1_std", "std(SOAP-KPCA PC1)", "source-defined", "Within-structure SOAP environment heterogeneity.", lambda r: n(r, "soap6_pc1_std")),
        Descriptor("soap6_pc2_mean", "mean(SOAP-KPCA PC2)", "source-defined", "Second local-environment coordinate.", lambda r: n(r, "soap6_pc2_mean")),
        Descriptor("soap6_pc2_std", "std(SOAP-KPCA PC2)", "source-defined", "Second-coordinate heterogeneity.", lambda r: n(r, "soap6_pc2_std")),
        Descriptor("soap6_pc3_mean", "mean(SOAP-KPCA PC3)", "source-defined", "Third local-environment coordinate.", lambda r: n(r, "soap6_pc3_mean")),
        Descriptor("soap6_pc3_std", "std(SOAP-KPCA PC3)", "source-defined", "Third-coordinate heterogeneity.", lambda r: n(r, "soap6_pc3_std")),
        Descriptor("soap6_variability", "mean(std(SOAP-KPCA PCs))", "source-defined", "Aggregate local-environment variability.", lambda r: n(r, "soap6_variability")),
        Descriptor("angle_distance_interaction", "angles_mean_0*distances_mean_0", "source-defined", "Coupled angular and distance scale.", lambda r: n(r, "angles_mean_0") * n(r, "distances_mean_0")),
    ]
    return {item.descriptor_id: item for item in definitions}


def _matrix(rows: list[dict[str, str]], ids: Iterable[str], catalog: dict[str, Descriptor]) -> np.ndarray:
    return np.asarray([[catalog[item].compute(row) for item in ids] for row in rows], dtype=float)


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "rmse": float(mean_squared_error(y_true, y_pred) ** 0.5),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def evaluate_atlas(dataset: ZeoliteAtlasDataset, descriptor_ids: tuple[str, ...] | list[str], catalog: dict[str, Descriptor]) -> dict[str, Any]:
    # Structure-ID modulo split is frozen before generation and keeps all atoms
    # from a structure in the same partition.
    groups = np.asarray([int("".join(ch for ch in row["sample_id"] if ch.isdigit())) % 5 for row in dataset.rows])
    train = groups < 3
    validation = groups == 3
    test = groups == 4
    x = _matrix(dataset.rows, descriptor_ids, catalog)
    fold_results: dict[str, Any] = {}
    for target_name, target in (("energy", dataset.energy), ("volume", dataset.volume)):
        candidates = []
        for alpha in ALPHA_GRID:
            pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=alpha)),
            ])
            pipeline.fit(x[train], target[train])
            candidates.append((float(mean_squared_error(target[validation], pipeline.predict(x[validation])) ** 0.5), alpha, pipeline))
        validation_rmse, alpha, pipeline = min(candidates, key=lambda item: (item[0], item[1]))
        fold_results[target_name] = {
            "train_rows": int(np.sum(train)),
            "validation_rows": int(np.sum(validation)),
            "test_rows": int(np.sum(test)),
            "selected_alpha": float(alpha),
            "validation_rmse": validation_rmse,
            "test": _metrics(target[test], pipeline.predict(x[test])),
        }
    return {
        "split": {"algorithm": "structure_id_modulo_5", "train_modulo": [0, 1, 2], "validation_modulo": [3], "test_modulo": [4]},
        "targets": fold_results,
    }


def run_zeolite_atlas_loop(
    *,
    service: KnowledgeModeRetriever,
    dataset_root: Path,
    output_path: Path,
    task: str,
    query: str,
    budget: RetrievalBudget,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4500,
    thinking: str = "enabled",
    reasoning_effort: str = "low",
    modes: Iterable[str] = EXPERIMENT_KNOWLEDGE_MODES,
    selected_descriptor_count: int = 3,
    client: GlmClient | None = None,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    dataset = load_zeolite_atlas(dataset_root)
    catalog = atlas_descriptor_catalog()
    allowed_inputs = sorted({key for row in dataset.rows for key in row if key != "sample_id"})
    system, _ = build_discovery_prompt(
        task=task, query=query, knowledge_mode="agent", evidence_context="", catalog=catalog,
        selected_descriptor_count=selected_descriptor_count, benchmark_name="Materials Cloud Zeolite Atlas v1",
        benchmark_target="structure-level energy and volume", benchmark_role="primary zeolite structure descriptor benchmark candidate",
        allowed_inputs=allowed_inputs, baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
    )
    api_client = client or GlmClient()
    mode_results: dict[str, Any] = {}
    for mode in modes:
        try:
            bundle = service.retrieve(query=query, experiment_mode=mode, budget=budget)
            system_mode, user = build_discovery_prompt(
                task=task, query=query, knowledge_mode=mode, evidence_context=_label_evidence_context(bundle), catalog=catalog,
                selected_descriptor_count=selected_descriptor_count, benchmark_name="Materials Cloud Zeolite Atlas v1",
                benchmark_target="structure-level energy and volume", benchmark_role="primary zeolite structure descriptor benchmark candidate",
                allowed_inputs=allowed_inputs, baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
            )
            response: GlmResponse = api_client.chat_json(model=model, system=system_mode, user=user, temperature=temperature, max_tokens=max_tokens, thinking=thinking, reasoning_effort=reasoning_effort)
            generation = validate_discovery_output(response.structured, catalog, selected_descriptor_count=selected_descriptor_count,
                allowed_evidence_ids={f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)},
                require_empty_evidence=mode == "agent", baseline_descriptor_ids=D0_DESCRIPTOR_IDS)
            d0 = evaluate_atlas(dataset, D0_DESCRIPTOR_IDS, catalog)
            d1 = evaluate_atlas(dataset, tuple(D0_DESCRIPTOR_IDS) + tuple(generation["selected_descriptor_ids"]), catalog)
            mode_results[mode] = {
                "status": "completed", "bundle": bundle,
                "prompt": {"system_sha256": _canonical_hash(system_mode), "user_sha256": _canonical_hash(user), "row_level_data_included": False, "row_level_labels_included": False},
                "model": {"provider": response.provider, "model": response.model, "requested_model": model, "usage": response.usage, "response_id": response.raw.get("id"), "temperature": temperature, "max_tokens": max_tokens, "thinking": thinking, "reasoning_effort": reasoning_effort},
                "generation": generation,
                "downstream": {"model": "sklearn.linear_model.Ridge", "alpha_grid": list(ALPHA_GRID), "D0_descriptor_ids": list(D0_DESCRIPTOR_IDS), "D0_plus_X_descriptor_ids": list(generation["selected_descriptor_ids"]), "D0": d0, "D0_plus_X": d1},
            }
        except Exception as error:
            mode_results[mode] = {"status": "failed", "error_type": type(error).__name__, "error": str(error)}
    finished = datetime.now(timezone.utc)
    result = {
        "schema_version": RUN_SCHEMA_VERSION, "run_classification": "EXPLORATORY_NOT_CONFIRMATORY", "protocol_status": "ACTIVATION_BLOCKED",
        "started_at": started.isoformat(), "finished_at": finished.isoformat(), "duration_seconds": (finished - started).total_seconds(), "task": task, "query": query,
        "warnings": ["This is the first Materials Cloud Zeolite Atlas adapter run; original-paper native model/unit reproduction remains to be signed off.", "No row-level labels or locked-test outcomes were exposed to GLM descriptor generation.", "The RAG/Small-KG source is evidence for hypothesis generation; D0/D0+X metrics are exploratory and do not establish a general KG claim."],
        "dataset": {**dataset.metadata, "archive_sha256": "d704adbccbfee6d5736abf0a5d68d5893c85bbab43483c37a5be525587d7b4e4"},
        "retrieval": {"budget": budget.__dict__, "source_identities": service.source_identities},
        "prompt": {"system_sha256": _canonical_hash(system), "schema_version": DISCOVERY_SCHEMA_VERSION, "selected_descriptor_count": selected_descriptor_count},
        "modes": mode_results, "environment": {"python": sys.version, "platform": platform.platform()},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output_path)
    return result
