"""AdsZeo v5: open-ended descriptor nomination with a restricted DSL executor.

Replaces the visible 42-item catalog with free-form nomination: the model
proposes descriptor formulas as single expressions over the allowed pre-
adsorption inputs. Every formula is parsed with a whitelisted AST walker
(no imports, attributes, indexing, comparisons), executed under guarded
numpy semantics, and quality-checked (non-finite, missingness, zero
variance, redundancy). Rejections are recorded in the pre-registered
failure taxonomy; executed proposals enter the same frozen D0 vs D0+X
HistGradientBoosting validation as v1-v4 (topology-level 80/10/10 split,
D0-tuned hyperparameters, test evaluated once after the final round).

Knowledge conditions remain budget-matched: agent receives no evidence,
rag_agent receives the single frozen query bundle, small_kg_rag_agent the
same via the KG-hybrid retriever.
"""

from __future__ import annotations

import ast
import hashlib
import json
import math
import platform
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

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
)
from catalysis_research.experiments.themecat_pilot import Descriptor
from catalysis_research.experiments.adszeo_v2 import (
    VALIDATION_MODE,
    _validation_mae,
    load_geometry,
)
from catalysis_research.models.glm import GlmClient, GlmResponse
from catalysis_research.retrieval import (
    EXPERIMENT_KNOWLEDGE_MODES,
    KnowledgeModeRetriever,
    RetrievalBudget,
)

RUN_SCHEMA_VERSION = "glm_scientific_discovery_adszeo_v5_open_nomination.v5"
RANDOM_STATE = 20260902
MAX_AST_DEPTH = 24
MISSINGNESS_LIMIT = 0.5
REDUNDANCY_LIMIT = 0.999

UNARY_FUNCTIONS = {
    "log": np.log, "log10": np.log10, "log2": np.log2, "exp": np.exp,
    "sqrt": np.sqrt, "abs": np.abs, "floor": np.floor, "ceil": np.ceil,
}
BINARY_FUNCTIONS = {
    "minimum": np.minimum, "maximum": np.maximum,
    "min": np.minimum, "max": np.maximum,
}
FUNCTION_WHITELIST = {**UNARY_FUNCTIONS, **BINARY_FUNCTIONS}
CONSTANT_WHITELIST = {"pi": math.pi, "e": math.e}


class DslError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def compile_formula(formula: str, allowed_inputs: set[str]) -> tuple[Callable[[dict[str, np.ndarray]], np.ndarray], set[str]]:
    """Parse and whitelist-check one formula; return an evaluator over env arrays."""
    if not isinstance(formula, str) or not formula.strip():
        raise DslError("schema_invalid", "formula is empty")
    try:
        tree = ast.parse(formula.strip(), mode="eval")
    except SyntaxError as exc:
        raise DslError("schema_invalid", f"not parseable: {exc.msg}") from exc

    used: set[str] = set()

    def visit(node: ast.AST, depth: int) -> None:
        if depth > MAX_AST_DEPTH:
            raise DslError("unsafe_expression", "expression nesting too deep")
        if isinstance(node, ast.Expression):
            visit(node.body, depth + 1)
        elif isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
        ):
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            visit(node.operand, depth + 1)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTION_WHITELIST:
                raise DslError("unsafe_expression", "function not in whitelist")
            if node.keywords:
                raise DslError("unsafe_expression", "keyword arguments not allowed")
            arity = 2 if node.func.id in BINARY_FUNCTIONS else 1
            if len(node.args) != arity:
                raise DslError("schema_invalid", f"{node.func.id} expects {arity} argument(s)")
            for argument in node.args:
                visit(argument, depth + 1)
        elif isinstance(node, ast.Name):
            if node.id in CONSTANT_WHITELIST:
                return
            if node.id in allowed_inputs:
                used.add(node.id)
                return
            raise DslError("unsupported_input", f"unknown name: {node.id}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return
        else:
            raise DslError("unsafe_expression", f"syntax element {type(node).__name__} not allowed")

    visit(tree, 0)

    def evaluate(env: dict[str, np.ndarray]) -> np.ndarray:
        return _eval_node(tree.body, env)

    return evaluate, used


def _eval_node(node: ast.AST, env: dict[str, np.ndarray]) -> np.ndarray:
    if isinstance(node, ast.Constant):
        return np.float64(node.value)
    if isinstance(node, ast.Name):
        if node.id in CONSTANT_WHITELIST:
            return np.float64(CONSTANT_WHITELIST[node.id])
        return np.asarray(env[node.id], dtype=float)
    if isinstance(node, ast.UnaryOp):
        value = _eval_node(node.operand, env)
        return -value if isinstance(node.op, ast.USub) else +value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env)
        right = _eval_node(node.right, env)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            if isinstance(node.op, ast.Mod):
                return np.mod(left, right)
            return left // right
    if isinstance(node, ast.Call):
        fn = FUNCTION_WHITELIST[node.func.id]
        arguments = [_eval_node(argument, env) for argument in node.args]
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            return fn(*arguments)
    raise DslError("unsafe_expression", "unexpected node during evaluation")


