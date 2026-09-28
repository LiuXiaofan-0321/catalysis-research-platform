from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Protocol

from .types import JevDecision


JEV_REQUEST_SCHEMA_VERSION = "jev_harness_request.v1"
JEV_DECISION_SCHEMA_VERSION = "jev_harness_decision.v1"


class JevError(RuntimeError):
    pass


class JevJudge(Protocol):
    def judge(self, request: dict[str, Any]) -> JevDecision:
        ...


_LOCKED_TEST_KEYS = {"test", "test_labels", "target_values", "row_level_labels", "locked_test"}


def _strip_locked_test(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_locked_test(item)
            for key, item in value.items()
            if key not in _LOCKED_TEST_KEYS and not key.startswith("test_")
        }
    if isinstance(value, list):
        return [_strip_locked_test(item) for item in value]
    return value


def build_jev_request(
    *,
    candidate: dict[str, Any],
    role_outputs: dict[str, dict[str, Any]],
    prior_candidates: list[dict[str, Any]],
    round_id: int,
    run_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    allowed_evidence_ids = set((run_context or {}).get("allowed_evidence_ids") or [])
    if allowed_evidence_ids:
        cited = {
            str(item.get("evidence_id"))
            for item in candidate.get("evidence", [])
            if isinstance(item, dict) and item.get("evidence_id") is not None
        }
        unknown = sorted(cited - allowed_evidence_ids)
        if unknown:
            raise JevError(f"candidate cites unavailable evidence IDs: {unknown}")
    return {
        "schema_version": JEV_REQUEST_SCHEMA_VERSION,
        "round_id": round_id,
        "candidate": _strip_locked_test(candidate),
        "role_outputs": _strip_locked_test(role_outputs),
        "prior_candidates": [
            {key: item.get(key) for key in ("candidate_id", "formula", "statement")}
            for item in prior_candidates
        ],
        "run_context": _strip_locked_test(run_context or {}),
        "decision_contract": {
            "evidence_verdict": ["supports", "contradicts", "insufficient", "not_applicable"],
            "novelty_verdict": ["novel", "duplicate", "uncertain"],
            "recommendation": ["compute_validate", "retrieve_more", "revise", "defer", "abandon"],
            "failure_disposition": ["revise", "defer", "abandon", "none"],
            "must_not_claim": [
                "A hypothesis is scientifically confirmed from literature support alone.",
                "A numerical validation result exists when execution.status is not executed.",
            ],
        },
    }


def validate_jev_decision(value: JevDecision | dict[str, Any], *, request: dict[str, Any] | None = None) -> JevDecision:
    if isinstance(value, JevDecision):
        return value
    if not isinstance(value, dict):
        raise JevError("Jev decision must be an object")
    try:
        decision = JevDecision(
            evidence_verdict=value["evidence_verdict"],
            evidence_confidence=float(value["evidence_confidence"]),
            novelty_verdict=value["novelty_verdict"],
            novelty_confidence=float(value["novelty_confidence"]),
            recommendation=value["recommendation"],
            rationale=str(value["rationale"]),
            missing_evidence=[str(item) for item in value.get("missing_evidence", [])],
            duplicate_candidate_ids=[str(item) for item in value.get("duplicate_candidate_ids", [])],
            retrieval_query=value.get("retrieval_query"),
            failure_disposition=value.get("failure_disposition", "none"),
        )
        if request is not None:
            prior_ids = {
                str(item.get("candidate_id"))
                for item in request.get("prior_candidates", [])
                if item.get("candidate_id")
            }
            unknown_duplicates = set(decision.duplicate_candidate_ids) - prior_ids
            if unknown_duplicates:
                raise JevError(f"Jev cited unknown duplicate candidates: {sorted(unknown_duplicates)}")
            if decision.retrieval_query and len(decision.retrieval_query.strip()) > 1200:
                raise JevError("Jev retrieval_query exceeds 1200 characters")
        return decision
    except (KeyError, TypeError, ValueError) as error:
        raise JevError(f"invalid Jev decision: {error}") from error


class RuleBasedJev:
    """Deterministic baseline and offline test oracle for the Jev interface."""

    def judge(self, request: dict[str, Any]) -> JevDecision:
        roles = request.get("role_outputs") or {}
        evidence = roles.get("evidence_critic") or {}
        novelty = roles.get("novelty_auditor") or {}
        feasibility = roles.get("feasibility_auditor") or {}
        validation = roles.get("validation_planner") or {}
        if novelty.get("verdict") == "duplicate":
            return JevDecision(
                evidence_verdict=evidence.get("verdict", "insufficient"),
                evidence_confidence=float(evidence.get("confidence", 0.0)),
                novelty_verdict="duplicate", novelty_confidence=1.0,
                recommendation="abandon", rationale="Candidate duplicates a prior formula.",
                duplicate_candidate_ids=list(novelty.get("duplicate_candidate_ids") or []),
                failure_disposition="abandon",
            )
        if feasibility.get("verdict") in {"infeasible", "degenerate"}:
            disposition = "revise" if feasibility.get("verdict") == "infeasible" else "abandon"
            return JevDecision(
                evidence_verdict=evidence.get("verdict", "insufficient"),
                evidence_confidence=float(evidence.get("confidence", 0.0)),
                novelty_verdict=novelty.get("verdict", "uncertain"),
                novelty_confidence=float(novelty.get("confidence", 0.0)),
                recommendation=disposition, rationale="Programmatic feasibility checks rejected the candidate.",
                failure_disposition=disposition,
            )
        if evidence.get("verdict") == "contradicts":
            return JevDecision(
                evidence_verdict="contradicts", evidence_confidence=float(evidence.get("confidence", 0.0)),
                novelty_verdict=novelty.get("verdict", "uncertain"), novelty_confidence=float(novelty.get("confidence", 0.0)),
                recommendation="revise", rationale="Retrieved evidence contradicts the proposed mechanism.",
                failure_disposition="revise",
            )
        if novelty.get("verdict") == "uncertain" and float(novelty.get("confidence", 0.0)) < 0.7:
            return JevDecision(
                evidence_verdict=evidence.get("verdict", "insufficient"), evidence_confidence=float(evidence.get("confidence", 0.0)),
                novelty_verdict="uncertain", novelty_confidence=float(novelty.get("confidence", 0.0)),
                recommendation="defer", rationale="Novelty could not be established with sufficient confidence.",
                failure_disposition="defer",
            )
        if evidence.get("verdict") == "insufficient" and not (request.get("candidate") or {}).get("evidence_optional", False):
            return JevDecision(
                evidence_verdict="insufficient", evidence_confidence=float(evidence.get("confidence", 0.0)),
                novelty_verdict=novelty.get("verdict", "uncertain"), novelty_confidence=float(novelty.get("confidence", 0.0)),
                recommendation="retrieve_more", rationale="Evidence is insufficient for a responsible compute decision.",
                missing_evidence=list(evidence.get("missing_evidence") or ["direct supporting evidence"]),
                retrieval_query=str((request.get("candidate") or {}).get("retrieval_query") or (request.get("candidate") or {}).get("statement") or "additional evidence for the candidate"),
            )
        if validation.get("verdict") == "not_beneficial":
            return JevDecision(
                evidence_verdict=evidence.get("verdict", "not_applicable"), evidence_confidence=float(evidence.get("confidence", 0.0)),
                novelty_verdict=novelty.get("verdict", "novel"), novelty_confidence=float(novelty.get("confidence", 0.0)),
                recommendation="defer", rationale="Validation did not show a positive marginal gain.",
                failure_disposition="defer",
            )
        return JevDecision(
            evidence_verdict=evidence.get("verdict", "not_applicable"), evidence_confidence=float(evidence.get("confidence", 0.0)),
            novelty_verdict=novelty.get("verdict", "novel"), novelty_confidence=float(novelty.get("confidence", 0.0)),
            recommendation="compute_validate", rationale="The candidate is novel, feasible, and has no blocking evidence conflict.",
        )


class HttpJevClient:
    """Provider-neutral HTTP adapter.

    The endpoint is intentionally configured rather than hard-coded because the
    Jev service contract must be pinned together with a model revision before a
    confirmatory run. The request and response schemas remain stable locally.
    """

    def __init__(self, *, endpoint: str | None = None, api_key: str | None = None, timeout_seconds: float = 120.0):
        self.endpoint = endpoint or os.environ.get("JEV_ENDPOINT")
        self.api_key = api_key or os.environ.get("JEV_API_KEY", "")
        self.timeout_seconds = timeout_seconds
        if not self.endpoint:
            raise JevError("JEV_ENDPOINT is not set")
        if not self.api_key:
            raise JevError("JEV_API_KEY is not set")

    def judge(self, request: dict[str, Any]) -> JevDecision:
        payload = json.dumps(request, ensure_ascii=False).encode("utf-8")
        http_request = urllib.request.Request(
            self.endpoint,
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise JevError(f"Jev request failed: {error}") from error
        decision = raw.get("decision", raw) if isinstance(raw, dict) else raw
        return validate_jev_decision(decision, request=request)
