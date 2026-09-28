from __future__ import annotations

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import duckdb


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.datasets.adszeo import AdsZeoError, load_adszeo, preflight_adszeo  # noqa: E402
from catalysis_research.experiments.adszeo import (  # noqa: E402
    D0_DESCRIPTOR_IDS,
    adszeo_descriptor_catalog,
    evaluate_adszeo,
    run_adszeo_loop,
)
from catalysis_research.models.glm import GlmResponse  # noqa: E402
from catalysis_research.retrieval import RetrievalBudget  # noqa: E402


def _synthetic_database(path: Path) -> None:
    connection = duckdb.connect(str(path))
    connection.execute(
        """CREATE TABLE structures (
        structure_id VARCHAR, framework_code VARCHAR, cell_a DOUBLE, cell_b DOUBLE,
        cell_c DOUBLE, cell_alpha DOUBLE, cell_beta DOUBLE, cell_gamma DOUBLE,
        cell_volume DOUBLE, si_count INTEGER, al_count_cif INTEGER, o_count INTEGER,
        si_al_ratio DOUBLE)"""
    )
    connection.execute(
        """CREATE TABLE framework_atoms (
        structure_id VARCHAR, atom_index INTEGER, element VARCHAR,
        frac_x DOUBLE, frac_y DOUBLE, frac_z DOUBLE)"""
    )
    connection.execute(
        """CREATE TABLE runs (
        run_id VARCHAR, structure_id VARCHAR, framework_code VARCHAR,
        pressure_pa_path DOUBLE, temperature_k DOUBLE,
        helium_void_fraction DOUBLE, parse_status VARCHAR)"""
    )
    connection.execute(
        """CREATE TABLE isotherms (
        run_id VARCHAR, component VARCHAR, loading_type VARCHAR,
        unit VARCHAR, value DOUBLE)"""
    )
    pressures = [10 ** (-1 + index * 3 / 12) for index in range(13)]
    for topology_index in range(10):
        framework = f"T{topology_index:02d}"
        for variant in range(2):
            structure_id = f"{framework}_{variant}"
            al_count = 2 + variant
            cell_a = 20.0 + topology_index * 0.2
            cell_b = 21.0 + variant
            cell_c = 22.0
            volume = cell_a * cell_b * cell_c
            connection.execute(
                "INSERT INTO structures VALUES (?, ?, ?, ?, ?, 90, 90, 90, ?, 30, ?, 64, ?)",
                [structure_id, framework, cell_a, cell_b, cell_c, volume, al_count, 30 / al_count],
            )
            for atom_index in range(al_count):
                connection.execute(
                    "INSERT INTO framework_atoms VALUES (?, ?, 'Al', ?, ?, ?)",
                    [structure_id, atom_index, 0.1 + 0.3 * atom_index, 0.2, 0.3 + 0.1 * variant],
                )
            void_fraction = 0.20 + topology_index * 0.015 + variant * 0.01
            for pressure_index, pressure in enumerate(pressures):
                run_id = f"{structure_id}_{pressure_index}"
                loading = (1.5 + 6 * void_fraction + 0.1 * al_count) * math.log1p(pressure)
                connection.execute(
                    "INSERT INTO runs VALUES (?, ?, ?, ?, 298, ?, 'ok')",
                    [run_id, structure_id, framework, pressure * 100000, void_fraction],
                )
                connection.execute(
                    "INSERT INTO isotherms VALUES (?, 'methane', 'absolute', 'mol/kg framework', ?)",
                    [run_id, loading],
                )
    connection.close()


class _FakeService:
    source_identities = {"rag": {}, "small_kg": {}, "normalization": {}}

    def retrieve(self, *, query: str, experiment_mode: str, budget: RetrievalBudget) -> dict[str, object]:
        has_evidence = experiment_mode != "agent"
        return {
            "query": query,
            "budget": budget.__dict__,
            "items": [{"paper_id": "p1"}] if has_evidence else [],
            "context": "[1 | paper=p1 | document=d1]\nAluminium siting affects adsorption." if has_evidence else "",
            "bundle_hash": experiment_mode,
        }


