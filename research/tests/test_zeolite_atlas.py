from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.datasets.materialscloud import load_zeolite_atlas  # noqa: E402
from catalysis_research.experiments.zeolite_atlas import (  # noqa: E402
    D0_DESCRIPTOR_IDS,
    atlas_descriptor_catalog,
    evaluate_atlas,
)


class ZeoliteAtlasTests(unittest.TestCase):
    def test_loader_aggregates_atom_rows_and_preserves_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "archive"
            (root / "DEEM_1k_Angles").mkdir(parents=True)
            (root / "DEEM_1k_Distances").mkdir()
            (root / "DEEM_1k_King_Distribution").mkdir()
            (root / "DEEM_1k_6.0A").mkdir()
            (root / "ids_natoms_1k.dat").write_text(
                "PCOD8000000\t2\nPCOD8000001\t2\n", encoding="utf-8"
            )
            np.savetxt(root / "DEEM_1k_Angles" / "angles.dat", np.ones((4, 4)))
            np.savetxt(root / "DEEM_1k_Distances" / "distances.dat", np.ones((4, 4)) * 2)
            np.savetxt(root / "DEEM_1k_King_Distribution" / "rings.dat", np.ones((4, 20)))
            np.savetxt(root / "DEEM_1k_6.0A" / "kpca100.dat", np.ones((4, 100)))
            np.savetxt(root / "DEEM_1k_6.0A" / "energies.dat", np.arange(4) + 1)
            np.savetxt(root / "DEEM_1k_6.0A" / "volumes.dat", np.arange(4) + 10)
            dataset = load_zeolite_atlas(Path(temporary))
        self.assertEqual(len(dataset.rows), 2)
        self.assertEqual(dataset.rows[0]["sample_id"], "PCOD8000000")
        self.assertEqual(dataset.energy.tolist(), [3.0, 7.0])
        self.assertEqual(dataset.volume.tolist(), [21.0, 25.0])
        self.assertEqual(len(atlas_descriptor_catalog()), 40)

    def test_structure_id_split_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "archive"
            for name in (
                "DEEM_1k_Angles",
                "DEEM_1k_Distances",
                "DEEM_1k_King_Distribution",
                "DEEM_1k_6.0A",
            ):
                (root / name).mkdir(parents=True)
            (root / "ids_natoms_1k.dat").write_text(
                "".join(f"PCOD80000{index:02d}\t2\n" for index in range(10)), encoding="utf-8"
            )
            atom_count = 20
            np.savetxt(root / "DEEM_1k_Angles" / "angles.dat", np.ones((atom_count, 4)))
            np.savetxt(root / "DEEM_1k_Distances" / "distances.dat", np.ones((atom_count, 4)))
            np.savetxt(root / "DEEM_1k_King_Distribution" / "rings.dat", np.ones((atom_count, 20)))
            np.savetxt(root / "DEEM_1k_6.0A" / "kpca100.dat", np.ones((atom_count, 100)))
            np.savetxt(root / "DEEM_1k_6.0A" / "energies.dat", np.arange(atom_count) + 1)
            np.savetxt(root / "DEEM_1k_6.0A" / "volumes.dat", np.arange(atom_count) + 10)
            dataset = load_zeolite_atlas(Path(temporary))
            first = evaluate_atlas(dataset, D0_DESCRIPTOR_IDS, atlas_descriptor_catalog())
            second = evaluate_atlas(dataset, D0_DESCRIPTOR_IDS, atlas_descriptor_catalog())
        self.assertEqual(first["split"], second["split"])
        self.assertEqual(first["targets"]["energy"]["test_rows"], 2)
        self.assertEqual(first["targets"]["energy"]["validation_rows"], 2)


if __name__ == "__main__":
    unittest.main()
