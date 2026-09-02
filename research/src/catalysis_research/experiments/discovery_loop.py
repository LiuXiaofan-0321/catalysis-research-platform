"""Exploratory evidence -> hypothesis -> descriptor -> ML loop.

This module keeps the three knowledge conditions matched. The model sees the
same task, catalog, output schema, temperature and token ceiling; only the
retrieved evidence bundle differs. It is intentionally exploratory until a
public benchmark, native baseline and split are formally frozen.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from catalysis_research.datasets.themecat import (
    TARGET_COLUMN,
    load_themecat,
)
from catalysis_research.models.glm import GlmClient, GlmResponse
from catalysis_research.retrieval import (
    EXPERIMENT_KNOWLEDGE_MODES,
    KnowledgeModeRetriever,
    RetrievalBudget,
)
from catalysis_research.experiments.themecat_pilot import (
    ALPHA_GRID,
    Descriptor,
    descriptor_catalog,
    evaluate_descriptor_set,
)


DISCOVERY_SCHEMA_VERSION = "scientific_discovery_output.v1"
RUN_SCHEMA_VERSION = "glm_scientific_discovery_themecat_exploratory.v1"
DEFAULT_MODEL = "glm-5.3-flash"
DEFAULT_SELECTED_DESCRIPTOR_COUNT = 3

# These six variables are the fixed, directly reported operating descriptors
# used as D0 for the TheMeCat exploratory sanity check.
D0_DESCRIPTOR_IDS = (
    "temperature_k",
    "pressure_bar",
    "h2_co2_ratio",
    "ghsv",
    "catalyst_load",
    "active_percent",
)


def _canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_discovery_prompt(
    *,
    task: str,
    query: str,
    knowledge_mode: str,
    evidence_context: str,
    catalog: dict[str, Descriptor],
    selected_descriptor_count: int = DEFAULT_SELECTED_DESCRIPTOR_COUNT,
) -> tuple[str, str]:
    system = (
        "You are an evidence-grounded scientific hypothesis agent. Return one "
        "valid JSON object only. Separate literature evidence from your own "
        "hypothesis. Never invent a citation, quote, page, formula, or measured "
        "result. If evidence is absent or insufficient, say so explicitly."
    )
    catalog_records = [item.prompt_record() for item in catalog.values()]
    user_payload = {
        "schema_version": DISCOVERY_SCHEMA_VERSION,
        "run_classification": "exploratory_not_confirmatory",
        "task": task,
        "retrieval_query": query,
        "knowledge_mode": knowledge_mode,
        "benchmark": {
            "name": "TheMeCat v1",
            "target": TARGET_COLUMN,
            "role": "secondary mechanism-transfer sanity check; not the final NMI benchmark",
            "label_visibility": "no row-level labels or test outcomes",
        },
        "allowed_inputs": [
            "active_comp_1",
            "active_1_percent",
            "support_comp_1",
            "temperature_k",
            "pressure_bar",
            "pH2_pCO2_ratio",
            "GHSV_nlph_gcat",
            "catalyst_load_g",
        ],
        "baseline_descriptor_ids_D0": list(D0_DESCRIPTOR_IDS),
        "descriptor_catalog": catalog_records,
        "descriptor_selection": {
            "candidate_budget": selected_descriptor_count,
            "selected_budget": selected_descriptor_count,
            "must_be_computable_from_allowed_inputs": True,
            "must_not_be_in_D0": True,
        },
        "evidence_context": evidence_context or "[NO_EXTERNAL_EVIDENCE]",
        "output_schema": {
            "evidence_chain": [
                {
                    "evidence_id": "E01 or null",
                    "role": "supporting|contradicting|context|none",
                    "claim": "what the evidence says, without extrapolation",
                }
            ],
            "hypothesis": "one falsifiable scientific hypothesis",
            "descriptor_candidates": [
                {
                    "descriptor_id": "catalog ID",
                    "rationale": "why it operationalizes the hypothesis",
                    "expected_direction": "positive|negative|nonlinear|unknown",
                    "falsification_criteria": "what result would reject it",
                }
            ],
            "selected_descriptor_ids": "exactly the selected budget IDs in candidate order",
            "expected_direction": "overall expected relationship",
            "falsification_criteria": ["testable rejection criteria"],
            "epistemic_status": "supported|tentative|insufficient_evidence",
        },
        "instructions": [
            "Use only descriptor IDs and formulas present in the catalog.",
            "Return exactly the selected budget descriptor candidates and select all of them in order.",
            "Do not use target values, outcome columns, or any row-level data.",
            "For agent mode, evidence_chain must be empty and epistemic_status should be insufficient_evidence or tentative.",
        ],
    }
    return system, json.dumps(user_payload, ensure_ascii=False, sort_keys=True)


def _label_evidence_context(bundle: dict[str, Any]) -> str:
    """Add stable aliases so the model can cite only retrieved bundle items."""
    context = str(bundle.get("context") or "")
    items = bundle.get("items") or []
    if not context or not items:
        return "[NO_EXTERNAL_EVIDENCE]"
    segments = context.split("\n\n")
    if len(segments) != len(items):
        # The bundle remains authoritative; this fallback still gives the model
        # an explicit finite citation vocabulary without changing source text.
        return "\n\n".join(
            f"E{index:02d}: {context}" for index in range(1, len(items) + 1)
        )
    return "\n\n".join(
        f"E{index:02d}: {segment}" for index, segment in enumerate(segments, 1)
    )


def validate_discovery_output(
    value: dict[str, Any],
    catalog: dict[str, Descriptor],
    *,
    selected_descriptor_count: int = DEFAULT_SELECTED_DESCRIPTOR_COUNT,
    allowed_evidence_ids: set[str] | None = None,
    require_empty_evidence: bool = False,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Discovery output must be an object")
    hypothesis = value.get("hypothesis")
    if not isinstance(hypothesis, str) or not hypothesis.strip():
        raise ValueError("Discovery output is missing hypothesis")
    evidence_chain = value.get("evidence_chain")
    if not isinstance(evidence_chain, list):
        raise ValueError("Discovery output evidence_chain must be a list")
    for record in evidence_chain:
        if not isinstance(record, dict):
            raise ValueError("Each evidence_chain entry must be an object")
        evidence_id = record.get("evidence_id")
        if evidence_id is not None:
            if not isinstance(evidence_id, str) or evidence_id not in (allowed_evidence_ids or set()):
                raise ValueError("evidence_chain cites an unavailable evidence ID")
        if require_empty_evidence:
            raise ValueError("agent mode must not cite external evidence")
        for field in ("role", "claim"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f"Evidence-chain entry is missing {field}")
    candidates = value.get("descriptor_candidates")
    selected = value.get("selected_descriptor_ids")
    if not isinstance(candidates, list) or len(candidates) != selected_descriptor_count:
        raise ValueError("Discovery output has the wrong descriptor candidate count")
    if not isinstance(selected, list) or len(selected) != selected_descriptor_count:
        raise ValueError("Discovery output has the wrong selected descriptor count")
    candidate_ids: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("Each descriptor candidate must be an object")
        descriptor_id = candidate.get("descriptor_id")
        if not isinstance(descriptor_id, str) or descriptor_id not in catalog:
            raise ValueError("Descriptor candidate is not in the frozen catalog")
        if descriptor_id in D0_DESCRIPTOR_IDS:
            raise ValueError("A D0 descriptor cannot be selected as new X")
        candidate_ids.append(descriptor_id)
        for field in ("rationale", "expected_direction", "falsification_criteria"):
            if not isinstance(candidate.get(field), str) or not candidate[field].strip():
                raise ValueError(f"Descriptor candidate is missing {field}")
    if len(set(candidate_ids)) != selected_descriptor_count:
        raise ValueError("Descriptor candidates must be unique")
    if selected != candidate_ids:
        raise ValueError("selected_descriptor_ids must match candidate order")
    if value.get("epistemic_status") not in {"supported", "tentative", "insufficient_evidence"}:
        raise ValueError("Invalid epistemic_status")
    direction = value.get("expected_direction")
    if not isinstance(direction, str) or not direction.strip():
        raise ValueError("Discovery output is missing expected_direction")
    criteria = value.get("falsification_criteria")
    if not isinstance(criteria, list) or not criteria or not all(isinstance(item, str) and item.strip() for item in criteria):
        raise ValueError("Discovery output needs falsification_criteria")
    return {
        "evidence_chain": evidence_chain,
        "hypothesis": hypothesis.strip(),
        "descriptor_candidates": candidates,
        "selected_descriptor_ids": candidate_ids,
        "expected_direction": direction.strip(),
        "falsification_criteria": criteria,
        "epistemic_status": value["epistemic_status"],
    }


def _error_result(error: Exception) -> dict[str, Any]:
    return {"status": "failed", "error_type": type(error).__name__, "error": str(error)}


def run_discovery_loop(
    *,
    service: KnowledgeModeRetriever,
    raw_path: Path,
    output_path: Path,
    task: str,
    query: str,
    budget: RetrievalBudget,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4500,
    thinking: str = "disabled",
    modes: Iterable[str] = EXPERIMENT_KNOWLEDGE_MODES,
    selected_descriptor_count: int = DEFAULT_SELECTED_DESCRIPTOR_COUNT,
    client: GlmClient | None = None,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    rows = load_themecat(raw_path)
    catalog = descriptor_catalog()
    prompt_system, _ = build_discovery_prompt(
        task=task,
        query=query,
        knowledge_mode="agent",
        evidence_context="",
        catalog=catalog,
        selected_descriptor_count=selected_descriptor_count,
    )
    api_client = client or GlmClient()
    mode_results: dict[str, Any] = {}
    for mode in modes:
        if mode not in EXPERIMENT_KNOWLEDGE_MODES:
            mode_results[mode] = _error_result(ValueError(f"Unsupported mode: {mode}"))
            continue
        try:
            bundle = service.retrieve(query=query, experiment_mode=mode, budget=budget)
            evidence_context = _label_evidence_context(bundle)
            system, user = build_discovery_prompt(
                task=task,
                query=query,
                knowledge_mode=mode,
                evidence_context=evidence_context,
                catalog=catalog,
                selected_descriptor_count=selected_descriptor_count,
            )
            response: GlmResponse = api_client.chat_json(
                model=model,
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
                thinking=thinking,
            )
            validated = validate_discovery_output(
                response.structured,
                catalog,
                selected_descriptor_count=selected_descriptor_count,
                allowed_evidence_ids={
                    f"E{index:02d}" for index in range(1, len(bundle.get("items") or []) + 1)
                },
                require_empty_evidence=mode == "agent",
            )
            d0 = evaluate_descriptor_set(rows, D0_DESCRIPTOR_IDS, catalog)
            d0_plus_x = evaluate_descriptor_set(
                rows,
                (*D0_DESCRIPTOR_IDS, *validated["selected_descriptor_ids"]),
                catalog,
            )
            mode_results[mode] = {
                "status": "completed",
                "bundle": bundle,
                "prompt": {
                    "system_sha256": _canonical_hash(system),
                    "user_sha256": _canonical_hash(user),
                    "row_level_data_included": False,
                    "row_level_labels_included": False,
                },
                "model": {
                    "provider": response.provider,
                    "model": response.model,
                    "requested_model": model,
                    "usage": response.usage,
                    "response_id": response.raw.get("id"),
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "thinking": thinking,
                },
                    "generation": validated,
                "downstream": {
                    "model": "sklearn.linear_model.Ridge",
                    "alpha_grid": list(ALPHA_GRID),
                    "baseline_descriptor_ids_D0": list(D0_DESCRIPTOR_IDS),
                    "selected_descriptor_ids_X": list(validated["selected_descriptor_ids"]),
                    "D0": d0,
                    "D0_plus_X": d0_plus_x,
                    "exploratory_normalized_rmse_improvement": (
                        d0["macro_test_rmse"] - d0_plus_x["macro_test_rmse"]
                    )
                    / d0["macro_test_rmse"],
                },
            }
        except Exception as error:  # retain failed conditions in the comparison artifact
            mode_results[mode] = _error_result(error)
    finished = datetime.now(timezone.utc)
    result = {
        "schema_version": RUN_SCHEMA_VERSION,
        "run_classification": "EXPLORATORY_NOT_CONFIRMATORY",
        "protocol_status": "ACTIVATION_BLOCKED",
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "duration_seconds": (finished - started).total_seconds(),
        "task": task,
        "query": query,
        "warnings": [
            "TheMeCat is a secondary mechanism-transfer sanity check and is not the final NMI benchmark.",
            "Small-KG evidence is zeolite-focused while TheMeCat targets CO2 hydrogenation; domain transfer is not a scientific conclusion.",
            "No row-level labels or locked-test outcomes were exposed to GLM descriptor generation.",
            "The downstream Ridge result is exploratory and not a confirmatory claim.",
        ],
        "dataset": {
            "name": "TheMeCat v1",
            "raw_sha256": _sha256_file(raw_path),
            "adapted_row_count": len(rows),
            "target": TARGET_COLUMN,
        },
        "retrieval": {
            "budget": budget.__dict__,
            "source_identities": service.source_identities,
        },
        "prompt": {
            "system_sha256": _canonical_hash(prompt_system),
            "schema_version": DISCOVERY_SCHEMA_VERSION,
            "selected_descriptor_count": selected_descriptor_count,
        },
        "modes": mode_results,
        "environment": {"python": sys.version, "platform": platform.platform()},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output_path)
    return result