class _FakeClient:
    def chat_json(self, *, model: str, user: str, **kwargs: object) -> GlmResponse:
        del kwargs
        mode = json.loads(user)["knowledge_mode"]
        selected = ["al_nn_mean", "al_close_pair_fraction_8a", "pressure_al_fraction"]
        structured = {
            "evidence_chain": [] if mode == "agent" else [{"evidence_id": "E01", "role": "supporting", "claim": "Aluminium siting affects adsorption."}],
            "hypothesis": "Al spacing and pressure jointly control methane loading.",
            "descriptor_candidates": [
                {"descriptor_id": item, "rationale": "Computable before adsorption.", "expected_direction": "nonlinear", "falsification_criteria": "No held-out improvement."}
                for item in selected
            ],
            "selected_descriptor_ids": selected,
            "expected_direction": "nonlinear",
            "falsification_criteria": ["Topology-macro MAE does not improve."],
            "epistemic_status": "insufficient_evidence" if mode == "agent" else "tentative",
        }
        return GlmResponse(structured=structured, raw={"id": mode}, provider="fake", model=model, usage={"total_tokens": 1})


class AdsZeoTests(unittest.TestCase):
    def test_loader_uses_topology_split_and_needs_no_outcome_derived_tables(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "adszeo.duckdb"
            _synthetic_database(database)
            dataset = load_adszeo(database, strict=False)
        self.assertEqual(len(dataset.rows), 260)
        self.assertEqual(dataset.metadata["pressures_per_structure"], 13)
        by_topology: dict[str, set[str]] = {}
        for row in dataset.rows:
            by_topology.setdefault(row["framework_code"], set()).add(row["split"])
        self.assertTrue(all(len(partitions) == 1 for partitions in by_topology.values()))
        self.assertTrue(math.isfinite(dataset.rows[0]["al_nn_mean_a"]))

    def test_strict_loader_rejects_noncanonical_cardinality(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "adszeo.duckdb"
            _synthetic_database(database)
            with self.assertRaisesRegex(AdsZeoError, "cardinality mismatch"):
                load_adszeo(database)

    def test_preflight_reports_noncanonical_fixture_without_large_tables(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "adszeo.duckdb"
            _synthetic_database(database)
            report = preflight_adszeo(database, strict=False)
        self.assertTrue(report["valid"])
        self.assertFalse(report["canonical_cardinality"])
        self.assertEqual(report["counts"]["methane_absolute_targets"], 260)
        self.assertEqual(report["forbidden_tables_not_queried"], ["positions", "cycle_stats"])

    def test_d0_parameters_are_reused_for_d0_plus_x(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "adszeo.duckdb"
            _synthetic_database(database)
            dataset = load_adszeo(database, strict=False)
            catalog = adszeo_descriptor_catalog()
            selection_only = evaluate_adszeo(dataset, D0_DESCRIPTOR_IDS, catalog, evaluate_test=False)
            d0 = evaluate_adszeo(dataset, D0_DESCRIPTOR_IDS, catalog)
            d1 = evaluate_adszeo(
                dataset,
                (*D0_DESCRIPTOR_IDS, "al_nn_mean"),
                catalog,
                fixed_parameters=d0["selected_parameters"],
            )
        self.assertEqual(d0["selected_parameters"], d1["selected_parameters"])
        self.assertEqual(selection_only["selected_parameters"], d0["selected_parameters"])
        self.assertNotIn("test", selection_only)
        self.assertTrue(math.isfinite(d1["test"]["topology_macro_mae_mol_kg"]))

    def test_three_mode_loop_runs_on_synthetic_database(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "adszeo.duckdb"
            output = Path(temporary) / "run.json"
            _synthetic_database(database)
            result = run_adszeo_loop(
                service=_FakeService(),  # type: ignore[arg-type]
                database_path=database,
                output_path=output,
                task="task",
                query="query",
                budget=RetrievalBudget(candidate_limit=3, item_limit=1, context_token_budget=100),
                strict_dataset=False,
                client=_FakeClient(),  # type: ignore[arg-type]
            )
        self.assertTrue(all(value["status"] == "completed" for value in result["modes"].values()))
        self.assertEqual(result["baseline_D0"]["selected_parameters"], result["modes"]["agent"]["downstream"]["D0_plus_X"]["selected_parameters"])


if __name__ == "__main__":
    unittest.main()
