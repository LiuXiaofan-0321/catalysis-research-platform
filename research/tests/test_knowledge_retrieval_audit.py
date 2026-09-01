from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "src"))

from catalysis_research.retrieval import (  # noqa: E402
    RetrievalBudget,
    run_knowledge_retrieval_audit,
)


class _Rag:
    filter_summary = {"excluded_paper_ids": ["paper:excluded"]}


class _Service:
    rag_retriever = _Rag()
    source_identities = {"rag": {}, "small_kg": {}, "normalization": {}}

    def retrieve(self, *, query: str, experiment_mode: str, budget: RetrievalBudget):
        del query
        kg = experiment_mode == "small_kg_rag_agent"
        item = {
            "paper_id": "paper:expected",
            "document_id": "document:1",
            "quote": "MTO conversion over MFI depends on Bronsted acidity.",
            "page": 2,
            "provenance_locator": {"kind": "pdf_page", "page": 2},
            "kg_path_ids": ["node:1", "node:2"] if kg else [],
        }
        return {
            "knowledge_mode": "small_kg_rag" if kg else "rag",
            "budget": {"item_limit": budget.item_limit},
            "items": [item],
            "context": item["quote"],
            "selected_token_count": 20,
        }


class KnowledgeRetrievalAuditTests(unittest.TestCase):
    def test_matched_modes_pass_frozen_gate(self) -> None:
        payload = {
            "schema_version": "knowledge_retrieval_audit_questions.v1",
            "acceptance_thresholds": {
                "minimum_evidence_question_recall": 1.0,
                "minimum_hybrid_multihop_success_rate": 1.0,
                "maximum_hybrid_to_rag_token_ratio": 1.0,
            },
            "questions": [
                {
                    "id": "q1",
                    "question": "test",
                    "query": "test",
                    "category": "multi_hop",
                    "expected_behavior": "evidence",
                    "expected_paper_ids": ["paper:expected"],
                    "expected_term_groups": [["mto"], ["mfi"]],
                    "minimum_term_groups": 2,
                    "requires_kg_multihop": True,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            questions = Path(temporary) / "questions.json"
            questions.write_text(json.dumps(payload), encoding="utf-8")
            report = run_knowledge_retrieval_audit(
                service=_Service(),  # type: ignore[arg-type]
                questions_path=questions,
                budget=RetrievalBudget(),
            )
        self.assertTrue(report["automatic_gate_passed"])
        self.assertEqual(report["hybrid_to_rag_token_ratio"], 1.0)
        self.assertEqual(
            report["modes"]["small_kg_rag_agent"]["multihop_success_rate"],
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
