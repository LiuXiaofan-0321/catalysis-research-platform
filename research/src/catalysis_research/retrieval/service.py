from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..normalization import ScientificNormalizationOverlay
from .bundle import build_evidence_bundle
from .kg import FrozenKgRetriever
from .schema import EvidenceContractError, RetrievalBudget


EXPERIMENT_KNOWLEDGE_MODES = (
    "agent",
    "rag_agent",
    "small_kg_rag_agent",
)

_BUNDLE_MODES = {
    "agent": "none",
    "rag_agent": "rag",
    "small_kg_rag_agent": "small_kg_rag",
}


class KnowledgeModeRetriever:
    """One matched-budget retrieval entry point for the three Agent conditions."""

    def __init__(
        self,
        *,
        rag_retriever: Any,
        kg_retriever: FrozenKgRetriever,
        normalization_overlay: ScientificNormalizationOverlay,
        source_identities: dict[str, Any],
    ):
        self.rag_retriever = rag_retriever
        self.kg_retriever = kg_retriever
        self.normalization_overlay = normalization_overlay
        self.source_identities = source_identities

    @classmethod
    def from_directories(
        cls,
        *,
        config_path: Path,
        rag_index_directory: Path,
        kg_snapshot_directory: Path,
        normalization_overlay_directory: Path,
    ) -> "KnowledgeModeRetriever":
        try:
            from catalysis_literature.retrieval import PortableRetriever
        except ImportError as error:
            raise EvidenceContractError(
                "catalysis-literature-pipeline must be installed for RAG retrieval"
            ) from error

        config = json.loads(config_path.read_text(encoding="utf-8"))
        rag_config = config["rag"]
        rag = PortableRetriever(
            rag_index_directory,
            excluded_paper_ids=rag_config["excluded_paper_ids"],
            expected_excluded_documents=int(
                rag_config["expected_excluded_documents"]
            ),
            expected_excluded_records=int(rag_config["expected_excluded_records"]),
            expected_retained_papers=int(rag_config["expected_retained_papers"]),
            expected_retained_documents=int(
                rag_config["expected_retained_documents"]
            ),
            expected_retained_chunks=int(rag_config["expected_retained_chunks"]),
        )
        if rag.manifest["index_id"] != rag_config["base_index_id"]:
            raise EvidenceContractError("Unexpected base RAG index ID")
        if rag.manifest["logical_content_hash"] != rag_config["base_index_hash"]:
            raise EvidenceContractError("Unexpected base RAG index hash")

        kg = FrozenKgRetriever(kg_snapshot_directory)
        kg_config = config["small_kg"]
        if kg.manifest["snapshot_id"] != kg_config["snapshot_id"]:
            raise EvidenceContractError("Unexpected Small KG snapshot ID")
        if kg.manifest["snapshot_content_hash"] != kg_config["snapshot_hash"]:
            raise EvidenceContractError("Unexpected Small KG snapshot hash")

        overlay = ScientificNormalizationOverlay(
            normalization_overlay_directory,
            minimum_confidence=float(config["normalization"]["minimum_confidence"]),
        )
        overlay_config = config["normalization"]
        if overlay.manifest["overlay_id"] != overlay_config["overlay_id"]:
            raise EvidenceContractError("Unexpected normalization overlay ID")
        if (
            overlay.manifest["overlay_content_hash"]
            != overlay_config["overlay_content_hash"]
        ):
            raise EvidenceContractError("Unexpected normalization overlay hash")
        return cls(
            rag_retriever=rag,
            kg_retriever=kg,
            normalization_overlay=overlay,
            source_identities={
                "rag": {
                    "index_id": rag.manifest["index_id"],
                    "index_hash": rag.manifest["logical_content_hash"],
                    "corpus_filter": rag.filter_summary,
                },
                "small_kg": {
                    "snapshot_id": kg.manifest["snapshot_id"],
                    "snapshot_hash": kg.manifest["snapshot_content_hash"],
                },
                "normalization": overlay.identity,
            },
        )

    def retrieve(
        self,
        *,
        query: str,
        experiment_mode: str,
        budget: RetrievalBudget,
    ) -> dict[str, Any]:
        if experiment_mode not in EXPERIMENT_KNOWLEDGE_MODES:
            raise EvidenceContractError(
                f"Unsupported experiment knowledge mode: {experiment_mode}"
            )
        bundle_mode = _BUNDLE_MODES[experiment_mode]
        if experiment_mode == "agent":
            expansion = {
                **self.normalization_overlay.identity,
                "original_query": query,
                "expanded_query": query,
                "added_terms": [],
                "matched_mappings": [],
                "applied": False,
            }
        else:
            expansion = {
                **self.normalization_overlay.expand_query(query),
                "applied": True,
            }
        retrieval_query = expansion["expanded_query"]
        rag_candidates: list[dict[str, Any]] = []
        kg_candidates: list[dict[str, Any]] = []
        if experiment_mode in {"rag_agent", "small_kg_rag_agent"}:
            rag_candidates = self.rag_retriever.retrieve_candidates(
                query=retrieval_query,
                limit=budget.candidate_limit,
            )
        if experiment_mode == "small_kg_rag_agent":
            kg_candidates = self.kg_retriever.retrieve(
                query=retrieval_query,
                candidate_limit=budget.candidate_limit,
                max_hops=2,
            )
            for candidate in kg_candidates:
                candidate["normalization_mappings"] = (
                    self.normalization_overlay.mappings_for_nodes(
                        candidate.get("kg_node_ids") or []
                    )
                )
        return build_evidence_bundle(
            query=query,
            mode=bundle_mode,
            budget=budget,
            rag_candidates=rag_candidates,
            kg_candidates=kg_candidates,
            experiment_mode=experiment_mode,
            retrieval_metadata={
                "retrieval_query": retrieval_query,
                "query_normalization": expansion,
                "sources": self.source_identities,
            },
        )
