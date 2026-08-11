from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Iterable

from .schema import (
    DATASET_MANIFEST_SCHEMA_VERSION,
    SPLIT_MANIFEST_SCHEMA_VERSION,
    DatasetError,
    manifest_hash,
    split_hash,
)


SUPPORTED_ACCESS_ROLES = {
    "descriptor_generation",
    "descriptor_computation",
    "downstream_training",
    "evaluation",
    "audit",
}


def is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, float):
        return math.isnan(value)
    return False


def _load_delimited(path: Path, delimiter: str) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, delimiter=delimiter)
        if reader.fieldnames is None:
            raise DatasetError(f"Dataset file has no header: {path}")
        if len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise DatasetError(f"Dataset file has duplicate columns: {path}")
        return [dict(row) for row in reader]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise DatasetError(
                    f"Invalid JSONL at {path}:{line_number}: {error}"
                ) from error
            if not isinstance(row, dict):
                raise DatasetError(
                    f"JSONL row must be an object at {path}:{line_number}"
                )
            rows.append(row)
    return rows


def load_data_file(path: Path, file_format: str) -> list[dict[str, Any]]:
    if file_format == "csv":
        return _load_delimited(path, ",")
    if file_format == "tsv":
        return _load_delimited(path, "\t")
    if file_format == "jsonl":
        return _load_jsonl(path)
    raise DatasetError(f"Unsupported dataset file format: {file_format}")


def resolve_public_data_path(repository_root: Path, relative_path: str) -> Path:
    repository_root = repository_root.resolve()
    configured_path = Path(relative_path)
    if configured_path.is_absolute():
        raise DatasetError("Public dataset file paths must be repository-relative")
    public_root = (repository_root / "research" / "datasets" / "raw").resolve()
    resolved = (repository_root / configured_path).resolve()
    try:
        resolved.relative_to(public_root)
    except ValueError as error:
        raise DatasetError(
            "Public dataset files must be staged under research/datasets/raw"
        ) from error
    if not resolved.is_file():
        raise DatasetError(f"Dataset file does not exist: {resolved}")
    return resolved


