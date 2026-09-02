from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.experiments.discovery_loop import (  # noqa: E402
    D0_DESCRIPTOR_IDS,
    build_discovery_prompt,
    run_discovery_loop,
    validate_discovery_output,
)
from catalysis_research.experiments.themecat_pilot import descriptor_catalog  # noqa: E402
from catalysis_research.models.glm import GlmResponse  # noqa: E402
from catalysis_research.retrieval import RetrievalBudget  # noqa: E402


class _FakeClient:
    def __init__(self, catalog: dict[str, object]) -> None:
        self.catalog = catalog
        self.calls: list[tuple[str, str, str]] = []

    def chat_json(self, *, model: str, system: str, user: str, **kwargs: object) -> GlmResponse:
        del kwargs
        payload = json.loads(user)
        mode = payload["knowledge_mode"]
        self.calls.append((mode, system, user))
        selected = ["inverse_temperature", "log_pressure", "pressure_over_ghsv"]
        data = {
            "evidence_chain": [] if mode == "agent" else [{
                "evidence_id": "E01",
                "role": "supporting",
                "claim": "The retrieved record reports a transport-related observation.",
            }],
            "hypothesis": "A process exposure descriptor captures a measurable rate trend.",
            "descriptor_candidates": [
                {
                    "descriptor_id": item,
                    "rationale": "It represents a computable process exposure.",
                    "expected_direction": "positive",
                    "falsification_criteria": "The effect disappears in the pre-registered OOD split.",
                }
                for item in selected
            ],
            "selected_descriptor_ids": selected,
            "expected_direction": "positive",
            "falsification_criteria": ["The paired OOD delta is non-positive."],
            "epistemic_status": "insufficient_evidence" if mode == "agent" else "tentative",
        }
        return GlmResponse(
            structured=data,
            raw={"id": f"fake-{mode}", "model": model, "usage": {"total_tokens": 42}},
            provider="fake",
            model=model,
            usage={"total_tokens": 42},
        )


class _FakeService:
    source_identities = {"rag": {}, "small_kg": {}, "normalization": {}}

    def retrieve(self, *, query: str, experiment_mode: str, budget: RetrievalBudget) -> dict[str, object]:
        return {
            "knowledge_mode": "none" if experiment_mode == "agent" else "rag",
            "query": query,
            "budget": budget.__dict__,
            "items": [] if experiment_mode == "agent" else [{"paper_id": "p1"}],
            "context": "" if experiment_mode == "agent" else "[E01 | paper=p1 | document=d1 | type=main | locator=pdf_page:1] Evidence.",
            "selected_token_count": 10,
            "bundle_hash": f"bundle-{experiment_mode}",
        }


class DiscoveryLoopTests(unittest.TestCase):
    def test_validation_rejects_d0_as_new_descriptor(self) -> None:
        catalog = descriptor_catalog()
        value = {
            "evidence_chain": [],
            "hypothesis": "A test hypothesis.",
            "descriptor_candidates": [
                {
                    "descriptor_id": item,
                    "rationale": "r",
                    "expected_direction": "positive",
                    "falsification_criteria": "f",
                }
                for item in [D0_DESCRIPTOR_IDS[0], "log_pressure", "pressure_over_ghsv"]
            ],
            "selected_descriptor_ids": [D0_DESCRIPTOR_IDS[0], "log_pressure", "pressure_over_ghsv"],
            "expected_direction": "positive",
            "falsification_criteria": ["f"],
            "epistemic_status": "tentative",
        }
        with self.assertRaisesRegex(ValueError, "D0"):
            validate_discovery_output(value, catalog)

    def test_prompt_has_same_schema_and_no_row_level_data(self) -> None:
        catalog = descriptor_catalog()
        system_a, user_a = build_discovery_prompt(
            task="task", query="query", knowledge_mode="agent", evidence_context="", catalog=catalog
        )
        system_b, user_b = build_discovery_prompt(
            task="task", query="query", knowledge_mode="rag_agent", evidence_context="E01 evidence", catalog=catalog
        )
        self.assertEqual(system_a, system_b)
        self.assertNotIn("STY_g_per_gcath:  ", user_a)
        self.assertEqual(json.loads(user_a)["baseline_descriptor_ids_D0"], list(D0_DESCRIPTOR_IDS))
        self.assertEqual(json.loads(user_b)["descriptor_selection"]["selected_budget"], 3)

    def test_three_modes_share_budget_and_emit_paired_downstream_results(self) -> None:
        raw = RESEARCH_ROOT / "datasets" / "raw" / "TheMeCat_v1.csv"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run.json"
            client = _FakeClient(descriptor_catalog())
            result = run_discovery_loop(
                service=_FakeService(),  # type: ignore[arg-type]
                raw_path=raw,
                output_path=output,
                task="task",
                query="query",
                budget=RetrievalBudget(candidate_limit=6, item_limit=2, context_token_budget=300),
                client=client,  # type: ignore[arg-type]
            )
            written_schema = json.loads(output.read_text(encoding="utf-8"))["schema_version"]
        self.assertEqual(set(result["modes"]), {"agent", "rag_agent", "small_kg_rag_agent"})
        self.assertTrue(all(row["status"] == "completed" for row in result["modes"].values()))
        self.assertEqual(len(client.calls), 3)
        self.assertEqual(len({call[1] for call in client.calls}), 1)
        self.assertEqual(
            {
                tuple(
                    result["modes"][mode]["bundle"]["budget"][field]
                    for field in ("candidate_limit", "item_limit", "context_token_budget")
                )
                for mode in result["modes"]
            },
            {(6, 2, 300)},
        )
        for row in result["modes"].values():
            self.assertIn("D0", row["downstream"])
            self.assertIn("D0_plus_X", row["downstream"])
            self.assertEqual(len(row["generation"]["selected_descriptor_ids"]), 3)
        self.assertEqual(written_schema, result["schema_version"])


if __name__ == "__main__":
    unittest.main()