def _sanitize_name(raw: Any, index: int) -> str:
    if not isinstance(raw, str) or not raw.strip():
        return f"proposal_{index:02d}"
    slug = re.sub(r"[^a-z0-9_]+", "_", raw.strip().lower()).strip("_")
    return (slug or f"proposal_{index:02d}")[:40]


def _validate_nomination_output(
    value: Any,
    *,
    proposal_count: int,
    require_empty_evidence: bool,
    allowed_evidence_ids: set[str],
) -> tuple[dict[str, Any], list[str]]:
    repairs: list[str] = []
    if not isinstance(value, dict):
        raise ValueError("nomination output must be a JSON object")
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
            if evidence_id is not None and evidence_id not in allowed_evidence_ids:
                repairs.append(f"evidence_chain cited unavailable ID {evidence_id}; entry dropped")
                continue
            if not claim.strip():
                continue
            evidence_chain.append({"evidence_id": evidence_id, "role": role, "claim": claim.strip()})

    raw_candidates = value.get("descriptor_candidates") or value.get("proposals")
    candidates: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    if isinstance(raw_candidates, list):
        for index, cand in enumerate(raw_candidates):
            if not isinstance(cand, dict):
                continue
            name = _sanitize_name(cand.get("name"), index)
            if name in seen_names:
                repairs.append(f"duplicate proposal name {name}; dropped")
                continue
            formula = cand.get("formula")
            if not isinstance(formula, str) or not formula.strip():
                repairs.append(f"proposal {name} missing formula; dropped")
                continue
            seen_names.add(name)
            record = {"name": name, "formula": formula.strip()}
            for field in ("rationale", "expected_direction", "falsification_criteria"):
                text = cand.get(field)
                if not isinstance(text, str) or not text.strip():
                    repairs.append(f"proposal {name} missing {field}; filled with 'unspecified'")
                    text = "unspecified"
                record[field] = text.strip()
            candidates.append(record)
            if len(candidates) >= proposal_count:
                break
    if len(raw_candidates if isinstance(raw_candidates, list) else []) > proposal_count:
        repairs.append(f"more than {proposal_count} proposals; truncated")
    if not candidates:
        raise ValueError("no usable proposals after repair (unrecoverable)")
    if len(candidates) < proposal_count:
        repairs.append(f"only {len(candidates)}/{proposal_count} proposals supplied")

    epistemic = value.get("epistemic_status")
    if epistemic not in {"supported", "tentative", "insufficient_evidence"}:
        repairs.append(f"epistemic_status {epistemic!r} invalid; coerced to 'tentative'")
        epistemic = "tentative"

    return {
        "evidence_chain": evidence_chain,
        "hypothesis": hypothesis,
        "descriptor_candidates": candidates,
        "epistemic_status": epistemic,
    }, repairs


def _pipeline(parameters: dict[str, float | int]) -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
            ("regressor", HistGradientBoostingRegressor(max_iter=250, random_state=RANDOM_STATE, **parameters)),
        ]
    )


def _feature_matrix(rows: list[dict[str, Any]], ids: Iterable[str], catalog: dict[str, Any]) -> np.ndarray:
    return np.asarray([[catalog[item].compute(row) for item in ids] for row in rows], dtype=float)


