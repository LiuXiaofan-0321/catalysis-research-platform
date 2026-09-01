from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from typing import Any, Iterable

from ..normalization.schema import canonical_hash
from .schema import (
    EVIDENCE_BUNDLE_SCHEMA_VERSION,
    KNOWLEDGE_MODES,
    EvidenceContractError,
    RetrievalBudget,
)


TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*|[\u4e00-\u9fff]|[^\s]", re.UNICODE)


def count_tokens(text: str) -> int:
    return len(TOKEN_RE.findall(text))


def _quote_hash(quote: str) -> str:
    return hashlib.sha256(quote.encode("utf-8")).hexdigest()


def _required(record: dict[str, Any], field: str) -> Any:
    value = record.get(field)
    if value is None or value == "":
        raise EvidenceContractError(
            f"Retrieval candidate {record.get('record_id')!r} lacks {field}"
        )
    return value


def _normalize_candidate(record: dict[str, Any], channel: str) -> dict[str, Any]:
    quote = str(record.get("quote") or record.get("text") or "").strip()
    if not quote:
        raise EvidenceContractError(
            f"Retrieval candidate {record.get('record_id')!r} lacks quote/text"
        )
    page = record.get("page")
    if page is None:
        page = record.get("pdf_page_index")
    if page is None:
        page = record.get("page_start")
    if page is None:
        raise EvidenceContractError(
            f"Retrieval candidate {record.get('record_id')!r} lacks page"
        )
    source_record = record.get("source_record") or {
        "type": record.get("source_record_type") or record.get("kind") or channel,
        "id": record.get("source_record_id") or record.get("record_id"),
    }
    if not source_record.get("type") or not source_record.get("id"):
        raise EvidenceContractError("source_record requires type and id")
    node_ids = sorted({str(value) for value in record.get("kg_node_ids") or []})
    edge_ids = sorted({str(value) for value in record.get("kg_edge_ids") or []})
    path_ids = [str(value) for value in record.get("kg_path_ids") or []]
    return {
        "record_id": str(_required(record, "record_id")),
        "paper_id": str(_required(record, "paper_id")),
        "document_id": str(_required(record, "document_id")),
        "document_type": str(_required(record, "document_type")),
        "page": int(page),
        "quote": quote,
        "quote_hash": _quote_hash(quote),
        "source_record": source_record,
        "kg_node_ids": node_ids,
        "kg_edge_ids": edge_ids,
        "kg_path_ids": path_ids,
        "retrieval_channels": [channel],
        "source_score": float(record.get("score", 0.0)),
        "evidence_validation": record.get("evidence_validation") or "unknown",
        "review_status": record.get("review_status") or "unknown",
    }


def _rank_channel(records: Iterable[dict[str, Any]], channel: str) -> list[dict[str, Any]]:
    ranked = sorted(
        [_normalize_candidate(record, channel) for record in records],
        key=lambda row: (-row["source_score"], row["record_id"]),
    )
    unique: dict[tuple[str, str, int, str], dict[str, Any]] = {}
    for row in ranked:
        key = (row["paper_id"], row["document_id"], row["page"], row["quote_hash"])
        if key not in unique:
            unique[key] = row
            continue
        current = unique[key]
        current["kg_node_ids"] = sorted(
            set(current["kg_node_ids"]) | set(row["kg_node_ids"])
        )
        current["kg_edge_ids"] = sorted(
            set(current["kg_edge_ids"]) | set(row["kg_edge_ids"])
        )
        if len(row["kg_path_ids"]) > len(current["kg_path_ids"]):
            current["kg_path_ids"] = row["kg_path_ids"]
    return list(unique.values())


