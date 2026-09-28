from __future__ import annotations

import sys
import unittest

RESEARCH_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.harness import HarnessController, RuleBasedJev, RuleBasedTopicScout  # noqa: E402
from catalysis_research.harness.jev import JevError, build_jev_request, validate_jev_decision  # noqa: E402
from catalysis_research.harness.types import RoundInput  # noqa: E402


def _candidate(candidate_id: str, *, evidence: list[dict[str, str]] | None = None, **extra: object) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "hypothesis_id": f"h-{candidate_id}",
        "statement": "A computable structural descriptor changes the measured response.",
        "formula": "log1p(void_fraction)",
        "evidence": evidence if evidence is not None else [{"evidence_id": "E01", "role": "supporting", "claim": "A related mechanism is reported."}],
        "execution": {"status": "ready"},
        "validation": {"marginal_gain": 0.12, "repeat_count": 3, "split_id": "validation-v1"},
        **extra,
    }


class HarnessTests(unittest.TestCase):
    def test_rule_judge_routes_evidence_gap_and_duplicate(self) -> None:
        controller = HarnessController(judge=RuleBasedJev())
        result = controller.run(
            run_id="fixture",
            rounds=[
                RoundInput(
                    round_id=1,
                    candidates=[
                        _candidate("c1", evidence=[]),
                        _candidate("c2", formula="x*y"),
                    ],
                    context={"allowed_evidence_ids": ["E01"]},
                ),
                RoundInput(
                    round_id=2,
                    candidates=[_candidate("c3")],
                    context={"allowed_evidence_ids": ["E01"]},
                ),
            ],
            run_context={"allowed_evidence_ids": ["E01"]},
        )
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.rounds[0]["decision_counts"]["retrieve_more"], 1)
        self.assertEqual(result.rounds[0]["decision_counts"]["compute_validate"], 1)
        self.assertIn("progress", result.rounds[0])
        self.assertEqual(result.rounds[1]["decision_counts"]["abandon"], 1)

    def test_jev_request_strips_locked_test_fields(self) -> None:
        request = build_jev_request(
            candidate=_candidate("c1", test={"mae": 0.1}, target_values=[1, 2]),
            role_outputs={},
            prior_candidates=[],
            round_id=1,
            run_context={"allowed_evidence_ids": ["E01"], "test_labels": [1, 2]},
        )
        self.assertNotIn("test", request["candidate"])
        self.assertNotIn("target_values", request["candidate"])
        self.assertNotIn("test_labels", request["run_context"])
        request = build_jev_request(
            candidate=_candidate("c2"),
            role_outputs={"custom": {"test_score": 0.99}},
            prior_candidates=[],
            round_id=1,
            run_context={"allowed_evidence_ids": ["E01"]},
        )
        self.assertNotIn("test_score", request["role_outputs"]["custom"])

    def test_unknown_evidence_id_fails_closed(self) -> None:
        with self.assertRaises(JevError):
            build_jev_request(
                candidate=_candidate("c1", evidence=[{"evidence_id": "E99", "role": "supporting"}]),
                role_outputs={},
                prior_candidates=[],
                round_id=1,
                run_context={"allowed_evidence_ids": ["E01"]},
            )

    def test_topic_scout_respects_frozen_cutoff_and_marks_priority_only(self) -> None:
        result = RuleBasedTopicScout(window_days=365).scout(
            [
                {"topic_id": "t1", "label": "zeolite", "published_at": "2025-12-01", "source_id": "p1"},
                {"topic_id": "t1", "label": "zeolite", "published_at": "2024-12-01", "source_id": "p2"},
                {"topic_id": "future", "label": "future", "published_at": "2027-01-01", "source_id": "p3"},
            ],
            cutoff="2026-01-01",
            corpus_hash="corpus-v1",
        )
        self.assertEqual(result["cutoff"], "2026-01-01")
        self.assertEqual([item["topic_id"] for item in result["signals"]], ["t1"])
        self.assertTrue(result["hotness_is_retrieval_priority_only"])

    def test_same_round_duplicate_is_abandoned(self) -> None:
        controller = HarnessController(judge=RuleBasedJev())
        result = controller.run(
            run_id="same-round",
            rounds=[RoundInput(round_id=1, candidates=[_candidate("c1"), _candidate("c2")])],
        )
        records = result.rounds[0]["records"]
        self.assertEqual(records[0]["jev"]["recommendation"], "compute_validate")
        self.assertEqual(records[1]["jev"]["recommendation"], "abandon")
        self.assertEqual(records[1]["jev"]["duplicate_candidate_ids"], ["c1"])

    def test_decision_contract_rejects_unsafe_routing(self) -> None:
        with self.assertRaises(JevError):
            validate_jev_decision({
                "evidence_verdict": "contradicts",
                "evidence_confidence": 1.0,
                "novelty_verdict": "novel",
                "novelty_confidence": 1.0,
                "recommendation": "compute_validate",
                "rationale": "unsafe",
            })
        with self.assertRaises(JevError):
            validate_jev_decision({
                "evidence_verdict": "supports",
                "evidence_confidence": 1.0,
                "novelty_verdict": "duplicate",
                "novelty_confidence": 1.0,
                "recommendation": "revise",
                "rationale": "unsafe",
            })


if __name__ == "__main__":
    unittest.main()
