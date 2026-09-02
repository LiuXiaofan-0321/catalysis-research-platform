from __future__ import annotations

import json
import sys
import unittest
from collections import defaultdict
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "src"))

from catalysis_research.retrieval import (  # noqa: E402
    EvidenceContractError,
    FrozenKgRetriever,
    KnowledgeModeRetriever,
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
    def test_frozen_retrieval_hashes_are_sha256_values(self) -> None:
        config = json.loads(
            (
                REPOSITORY_ROOT
                / "research"
                / "configs"
                / "retrieval"
                / "small-kg-hybrid-v1.json"
            ).read_text(encoding="utf-8")
        )
        hashes = (
            config["rag"]["base_index_hash"],
            config["small_kg"]["snapshot_hash"],
            config["normalization"]["overlay_content_hash"],
        )
        self.assertTrue(
            all(
                len(value) == 64
                and all(character in "0123456789abcdef" for character in value)
                for value in hashes
            )
        )

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

    def test_markdown_page_is_not_claimed_as_a_pdf_page(self) -> None:
        candidate = _candidate("rag:markdown")
        candidate.pop("page")
        candidate.update(
            {
                "page_start": 1,
                "source_path": "/source/article.md",
                "section": "Experimental methods",
            }
        )
        bundle = build_evidence_bundle(
            query="test",
            mode="rag",
            budget=RetrievalBudget(),
            rag_candidates=[candidate],
        )
        item = bundle["items"][0]
        self.assertIsNone(item["page"])
        self.assertEqual(
            item["provenance_locator"],
            {
                "kind": "markdown_section",
                "section": "Experimental methods",
            },
        )
        self.assertIn("locator=markdown_section:Experimental methods", bundle["context"])

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

        excluded = retriever.retrieve(
            query="MTO conversion",
            candidate_limit=30,
            max_hops=2,
            excluded_paper_ids={"paper:1"},
        )
        self.assertEqual(excluded, [])

    def test_agent_modes_use_only_their_allowed_sources_with_one_budget(self) -> None:
        class FakeRag:
            def __init__(self) -> None:
                self.queries: list[str] = []

            def retrieve_candidates(self, *, query: str, limit: int) -> list[dict[str, object]]:
                self.queries.append(query)
                return [_candidate("rag:mode", score=3.0)][:limit]

        class FakeKg:
            def __init__(self) -> None:
                self.queries: list[str] = []

            def retrieve(
                self,
                *,
                query: str,
                candidate_limit: int,
                max_hops: int,
                excluded_paper_ids: object = (),
            ) -> list[dict[str, object]]:
                del excluded_paper_ids
                self.queries.append(query)
                candidate = _candidate(
                    "kg:mode",
                    paper_id="paper:kg",
                    document_id="document:kg",
                    score=4.0,
                )
                candidate.update({
                    "kg_node_ids": ["node:mto"],
                    "kg_edge_ids": ["edge:mto"],
                    "kg_path_ids": ["node:mto"],
                })
                return [candidate][:candidate_limit]

        class FakeOverlay:
            identity = {"overlay_id": "overlay:v1", "overlay_content_hash": "hash", "rule_version": "v1"}

            def expand_query(self, query: str) -> dict[str, object]:
                return {
                    **self.identity,
                    "original_query": query,
                    "expanded_query": query + " methanol-to-olefins",
                    "added_terms": ["methanol-to-olefins"],
                    "matched_mappings": [],
                }

            def mappings_for_nodes(self, node_ids: list[str]) -> list[dict[str, object]]:
                return [{
                    "mapping_id": "norm:mto",
                    "category": "reaction",
                    "raw_value": "MTO",
                    "canonical_value": "methanol-to-olefins",
                    "rule_id": "reaction_alias",
                    "confidence": 1.0,
                }] if node_ids else []

        rag = FakeRag()
        kg = FakeKg()
        service = KnowledgeModeRetriever(
            rag_retriever=rag,
            kg_retriever=kg,  # type: ignore[arg-type]
            normalization_overlay=FakeOverlay(),  # type: ignore[arg-type]
            source_identities={"rag": {}, "small_kg": {}, "normalization": {}},
        )
        budget = RetrievalBudget(candidate_limit=4, item_limit=3, context_token_budget=300)

        agent = service.retrieve(query="MTO conversion", experiment_mode="agent", budget=budget)
        raw = service.retrieve(query="MTO conversion", experiment_mode="rag_agent", budget=budget)
        hybrid = service.retrieve(query="MTO conversion", experiment_mode="small_kg_rag_agent", budget=budget)

        self.assertEqual(agent["knowledge_mode"], "none")
        self.assertEqual(agent["items"], [])
        self.assertEqual(raw["knowledge_mode"], "rag")
        self.assertEqual(hybrid["knowledge_mode"], "small_kg_rag")
        self.assertEqual(agent["budget"], raw["budget"])
        self.assertEqual(raw["budget"], hybrid["budget"])
        self.assertEqual(rag.queries, [
            "MTO conversion methanol-to-olefins",
            "MTO conversion methanol-to-olefins",
        ])
        self.assertEqual(kg.queries, ["MTO conversion methanol-to-olefins"])
        kg_item = next(item for item in hybrid["items"] if item["paper_id"] == "paper:kg")
        self.assertEqual(kg_item["normalization_mappings"][0]["mapping_id"], "norm:mto")


if __name__ == "__main__":
    unittest.main()
