from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


EvidenceVerdict = Literal["supports", "contradicts", "insufficient", "not_applicable"]
NoveltyVerdict = Literal["novel", "duplicate", "uncertain"]
Recommendation = Literal["compute_validate", "retrieve_more", "revise", "defer", "abandon"]


def _bounded_score(name: str, value: float) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


@dataclass(frozen=True)
class JevDecision:
    """A machine-checkable decision for one hypothesis candidate."""

    evidence_verdict: EvidenceVerdict
    evidence_confidence: float
    novelty_verdict: NoveltyVerdict
    novelty_confidence: float
    recommendation: Recommendation
    rationale: str
    missing_evidence: list[str] = field(default_factory=list)
    duplicate_candidate_ids: list[str] = field(default_factory=list)
    retrieval_query: str | None = None
    failure_disposition: Literal["revise", "defer", "abandon", "none"] = "none"

    def __post_init__(self) -> None:
        if self.evidence_verdict not in {"supports", "contradicts", "insufficient", "not_applicable"}:
            raise ValueError("invalid evidence_verdict")
        if self.novelty_verdict not in {"novel", "duplicate", "uncertain"}:
            raise ValueError("invalid novelty_verdict")
        if self.recommendation not in {"compute_validate", "retrieve_more", "revise", "defer", "abandon"}:
            raise ValueError("invalid recommendation")
        _bounded_score("evidence_confidence", self.evidence_confidence)
        _bounded_score("novelty_confidence", self.novelty_confidence)
        if not self.rationale.strip():
            raise ValueError("rationale must be non-empty")
        if self.recommendation == "retrieve_more" and not self.retrieval_query:
            raise ValueError("retrieve_more requires retrieval_query")
        if self.recommendation == "revise" and self.failure_disposition not in {"revise", "none"}:
            raise ValueError("revise recommendation has incompatible failure_disposition")
        if self.novelty_verdict == "duplicate" and self.recommendation != "abandon":
            raise ValueError("duplicate candidates must be abandoned")
        if self.evidence_verdict == "contradicts" and self.recommendation == "compute_validate":
            raise ValueError("contradicting evidence cannot be sent directly to compute")
        if self.recommendation == "retrieve_more" and self.evidence_verdict not in {"insufficient", "not_applicable"}:
            raise ValueError("retrieve_more requires insufficient or unavailable evidence")
        if self.recommendation == "abandon" and self.failure_disposition not in {"abandon", "none"}:
            raise ValueError("abandon recommendation has incompatible failure_disposition")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RoundInput:
    """Inputs for one hypothesis round.

    Candidate dictionaries are intentionally open-ended: adapters can attach
    domain-specific formulas and execution reports while the harness only
    consumes the documented fields.
    """

    round_id: int
    candidates: list[dict[str, Any]]
    context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.round_id < 1:
            raise ValueError("round_id must be positive")
        seen: set[str] = set()
        for candidate in self.candidates:
            candidate_id = candidate.get("candidate_id")
            if not isinstance(candidate_id, str) or not candidate_id.strip():
                raise ValueError("every candidate needs a non-empty candidate_id")
            if candidate_id in seen:
                raise ValueError(f"duplicate candidate_id: {candidate_id}")
            seen.add(candidate_id)


@dataclass
class HarnessRun:
    schema_version: str
    run_id: str
    rounds: list[dict[str, Any]]
    status: str = "completed"
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "status": self.status,
            "rounds": self.rounds,
            "warnings": self.warnings,
        }
