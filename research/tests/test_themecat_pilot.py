from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.datasets.themecat import adapt_rows, audit_rows, catalyst_family
from catalysis_research.experiments.themecat_pilot import descriptor_catalog, validate_selection


class TheMeCatPilotTests(unittest.TestCase):
    def test_adapter_removes_blank_and_missing_target_rows(self) -> None:
        rows = [
            {"reference": "paper", "doi_link": "https://doi.org/10.1/x", "active_comp_1": "Cu", "STY_g_per_gcath": "1.5"},
            {"reference": "paper", "doi_link": "10.1/x", "active_comp_1": "Cu", "STY_g_per_gcath": "NA"},
            {"reference": "", "doi_link": "", "active_comp_1": "", "STY_g_per_gcath": ""},
        ]
        adapted = adapt_rows(rows)
        self.assertEqual(len(adapted), 1)
        self.assertEqual(adapted[0]["sample_id"], "themecat-v1-row-0002")
        self.assertEqual(adapted[0]["source_group"], "10.1/x")
        self.assertEqual(adapted[0]["catalyst_family"], "copper")

    def test_family_mapping_is_frozen_and_deterministic(self) -> None:
        self.assertEqual(catalyst_family("In2O3"), "indium_oxide")
        self.assertEqual(catalyst_family("NA"), "unknown")
        self.assertEqual(catalyst_family("LaMn0.3Cu0.7O3"), "lanthanum_manganite")

    def test_catalog_has_exact_fixed_candidate_budget(self) -> None:
        catalog = descriptor_catalog()
        self.assertEqual(len(catalog), 30)
        self.assertEqual(len(set(catalog)), 30)

    def test_selection_rejects_mismatch_between_rank_and_selected(self) -> None:
        catalog = descriptor_catalog()
        identifiers = list(catalog)
        value = {
            "hypothesis": "Process descriptors should transfer.",
            "candidates": [
                {"rank": index, "descriptor_id": descriptor_id, "rationale": "test"}
                for index, descriptor_id in enumerate(identifiers, start=1)
            ],
            "selected_descriptor_ids": identifiers[:10],
        }
        self.assertEqual(validate_selection(value, catalog), identifiers[:10])
        value["selected_descriptor_ids"] = identifiers[1:11]
        with self.assertRaises(ValueError):
            validate_selection(value, catalog)


if __name__ == "__main__":
    unittest.main()
