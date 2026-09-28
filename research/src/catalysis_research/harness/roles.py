from __future__ import annotations

import ast
import hashlib
import re
from dataclasses import dataclass
from typing import Any, Protocol


def _normalise_formula(value: str) -> str:
    return re.sub(r"\s+", "", value).lower()


def _canonical_ast(node: ast.AST) -> str:
    if isinstance(node, ast.Expression):
        return _canonical_ast(node.body)
    if isinstance(node, ast.Name):
        return f"name:{node.id.lower()}"
    if isinstance(node, ast.Constant):
        return f"const:{node.value!r}"
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        return f"unary:{type(node.op).__name__}:{_canonical_ast(node.operand)}"
    if isinstance(node, ast.BinOp):
        children = [_canonical_ast(node.left), _canonical_ast(node.right)]
        if isinstance(node.op, (ast.Add, ast.Mult)):
            children.sort()
        return f"bin:{type(node.op).__name__}({','.join(children)})"
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return f"call:{node.func.id.lower()}({','.join(_canonical_ast(arg) for arg in node.args)})"
    return ast.dump(node, annotate_fields=False, include_attributes=False)


def _canonical_formula(value: str) -> tuple[str, str | None]:
    try:
        canonical = _canonical_ast(ast.parse(value, mode="eval"))
    except (SyntaxError, ValueError):
        canonical = _normalise_formula(value)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest() if canonical else None
    return canonical, digest


class HarnessRole(Protocol):
    role_id: str

    def evaluate(self, candidate: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class EvidenceRole:
    role_id: str = "evidence_critic"

    def evaluate(self, candidate: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        evidence = candidate.get("evidence") or []
        allowed_ids = set(context.get("allowed_evidence_ids") or [])
        invalid_ids = [
            item.get("evidence_id") if isinstance(item, dict) else None
            for item in evidence
            if not isinstance(item, dict)
            or not item.get("evidence_id")
            or (allowed_ids and item.get("evidence_id") not in allowed_ids)
            or not (item.get("quote") or item.get("claim"))
        ]
        supporting = [item for item in evidence if item.get("role") == "supporting"]
        contradicting = [item for item in evidence if item.get("role") == "contradicting"]
        missing = []
        if not evidence:
            missing.append("direct evidence linking the mechanism to the candidate")
        if invalid_ids:
            missing.append("valid evidence IDs with provenance and a quote or claim")
        if not candidate.get("falsification_criteria"):
            missing.append("explicit falsification criteria")
        if invalid_ids:
            verdict = "insufficient"
        elif contradicting and not supporting:
            verdict = "contradicts"
        elif supporting and not contradicting:
            verdict = "supports"
        elif supporting:
            verdict = "insufficient"
        else:
            verdict = "insufficient"
        if not supporting and not contradicting:
            confidence = 0.0
        else:
            confidence = min(1.0, max(0.0, (len(supporting) - len(contradicting) + 1) / 3))
        return {
            "verdict": verdict,
            "confidence": confidence,
            "supporting_evidence_ids": [item.get("evidence_id") for item in supporting],
            "contradicting_evidence_ids": [item.get("evidence_id") for item in contradicting],
            "missing_evidence": missing,
            "invalid_evidence_ids": invalid_ids,
        }


@dataclass(frozen=True)
class NoveltyRole:
    role_id: str = "novelty_auditor"

    def evaluate(self, candidate: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        formula, formula_hash = _canonical_formula(str(candidate.get("formula") or candidate.get("statement") or ""))
        prior = context.get("prior_candidates") or []
        duplicates = []
        for item in prior:
            prior_formula, _ = _canonical_formula(str(item.get("formula") or item.get("statement") or ""))
            if formula and formula == prior_formula:
                duplicates.append(item.get("candidate_id"))
        if duplicates:
            verdict, confidence = "duplicate", 1.0
        elif not formula:
            verdict, confidence = "uncertain", 0.0
        else:
            verdict, confidence = "novel", 0.6
        return {
            "verdict": verdict,
            "confidence": confidence,
            "duplicate_candidate_ids": duplicates,
            "canonical_formula_hash": formula_hash if formula else None,
            "similarity_method": "ast_commutative_canonical_v1",
        }


@dataclass(frozen=True)
class FeasibilityRole:
    role_id: str = "feasibility_auditor"

    def evaluate(self, candidate: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        execution = candidate.get("execution") or {}
        status = execution.get("status", "unexecuted")
        failure_code = execution.get("failure_code")
        if status in {"executed", "ready"}:
            verdict, confidence = "feasible", 1.0
        elif failure_code in {"unsafe_expression", "unsupported_input", "non_computable"}:
            verdict, confidence = "infeasible", 1.0
        elif failure_code in {"zero_variance", "redundant", "missingness", "missingness_exceeded"}:
            verdict, confidence = "degenerate", 1.0
        else:
            verdict, confidence = "unknown", 0.2
        return {
            "verdict": verdict,
            "confidence": confidence,
            "execution_status": status,
            "failure_code": failure_code,
        }


@dataclass(frozen=True)
class ValidationRole:
    role_id: str = "validation_planner"

    def evaluate(self, candidate: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        validation = candidate.get("validation") or {}
        if context.get("stage", "precompute") != "postcompute":
            return {
                "verdict": "unmeasured",
                "confidence": 0.0,
                "marginal_gain": None,
                "repeat_count": 0,
                "split_id": validation.get("split_id"),
            }
        gain = validation.get("marginal_gain")
        if gain is None and isinstance(validation.get("marginal_validation_delta"), (int, float)):
            # v5 stores candidate_mae - current_mae; negative is beneficial.
            gain = -float(validation["marginal_validation_delta"])
        if isinstance(gain, (int, float)):
            gain = float(gain)
            verdict = "beneficial" if gain > 0 else "not_beneficial"
            confidence = min(1.0, 0.5 + min(0.5, int(validation.get("repeat_count", 1)) / 20))
        else:
            verdict, confidence = "unmeasured", 0.0
        return {
            "verdict": verdict,
            "confidence": confidence,
            "marginal_gain": gain,
            "repeat_count": validation.get("repeat_count", 0),
            "split_id": validation.get("split_id"),
        }


DEFAULT_ROLES: tuple[HarnessRole, ...] = (
    EvidenceRole(),
    NoveltyRole(),
    FeasibilityRole(),
    ValidationRole(),
)