def _fuse(channels: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    fused: dict[tuple[str, str, int, str], dict[str, Any]] = {}
    rrf_scores: defaultdict[tuple[str, str, int, str], float] = defaultdict(float)
    for channel, rows in channels.items():
        for rank, row in enumerate(rows, start=1):
            key = (row["paper_id"], row["document_id"], row["page"], row["quote_hash"])
            rrf_scores[key] += 1.0 / (60 + rank)
            if key not in fused:
                fused[key] = row
            else:
                current = fused[key]
                current["retrieval_channels"] = sorted(
                    set(current["retrieval_channels"]) | {channel}
                )
                current["kg_node_ids"] = sorted(
                    set(current["kg_node_ids"]) | set(row["kg_node_ids"])
                )
                current["kg_edge_ids"] = sorted(
                    set(current["kg_edge_ids"]) | set(row["kg_edge_ids"])
                )
                if len(row["kg_path_ids"]) > len(current["kg_path_ids"]):
                    current["kg_path_ids"] = row["kg_path_ids"]
    for key, row in fused.items():
        row["score"] = rrf_scores[key]
    return sorted(fused.values(), key=lambda row: (-row["score"], row["record_id"]))


def _format_item(index: int, row: dict[str, Any]) -> str:
    path = ">".join(row["kg_path_ids"]) or "none"
    return (
        f"[{index} | paper={row['paper_id']} | document={row['document_id']} | "
        f"type={row['document_type']} | page={row['page']} | "
        f"record={row['source_record']['type']}:{row['source_record']['id']} | "
        f"path={path}]\n{row['quote']}"
    )


def build_evidence_bundle(
    *,
    query: str,
    mode: str,
    budget: RetrievalBudget,
    rag_candidates: Iterable[dict[str, Any]] = (),
    kg_candidates: Iterable[dict[str, Any]] = (),
) -> dict[str, Any]:
    if mode not in KNOWLEDGE_MODES:
        raise EvidenceContractError(f"Unsupported knowledge mode: {mode}")
    if mode == "small_kg_rag_shuffled":
        raise EvidenceContractError(
            "small_kg_rag_shuffled is reserved until a frozen corruption manifest exists"
        )
    channels: dict[str, list[dict[str, Any]]] = {}
    if mode == "rag":
        channels["rag"] = _rank_channel(rag_candidates, "rag")[: budget.candidate_limit]
    elif mode == "small_kg_rag":
        rag_limit = (budget.candidate_limit + 1) // 2
        kg_limit = budget.candidate_limit - rag_limit
        channels["rag"] = _rank_channel(rag_candidates, "rag")[:rag_limit]
        channels["kg"] = _rank_channel(kg_candidates, "kg")[:kg_limit]
    ranked = _fuse(channels)[: budget.candidate_limit] if channels else []

    selected: list[dict[str, Any]] = []
    paper_counts: Counter[str] = Counter()
    used_tokens = 0
    for row in ranked:
        if paper_counts[row["paper_id"]] >= budget.max_items_per_paper:
            continue
        rendered = _format_item(len(selected) + 1, row)
        token_count = count_tokens(rendered)
        if token_count > budget.context_token_budget:
            continue
        if used_tokens + token_count > budget.context_token_budget:
            continue
        row["token_count"] = token_count
        selected.append(row)
        paper_counts[row["paper_id"]] += 1
        used_tokens += token_count
        if len(selected) >= budget.item_limit:
            break
    context = "\n\n".join(_format_item(index, row) for index, row in enumerate(selected, 1))
    bundle = {
        "schema_version": EVIDENCE_BUNDLE_SCHEMA_VERSION,
        "query": query,
        "knowledge_mode": mode,
        "budget": {
            "candidate_limit": budget.candidate_limit,
            "item_limit": budget.item_limit,
            "context_token_budget": budget.context_token_budget,
            "max_items_per_paper": budget.max_items_per_paper,
            "tokenizer_id": budget.tokenizer_id,
        },
        "candidate_count": len(ranked),
        "selected_count": len(selected),
        "selected_token_count": used_tokens,
        "items": selected,
        "context": context,
        "context_hash": canonical_hash(context),
    }
    bundle["bundle_hash"] = canonical_hash({**bundle, "bundle_hash": ""})
    return bundle
