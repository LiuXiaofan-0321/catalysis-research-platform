from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .hashing import content_hash
from .retrieval import PortableRetriever


AUDIT_SCHEMA_VERSION = "retrieval_audit.v1"


def load_questions(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "retrieval_audit_questions.v1":
        raise ValueError("Unsupported retrieval audit question schema")
    questions = payload.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("Retrieval audit requires at least one question")
    identifiers = [str(question.get("id") or "") for question in questions]
    if any(not identifier for identifier in identifiers):
        raise ValueError("Every retrieval audit question requires an id")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Retrieval audit question ids must be unique")
    return payload


def evaluate_trace(question: dict[str, Any], trace: dict[str, Any]) -> dict[str, Any]:
    evidence = trace.get("retrieved_evidence") or []
    max_rank = int(question.get("max_rank") or 5)
    expected_document_types = {
        str(value) for value in question.get("expected_document_types") or []
    }
    expected_paper_ids = {
        str(value) for value in question.get("expected_paper_ids") or []
    }

    document_type_rank = next(
        (
            rank
            for rank, row in enumerate(evidence, start=1)
            if row.get("document_type") in expected_document_types
        ),
        None,
    )
    target_paper_rank = next(
        (
            rank
            for rank, row in enumerate(evidence, start=1)
            if row.get("paper_id") in expected_paper_ids
        ),
        None,
    )
    target_document_rank = next(
        (
            rank
            for rank, row in enumerate(evidence, start=1)
            if row.get("paper_id") in expected_paper_ids
            and (
                not expected_document_types
                or row.get("document_type") in expected_document_types
            )
        ),
        None,
    )
    context = str(trace.get("context") or "").casefold()
    term_groups = question.get("expected_term_groups") or []
    matched_groups = [
        [str(term) for term in group if str(term).casefold() in context]
        for group in term_groups
    ]
    matched_group_count = sum(bool(group) for group in matched_groups)
    minimum_groups = int(question.get("minimum_term_groups") or len(term_groups))

    checks: list[bool] = []
    if expected_document_types and not expected_paper_ids:
        checks.append(document_type_rank is not None and document_type_rank <= max_rank)
    if expected_paper_ids:
        checks.append(
            target_document_rank is not None and target_document_rank <= max_rank
        )
    if term_groups:
        checks.append(matched_group_count >= minimum_groups)
    return {
        "automatic_pass": all(checks) if checks else False,
        "manual_review_required": True,
        "max_rank": max_rank,
        "document_type_hit_rank": document_type_rank,
        "target_paper_hit_rank": target_paper_rank,
        "target_document_hit_rank": target_document_rank,
        "matched_term_groups": matched_groups,
        "matched_term_group_count": matched_group_count,
        "minimum_term_groups": minimum_groups,
    }


def run_retrieval_audit(
    *,
    index_directory: Path,
    questions_path: Path,
    top_k: int | None = None,
    context_token_budget: int | None = None,
) -> dict[str, Any]:
    question_set = load_questions(questions_path)
    retriever = PortableRetriever(index_directory)
    results: list[dict[str, Any]] = []
    for question in question_set["questions"]:
        trace = retriever.retrieve(
            query=str(question["query"]),
            top_k=top_k,
            context_token_budget=context_token_budget,
            include_unverified=False,
        )
        results.append(
            {
                "id": question["id"],
                "question": question.get("question"),
                "intent": question.get("intent"),
                "evaluation": evaluate_trace(question, trace),
                "trace": trace,
            }
        )
    automatic_passed = sum(
        bool(result["evaluation"]["automatic_pass"]) for result in results
    )
    report = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "question_set": str(questions_path.resolve()),
        "question_set_hash": content_hash(question_set),
        "index_id": retriever.manifest["index_id"],
        "index_hash": retriever.manifest["logical_content_hash"],
        "question_count": len(results),
        "automatic_passed": automatic_passed,
        "manual_review_required": sum(
            bool(result["evaluation"]["manual_review_required"])
            for result in results
        ),
        "results": results,
    }
    report["report_hash"] = content_hash(report)
    return report
