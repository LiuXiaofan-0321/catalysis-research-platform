from __future__ import annotations

import sys
import unittest
from collections import defaultdict
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "src"))

from catalysis_research.retrieval import (  # noqa: E402
    EvidenceContractError,
    FrozenKgRetriever,
    RetrievalBudget,
    build_evidence_bundle,
)
from catalysis_research.retrieval.bundle import count_tokens  # noqa: E402


def _candidate(
    record_id: str,
    *,
    paper_id: str = "paper:1",
    document_id: str = "document:1",
    quote: str = "Conversion reached 80 percent at 673 K.",
    score: float = 1.0,
) -> dict[str, object]:
    return {
        "record_id": record_id,
        "paper_id": paper_id,
        "document_id": document_id,
        "document_type": "main",
        "page": 3,
        "quote": quote,
        "source_record": {"type": "chunk", "id": record_id},
        "score": score,
        "evidence_validation": "exact",
        "review_status": "verified",
    }


class RetrievalContractTests(unittest.TestCase):
    def test_modes_share_budget_and_hybrid_deduplicates_provenance(self) -> None:
        budget = RetrievalBudget(
            candidate_limit=4,
            item_limit=2,
            context_token_budget=200,
            max_items_per_paper=2,
        )
        rag = [
            _candidate("rag:1", score=3.0),
            _candidate("rag:2", paper_id="paper:2", document_id="document:2", quote="Selectivity was 90 percent.", score=2.0),
            _candidate("rag:3", paper_id="paper:3", document_id="document:3", quote="Yield was 70 percent.", score=1.0),
        ]
        kg_first = _candidate("kg:edge:1", score=4.0)
        kg_first.update({
            "source_record": {"type": "edge", "id": "edge:1"},
            "kg_node_ids": ["node:reaction", "node:experiment"],
            "kg_edge_ids": ["edge:1"],
            "kg_path_ids": ["node:reaction", "node:experiment"],
        })
        kg = [
            kg_first,
            {**kg_first, "record_id": "kg:duplicate", "score": 3.5},
            _candidate("kg:2", paper_id="paper:4", document_id="document:4", quote="Pressure was 200 kPa.", score=2.0),
            _candidate("kg:3", paper_id="paper:5", document_id="document:5", quote="WHSV was 3 h^-1.", score=1.0),
        ]
        raw = build_evidence_bundle(query="conversion", mode="rag", budget=budget, rag_candidates=rag)
        hybrid = build_evidence_bundle(query="conversion", mode="small_kg_rag", budget=budget, rag_candidates=rag, kg_candidates=kg)

        self.assertLessEqual(raw["candidate_count"], budget.candidate_limit)
        self.assertLessEqual(hybrid["candidate_count"], budget.candidate_limit)
        self.assertEqual(raw["budget"], hybrid["budget"])
        merged = next(item for item in hybrid["items"] if item["paper_id"] == "paper:1")
        self.assertEqual(merged["retrieval_channels"], ["kg", "rag"])
        self.assertEqual(merged["kg_edge_ids"], ["edge:1"])
        self.assertEqual(merged["kg_path_ids"], ["node:reaction", "node:experiment"])
        self.assertEqual(hybrid["selected_token_count"], count_tokens(hybrid["context"]))

    def test_none_is_empty_and_reserved_mode_is_blocked(self) -> None:
        budget = RetrievalBudget()
        bundle = build_evidence_bundle(query="test", mode="none", budget=budget)
        self.assertEqual(bundle["items"], [])
        self.assertEqual(bundle["selected_token_count"], 0)
        with self.assertRaisesRegex(EvidenceContractError, "reserved"):
            build_evidence_bundle(query="test", mode="small_kg_rag_shuffled", budget=budget)

    def test_missing_provenance_is_rejected(self) -> None:
        candidate = _candidate("rag:bad")
        candidate.pop("document_id")
        with self.assertRaisesRegex(EvidenceContractError, "document_id"):
            build_evidence_bundle(query="test", mode="rag", budget=RetrievalBudget(), rag_candidates=[candidate])

    def test_kg_retriever_returns_grounded_multihop_paths(self) -> None:
        evidence = [{
            "document_id": "document:1",
            "document_type": "main",
            "pdf_page_index": 2,
            "quote": "MTO on H-ZSM-5 reached 80 percent conversion.",
            "evidence_validation": "exact",
        }]
        reaction = {"id": "node:reaction", "node_type": "reaction", "label": "MTO", "canonical_name": "methanol-to-olefins", "data": {}, "evidence": evidence, "review_status": "verified"}
        experiment = {"id": "node:experiment", "node_type": "experiment", "label": "activity test", "canonical_name": "activity_test", "data": {}, "evidence": evidence, "review_status": "verified"}
        metric = {"id": "node:metric", "node_type": "metric", "label": "conversion", "canonical_name": "conversion", "data": {}, "evidence": evidence, "review_status": "verified"}
        edges = [
            {"id": "edge:1", "from_node_id": "node:reaction", "to_node_id": "node:experiment", "source_paper_id": "paper:1", "evidence": evidence, "review_status": "verified"},
            {"id": "edge:2", "from_node_id": "node:experiment", "to_node_id": "node:metric", "source_paper_id": "paper:1", "evidence": evidence, "review_status": "verified"},
        ]
        retriever = FrozenKgRetriever.__new__(FrozenKgRetriever)
        retriever.nodes = {node["id"]: node for node in (reaction, experiment, metric)}
        retriever.edges = edges
        retriever.adjacency = defaultdict(list)
        for edge in edges:
            retriever.adjacency[edge["from_node_id"]].append(edge)
            retriever.adjacency[edge["to_node_id"]].append(edge)

        rows = retriever.retrieve(query="MTO conversion", candidate_limit=30, max_hops=2)
        self.assertTrue(rows)
        self.assertTrue(all(row["paper_id"] == "paper:1" for row in rows))
        self.assertTrue(any(len(row["kg_path_ids"]) >= 2 for row in rows))
        self.assertTrue(any(row["kg_edge_ids"] for row in rows))


if __name__ == "__main__":
    unittest.main()