def _topology_macro_mae(rows: list[dict[str, Any]], prediction: np.ndarray) -> float:
    errors: dict[str, list[float]] = {}
    for row, predicted in zip(rows, prediction):
        errors.setdefault(str(row["framework_code"]), []).append(float(row[TARGET_COLUMN]) - float(predicted))
    return float(np.mean([np.mean(np.abs(values)) for values in errors.values()]))


def _validation_mae(
    rows: list[dict[str, Any]],
    descriptor_ids: tuple[str, ...],
    catalog: dict[str, Any],
    parameters: dict[str, float | int],
) -> float:
    train = [row for row in rows if row["split"] == "train"]
    validation = [row for row in rows if row["split"] == "validation"]
    model = _pipeline(parameters)
    model.fit(
        _feature_matrix(train, descriptor_ids, catalog),
        np.log1p([float(row[TARGET_COLUMN]) for row in train]),
    )
    prediction = np.maximum(np.expm1(model.predict(_feature_matrix(validation, descriptor_ids, catalog))), 0.0)
    return _topology_macro_mae(validation, prediction)


def build_nomination_prompt(
    *,
    task: str,
    query: str,
    knowledge_mode: str,
    evidence_context: str,
    allowed_inputs: list[str],
    proposal_count: int,
) -> tuple[str, str]:
    system = (
        "You are an evidence-grounded scientific hypothesis agent. Return one "
        "valid JSON object only. Separate literature evidence from your own "
        "hypothesis. Never invent a citation, quote, page, formula, or measured "
        "result. If evidence is absent or insufficient, say so explicitly."
    )
    payload = {
        "schema_version": "descriptor_nomination.v1",
        "run_classification": "exploratory_not_confirmatory",
        "task": task,
        "retrieval_query": query,
        "knowledge_mode": knowledge_mode,
        "benchmark": {
            "name": "AdsZeo v1",
            "target": "298 K methane absolute loading (mol/kg framework)",
            "role": "primary zeolite scientific-descriptor benchmark",
            "label_visibility": "no row-level labels or test outcomes",
        },
        "baseline_descriptor_ids_D0": list(D0_DESCRIPTOR_IDS),
        "allowed_inputs": allowed_inputs,
        "formula_contract": {
            "grammar": "one arithmetic expression over allowed_inputs; no renames of D0 inputs",
            "binary_operators": ["+", "-", "*", "/", "**", "%"],
            "unary_functions": sorted(UNARY_FUNCTIONS),
            "binary_functions": sorted(BINARY_FUNCTIONS),
            "constants": sorted(CONSTANT_WHITELIST),
            "forbidden": "imports, attributes, indexing, comparisons, booleans, any name outside allowed_inputs",
            "practical_notes": [
                "guard divisions: denominators may be zero or tiny",
                "a proposal whose values are constant or a near-duplicate of D0 will be rejected",
                "propose physically meaningful combinations, not bare inputs",
            ],
        },
        "descriptor_nomination": {
            "budget": proposal_count,
            "each_proposal": ["name (snake_case)", "formula", "rationale", "expected_direction", "falsification_criteria"],
        },
        "evidence_context": evidence_context or "[NO_EXTERNAL_EVIDENCE]",
        "output_schema": {
            "evidence_chain": [{"evidence_id": "E01 or null", "role": "supporting|contradicting|context|none", "claim": "what the evidence says, without extrapolation"}],
            "hypothesis": "one falsifiable scientific hypothesis",
            "descriptor_candidates": [
                {"name": "snake_case", "formula": "single expression", "rationale": "mechanism", "expected_direction": "positive|negative|nonlinear|unknown", "falsification_criteria": "what result would reject it"}
            ],
            "epistemic_status": "supported|tentative|insufficient_evidence",
        },
        "instructions": [
            "Use only allowed_inputs inside formulas; only whitelisted functions and operators.",
            "Return exactly the proposal budget; each formula must define a new quantity, not rename a D0 input.",
            "Do not use target values, outcome columns, or any row-level data.",
            "For agent mode, evidence_chain must be empty and epistemic_status should be insufficient_evidence or tentative.",
        ],
    }
    return system, json.dumps(payload, ensure_ascii=False, sort_keys=True)


