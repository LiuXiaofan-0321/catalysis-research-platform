from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from .chunking import token_count
from .config import IndexConfig
from .hashing import canonical_json, content_hash
from .indexing import EmbeddingProvider, search_tokens, verify_index


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _rrf(rankings: list[list[int]], constant: int = 60) -> dict[int, float]:
    scores: dict[int, float] = defaultdict(float)
    for ranking in rankings:
        for rank, index in enumerate(ranking, start=1):
            scores[index] += 1.0 / (constant + rank)
    return scores


def _quality_multiplier(row: dict[str, Any]) -> float:
    validation = row.get("evidence_validation")
    review = row.get("review_status")
    multiplier = {
        "exact": 1.0,
        "locally_recovered": 0.86,
        "unverified": 0.45,
    }.get(validation, 0.75)
    if review == "needs_review":
        multiplier *= 0.7
    return multiplier


class PortableRetriever:
    def __init__(self, index_directory: Path):
        self.index_directory = index_directory.resolve()
        report = verify_index(self.index_directory)
        if not report["valid"]:
            raise RuntimeError("Invalid index: " + "; ".join(report["failures"]))
        self.manifest = json.loads(
            (self.index_directory / "manifest.json").read_text(encoding="utf-8")
        )
        self.chunk_rows = _load_jsonl(self.index_directory / "chunks.jsonl")
        self.evidence_rows = _load_jsonl(
            self.index_directory / "evidence_records.jsonl"
        )
        self.rows = self.chunk_rows + self.evidence_rows
        self.row_index_by_id = {
            row["record_id"]: index for index, row in enumerate(self.rows)
        }
        chunk_vectors = np.load(
            self.index_directory / "chunk_vectors.npy",
            mmap_mode="r",
        )
        evidence_vectors = np.load(
            self.index_directory / "evidence_vectors.npy",
            mmap_mode="r",
        )
        self.vectors = np.concatenate(
            [np.asarray(chunk_vectors), np.asarray(evidence_vectors)],
            axis=0,
        )
        embedding = self.manifest["embedding"]
        self.embedder = EmbeddingProvider(
            IndexConfig(
                embedding_model=embedding["requested_model"],
                embedding_revision=embedding["requested_revision"],
                vector_dimensions=int(embedding["dimensions"]),
                allow_hash_embedding_fallback=True,
            )
        )
        if (
            self.embedder.actual_model != embedding["actual_model"]
            or self.embedder.dimensions != int(embedding["dimensions"])
        ):
            if embedding["actual_model"] != "hash-embedding-v1":
                raise RuntimeError(
                    "The embedding model used to build this index is unavailable"
                )

    def retrieve(
        self,
        *,
        query: str,
        top_k: int | None = None,
        context_token_budget: int | None = None,
        include_unverified: bool = False,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        settings = self.manifest["retrieval"]
        dense_k = int(settings["top_k_dense"])
        lexical_k = int(settings["top_k_lexical"])
        final_k = int(top_k or settings["top_k_final"])
        max_per_paper = int(settings["max_records_per_paper"])
        token_budget = int(
            context_token_budget or settings["context_token_budget"]
        )
        query_vector = self.embedder.encode([query])[0]
        dense_scores = self.vectors @ query_vector
        dense_ranking = (
            np.argsort(-dense_scores)[: min(dense_k, len(self.rows))].tolist()
            if len(self.rows)
            else []
        )
        query_terms = set(search_tokens(query))
        lexical_scores: list[tuple[float, int]] = []
        for index, row in enumerate(self.rows):
            row_terms = set(str(row.get("fts_text") or "").split())
            overlap = query_terms & row_terms
            score = sum(1.0 + len(term) ** 1.35 for term in overlap)
            if score:
                lexical_scores.append((score, index))
        lexical_ranking = [
            index
            for _, index in sorted(
                lexical_scores,
                key=lambda item: (-item[0], self.rows[item[1]]["record_id"]),
            )[:lexical_k]
        ]
        fused = _rrf([dense_ranking, lexical_ranking])
        candidates: list[dict[str, Any]] = []
        for index, score in fused.items():
            row = self.rows[index]
            if (
                not include_unverified
                and row.get("kind") != "chunk"
                and row.get("evidence_validation") == "unverified"
            ):
                continue
            candidates.append(
                {
                    **row,
                    "score": score * _quality_multiplier(row),
                    "dense_score": float(dense_scores[index]),
                }
            )
        candidates.sort(key=lambda row: (-row["score"], row["record_id"]))

        related_by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in candidates:
            related_by_paper[row["paper_id"]].append(row)
        candidate_by_id = {row["record_id"]: row for row in candidates}
        expanded: list[dict[str, Any]] = []
        seen: set[str] = set()
        for row in candidates[: max(final_k * 3, 20)]:
            if row["record_id"] not in seen:
                expanded.append(row)
                seen.add(row["record_id"])
            explicit_neighbors = [
                (
                    candidate_by_id[record_id]
                    if record_id in candidate_by_id
                    else {
                        **self.rows[self.row_index_by_id[record_id]],
                        "score": row["score"],
                        "dense_score": float(
                            dense_scores[self.row_index_by_id[record_id]]
                        ),
                    }
                )
                for record_id in json.loads(row.get("neighbor_ids_json") or "[]")
                if record_id in self.row_index_by_id
            ]
            fallback_neighbors = related_by_paper[row["paper_id"]]
            for neighbor in [*explicit_neighbors, *fallback_neighbors]:
                if neighbor["record_id"] in seen or neighbor["kind"] == row["kind"]:
                    continue
                explicit = neighbor in explicit_neighbors
                expanded.append(
                    {
                        **neighbor,
                        "score": neighbor["score"] * (0.96 if explicit else 0.9),
                        "expanded_from": row["record_id"],
                        "expansion_type": "kg_neighbor" if explicit else "same_paper",
                    }
                )
                seen.add(neighbor["record_id"])
                break
        expanded.sort(key=lambda row: (-row["score"], row["record_id"]))

        selected: list[dict[str, Any]] = []
        paper_counts: Counter[str] = Counter()
        used_tokens = 0
        for row in expanded:
            if paper_counts[row["paper_id"]] >= max_per_paper:
                continue
            count = token_count(row["text"])
            if selected and used_tokens + count > token_budget:
                continue
            selected.append(row)
            paper_counts[row["paper_id"]] += 1
            used_tokens += count
            if len(selected) >= final_k or used_tokens >= token_budget:
                break
        context = "\n\n".join(
            (
                f"[{row['record_id']} | paper={row['paper_id']} | "
                f"document={row.get('document_id')} | "
                f"document_type={row.get('document_type')} | "
                f"pages={row.get('page_start')}-{row.get('page_end')} | "
                f"kind={row['kind']}]\n{row['text']}"
            )
            for row in selected
        )
        trace = {
            "schema_version": "retrieval_trace.v1",
            "query": query,
            "index_id": self.manifest["index_id"],
            "index_hash": self.manifest["logical_content_hash"],
            "retrieval_mode": "dense+lexical+rrf+quality+paper-expansion",
            "dense_candidates": len(dense_ranking),
            "lexical_candidates": len(lexical_ranking),
            "selected_count": len(selected),
            "selected_token_count": used_tokens,
            "retrieved_evidence": [
                {
                    "record_id": row["record_id"],
                    "paper_id": row["paper_id"],
                    "document_id": row.get("document_id"),
                    "document_type": row.get("document_type"),
                    "source_path": row.get("source_path"),
                    "kind": row["kind"],
                    "page_start": row.get("page_start"),
                    "page_end": row.get("page_end"),
                    "score": row["score"],
                    "dense_score": row["dense_score"],
                    "review_status": row.get("review_status"),
                    "evidence_validation": row.get("evidence_validation"),
                }
                for row in selected
            ],
            "context": context,
            "context_hash": content_hash(context),
            "runtime_seconds": time.perf_counter() - started,
        }
        trace["trace_hash"] = content_hash(
            {**trace, "runtime_seconds": None, "trace_hash": ""}
        )
        return trace
