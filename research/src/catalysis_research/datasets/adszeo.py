"""Leakage-aware adapter for the AdsZeo methane adsorption dataset."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


TARGET_COLUMN = "loading_mol_kg"
EXPECTED_STRUCTURE_COUNT = 4775
EXPECTED_TOPOLOGY_COUNT = 191
EXPECTED_PRESSURES_PER_STRUCTURE = 13
EXPECTED_RUN_COUNT = EXPECTED_STRUCTURE_COUNT * EXPECTED_PRESSURES_PER_STRUCTURE
SPLIT_SEED = 20260902

REQUIRED_COLUMNS = {
    "structures": {
        "structure_id", "framework_code", "cell_a", "cell_b", "cell_c",
        "cell_alpha", "cell_beta", "cell_gamma", "si_count", "al_count_cif",
    },
    "framework_atoms": {
        "structure_id", "atom_index", "element", "frac_x", "frac_y", "frac_z",
    },
    "runs": {
        "run_id", "structure_id", "framework_code", "pressure_pa_path",
        "temperature_k", "helium_void_fraction",
    },
    "isotherms": {"run_id", "component", "loading_type", "unit", "value"},
}


class AdsZeoError(RuntimeError):
    """Raised when the frozen AdsZeo data contract is violated."""


@dataclass(frozen=True)
class AdsZeoDataset:
    rows: list[dict[str, Any]]
    metadata: dict[str, Any]


def stable_topology_split(
    framework_codes: set[str] | list[str] | tuple[str, ...],
    *,
    seed: int = SPLIT_SEED,
) -> dict[str, str]:
    """Assign whole topologies to an exact 80/10/10 split reproducibly."""
    codes = sorted(set(framework_codes))
    if len(codes) < 3:
        raise AdsZeoError("At least three framework topologies are required")
    ranked = sorted(
        codes,
        key=lambda code: hashlib.sha256(f"{seed}:{code}".encode("utf-8")).hexdigest(),
    )
    test_count = max(1, round(len(ranked) * 0.10))
    validation_count = max(1, round(len(ranked) * 0.10))
    test = set(ranked[:test_count])
    validation = set(ranked[test_count : test_count + validation_count])
    return {
        code: "test" if code in test else "validation" if code in validation else "train"
        for code in codes
    }


def _cell_matrix(record: dict[str, Any]) -> np.ndarray:
    a, b, c = (float(record[f"cell_{axis}"]) for axis in "abc")
    alpha, beta, gamma = np.deg2rad(
        [float(record["cell_alpha"]), float(record["cell_beta"]), float(record["cell_gamma"])]
    )
    sin_gamma = math.sin(gamma)
    if abs(sin_gamma) < 1e-12:
        raise AdsZeoError(f"Degenerate cell for {record['structure_id']}")
    va = np.array([a, 0.0, 0.0])
    vb = np.array([b * math.cos(gamma), b * sin_gamma, 0.0])
    cx = c * math.cos(beta)
    cy = c * (math.cos(alpha) - math.cos(beta) * math.cos(gamma)) / sin_gamma
    cz = math.sqrt(max(c * c - cx * cx - cy * cy, 0.0))
    return np.vstack([va, vb, [cx, cy, cz]])


def _cell_volume(record: dict[str, Any]) -> float:
    return float(abs(np.linalg.det(_cell_matrix(record))))


def _al_spatial_features(record: dict[str, Any], fractional: np.ndarray) -> dict[str, float]:
    if fractional.shape[0] < 2:
        return {
            "al_nn_mean_a": float("nan"),
            "al_nn_std_a": float("nan"),
            "al_nn_min_a": float("nan"),
            "al_pair_mean_a": float("nan"),
            "al_pair_std_a": float("nan"),
            "al_close_pair_fraction_5a": float("nan"),
            "al_close_pair_fraction_8a": float("nan"),
            "al_clustering_index": float("nan"),
        }
    delta = fractional[:, None, :] - fractional[None, :, :]
    delta -= np.rint(delta)
    distance = np.linalg.norm(delta @ _cell_matrix(record), axis=2)
    np.fill_diagonal(distance, np.inf)
    nearest = np.min(distance, axis=1)
    pairs = distance[np.triu_indices(distance.shape[0], k=1)]
    expected_spacing = (float(record["cell_volume"]) / fractional.shape[0]) ** (1.0 / 3.0)
    return {
        "al_nn_mean_a": float(np.mean(nearest)),
        "al_nn_std_a": float(np.std(nearest)),
        "al_nn_min_a": float(np.min(nearest)),
        "al_pair_mean_a": float(np.mean(pairs)),
        "al_pair_std_a": float(np.std(pairs)),
        "al_close_pair_fraction_5a": float(np.mean(pairs < 5.0)),
        "al_close_pair_fraction_8a": float(np.mean(pairs < 8.0)),
        "al_clustering_index": float(np.mean(nearest) / max(expected_spacing, 1e-12)),
    }


def _connect_read_only(database_path: Path):
    try:
        import duckdb
    except ImportError as error:
        raise AdsZeoError("duckdb is required to read AdsZeo_data.duckdb") from error
    if not database_path.is_file():
        raise AdsZeoError(f"AdsZeo database not found: {database_path}")
    return duckdb.connect(str(database_path), read_only=True)


def preflight_adszeo(database_path: Path, *, strict: bool = True) -> dict[str, Any]:
    """Check the small benchmark contract without reading outcome-derived tables."""
    connection = _connect_read_only(database_path)
    try:
        schema_rows = connection.execute(
            """
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_name IN ('structures', 'framework_atoms', 'runs', 'isotherms')
            """
        ).fetchall()
        available: dict[str, set[str]] = {}
        for table_name, column_name in schema_rows:
            available.setdefault(str(table_name), set()).add(str(column_name))
        missing = {
            table: sorted(columns - available.get(table, set()))
            for table, columns in REQUIRED_COLUMNS.items()
            if columns - available.get(table, set())
        }
        if missing:
            raise AdsZeoError(f"AdsZeo schema mismatch: missing={missing}")

        structure_count, topology_count = connection.execute(
            "SELECT count(*), count(DISTINCT framework_code) FROM structures"
        ).fetchone()
        run_count, pressure_count = connection.execute(
            "SELECT count(*), count(DISTINCT pressure_pa_path) FROM runs"
        ).fetchone()
        target_count, target_structure_count = connection.execute(
            """
            SELECT count(*), count(DISTINCT r.structure_id)
            FROM runs r
            JOIN isotherms i USING (run_id)
            WHERE lower(i.component) = 'methane'
              AND i.loading_type = 'absolute'
              AND i.unit = 'mol/kg framework'
            """
        ).fetchone()
        incomplete_structure_count = connection.execute(
            """
            SELECT count(*) FROM (
                SELECT r.structure_id, count(*) AS n
                FROM runs r
                JOIN isotherms i USING (run_id)
                WHERE lower(i.component) = 'methane'
                  AND i.loading_type = 'absolute'
                  AND i.unit = 'mol/kg framework'
                GROUP BY r.structure_id
                HAVING count(*) <> ?
            )
            """,
            [EXPECTED_PRESSURES_PER_STRUCTURE],
        ).fetchone()[0]
    finally:
        connection.close()

    counts = {
        "structures": int(structure_count),
        "topologies": int(topology_count),
        "runs": int(run_count),
        "distinct_pressures": int(pressure_count),
        "methane_absolute_targets": int(target_count),
        "target_structures": int(target_structure_count),
        "incomplete_target_structures": int(incomplete_structure_count),
    }
    canonical = (
        counts["structures"] == EXPECTED_STRUCTURE_COUNT
        and counts["topologies"] == EXPECTED_TOPOLOGY_COUNT
        and counts["runs"] == EXPECTED_RUN_COUNT
        and counts["methane_absolute_targets"] == EXPECTED_RUN_COUNT
        and counts["target_structures"] == EXPECTED_STRUCTURE_COUNT
        and counts["incomplete_target_structures"] == 0
    )
    if strict and not canonical:
        raise AdsZeoError(f"AdsZeo cardinality mismatch: {counts}")
    return {
        "valid": not missing and (canonical or not strict),
        "canonical_cardinality": canonical,
        "counts": counts,
        "queried_tables": sorted(REQUIRED_COLUMNS),
        "forbidden_tables_not_queried": ["positions", "cycle_stats"],
    }


def load_adszeo(database_path: Path, *, strict: bool = True) -> AdsZeoDataset:
    """Load only pre-simulation structure fields and scalar methane targets.

    The billion-row ``positions`` table and outcome-derived ``cycle_stats`` table
    are intentionally never queried.
    """
    connection = _connect_read_only(database_path)
    try:
        structures_frame = connection.execute(
            """
            SELECT structure_id, framework_code, cell_a, cell_b, cell_c,
                   cell_alpha, cell_beta, cell_gamma, si_count, al_count_cif
            FROM structures
            ORDER BY structure_id
            """
        ).fetchdf()
        al_frame = connection.execute(
            """
            SELECT structure_id, frac_x, frac_y, frac_z
            FROM framework_atoms
            WHERE element = 'Al'
            ORDER BY structure_id, atom_index
            """
        ).fetchdf()
        targets_frame = connection.execute(
            """
            SELECT r.run_id, r.structure_id, r.framework_code,
                   r.pressure_pa_path::DOUBLE / 100000.0 AS pressure_bar,
                   r.temperature_k, r.helium_void_fraction,
                   i.value::DOUBLE AS loading_mol_kg
            FROM runs r
            JOIN isotherms i USING (run_id)
            WHERE lower(i.component) = 'methane'
              AND i.loading_type = 'absolute'
              AND i.unit = 'mol/kg framework'
            ORDER BY r.structure_id, r.pressure_pa_path
            """
        ).fetchdf()
    finally:
        connection.close()

    structures: dict[str, dict[str, Any]] = {}
    for _, row in structures_frame.iterrows():
        record = row.to_dict()
        record["cell_volume"] = _cell_volume(record)
        structures[str(row["structure_id"])] = record
    al_by_structure = {
        str(structure_id): group[["frac_x", "frac_y", "frac_z"]].to_numpy(dtype=float)
        for structure_id, group in al_frame.groupby("structure_id", sort=False)
    }
    if set(al_by_structure) - set(structures):
        raise AdsZeoError("framework_atoms contains unknown structure IDs")

    spatial = {
        structure_id: _al_spatial_features(
            record, al_by_structure.get(structure_id, np.empty((0, 3), dtype=float))
        )
        for structure_id, record in structures.items()
    }
    split = stable_topology_split(set(map(str, structures_frame["framework_code"])))
    rows: list[dict[str, Any]] = []
    for _, target in targets_frame.iterrows():
        structure_id = str(target["structure_id"])
        if structure_id not in structures:
            raise AdsZeoError(f"Target references unknown structure: {structure_id}")
        record = {**structures[structure_id], **spatial[structure_id], **target.to_dict()}
        record["structure_id"] = structure_id
        record["framework_code"] = str(record["framework_code"])
        record["split"] = split[record["framework_code"]]
        rows.append(record)

    pressure_counts: dict[str, int] = {}
    for row in rows:
        pressure_counts[row["structure_id"]] = pressure_counts.get(row["structure_id"], 0) + 1
        if not math.isfinite(float(row[TARGET_COLUMN])) or float(row[TARGET_COLUMN]) < 0:
            raise AdsZeoError("AdsZeo contains a non-finite or negative methane loading")
    incomplete = sorted(
        key for key, count in pressure_counts.items() if count != EXPECTED_PRESSURES_PER_STRUCTURE
    )
    topology_count = len(split)
    if strict and (
        len(structures) != EXPECTED_STRUCTURE_COUNT
        or topology_count != EXPECTED_TOPOLOGY_COUNT
        or len(rows) != EXPECTED_RUN_COUNT
        or incomplete
    ):
        raise AdsZeoError(
            "AdsZeo cardinality mismatch: "
            f"structures={len(structures)}, topologies={topology_count}, rows={len(rows)}, "
            f"incomplete_structures={len(incomplete)}"
        )

    split_topologies = {
        name: sorted(code for code, assigned in split.items() if assigned == name)
        for name in ("train", "validation", "test")
    }
    return AdsZeoDataset(
        rows=rows,
        metadata={
            "name": "AdsZeo v1",
            "record": "10.5281/zenodo.21445386",
            "target": TARGET_COLUMN,
            "target_unit": "mol/kg framework",
            "structure_count": len(structures),
            "topology_count": topology_count,
            "row_count": len(rows),
            "pressures_per_structure": EXPECTED_PRESSURES_PER_STRUCTURE,
            "temperature_k": sorted({float(row["temperature_k"]) for row in rows}),
            "split_algorithm": "sha256_topology_rank_80_10_10.v1",
            "split_seed": SPLIT_SEED,
            "split_topologies": split_topologies,
            "license": "CC BY 4.0",
            "forbidden_feature_tables": ["positions", "cycle_stats"],
        },
    )
