from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from ..normalization.schema import canonical_hash
from .schema import EvidenceContractError, RetrievalBudget
from .service import KnowledgeModeRetriever


QUESTION_SCHEMA_VERSION = "knowledge_retrieval_audit_questions.v1"
REPORT_SCHEMA_VERSION = "knowledge_retrieval_audit.v1"


def load_audit_questions(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != QUESTION_SCHEMA_VERSION:
        raise EvidenceContractError("Unsupported knowledge retrieval audit schema")
    questions = payload.get("questions")
    if not isinstance(questions, list) or not questions:
        raise EvidenceContractError("Retrieval audit requires questions")
    identifiers = [str(row.get("id") or "") for row in questions]
    if any(not value for value in identifiers) or len(identifiers) != len(
        set(identifiers)
    ):
        raise EvidenceContractError("Audit question IDs must be present and unique")
    return payload


def _locator_valid(item: dict[str, Any]) -> bool:
    locator = item.get("provenance_locator") or {}
    kind = locator.get("kind")
    if kind == "pdf_page":
        page = locator.get("page")
        return isinstance(page, int) and not isinstance(page, bool) and page >= 1
    if kind in {"markdown_section", "markdown_document"}:
        return item.get("page") is None
    return False


def evaluate_bundle(
    question: dict[str, Any],
    bundle: dict[str, Any],
    *,
    excluded_paper_ids: Iterable[str],
) -> dict[str, Any]:
    items = bundle.get("items") or []
    context = str(bundle.get("context") or "").casefold()
    expected_papers = {
        str(value) for value in question.get("expected_paper_ids") or []
    }
    term_groups = question.get("expected_term_groups") or []
    matched_groups = [
        [str(term) for term in group if str(term).casefold() in context]
        for group in term_groups
    ]
    minimum_groups = int(question.get("minimum_term_groups") or len(term_groups))
    target_rank = next(
        (
            rank
            for rank, item in enumerate(items, start=1)
            if item.get("paper_id") in expected_papers
        ),
        None,
    )
    maximum_rank = int(question.get("max_rank") or bundle["budget"]["item_limit"])
    excluded = set(excluded_paper_ids)
    leaked = sorted(
        {
            str(item.get("paper_id"))
            for item in items
            if str(item.get("paper_id")) in excluded
        }
    )
    complete_items = sum(
        bool(item.get("paper_id"))
        and bool(item.get("document_id"))
        and bool(item.get("quote"))
        and _locator_valid(item)
        for item in items
    )
    provenance_rate = complete_items / len(items) if items else 1.0
    requires_multihop = bool(question.get("requires_kg_multihop"))
    multihop_found = any(len(item.get("kg_path_ids") or []) >= 2 for item in items)
    behavior = str(question.get("expected_behavior") or "evidence")
    relevance_checks = []
    if expected_papers:
        relevance_checks.append(target_rank is not None and target_rank <= maximum_rank)
    if term_groups:
        relevance_checks.append(sum(bool(group) for group in matched_groups) >= minimum_groups)
    if requires_multihop and bundle.get("knowledge_mode") == "small_kg_rag":
        relevance_checks.append(multihop_found)
    automatic_pass = (
        behavior == "evidence"
        and bool(relevance_checks)
        and all(relevance_checks)
        and not leaked
        and provenance_rate == 1.0
    )
    return {
        "expected_behavior": behavior,
        "automatic_pass": automatic_pass,
        "manual_review_required": True,
        "target_paper_hit_rank": target_rank,
        "target_paper_pass": (
            target_rank is not None and target_rank <= maximum_rank
            if expected_papers
            else None
        ),
        "matched_term_groups": matched_groups,
        "matched_term_group_count": sum(bool(group) for group in matched_groups),
        "minimum_term_groups": minimum_groups,
        "term_group_pass": (
            sum(bool(group) for group in matched_groups) >= minimum_groups
            if term_groups
            else None
        ),
        "requires_kg_multihop": requires_multihop,
        "kg_multihop_found": multihop_found,
        "excluded_paper_leaks": leaked,
        "provenance_complete_items": complete_items,
        "provenance_item_count": len(items),
        "provenance_completeness": provenance_rate,
    }


def run_knowledge_retrieval_audit(
    *,
    service: KnowledgeModeRetriever,
    questions_path: Path,
    budget: RetrievalBudget,
    modes: Iterable[str] = ("rag_agent", "small_kg_rag_agent"),
) -> dict[str, Any]:
    question_set = load_audit_questions(questions_path)
    excluded = service.rag_retriever.filter_summary["excluded_paper_ids"]
    mode_reports: dict[str, dict[str, Any]] = {}
    for mode in modes:
        results = []
        for question in question_set["questions"]:
            bundle = service.retrieve(
                query=str(question["query"]),
                experiment_mode=mode,
                budget=budget,
            )
            results.append(
                {
                    "id": question["id"],
                    "question": question["question"],
                    "category": question["category"],
                    "evaluation": evaluate_bundle(
                        question,
                        bundle,
                        excluded_paper_ids=excluded,
                    ),
                    "bundle": bundle,
                }
            )
        evidence_results = [
            row
            for row in results
            if row["evaluation"]["expected_behavior"] == "evidence"
        ]
        multihop_results = [
            row for row in results if row["evaluation"]["requires_kg_multihop"]
        ]
        total_items = sum(
            row["evaluation"]["provenance_item_count"] for row in results
        )
        complete_items = sum(
            row["evaluation"]["provenance_complete_items"] for row in results
        )
        passed = sum(
            bool(row["evaluation"]["automatic_pass"])
            for row in evidence_results
        )
        target_results = [
            row
            for row in evidence_results
            if row["evaluation"]["target_paper_pass"] is not None
        ]
        term_results = [
            row
            for row in evidence_results
            if row["evaluation"]["term_group_pass"] is not None
        ]
        mode_reports[mode] = {
            "question_count": len(results),
            "scored_evidence_question_count": len(evidence_results),
            "automatic_passed": passed,
            "question_pass_rate": passed / len(evidence_results),
            "strict_target_recall": (
                sum(
                    bool(row["evaluation"]["target_paper_pass"])
                    for row in target_results
                )
                / len(target_results)
                if target_results
                else None
            ),
            "term_group_pass_rate": (
                sum(
                    bool(row["evaluation"]["term_group_pass"])
                    for row in term_results
                )
                / len(term_results)
                if term_results
                else None
            ),
            "multihop_success_rate": (
                sum(
                    bool(row["evaluation"]["kg_multihop_found"])
                    for row in multihop_results
                )
                / len(multihop_results)
                if multihop_results
                else None
            ),
            "provenance_completeness": (
                complete_items / total_items if total_items else 1.0
            ),
            "excluded_paper_leak_count": sum(
                len(row["evaluation"]["excluded_paper_leaks"])
                for row in results
            ),
            "mean_selected_tokens": sum(
                row["bundle"]["selected_token_count"] for row in results
            )
            / len(results),
            "results": results,
        }

    thresholds = question_set["acceptance_thresholds"]
    raw = mode_reports.get("rag_agent")
    hybrid = mode_reports.get("small_kg_rag_agent")
    token_ratio = (
        hybrid["mean_selected_tokens"] / raw["mean_selected_tokens"]
        if raw and hybrid and raw["mean_selected_tokens"]
        else None
    )
    checks = {
        f"{mode}.question_pass_rate": report["question_pass_rate"]
        >= float(thresholds["minimum_question_pass_rate"])
        for mode, report in mode_reports.items()
    }
    checks.update(
        {
            f"{mode}.strict_target_recall": report["strict_target_recall"]
            >= float(thresholds["minimum_strict_target_recall"])
            for mode, report in mode_reports.items()
            if report["strict_target_recall"] is not None
        }
    )
    checks.update(
        {
            f"{mode}.provenance_completeness": report[
                "provenance_completeness"
            ]
            == 1.0
            for mode, report in mode_reports.items()
        }
    )
    checks.update(
        {
            f"{mode}.excluded_paper_leak_count": report[
                "excluded_paper_leak_count"
            ]
            == 0
            for mode, report in mode_reports.items()
        }
    )
    if hybrid and hybrid["multihop_success_rate"] is not None:
        checks["small_kg_rag_agent.multihop_success_rate"] = (
            hybrid["multihop_success_rate"]
            >= float(thresholds["minimum_hybrid_multihop_success_rate"])
        )
    if token_ratio is not None:
        checks["hybrid_to_rag_token_ratio"] = token_ratio <= float(
            thresholds["maximum_hybrid_to_rag_token_ratio"]
        )
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "question_set": str(questions_path.resolve()),
        "question_set_hash": canonical_hash(question_set),
        "acceptance_thresholds": thresholds,
        "acceptance_checks": checks,
        "automatic_gate_passed": all(checks.values()),
        "manual_review_required": True,
        "hybrid_to_rag_token_ratio": token_ratio,
        "source_identities": service.source_identities,
        "modes": mode_reports,
    }
    report["report_hash"] = canonical_hash(report)
    return report