def load_configured_rows(
    config: dict[str, Any],
    repository_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    file_records: list[dict[str, Any]] = []
    for file_config in config["files"]:
        path = resolve_public_data_path(
            repository_root,
            file_config["path"],
        )
        file_rows = load_data_file(path, file_config["format"])
        if not file_rows:
            raise DatasetError(f"Dataset file contains no rows: {path}")
        columns = sorted(
            {
                str(column)
                for row in file_rows
                for column in row
            }
        )
        rows.extend(file_rows)
        file_records.append(
            {
                "path": file_config["path"].replace("\\", "/"),
                "format": file_config["format"],
                "role": file_config["role"],
                "row_count": len(file_rows),
                "columns": columns,
            }
        )
    return rows, file_records


def load_manifest_rows(
    manifest: dict[str, Any],
    repository_root: Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for file_record in manifest.get("files") or []:
        path = resolve_public_data_path(
            repository_root,
            str(file_record["path"]),
        )
        rows.extend(load_data_file(path, str(file_record["format"])))
    return rows


def sample_id(row: dict[str, Any], sample_id_column: str) -> str:
    value = row.get(sample_id_column)
    if is_missing(value):
        raise DatasetError(f"Missing sample ID in column {sample_id_column}")
    return str(value).strip()


def index_rows(
    rows: Iterable[dict[str, Any]],
    sample_id_column: str,
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        identifier = sample_id(row, sample_id_column)
        if identifier in indexed:
            raise DatasetError(f"Duplicate sample ID: {identifier}")
        indexed[identifier] = row
    return indexed


def generation_context(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != DATASET_MANIFEST_SCHEMA_VERSION:
        raise DatasetError("Unsupported dataset manifest schema version")
    if manifest_hash(manifest) != manifest.get("manifest_content_hash"):
        raise DatasetError("Dataset manifest content hash mismatch")
    try:
        return {
            "schema_version": "dataset_generation_context.v1",
            "dataset_id": manifest["dataset_id"],
            "dataset_version": manifest["version"],
            "domain": manifest["domain"],
            "task": {
                "target_name": manifest["target"]["name"],
                "target_definition": manifest["target"]["definition"],
                "target_units": manifest["target"]["units"],
                "task_type": manifest["target"]["task_type"],
            },
            "allowed_input_schema": manifest["allowed_inputs"],
            "label_visibility": "no_row_level_labels",
            "row_data_included": False,
        }
    except (KeyError, TypeError) as error:
        raise DatasetError("Dataset manifest is missing context fields") from error


def _partition_ids(
    split_manifest: dict[str, Any],
    partition: str,
    fold_id: str | None,
) -> list[str]:
    if partition not in {"train", "validation", "test"}:
        raise DatasetError(f"Unsupported partition: {partition}")
    strategy = split_manifest.get("strategy")
    if strategy == "iid":
        if fold_id is not None:
            raise DatasetError("IID split does not accept fold_id")
        partitions = split_manifest.get("partitions") or {}
        return [str(value) for value in partitions.get(partition, [])]
    if strategy == "ood":
        if not fold_id:
            raise DatasetError("OOD split access requires fold_id")
        for fold in split_manifest.get("folds") or []:
            if fold.get("fold_id") == fold_id:
                partitions = fold.get("partitions") or {}
                return [
                    str(value)
                    for value in partitions.get(partition, [])
                ]
        raise DatasetError(f"Unknown OOD fold_id: {fold_id}")
    raise DatasetError("Unsupported split manifest strategy")


def load_partition_rows(
    *,
    dataset_manifest: dict[str, Any],
    split_manifest: dict[str, Any],
    repository_root: Path,
    partition: str,
    access_role: str,
    fold_id: str | None = None,
) -> list[dict[str, Any]]:
    if (
        dataset_manifest.get("schema_version")
        != DATASET_MANIFEST_SCHEMA_VERSION
    ):
        raise DatasetError("Unsupported dataset manifest schema version")
    if manifest_hash(dataset_manifest) != dataset_manifest.get(
        "manifest_content_hash"
    ):
        raise DatasetError("Dataset manifest content hash mismatch")
    if (
        split_manifest.get("schema_version")
        != SPLIT_MANIFEST_SCHEMA_VERSION
    ):
        raise DatasetError("Unsupported split manifest schema version")
    if manifest_hash(split_manifest) != split_manifest.get(
        "manifest_content_hash"
    ):
        raise DatasetError("Split manifest content hash mismatch")
    if split_hash(split_manifest) != split_manifest.get("split_hash"):
        raise DatasetError("Split content hash mismatch")
    if (
        split_manifest.get("dataset_id") != dataset_manifest.get("dataset_id")
        or split_manifest.get("dataset_version")
        != dataset_manifest.get("version")
        or split_manifest.get("dataset_content_hash")
        != dataset_manifest.get("dataset_content_hash")
    ):
        raise DatasetError("Dataset and split manifests are incompatible")
    if access_role not in SUPPORTED_ACCESS_ROLES:
        raise DatasetError(f"Unsupported dataset access role: {access_role}")
    if access_role == "descriptor_generation":
        raise DatasetError(
            "Descriptor generation receives metadata only; use generation_context"
        )
    if access_role == "downstream_training" and partition == "test":
        raise DatasetError(
            "Downstream training cannot access test labels"
        )
    if access_role == "evaluation" and partition != "test":
        raise DatasetError("Evaluation label access is restricted to test")

    try:
        sample_column = dataset_manifest["sample_id_column"]
        allowed_columns = [
            entry["name"] for entry in dataset_manifest["allowed_inputs"]
        ]
        target_column = dataset_manifest["target"]["column"]
    except (KeyError, TypeError) as error:
        raise DatasetError("Dataset manifest is missing access fields") from error

    rows = load_manifest_rows(dataset_manifest, repository_root)
    indexed = index_rows(rows, sample_column)
    identifiers = _partition_ids(split_manifest, partition, fold_id)
    missing_ids = sorted(set(identifiers) - set(indexed))
    if missing_ids:
        raise DatasetError(
            "Split references unknown sample IDs: " + ", ".join(missing_ids)
        )

    if access_role == "audit":
        return [dict(indexed[identifier]) for identifier in identifiers]

    projected_columns = [sample_column, *allowed_columns]
    if access_role in {"downstream_training", "evaluation"}:
        projected_columns.append(target_column)

    return [
        {
            column: indexed[identifier].get(column)
            for column in projected_columns
        }
        for identifier in identifiers
    ]
