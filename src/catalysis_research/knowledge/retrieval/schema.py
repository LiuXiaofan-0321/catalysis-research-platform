from __future__ import annotations

from dataclasses import dataclass


EVIDENCE_BUNDLE_SCHEMA_VERSION = "evidence_bundle.v1"
KNOWLEDGE_MODES = (
    "none",
    "rag",
    "small_kg_rag",
    "small_kg_rag_shuffled",
)


class EvidenceContractError(ValueError):
    pass


@dataclass(frozen=True)
class RetrievalBudget:
    candidate_limit: int = 30
    item_limit: int = 10
    context_token_budget: int = 4000
    max_items_per_paper: int = 3
    tokenizer_id: str = "unicode_lexical_v1"

    def __post_init__(self) -> None:
        for name in (
            "candidate_limit",
            "item_limit",
            "context_token_budget",
            "max_items_per_paper",
        ):
            if getattr(self, name) < 1:
                raise EvidenceContractError(f"{name} must be at least 1")
