from __future__ import annotations

import sys
import unittest
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.harness import (  # noqa: E402
    HarnessController,
    RuleBasedJev,
    compute_round_metrics,
    parse_round_counts,
    run_round_prefix_experiment,
)
from catalysis_research.harness.types import RoundInput  # noqa: E402


def candidate(candidate_id: str, formula: str, gain: float, *, useful: bool, feedback_used: bool = False, revision_of: str | None = None) -> dict[str, object]:
    value: dict[str, object] = {
        "candidate_id": candidate_id,
        "hypothesis_id": f"h-{candidate_id}",
        "statement": f"Candidate {candidate_id} has a measurable mechanism.",
        "formula": formula,
        "evidence": [{"evidence_id": "E01", "role": "supporting", "claim": "related mechanism"}],
        "falsification_criteria": "validation gain is absent",
        "execution": {"status": "executed"},
        "validation": {"marginal_gain": gain, "repeat_count": 3, "split_id": "validation-v1"},
        "useful": useful,
        "feedback_used": feedback_used,
    }
    if revision_of:
        value["revision_of"] = revision_of
    return value


class RoundExperimentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rounds = [
            RoundInput(1, [candidate("c1", "x + 1", 0.10, useful=True)], {"stage": "postcompute", "allowed_evidence_ids": ["E01"]}),
            RoundInput(2, [candidate("c2", "x + 2", 0.20, useful=True, feedback_used=True, revision_of="c1")], {"stage": "postcompute", "allowed_evidence_ids": ["E01"]}),
            RoundInput(3, [candidate("c3", "x + 3", 0.0, useful=False, feedback_used=False)], {"stage": "postcompute", "allowed_evidence_ids": ["E01"]}),
        ]

    def test_parse_round_counts(self) -> None:
        self.assertEqual(parse_round_counts("1,3,3", available_rounds=3), (1, 3))
        self.assertEqual(parse_round_counts("one-shot", available_rounds=3), (1,))
        with self.assertRaises(ValueError):
            parse_round_counts("1,5", available_rounds=3)

    def test_metrics_include_curve_auc_feedback_and_oracle_rates(self) -> None:
        run = HarnessController(judge=RuleBasedJev()).run(
            run_id="fixture", rounds=self.rounds, run_context={"allowed_evidence_ids": ["E01"]}
        )
        metrics = compute_round_metrics(run)
        self.assertEqual(metrics["round_count"], 3)
        self.assertEqual(metrics["positive_gain_count"], 2)
        self.assertAlmostEqual(metrics["final_cumulative_positive_gain"], 0.30)
        self.assertAlmostEqual(metrics["final_cumulative_positive_accepted_gain"], 0.30)
        self.assertGreater(metrics["discovery_curve_auc"], 0.0)
        self.assertEqual(metrics["feedback_use_rate"], 0.5)
        self.assertEqual(metrics["revision_success_rate"], 1.0)
        self.assertEqual(metrics["failed_candidate_count"], 0)
        self.assertEqual(metrics["useful_candidate_recall"], 1.0)
        self.assertEqual(metrics["false_rejection_rate"], 0.0)

    def test_prefix_experiment_replays_one_three_and_available_rounds(self) -> None:
        result = run_round_prefix_experiment(
            controller=HarnessController(judge=RuleBasedJev()),
            run_id="fixture",
            rounds=self.rounds,
            round_counts="1,3",
            run_context={"allowed_evidence_ids": ["E01"]},
        )
        self.assertEqual(result["round_counts"], [1, 3])
        self.assertEqual(result["protocols"][0]["protocol"], "one_shot")
        self.assertEqual(result["protocols"][0]["metrics"]["round_count"], 1)
        self.assertEqual(result["protocols"][1]["metrics"]["round_count"], 3)


if __name__ == "__main__":
    unittest.main()
