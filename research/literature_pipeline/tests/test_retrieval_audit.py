from catalysis_literature.audit import evaluate_trace


def test_evaluate_trace_checks_si_rank_and_term_groups() -> None:
    question = {
        "expected_document_types": ["si"],
        "expected_term_groups": [["afx"], ["milling"], ["recrystallization"]],
        "minimum_term_groups": 2,
        "max_rank": 3,
    }
    trace = {
        "context": "AFX crystals were treated by post-milling recrystallization.",
        "retrieved_evidence": [
            {"paper_id": "doi:test", "document_type": "si"},
        ],
    }

    result = evaluate_trace(question, trace)

    assert result["automatic_pass"] is True
    assert result["manual_review_required"] is True
    assert result["document_type_hit_rank"] == 1
    assert result["matched_term_group_count"] == 3
