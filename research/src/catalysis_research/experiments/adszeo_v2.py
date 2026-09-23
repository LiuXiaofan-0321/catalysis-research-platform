"""AdsZeo v2: geometry-extended descriptor catalog + 3-round discovery loop.

Changes versus the v1 experiment (release adszeo-v1-20260903):
  1. The frozen 25-descriptor catalog is extended with leakage-safe pore-geometry
     descriptors precomputed from framework coordinates (ring-size distribution,
     coordination sequence, bond geometry, Al second-shell siting).
  2. Each knowledge mode runs `rounds` generation rounds. After every round the
     model receives validation-only feedback (topology macro-MAE delta of the
     selected set and of each selected descriptor individually) and may revise
     its selection. The held-out test split is evaluated exactly once, after the
     final round, with the D0-tuned hyperparameters.

Task text, query, model, budgets and split are identical to v1, so the only
protocol changes are the catalog and the iterative loop.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from catalysis_research.datasets.adszeo import TARGET_COLUMN, load_adszeo
from catalysis_research.experiments.adszeo import (
    D0_DESCRIPTOR_IDS,
    adszeo_descriptor_catalog,
    evaluate_adszeo,
)
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
from catalysis_research.retrieval import (
    EXPERIMENT_KNOWLEDGE_MODES,
    KnowledgeModeRetriever,
    RetrievalBudget,
)

RUN_SCHEMA_VERSION = "glm_scientific_discovery_adszeo_v3_blinded_catalog.v3"
VALIDATION_MODE = "lenient_deterministic_repair_plus_schema_retry.v2"

# Frozen evidence-family queries for the purified retrieval strategy. Each
# family targets one descriptor class; the merged bundle stays inside the same
# item/token/per-paper budgets as the single-query strategy, so the knowledge
# conditions remain budget-matched against the agent condition.
EVIDENCE_FAMILY_QUERIES = (
    "zeolite framework topology ring size channel pore architecture methane adsorption selectivity",
    "zeolite pore volume void fraction accessible porosity methane loading adsorption capacity",
    "zeolite aluminium sodium cation silicon aluminium ratio methane adsorption heat",
)


def _item_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (row.get("paper_id"), row.get("document_id"), str(row.get("quote"))[:200])


def retrieve_purified_bundle(
    service: KnowledgeModeRetriever,
    *,
    queries: Iterable[str],
    experiment_mode: str,
    budget: RetrievalBudget,
) -> dict[str, Any]:
    """Retrieve per evidence family, then merge under the frozen budgets.

    Families are interleaved round-robin so no single query dominates the
    bundle; duplicates (same paper/document/quote) and per-paper overruns are
    dropped; the merged bundle keeps item_limit and context_token_budget, so
    the model-visible budget matches the single-query strategy exactly.
    """
    from catalysis_research.retrieval.bundle import _format_item

    family_items: list[list[dict[str, Any]]] = []
    family_stats: list[dict[str, Any]] = []
    for query in queries:
        bundle = service.retrieve(query=query, experiment_mode=experiment_mode, budget=budget)
        items = list(bundle.get("items") or [])
        family_stats.append({
            "query": query,
            "items": len(items),
            "context_chars": len(str(bundle.get("context") or "")),
        })
        family_items.append(items)

    merged: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    paper_counts: Counter[str] = Counter()
    used_tokens = 0
    index = 0
    while len(merged) < budget.item_limit:
        added = False
        for items in family_items:
            if index >= len(items):
                continue
            row = items[index]
            key = _item_key(row)
            if key in seen:
                continue
            tokens = int(row.get("token_count") or 0)
            paper_id = row.get("paper_id")
            if paper_counts[paper_id] >= budget.max_items_per_paper:
                continue
            if used_tokens + tokens > budget.context_token_budget:
                continue
            seen.add(key)
            paper_counts[paper_id] += 1
            used_tokens += tokens
            merged.append(row)
            added = True
            if len(merged) >= budget.item_limit:
                break
        if not added:
            break
        index += 1

    context = "\n\n".join(_format_item(i, row) for i, row in enumerate(merged, 1))
    return {
        "context": context,
        "items": merged,
        "mode": experiment_mode,
        "evidence_strategy": "three_family_purified",
        "family_queries": list(queries),
        "family_stats": family_stats,
        "merged_item_count": len(merged),
        "merged_token_count": used_tokens,
    }


class _BlindedDescriptor:
    """Prompt-side wrapper that hides the curated scientific_rationale text.

    The rationale stays in the run artifact for auditability but is not shown
    to any knowledge mode, so retrieved evidence is the only channel that can
    explain why a descriptor might matter. compute() is delegated unchanged,
    so evaluation behaves identically.
    """

    def __init__(self, inner: Descriptor) -> None:
        self._inner = inner

    @property
    def descriptor_id(self) -> str:
        return self._inner.descriptor_id

    @property
    def rationale(self) -> str:
        return self._inner.rationale

    def compute(self, row: dict[str, Any]) -> float:
        return self._inner.compute(row)

    def prompt_record(self) -> dict[str, str]:
        return {
            "descriptor_id": self._inner.descriptor_id,
            "formula": self._inner.formula,
            "units": self._inner.units,
        }
RANDOM_STATE = 20260902

GEOMETRY_RATIONALES = {
    "ring4_frac": "Fraction of framework T sites whose smallest ring is 4-membered.",
    "ring5_frac": "Fraction of framework T sites whose smallest ring is 5-membered.",
    "ring6_frac": "Fraction of framework T sites whose smallest ring is 6-membered.",
    "ring7_frac": "Fraction of framework T sites whose smallest ring is 7-membered.",
    "ring8_frac": "Fraction of framework T sites whose smallest ring is 8-membered.",
    "ring10_frac": "Fraction of framework T sites whose smallest ring is 10-membered.",
    "ring12_frac": "Fraction of framework T sites whose smallest ring is 12-membered.",
    "ring13p_frac": "Fraction of framework T sites whose smallest ring has 13 or more members.",
    "ring_mean": "Mean smallest-ring size over framework T sites.",
    "ring_entropy": "Shannon entropy of the smallest-ring size distribution over T sites.",
    "cs2_mean": "Mean number of T atoms at graph distance two (coordination sequence).",
    "cs3_mean": "Mean number of T atoms at graph distance three (coordination sequence).",
    "tt_bond_mean": "Mean T-T distance across O-bridged T-T bonds.",
    "tt_bond_std": "Standard deviation of O-bridged T-T bond distances.",
    "otot_angle_mean": "Mean O-T-O angle over framework T sites.",
    "otot_angle_std": "Standard deviation of O-T-O angles over framework T sites.",
    "al_second_shell_al_frac": "Fraction of Al sites with another Al within two T-O-T hops.",
}


def _number(row: dict[str, Any], key: str) -> float:
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")
    return value if math.isfinite(value) else float("nan")


def load_geometry(path: Path) -> tuple[list[str], dict[str, dict[str, float]]]:
    import pandas as pd

    frame = pd.read_csv(path)
    columns = [c for c in frame.columns if c in GEOMETRY_RATIONALES]
    missing = sorted(set(GEOMETRY_RATIONALES) - set(columns))
    if missing:
        raise ValueError(f"geometry CSV is missing descriptor columns: {missing}")
    mapping = {
        str(row["structure_id"]): {c: float(row[c]) for c in columns}
        for _, row in frame.iterrows()
    }
    return columns, mapping


def adszeo_v2_catalog(geometry_columns: list[str]) -> dict[str, Descriptor]:
    catalog = dict(adszeo_descriptor_catalog())
    for column in geometry_columns:
        catalog[column] = Descriptor(
            column,
            column,
            "unitless" if "frac" in column or "entropy" in column else "mixed",
            GEOMETRY_RATIONALES[column],
            lambda row, key=column: _number(row, key),
        )
    return catalog


def _pipeline(parameters: dict[str, float | int]) -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
            ("regressor", HistGradientBoostingRegressor(max_iter=250, random_state=RANDOM_STATE, **parameters)),
        ]
    )


def _feature_matrix(rows: list[dict[str, Any]], ids: Iterable[str], catalog: dict[str, Descriptor]) -> np.ndarray:
    return np.asarray([[catalog[item].compute(row) for item in ids] for row in rows], dtype=float)


def _topology_macro_mae(rows: list[dict[str, Any]], prediction: np.ndarray) -> float:
    errors: dict[str, list[float]] = {}
    for row, predicted in zip(rows, prediction):
        errors.setdefault(str(row["framework_code"]), []).append(float(row[TARGET_COLUMN]) - float(predicted))
    return float(np.mean([np.mean(np.abs(values)) for values in errors.values()]))


def _validation_mae(
    dataset_rows: list[dict[str, Any]],
    descriptor_ids: tuple[str, ...],
    catalog: dict[str, Descriptor],
    parameters: dict[str, float | int],
) -> float:
    train = [row for row in dataset_rows if row["split"] == "train"]
    validation = [row for row in dataset_rows if row["split"] == "validation"]
    model = _pipeline(parameters)
    model.fit(
        _feature_matrix(train, descriptor_ids, catalog),
        np.log1p([float(row[TARGET_COLUMN]) for row in train]),
    )
    prediction = np.maximum(np.expm1(model.predict(_feature_matrix(validation, descriptor_ids, catalog))), 0.0)
    return _topology_macro_mae(validation, prediction)


def validate_discovery_output_lenient(
    value: dict[str, Any],
    catalog: dict[str, Descriptor],
    *,
    selected_descriptor_count: int = 3,
    allowed_evidence_ids: set[str] | None = None,
    require_empty_evidence: bool = False,
    baseline_descriptor_ids: tuple[str, ...] = D0_DESCRIPTOR_IDS,
) -> tuple[dict[str, Any], list[str]]:
    """Lenient schema validation with deterministic repairs.

    Format violations are repaired mechanically and recorded instead of
    failing the run: over-budget selections are truncated, descriptors that
    are absent from the catalog or belong to D0 are dropped, missing text
    fields are filled with "unspecified", invalid epistemic_status values are
    coerced to "tentative", and unavailable or agent-mode evidence citations
    are stripped. Only an unusable output (missing hypothesis or zero usable
    descriptors) raises, which triggers one schema-repair model retry.
    """
    repairs: list[str] = []
    if not isinstance(value, dict):
        raise ValueError("Discovery output must be a JSON object")
    hypothesis = value.get("hypothesis")
    if not isinstance(hypothesis, str) or not hypothesis.strip():
        raise ValueError("hypothesis missing or empty (unrecoverable by repair)")
    hypothesis = hypothesis.strip()

    raw_chain = value.get("evidence_chain")
    evidence_chain = []
    if isinstance(raw_chain, list):
        for record in raw_chain:
            if not isinstance(record, dict):
                continue
            evidence_id = record.get("evidence_id")
            claim = record.get("claim") if isinstance(record.get("claim"), str) else ""
            role = record.get("role") if isinstance(record.get("role"), str) and record["role"].strip() else "context"
            if require_empty_evidence:
                if evidence_id is not None:
                    repairs.append("agent mode cited external evidence; citations stripped")
                continue
            if evidence_id is not None and evidence_id not in (allowed_evidence_ids or set()):
                repairs.append(f"evidence_chain cited unavailable ID {evidence_id}; entry dropped")
                continue
            if not claim.strip():
                continue
            evidence_chain.append({"evidence_id": evidence_id, "role": role, "claim": claim.strip()})
    elif raw_chain not in (None, [], {}):
        repairs.append("evidence_chain was not a list; replaced with empty list")

    raw_candidates = value.get("descriptor_candidates")
    candidate_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(raw_candidates, list):
        for cand in raw_candidates:
            if isinstance(cand, dict) and isinstance(cand.get("descriptor_id"), str):
                candidate_by_id[cand["descriptor_id"]] = cand
    elif raw_candidates not in (None, []):
        repairs.append("descriptor_candidates was not a list; recovered from selected_descriptor_ids")

    order: list[str] = []
    raw_selected = value.get("selected_descriptor_ids")
    if isinstance(raw_selected, list):
        order.extend(item for item in raw_selected if isinstance(item, str))
    if not order and raw_candidates:
        repairs.append("selected_descriptor_ids missing; recovered from candidate order")
    for cand_id in candidate_by_id:
        if cand_id not in order:
            order.append(cand_id)

    selected: list[str] = []
    for did in order:
        if did in selected:
            continue
        if did not in catalog:
            repairs.append(f"descriptor {did} not in catalog; dropped")
            continue
        if did in baseline_descriptor_ids:
            repairs.append(f"descriptor {did} is a D0 descriptor; dropped")
            continue
        selected.append(did)
    if len(selected) > selected_descriptor_count:
        repairs.append(
            f"{len(selected)} descriptors exceeded budget {selected_descriptor_count}; "
            "truncated to the first reported"
        )
        selected = selected[:selected_descriptor_count]
    if not selected:
        raise ValueError("no usable new descriptor after repair (unrecoverable)")
    if len(selected) < selected_descriptor_count:
        repairs.append(
            f"only {len(selected)}/{selected_descriptor_count} descriptors supplied; "
            "proceeding with the undersized set"
        )

    descriptor_candidates = []
    for did in selected:
        cand = candidate_by_id.get(did, {})
        record = {"descriptor_id": did}
        for field in ("rationale", "expected_direction", "falsification_criteria"):
            text = cand.get(field)
            if not isinstance(text, str) or not text.strip():
                repairs.append(f"candidate {did} missing {field}; filled with 'unspecified'")
                text = "unspecified"
            record[field] = text.strip()
        descriptor_candidates.append(record)

    epistemic = value.get("epistemic_status")
    if epistemic not in {"supported", "tentative", "insufficient_evidence"}:
        repairs.append(f"epistemic_status {epistemic!r} invalid; coerced to 'tentative'")
        epistemic = "tentative"
    direction = value.get("expected_direction")
    if not isinstance(direction, str) or not direction.strip():
        repairs.append("expected_direction missing; filled with 'unspecified'")
        direction = "unspecified"
    criteria = value.get("falsification_criteria")
    if not isinstance(criteria, list) or not criteria or not all(isinstance(c, str) and c.strip() for c in criteria):
        repairs.append("falsification_criteria missing or invalid; filled with ['unspecified']")
        criteria = ["unspecified"]

    return {
        "evidence_chain": evidence_chain,
        "hypothesis": hypothesis,
        "descriptor_candidates": descriptor_candidates,
        "selected_descriptor_ids": selected,
        "expected_direction": direction.strip(),
        "falsification_criteria": criteria,
        "epistemic_status": epistemic,
    }, repairs


def run_adszeo_v2_loop(
    *,
    service: KnowledgeModeRetriever,
    database_path: Path,
    geometry_csv: Path,
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
    rounds: int = 3,
    evidence_queries: tuple[str, ...] | None = None,
    database_sha256: str | None = None,
    client: GlmClient | None = None,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    dataset = load_adszeo(database_path)
    geometry_columns, geometry_map = load_geometry(geometry_csv)
    for row in dataset.rows:
        row.update(geometry_map[row["structure_id"]])
    catalog_full = adszeo_v2_catalog(geometry_columns)
    catalog = {key: _BlindedDescriptor(item) for key, item in catalog_full.items()}
    allowed_inputs = sorted(
        {key for row in dataset.rows for key in row}
        - {TARGET_COLUMN, "run_id", "structure_id", "framework_code", "split"}
    )
    geometry_sha256 = hashlib.sha256(Path(geometry_csv).read_bytes()).hexdigest()

    baseline = evaluate_adszeo(dataset, D0_DESCRIPTOR_IDS, catalog)
    parameters = baseline["selected_parameters"]
    d0_validation_mae = baseline["validation_topology_macro_mae_mol_kg"]

    prompt_system, _ = build_discovery_prompt(
        task=task, query=query, knowledge_mode="agent", evidence_context="", catalog=catalog,
        selected_descriptor_count=selected_descriptor_count, benchmark_name="AdsZeo v1",
        benchmark_target="298 K methane absolute loading (mol/kg framework)",
        benchmark_role="primary zeolite scientific-descriptor benchmark",
        allowed_inputs=allowed_inputs, baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
    )
    api_client = client or GlmClient()
    mode_results: dict[str, Any] = {}
    for mode in modes:
        try:
            if evidence_queries:
                bundle = retrieve_purified_bundle(
                    service, queries=evidence_queries, experiment_mode=mode, budget=budget,
                )
            else:
                bundle = service.retrieve(query=query, experiment_mode=mode, budget=budget)
            evidence_context = _label_evidence_context(bundle)
            history: list[dict[str, Any]] = []
            round_records: list[dict[str, Any]] = []
            final_generation: dict[str, Any] | None = None
            for round_index in range(1, rounds + 1):
                system, user = build_discovery_prompt(
                    task=task, query=query, knowledge_mode=mode, evidence_context=evidence_context,
                    catalog=catalog, selected_descriptor_count=selected_descriptor_count,
                    benchmark_name="AdsZeo v1",
                    benchmark_target="298 K methane absolute loading (mol/kg framework)",
                    benchmark_role="primary zeolite scientific-descriptor benchmark",
                    allowed_inputs=allowed_inputs, baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
                )
                if history:
                    payload = json.loads(user)
                    payload["previous_rounds"] = history
                    payload["revision_instructions"] = [
                        "This is a revision round. You may keep or replace any previously selected descriptor.",
                        "Prefer replacing descriptors whose individual validation delta shows no benefit.",
                        "The validation feedback comes from held-out topologies in the validation split; it never includes test outcomes.",
                    ]
                    user = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                response: GlmResponse = api_client.chat_json(
                    model=model, system=system, user=user, temperature=temperature,
                    max_tokens=max_tokens, thinking=thinking, reasoning_effort=reasoning_effort,
                )
                generation: dict[str, Any]
                repairs: list[str]
                schema_retry_used = False
                usage = dict(response.usage or {})
                try:
                    generation, repairs = validate_discovery_output_lenient(
                        response.structured, catalog,
                        selected_descriptor_count=selected_descriptor_count,
                        allowed_evidence_ids={f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)},
                        require_empty_evidence=mode == "agent",
                        baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
                    )
                except ValueError as first_error:
                    repair_payload = {
                        "schema_repair": {
                            "previous_output_rejected": str(first_error),
                            "previous_output": response.structured,
                            "instructions": (
                                "Your previous output violated the required schema. Return the same "
                                "JSON object with the reported problem corrected. Keep the same "
                                "hypothesis and descriptor selections; fix only the format."
                            ),
                        }
                    }
                    response = api_client.chat_json(
                        model=model, system=system, user=json.dumps(repair_payload, ensure_ascii=False, sort_keys=True),
                        temperature=temperature, max_tokens=max_tokens, thinking=thinking,
                        reasoning_effort=reasoning_effort,
                    )
                    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
                        usage[key] = usage.get(key, 0) + (response.usage or {}).get(key, 0)
                    generation, repairs = validate_discovery_output_lenient(
                        response.structured, catalog,
                        selected_descriptor_count=selected_descriptor_count,
                        allowed_evidence_ids={f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)},
                        require_empty_evidence=mode == "agent",
                        baseline_descriptor_ids=D0_DESCRIPTOR_IDS,
                    )
                    repairs.append("schema repair retry used")
                    schema_retry_used = True
                selected = generation["selected_descriptor_ids"]
                individual = {
                    did: _validation_mae(dataset.rows, (*D0_DESCRIPTOR_IDS, did), catalog, parameters) - d0_validation_mae
                    for did in selected
                }
                set_delta = (
                    _validation_mae(dataset.rows, (*D0_DESCRIPTOR_IDS, *selected), catalog, parameters)
                    - d0_validation_mae
                )
                feedback = {
                    "d0_validation_macro_mae": d0_validation_mae,
                    "validation_set_delta_macro_mae": set_delta,
                    "validation_individual_deltas_macro_mae": individual,
                }
                history.append({
                    "round": round_index,
                    "hypothesis": generation["hypothesis"],
                    "selected_descriptor_ids": selected,
                    **feedback,
                })
                round_records.append({
                    "round": round_index,
                    "generation": generation,
                    "validation_repairs": repairs,
                    "schema_retry_used": schema_retry_used,
                    "validation_feedback": feedback,
                    "prompt": {"system_sha256": _canonical_hash(system), "user_sha256": _canonical_hash(user)},
                    "model": {"usage": usage, "response_id": response.raw.get("id")},
                })
                final_generation = generation
            assert final_generation is not None
            d1 = evaluate_adszeo(
                dataset, (*D0_DESCRIPTOR_IDS, *final_generation["selected_descriptor_ids"]), catalog,
                fixed_parameters=parameters,
            )
            d0_mae = baseline["test"]["topology_macro_mae_mol_kg"]
            d1_mae = d1["test"]["topology_macro_mae_mol_kg"]
            mode_results[mode] = {
                "status": "completed",
                "bundle": bundle,
                "rounds": round_records,
                "final_selection": final_generation["selected_descriptor_ids"],
                "prompt": {
                    "system_sha256": _canonical_hash(prompt_system),
                    "schema_version": DISCOVERY_SCHEMA_VERSION,
                    "row_level_data_included": False,
                    "row_level_labels_included": False,
                },
                "model": {
                    "provider": response.provider, "model": response.model, "requested_model": model,
                    "temperature": temperature, "max_tokens": max_tokens,
                    "thinking": thinking, "reasoning_effort": reasoning_effort,
                    "total_usage": {
                        "prompt_tokens": sum(r["model"]["usage"].get("prompt_tokens", 0) for r in round_records),
                        "completion_tokens": sum(r["model"]["usage"].get("completion_tokens", 0) for r in round_records),
                        "total_tokens": sum(r["model"]["usage"].get("total_tokens", 0) for r in round_records),
                    },
                },
                "downstream": {
                    "model": "sklearn.HistGradientBoostingRegressor",
                    "target_transform": "log1p",
                    "D0": baseline,
                    "D0_plus_X": d1,
                    "topology_macro_mae_relative_improvement": (d0_mae - d1_mae) / max(d0_mae, 1e-12),
                },
            }
        except Exception as error:  # noqa: BLE001
            mode_results[mode] = {"status": "failed", "error_type": type(error).__name__, "error": str(error)}
    finished = datetime.now(timezone.utc)
    result = {
        "schema_version": RUN_SCHEMA_VERSION,
        "validation_mode": VALIDATION_MODE,
        "catalog_blinding": {
            "enabled": True,
            "hidden_prompt_field": "scientific_rationale",
            "rationales_hidden_from_prompt": {
                key: item.rationale for key, item in catalog_full.items()
            },
        },
        "run_classification": "EXPLORATORY_BENCHMARK_V3",
        "protocol_status": "FROZEN_BEFORE_OUTCOME_RUN",
        "replicate_id": replicate_id,
        "rounds": rounds,
        "started_at": started.isoformat(), "finished_at": finished.isoformat(),
        "duration_seconds": (finished - started).total_seconds(),
        "task": task, "query": query,
        "warnings": [
            "Descriptor catalog rationales are blinded for every mode; the prompt shows only descriptor_id, formula and units, and retrieved evidence is the only channel explaining why a descriptor might matter.",
            "Only pre-adsorption framework fields, scalar GCMC targets, and precomputed pore-geometry descriptors are used; positions and cycle_stats remain forbidden features.",
            "Geometry descriptors are deterministic functions of the frozen framework coordinates (T-graph rings, coordination sequences, bond geometry, Al second shell).",
            "Iteration feedback uses validation topologies only; the test split is evaluated once after the final round.",
            "Task, query, model, budgets and split are identical to the v1 run; the catalog and the iterative loop are the only protocol changes.",
        ],
        "dataset": {
            **dataset.metadata,
            "database_sha256": database_sha256,
            "geometry_csv": str(geometry_csv),
            "geometry_sha256": geometry_sha256,
            "geometry_descriptor_columns": geometry_columns,
        },
        "retrieval": {
            "budget": budget.__dict__,
            "source_identities": service.source_identities,
            "evidence_strategy": "three_family_purified" if evidence_queries else "single_frozen_query",
            "evidence_queries": list(evidence_queries) if evidence_queries else [query],
        },
        "modes": mode_results,
        "environment": {"python": sys.version, "platform": platform.platform()},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output_path)
    return result