def run_adszeo_nomination_loop(
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
    reasoning_effort: str | None = "low",
    replicate_id: int | None = None,
    modes: Iterable[str] = EXPERIMENT_KNOWLEDGE_MODES,
    proposal_count: int = 3,
    rounds: int = 3,
    database_sha256: str | None = None,
    client: GlmClient | None = None,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    dataset = load_adszeo(database_path)
    geometry_columns, geometry_map = load_geometry(geometry_csv)
    for row in dataset.rows:
        row.update(geometry_map[row["structure_id"]])
    allowed_inputs = sorted(
        {key for row in dataset.rows for key in row}
        - {TARGET_COLUMN, "run_id", "structure_id", "framework_code", "split"}
    )
    env = {key: np.array([float(row.get(key, float("nan"))) for row in dataset.rows]) for key in allowed_inputs}
    geometry_sha256 = hashlib.sha256(Path(geometry_csv).read_bytes()).hexdigest()

    baseline = evaluate_adszeo(dataset, D0_DESCRIPTOR_IDS, adszeo_descriptor_catalog())
    parameters = baseline["selected_parameters"]
    d0_validation_mae = baseline["validation_topology_macro_mae_mol_kg"]
    d0_catalog = {key: item for key, item in adszeo_descriptor_catalog().items() if key in D0_DESCRIPTOR_IDS}
    d0_values = {
        key: np.array([float(item.compute(row)) for row in dataset.rows])
        for key, item in d0_catalog.items()
    }

    prompt_system, _ = build_nomination_prompt(
        task=task, query=query, knowledge_mode="agent", evidence_context="",
        allowed_inputs=allowed_inputs, proposal_count=proposal_count,
    )
    api_client = client or GlmClient()
    mode_results: dict[str, Any] = {}
    for mode in modes:
        try:
            bundle = service.retrieve(query=query, experiment_mode=mode, budget=budget)
            evidence_context = _label_evidence_context(bundle)
            history: list[dict[str, Any]] = []
            round_records: list[dict[str, Any]] = []
            accepted: dict[str, dict[str, Any]] = {}
            final_executed: list[str] = []
            response: GlmResponse | None = None
            for round_index in range(1, rounds + 1):
                system, user = build_nomination_prompt(
                    task=task, query=query, knowledge_mode=mode, evidence_context=evidence_context,
                    allowed_inputs=allowed_inputs, proposal_count=proposal_count,
                )
                if history:
                    payload = json.loads(user)
                    payload["previous_rounds"] = history
                    payload["revision_instructions"] = [
                        "This is a revision round. You may keep or replace any previously proposed descriptor.",
                        "Failed proposals report a failure_code; fix the formula (guard divisions, use allowed functions) or propose different quantities.",
                        "Executed proposals report their individual validation delta; prefer keeping those with positive benefit.",
                        "The validation feedback comes from held-out topologies; it never includes test outcomes.",
                    ]
                    user = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                response = api_client.chat_json(
                    model=model, system=system, user=user, temperature=temperature,
                    max_tokens=max_tokens, thinking=thinking, reasoning_effort=reasoning_effort,
                )
                usage = dict(response.usage or {})
                try:
                    generation, repairs = _validate_nomination_output(
                        response.structured, proposal_count=proposal_count,
                        require_empty_evidence=mode == "agent",
                        allowed_evidence_ids={f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)},
                    )
                except ValueError as first_error:
                    repair_payload = {
                        "schema_repair": {
                            "previous_output_rejected": str(first_error),
                            "previous_output": response.structured,
                            "instructions": "Return the same JSON object with the reported problem corrected. Keep the same hypothesis and proposals; fix only the format.",
                        }
                    }
                    response = api_client.chat_json(
                        model=model, system=system, user=json.dumps(repair_payload, ensure_ascii=False, sort_keys=True),
                        temperature=temperature, max_tokens=max_tokens, thinking=thinking, reasoning_effort=reasoning_effort,
                    )
                    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
                        usage[key] = usage.get(key, 0) + (response.usage or {}).get(key, 0)
                    generation, repairs = _validate_nomination_output(
                        response.structured, proposal_count=proposal_count,
                        require_empty_evidence=mode == "agent",
                        allowed_evidence_ids={f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)},
                    )
                    repairs.append("schema repair retry used")

                # execute proposals
                proposals_feedback = []
                round_executed: list[str] = []
                for proposal in generation["descriptor_candidates"]:
                    name = proposal["name"]
                    exec_id = f"nom_{name}"
                    entry: dict[str, Any] = {"name": name, "formula": proposal["formula"]}
                    try:
                        fn, _used = compile_formula(proposal["formula"], set(allowed_inputs))
                        values = np.asarray(fn(env), dtype=float)
                        values[~np.isfinite(values)] = np.nan
                        nan_fraction = float(np.mean(np.isnan(values)))
                        if nan_fraction >= 1.0:
                            raise DslError("non_finite", "all values non-finite")
                        if nan_fraction > MISSINGNESS_LIMIT:
                            raise DslError("missingness_exceeded", f"{nan_fraction:.0%} non-finite values")
                        if float(np.nanstd(values)) == 0.0:
                            raise DslError("zero_variance", "constant over all rows")
                        redundant_with = None
                        for ref_id, ref_values in (
                            list(d0_values.items())
                            + [(f"nom_{key}", item["values"]) for key, item in accepted.items()]
                        ):
                            mask = np.isfinite(values) & np.isfinite(ref_values)
                            if mask.sum() > 10 and float(np.nanstd(ref_values[mask])) > 0:
                                correlation = float(np.corrcoef(values[mask], ref_values[mask])[0, 1])
                                if abs(correlation) >= REDUNDANCY_LIMIT:
                                    redundant_with = ref_id
                                    break
                        if redundant_with is not None:
                            raise DslError("redundant", f"|corr|>={REDUNDANCY_LIMIT} with {redundant_with}")
                    except DslError as error:
                        entry.update({"status": "failed", "failure_code": error.code, "detail": str(error)})
                        proposals_feedback.append(entry)
                        continue
                    except Exception as exc:  # noqa: BLE001
                        entry.update({"status": "failed", "failure_code": "execution_error", "detail": str(exc)[:200]})
                        proposals_feedback.append(entry)
                        continue
                    for row, value in zip(dataset.rows, values):
                        row[exec_id] = float(value) if math.isfinite(float(value)) else float("nan")
                    accepted[exec_id] = {
                        "values": values,
                        "descriptor": Descriptor(
                            exec_id, proposal["formula"], "derived", proposal["rationale"],
                            lambda row, key=exec_id: float(row.get(key, float("nan"))),
                        ),
                        "name": name,
                    }
                    round_executed.append(exec_id)
                    entry.update({"status": "executed", "exec_id": exec_id})
                    proposals_feedback.append(entry)

                if round_executed:
                    catalog_now = {**d0_catalog, **{key: item["descriptor"] for key, item in accepted.items()}}
                    for entry in proposals_feedback:
                        if entry.get("status") == "executed":
                            entry["validation_delta_macro_mae"] = float(
                                _validation_mae(dataset.rows, (*D0_DESCRIPTOR_IDS, entry["exec_id"]), catalog_now, parameters)
                                - d0_validation_mae
                            )
                    set_delta = float(
                        _validation_mae(dataset.rows, (*D0_DESCRIPTOR_IDS, *round_executed), catalog_now, parameters)
                        - d0_validation_mae
                    )
                if round_executed:
                    final_executed = list(round_executed)
                history.append({
                    "round": round_index,
                    "hypothesis": generation["hypothesis"],
                    "proposals": generation["descriptor_candidates"],
                    "execution_feedback": proposals_feedback,
                    "validation_set_delta_macro_mae": set_delta,
                })
                round_records.append({
                    "round": round_index,
                    "generation": generation,
                    "validation_repairs": repairs,
                    "execution_feedback": proposals_feedback,
                    "validation_set_delta_macro_mae": set_delta,
                    "prompt": {"system_sha256": _canonical_hash(system), "user_sha256": _canonical_hash(user)},
                    "model": {"usage": usage, "response_id": response.raw.get("id")},
                })

            downstream = None
            improvement = None
            if final_executed:
                catalog_final = {**d0_catalog, **{key: item["descriptor"] for key, item in accepted.items()}}
                d1 = evaluate_adszeo(
                    dataset, (*D0_DESCRIPTOR_IDS, *final_executed), catalog_final, fixed_parameters=parameters,
                )
                d0_mae = baseline["test"]["topology_macro_mae_mol_kg"]
                d1_mae = d1["test"]["topology_macro_mae_mol_kg"]
                improvement = (d0_mae - d1_mae) / max(d0_mae, 1e-12)
                downstream = {
                    "model": "sklearn.HistGradientBoostingRegressor",
                    "target_transform": "log1p",
                    "D0": baseline,
                    "D0_plus_X": d1,
                    "topology_macro_mae_relative_improvement": improvement,
                    "final_executed_descriptor_ids": final_executed,
                }
            taxonomy_counts = Counter(
                entry.get("failure_code")
                for record in round_records
                for entry in record["execution_feedback"]
                if entry.get("status") == "failed"
            )
            mode_results[mode] = {
                "status": "completed",
                "bundle": bundle,
                "rounds": round_records,
                "final_executed_descriptor_ids": final_executed,
                "accepted_catalog": {key: {"name": item["name"], "formula": item["descriptor"].formula} for key, item in accepted.items()},
                "failure_taxonomy_counts": dict(taxonomy_counts),
                "prompt": {
                    "system_sha256": _canonical_hash(prompt_system),
                    "schema_version": DISCOVERY_SCHEMA_VERSION,
                    "row_level_data_included": False,
                    "row_level_labels_included": False,
                },
                "model": {
                    "provider": response.provider if response else None,
                    "model": response.model if response else model,
                    "requested_model": model,
                    "temperature": temperature, "max_tokens": max_tokens,
                    "thinking": thinking, "reasoning_effort": reasoning_effort,
                    "total_usage": {
                        "prompt_tokens": sum(r["model"]["usage"].get("prompt_tokens", 0) for r in round_records),
                        "completion_tokens": sum(r["model"]["usage"].get("completion_tokens", 0) for r in round_records),
                        "total_tokens": sum(r["model"]["usage"].get("total_tokens", 0) for r in round_records),
                    },
                },
                "downstream": downstream,
                "topology_macro_mae_relative_improvement": improvement,
            }
        except Exception as error:  # noqa: BLE001
            mode_results[mode] = {"status": "failed", "error_type": type(error).__name__, "error": str(error)}
    finished = datetime.now(timezone.utc)
    result = {
        "schema_version": RUN_SCHEMA_VERSION,
        "validation_mode": VALIDATION_MODE,
        "catalog_blinding": {"enabled": True, "note": "no catalog is shown; descriptors are freely nominated"},
        "run_classification": "EXPLORATORY_BENCHMARK_V5",
        "protocol_status": "FROZEN_BEFORE_OUTCOME_RUN",
        "replicate_id": replicate_id,
        "rounds": rounds,
        "proposal_count": proposal_count,
        "started_at": started.isoformat(), "finished_at": finished.isoformat(),
        "duration_seconds": (finished - started).total_seconds(),
        "task": task, "query": query,
        "warnings": [
            "Descriptors are freely nominated as DSL expressions over pre-adsorption inputs; a whitelisted AST executor rejects unsafe, non-computable, degenerate, or redundant proposals with recorded failure codes.",
            "positions and cycle_stats remain forbidden features; geometry columns are the same frozen precomputed descriptors as v2-v4.",
            "Iteration feedback uses validation topologies only; the test split is evaluated once after the final round.",
            "Executability rate, failure taxonomy, and novelty are now first-class outcome measures alongside topology macro-MAE.",
        ],
        "dataset": {
            **dataset.metadata,
            "database_sha256": database_sha256,
            "geometry_csv": str(geometry_csv),
            "geometry_sha256": geometry_sha256,
        },
        "retrieval": {"budget": budget.__dict__, "source_identities": service.source_identities, "evidence_strategy": "single_frozen_query"},
        "modes": mode_results,
        "environment": {"python": sys.version, "platform": platform.platform()},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output_path)
    return result
