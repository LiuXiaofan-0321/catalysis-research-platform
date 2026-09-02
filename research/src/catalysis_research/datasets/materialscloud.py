"""Adapter for the public Materials Cloud Zeolite Atlas v1 archive.

The archive stores per-Si-atom descriptors and per-atom energy/volume
contributions. This adapter aggregates those rows to structure-level records
using the supplied ``ids_natoms_1k.dat`` mapping. It never reads a locked
outcome during descriptor generation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


class MaterialsCloudError(RuntimeError):
    """Raised when the Zeolite Atlas archive violates its file contract."""


@dataclass(frozen=True)
class ZeoliteAtlasDataset:
    rows: list[dict[str, str]]
    energy: np.ndarray
    volume: np.ndarray
    metadata: dict[str, Any]


def _matrix(path: Path, *, expected_rows: int | None = None) -> np.ndarray:
    if not path.exists():
        raise MaterialsCloudError(f"Missing Materials Cloud file: {path}")
    try:
        values = np.loadtxt(path, ndmin=2)
    except (OSError, ValueError) as error:
        raise MaterialsCloudError(f"Cannot parse Materials Cloud file: {path}") from error
    if expected_rows is not None and values.shape[0] != expected_rows:
        raise MaterialsCloudError(
            f"Row count mismatch for {path.name}: {values.shape[0]} != {expected_rows}"
        )
    if not np.isfinite(values).all():
        raise MaterialsCloudError(f"Non-finite values in Materials Cloud file: {path}")
    return values


def _ids(path: Path) -> tuple[list[str], list[int]]:
    identifiers: list[str] = []
    natoms: list[int] = []
    with path.open("r", encoding="utf-8") as source:
        for line in source:
            fields = line.split()
            if not fields:
                continue
            if len(fields) < 2 or not re.fullmatch(r"\d+", fields[1]):
                raise MaterialsCloudError(f"Invalid ids_natoms row: {line.rstrip()}")
            identifiers.append(fields[0])
            natoms.append(int(fields[1]))
    if not identifiers or any(value < 1 for value in natoms):
        raise MaterialsCloudError("ids_natoms_1k.dat contains no valid structures")
    if len(set(identifiers)) != len(identifiers):
        raise MaterialsCloudError("Duplicate structure IDs in ids_natoms_1k.dat")
    return identifiers, natoms


def _mean_std(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return np.mean(values, axis=0), np.std(values, axis=0)


def _feature_row(
    structure_id: str,
    angles: np.ndarray,
    distances: np.ndarray,
    rings: np.ndarray,
    soap: np.ndarray,
) -> dict[str, str]:
    angle_mean, angle_std = _mean_std(angles)
    distance_mean, distance_std = _mean_std(distances)
    ring_mean, _ = _mean_std(rings)
    soap_mean, soap_std = _mean_std(soap)
    ring_total = float(np.sum(np.maximum(ring_mean, 0.0)))
    probabilities = np.maximum(ring_mean, 0.0) / max(ring_total, 1e-12)
    ring_entropy = float(-np.sum(probabilities * np.log(np.maximum(probabilities, 1e-12))))
    row: dict[str, str] = {"sample_id": structure_id}
    for index, value in enumerate(angle_mean):
        row[f"angles_mean_{index}"] = str(float(value))
    for index, value in enumerate(angle_std):
        row[f"angles_std_{index}"] = str(float(value))
    for index, value in enumerate(distance_mean):
        row[f"distances_mean_{index}"] = str(float(value))
    for index, value in enumerate(distance_std):
        row[f"distances_std_{index}"] = str(float(value))
    for index, value in enumerate(ring_mean):
        row[f"ring_mean_{index}"] = str(float(value))
    row["ring_entropy"] = str(ring_entropy)
    row["ring_nonzero_fraction"] = str(float(np.mean(ring_mean > 0)))
    for index in range(min(8, soap_mean.size)):
        row[f"soap6_pc{index + 1}_mean"] = str(float(soap_mean[index]))
        row[f"soap6_pc{index + 1}_std"] = str(float(soap_std[index]))
    row["soap6_variability"] = str(float(np.mean(soap_std)))
    return row


def load_zeolite_atlas(root: Path, *, subset: str = "1k", cutoff: str = "6.0A") -> ZeoliteAtlasDataset:
    """Load the 1k structure-level view from an extracted archive directory."""
    archive = root / "archive" if (root / "archive").exists() else root
    if subset != "1k" or cutoff not in {"3.5A", "6.0A"}:
        raise MaterialsCloudError("Only the frozen 1k, 3.5A/6.0A view is supported")
    identifiers, natoms = _ids(archive / "ids_natoms_1k.dat")
    atom_count = sum(natoms)
    angles = _matrix(archive / "DEEM_1k_Angles" / "angles.dat", expected_rows=atom_count)
    distances = _matrix(archive / "DEEM_1k_Distances" / "distances.dat", expected_rows=atom_count)
    rings = _matrix(archive / "DEEM_1k_King_Distribution" / "rings.dat", expected_rows=atom_count)
    soap = _matrix(archive / f"DEEM_1k_{cutoff}" / "kpca100.dat", expected_rows=atom_count)
    energy = _matrix(archive / f"DEEM_1k_{cutoff}" / "energies.dat", expected_rows=atom_count).reshape(-1)
    volume = _matrix(archive / f"DEEM_1k_{cutoff}" / "volumes.dat", expected_rows=atom_count).reshape(-1)
    rows: list[dict[str, str]] = []
    energy_totals: list[float] = []
    volume_totals: list[float] = []
    offset = 0
    for structure_id, count in zip(identifiers, natoms):
        end = offset + count
        rows.append(_feature_row(structure_id, angles[offset:end], distances[offset:end], rings[offset:end], soap[offset:end]))
        energy_totals.append(float(np.sum(energy[offset:end])))
        volume_totals.append(float(np.sum(volume[offset:end])))
        offset = end
    return ZeoliteAtlasDataset(
        rows=rows,
        energy=np.asarray(energy_totals, dtype=float),
        volume=np.asarray(volume_totals, dtype=float),
        metadata={
            "name": "Materials Cloud Zeolite Atlas v1",
            "record": "10.24435/materialscloud:2019.0079/v1",
            "subset": subset,
            "soap_cutoff": cutoff,
            "structure_count": len(rows),
            "atom_count": atom_count,
            "aggregation": "sum per-atom energy/volume contributions; mean/std descriptor aggregation",
            "license": "CC BY 4.0",
            "unit_status": "verify against source paper before confirmatory activation",
        },
    )
