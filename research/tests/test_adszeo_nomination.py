from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.experiments import adszeo_nomination as nomination  # noqa: E402
from catalysis_research.harness.types import JevDecision  # noqa: E402
from catalysis_research.models.glm import GlmResponse  # noqa: E402
from catalysis_research.retrieval import RetrievalBudget  # noqa: E402


class _FakeService:
    source_identities = {"rag": {}, "small_kg": {}, "normalization": {}}

    def retrieve(self, *, query, experiment_mode, budget):
        return {"query": query, "knowledge_mode": experiment_mode, "items": [],
                "context": "", "budget": budget.__dict__, "bundle_hash": "empty"}


class _FakeClient:
    def __init__(self, formulas_by_round):
        self.formulas_by_round = formulas_by_round
        self.prompts = []

    def chat_json(self, *, model, user, **kwargs):
        del kwargs
        payload = json.loads(user)
        self.prompts.append(payload)
        round_number = len(self.prompts)
        candidates = [
            {"name": name, "formula": formula, "rationale": "physical proposal",
             "expected_direction": "nonlinear", "falsification_criteria": "no validation gain"}
            for name, formula in self.formulas_by_round[round_number - 1]
        ]
        return GlmResponse(
            structured={"evidence_chain": [], "hypothesis": "A testable hypothesis",
                        "descriptor_candidates": candidates, "epistemic_status": "tentative"},
            raw={"id": f"round-{round_number}"}, provider="fake", model=model,
            usage={"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        )


class _DeferJev:
    """Jev fixture that records requests and blocks pre-compute validation."""

    def __init__(self):
        self.requests = []

    def judge(self, request):
        self.requests.append(request)
        return JevDecision(
            evidence_verdict="insufficient",
            evidence_confidence=0.0,
            novelty_verdict="novel",
            novelty_confidence=0.6,
            recommendation="defer",
            rationale="fixture blocks computation until more evidence is available",
            failure_disposition="defer",
        )


class NominationLoopTests(unittest.TestCase):
    def _run(self, formulas_by_round, scores, *, score_only=False, jev_judge=None):
        rows = [
            {"structure_id": f"s{i}", "framework_code": f"T{i % 5}",
             "split": ("train" if i < 12 else "validation" if i < 18 else "test"),
             "loading_mol_kg": float(i), "x": float(i + 1),
             "y": float((i * i) % 17 + 1), "z": float((i * 7) % 13 + 1),
             "w": float((i * 3) % 11 + 1)}
            for i in range(22)
        ]
        dataset = SimpleNamespace(rows=rows, metadata={"fixture": True})
        d0_catalog = {
            key: SimpleNamespace(compute=lambda row: 0.0)
            for key in nomination.D0_DESCRIPTOR_IDS
        }
        client = _FakeClient(formulas_by_round)
        evaluation_calls = []

        def evaluate(_dataset, descriptor_ids, _catalog, *, fixed_parameters=None, evaluate_test=True):
            evaluation_calls.append((tuple(descriptor_ids), evaluate_test, len(client.prompts)))
            result = {"selected_parameters": fixed_parameters or {},
                      "validation_topology_macro_mae_mol_kg": 10.0}
            if evaluate_test:
                result["test"] = {"topology_macro_mae_mol_kg": 10.0 if len(descriptor_ids) == 6 else 7.0}
            return result

        def validation(_rows, descriptor_ids, _catalog, _parameters):
            return scores[descriptor_ids[-1]]

        with tempfile.TemporaryDirectory() as temporary:
            geometry = Path(temporary) / "geometry.csv"
            geometry.write_text("fixture\n", encoding="utf-8")
            output = Path(temporary) / "result.json"
            with (
                patch.object(nomination, "load_adszeo", return_value=dataset),
                patch.object(nomination, "load_geometry", return_value=([], {row["structure_id"]: {} for row in rows})),
                patch.object(nomination, "adszeo_descriptor_catalog", return_value=d0_catalog),
                patch.object(nomination, "evaluate_adszeo", side_effect=evaluate),
                patch.object(nomination, "_validation_mae", side_effect=validation),
            ):
                result = nomination.run_adszeo_nomination_loop(
                    service=_FakeService(), database_path=Path(temporary) / "unused.duckdb",
                    geometry_csv=geometry, output_path=output, task="task", query="query",
                    budget=RetrievalBudget(candidate_limit=3, item_limit=1, context_token_budget=100),
                    modes=("agent",), client=client, score_only=score_only,
                    jev_judge=jev_judge,
                )
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["schema_version"], result["schema_version"])
        return result, client.prompts, evaluation_calls

    def test_three_rounds_accumulate_only_positive_marginal_winners(self):
        formulas = [
            [("a", "x+y"), ("b", "x*y"), ("c", "x/(y+1)")],
            [("a", "z+x"), ("b", "z*y"), ("c", "z/(x+1)")],
            [("a", "w+x"), ("b", "w*y"), ("c", "w/(z+1)")],
        ]
        scores = {"nom_r1_a": 9.0, "nom_r1_b": 8.0, "nom_r1_c": 9.5,
                  "nom_r2_a": 7.0, "nom_r2_b": 8.5, "nom_r2_c": 9.0,
                  "nom_r3_a": 7.2, "nom_r3_b": 6.0, "nom_r3_c": 6.5}
        result, prompts, evaluations = self._run(formulas, scores)
        mode = result["modes"]["agent"]
        selected = ["nom_r1_b", "nom_r2_a", "nom_r3_b"]
        self.assertEqual(mode["status"], "completed")
        self.assertEqual(mode["final_executed_descriptor_ids"], selected)
        self.assertEqual([record["retained_this_round"] for record in mode["rounds"]], selected)
        self.assertEqual([record["validation_after_topology_macro_mae_mol_kg"] for record in mode["rounds"]], [8.0, 7.0, 6.0])
        self.assertEqual(prompts[1]["retained_descriptors"][0]["descriptor_id"], selected[0])
        self.assertEqual(len(prompts[2]["retained_descriptors"]), 2)
        self.assertEqual(evaluations[-1][0], (*nomination.D0_DESCRIPTOR_IDS, *selected))
        self.assertFalse(evaluations[0][1])
        self.assertTrue(all(not evaluate_test or prompt_count == 3 for _, evaluate_test, prompt_count in evaluations))
        self.assertEqual(mode["topology_macro_mae_relative_improvement"], 0.3)

    def test_no_beneficial_or_executable_proposal_keeps_d0(self):
        formulas = [[("a", "unknown"), ("b", "x[0]"), ("c", "1")]] * 3
        result, prompts, evaluations = self._run(formulas, {})
        mode = result["modes"]["agent"]
        self.assertEqual(mode["status"], "completed")
        self.assertEqual(len(prompts), 3)
        self.assertEqual(mode["final_executed_descriptor_ids"], [])
        self.assertEqual([record["retained_this_round"] for record in mode["rounds"]], [None] * 3)
        self.assertEqual(mode["topology_macro_mae_relative_improvement"], 0.0)
        self.assertEqual([item[0] for item in evaluations], [nomination.D0_DESCRIPTOR_IDS] * 2)
        self.assertTrue({
            item["jev_recommendation"]
            for item in mode["rounds"][0]["execution_feedback"]
        } <= {"revise", "abandon"})

    def test_executable_but_unhelpful_round_does_not_force_an_addition(self):
        formulas = [
            [("a", "x+y"), ("b", "x*y"), ("c", "x/(y+1)")],
            [("a", "z+x"), ("b", "z*y"), ("c", "z/(x+1)")],
            [("a", "w+x"), ("b", "w*y"), ("c", "w/(z+1)")],
        ]
        scores = {"nom_r1_a": 9.0, "nom_r1_b": 8.0, "nom_r1_c": 9.5,
                  "nom_r2_a": 8.1, "nom_r2_b": 9.0, "nom_r2_c": 8.5,
                  "nom_r3_a": 7.0, "nom_r3_b": 7.5, "nom_r3_c": 8.1}
        result, prompts, _ = self._run(formulas, scores)
        mode = result["modes"]["agent"]
        self.assertEqual([record["retained_this_round"] for record in mode["rounds"]],
                         ["nom_r1_b", None, "nom_r3_a"])
        self.assertEqual(mode["final_executed_descriptor_ids"], ["nom_r1_b", "nom_r3_a"])
        self.assertEqual(len(prompts[2]["retained_descriptors"]), 1)
        self.assertEqual(mode["rounds"][1]["validation_after_topology_macro_mae_mol_kg"], 8.0)

    def test_single_score_reports_selected_validation_gain_without_test_evaluation(self):
        formulas = [
            [("a", "x+y"), ("b", "x*y"), ("c", "x/(y+1)")],
            [("a", "z+x"), ("b", "z*y"), ("c", "z/(x+1)")],
            [("a", "w+x"), ("b", "w*y"), ("c", "w/(z+1)")],
        ]
        scores = {"nom_r1_a": 9.0, "nom_r1_b": 8.0, "nom_r1_c": 9.5,
                  "nom_r2_a": 7.0, "nom_r2_b": 8.5, "nom_r2_c": 9.0,
                  "nom_r3_a": 7.2, "nom_r3_b": 6.0, "nom_r3_c": 6.5}
        result, _, evaluations = self._run(formulas, scores, score_only=True)
        mode = result["modes"]["agent"]
        self.assertEqual(result["evaluation_protocol"], "single_adaptive_score")
        self.assertEqual(result["outcome_split"], "validation")
        self.assertFalse(result["test_evaluated"])
        self.assertEqual(len(evaluations), 1)
        self.assertFalse(evaluations[0][1])
        self.assertEqual(mode["downstream"]["D0"]["validation_topology_macro_mae_mol_kg"], 10.0)
        self.assertEqual(mode["downstream"]["D0_plus_X"]["validation_topology_macro_mae_mol_kg"], 6.0)
        self.assertNotIn("test", mode["downstream"]["D0"])
        self.assertNotIn("test", mode["downstream"]["D0_plus_X"])
        self.assertEqual(mode["topology_macro_mae_relative_improvement"], 0.4)

    def test_single_score_retains_d0_when_no_proposal_helps(self):
        formulas = [[("a", "unknown"), ("b", "x[0]"), ("c", "1")]] * 3
        result, _, evaluations = self._run(formulas, {}, score_only=True)
        mode = result["modes"]["agent"]
        self.assertEqual(mode["final_executed_descriptor_ids"], [])
        self.assertEqual(mode["topology_macro_mae_relative_improvement"], 0.0)
        self.assertEqual(len(evaluations), 1)
        self.assertFalse(evaluations[0][1])

    def test_explicit_jev_gate_blocks_validation_and_strips_locked_test_fields(self):
        formulas = [[("a", "x+y"), ("b", "x*y"), ("c", "x/(y+1)")]] * 3
        scores = {"nom_r1_a": 9.0, "nom_r1_b": 8.0, "nom_r1_c": 9.5,
                  "nom_r2_a": 9.0, "nom_r2_b": 8.0, "nom_r2_c": 9.5,
                  "nom_r3_a": 9.0, "nom_r3_b": 8.0, "nom_r3_c": 9.5}
        jev = _DeferJev()
        result, _, evaluations = self._run(formulas, scores, jev_judge=jev)
        mode = result["modes"]["agent"]
        self.assertTrue(result["harness"]["enabled"])
        self.assertEqual(mode["harness"]["precompute_gate"], "enabled")
        # Baseline selection may use validation, but no proposal reaches the
        # candidate _validation_mae call after Jev returns defer.
        self.assertEqual(len(evaluations), 2)
        self.assertTrue(all("test" not in request["candidate"] for request in jev.requests))
        self.assertTrue(all("test_labels" not in request["run_context"] for request in jev.requests))
        self.assertEqual(mode["final_executed_descriptor_ids"], [])
        self.assertEqual(len(mode["harness"]["postcompute_rounds"]), 3)
        self.assertTrue(all(
            item.get("validation_skip_reason") == "jev_defer"
            for item in mode["rounds"][0]["execution_feedback"]
        ))


if __name__ == "__main__":
    unittest.main()
