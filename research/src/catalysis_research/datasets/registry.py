from __future__ import annotations

import copy
import json
import math
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from catalysis_research.provenance.run_manifest import inspect_git_state

from .loader import (
    index_rows,
    is_missing,
    load_configured_rows,
    load_manifest_rows,
)
from .schema import (
    DATASET_MANIFEST_SCHEMA_VERSION,
    DatasetError,
    content_hash,
    manifest_hash,
    sha256_file,
    validate_registration_config,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise DatasetError(f"Frozen dataset manifest already exists: {path}")
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as output:
            json.dump(
                value,
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            raise DatasetError(
                f"Frozen dataset manifest already exists: {path}"
            )
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def load_dataset_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise DatasetError(f"Dataset manifest does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise DatasetError(f"Invalid dataset manifest JSON: {path}") from error
    if not isinstance(value, dict):
        raise DatasetError("Dataset manifest must be a JSON object")
    return value


def require_tracked_file(
    *,
    repository_root: Path,
    path: Path,
    required_directory: str,
    artifact_name: str,
) -> Path:
    repository_root = repository_root.resolve()
    resolved_path = path.resolve()
    allowed_root = (repository_root / required_directory).resolve()
    try:
        resolved_path.relative_to(allowed_root)
        relative_path = resolved_path.relative_to(repository_root)
    except ValueError as error:
        raise DatasetError(
            f"{artifact_name} must be stored under {required_directory}"
        ) from error
    tracked = subprocess.run(
        [
            "git",
            "ls-files",
            "--error-unmatch",
            "--",
            relative_path.as_posix(),
        ],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if tracked.returncode != 0:
        raise DatasetError(
            f"{artifact_name} must be committed before freezing"
        )
    return resolved_path


def _required_columns(config: dict[str, Any]) -> set[str]:
    return {
        config["sample_id_column"],
        config["target"]["column"],
        *(entry["name"] for entry in config["allowed_inputs"]),
        *(entry["name"] for entry in config["group_columns"]),
        *config["duplicate_key_columns"],
    }


def _target_value(value: Any, task_type: str, sample_id: str) -> Any:
    if is_missing(value):
        raise DatasetError(f"Missing target for sample {sample_id}")
    if task_type == "classification":
        return str(value).strip()
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise DatasetError(
            f"Non-numeric regression target for sample {sample_id}"
        ) from error
    if not math.isfinite(number):
        raise DatasetError(
            f"Non-finite regression target for sample {sample_id}"
        )
    return number


def _duplicate_key(row: dict[str, Any], columns: list[str]) -> str:
    values = [row.get(column) for column in columns]
    if any(is_missing(value) for value in values):
        missing_columns = [
            column
            for column, value in zip(columns, values)
            if is_missing(value)
        ]
        raise DatasetError(
            "Missing duplicate key columns: " + ", ".join(missing_columns)
        )
    return content_hash([str(value).strip() for value in values])


def _inspect_registration(
    config: dict[str, Any],
    repository_root: Path,
) -> dict[str, Any]:
    rows, file_records = load_configured_rows(config, repository_root)
    required_columns = _required_columns(config)
    for record in file_records:
        missing_columns = sorted(required_columns - set(record["columns"]))
        if missing_columns:
            raise DatasetError(
                f"Dataset file {record['path']} is missing columns: "
                + ", ".join(missing_columns)
            )
        resolved_path = (repository_root / record["path"]).resolve()
        record["sha256"] = sha256_file(resolved_path)
        record["bytes"] = resolved_path.stat().st_size

    sample_column = config["sample_id_column"]
    indexed = index_rows(rows, sample_column)
    target_column = config["target"]["column"]
    task_type = config["target"]["task_type"]
    allowed_columns = [
        entry["name"] for entry in config["allowed_inputs"]
    ]
    group_column_names = [
        entry["name"] for entry in config["group_columns"]
    ]
    duplicate_columns = list(config["duplicate_key_columns"])

    missing_counts = {column: 0 for column in allowed_columns}
    group_values = {column: set() for column in group_column_names}
    duplicate_groups: dict[str, list[str]] = {}
    targets: dict[str, Any] = {}
    for identifier, row in indexed.items():
        targets[identifier] = _target_value(
            row.get(target_column),
            task_type,
            identifier,
        )
        for column in allowed_columns:
            if is_missing(row.get(column)):
                missing_counts[column] += 1
        for column in group_column_names:
            value = row.get(column)
            if is_missing(value):
                raise DatasetError(
                    f"Missing OOD group value {column} for sample {identifier}"
                )
            group_values[column].add(str(value).strip())
        key = _duplicate_key(row, duplicate_columns)
        duplicate_groups.setdefault(key, []).append(identifier)

    row_count = len(indexed)
    maximum_missing = config["missing_data_policy"][
        "maximum_allowed_fraction"
    ]
    missing_fractions = {
        column: count / row_count
        for column, count in missing_counts.items()
    }
    exceeded = [
        column
        for column, fraction in missing_fractions.items()
        if fraction > maximum_missing
    ]
    if exceeded:
        raise DatasetError(
            "Missingness exceeds frozen policy for: " + ", ".join(exceeded)
        )

    duplicate_sets = [
        sorted(identifiers)
        for identifiers in duplicate_groups.values()
        if len(identifiers) > 1
    ]
    duplicate_action = config["duplicate_policy"]["action"]
    if duplicate_sets and duplicate_action in {
        "reject",
        "aggregate_before_registration",
    }:
        raise DatasetError(
            "Duplicate records remain after applying frozen duplicate policy"
        )

    ood = config["ood_split"]
    ood_group_values = group_values[ood["group_column"]]
    for fold in ood["folds"]:
        configured_groups = {
            str(value) for value in fold["test_groups"]
        } | {
            str(value) for value in fold["validation_groups"]
        }
        unknown_groups = sorted(configured_groups - ood_group_values)
        if unknown_groups:
            raise DatasetError(
                f"OOD fold {fold['fold_id']} references unknown groups: "
                + ", ".join(unknown_groups)
            )
        if not ood_group_values - configured_groups:
            raise DatasetError(
                f"OOD fold {fold['fold_id']} leaves no training groups"
            )

    sample_ids = sorted(indexed)
    identity = {
        "registration_config": config,
        "files": [
            {
                "path": record["path"],
                "sha256": record["sha256"],
                "bytes": record["bytes"],
                "format": record["format"],
                "role": record["role"],
            }
            for record in file_records
        ],
        "sample_ids": sample_ids,
    }
    return {
        "rows": rows,
        "files": file_records,
        "row_count": row_count,
        "columns": sorted(required_columns),
        "sample_ids": sample_ids,
        "sample_id_hash": content_hash(sample_ids),
        "dataset_content_hash": content_hash(identity),
        "missing_fractions": missing_fractions,
        "duplicate_groups": duplicate_sets,
        "group_values": {
            column: sorted(values)
            for column, values in group_values.items()
        },
        "target_class_count": (
            len(set(targets.values()))
            if task_type == "classification"
            else None
        ),
    }


def register_dataset(
    *,
    config_path: Path,
    output_root: Path,
    repository_root: Path,
    allow_dirty: bool = False,
    timestamp: str | None = None,
    git_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    config_path = require_tracked_file(
        repository_root=repository_root,
        path=config_path,
        required_directory="research/configs/datasets",
        artifact_name="Dataset registration config",
    )
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise DatasetError(f"Invalid registration config: {config_path}") from error
    validate_registration_config(config)

    state = git_state or inspect_git_state(repository_root)
    if state.get("dirty") and not allow_dirty:
        raise DatasetError(
            "Refusing to freeze a dataset from a dirty Git worktree"
        )
    commit = str(state.get("commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise DatasetError("Git state must contain a full commit hash")

    inspection = _inspect_registration(config, repository_root)
    registered_at = timestamp or utc_now()
    manifest = {
        "schema_version": DATASET_MANIFEST_SCHEMA_VERSION,
        "dataset_id": config["dataset_id"],
        "version": config["version"],
        "status": config["status"],
        "study_role": config["study_role"],
        "domain": config["domain"],
        "data_classification": "public",
        "contains_private_data": False,
        "registered_at": registered_at,
        "git_commit": commit,
        "git_tree": state.get("tree"),
        "git_branch": state.get("branch"),
        "git_dirty": bool(state.get("dirty")),
        "registration_config_hash": content_hash(config),
        "source": copy.deepcopy(config["source"]),
        "license": copy.deepcopy(config["license"]),
        "files": inspection["files"],
        "row_count": inspection["row_count"],
        "required_columns": inspection["columns"],
        "sample_id_column": config["sample_id_column"],
        "sample_id_hash": inspection["sample_id_hash"],
        "target": copy.deepcopy(config["target"]),
        "allowed_inputs": copy.deepcopy(config["allowed_inputs"]),
        "forbidden_inputs": copy.deepcopy(config["forbidden_inputs"]),
        "group_columns": copy.deepcopy(config["group_columns"]),
        "group_values": inspection["group_values"],
        "duplicate_key_columns": copy.deepcopy(
            config["duplicate_key_columns"]
        ),
        "duplicate_group_count": len(inspection["duplicate_groups"]),
        "missing_data_policy": copy.deepcopy(
            config["missing_data_policy"]
        ),
        "missing_fractions": inspection["missing_fractions"],
        "duplicate_policy": copy.deepcopy(config["duplicate_policy"]),
        "label_access_policy": copy.deepcopy(
            config["label_access_policy"]
        ),
        "iid_split": copy.deepcopy(config["iid_split"]),
        "ood_split": copy.deepcopy(config["ood_split"]),
        "dataset_content_hash": inspection["dataset_content_hash"],
        "registration": copy.deepcopy(config),
        "manifest_content_hash": "",
    }
    manifest["manifest_content_hash"] = manifest_hash(manifest)
    output_path = (
        output_root.resolve()
        / f"{config['dataset_id']}.manifest.json"
    )
    _atomic_write_json(output_path, manifest)
    return {
        "dataset_id": config["dataset_id"],
        "manifest_path": str(output_path),
        "manifest": manifest,
    }


def verify_dataset_manifest(
    manifest_path: Path,
    repository_root: Path,
) -> dict[str, Any]:
    failures: list[str] = []
    try:
        manifest = load_dataset_manifest(manifest_path)
    except DatasetError as error:
        return {
            "dataset_id": manifest_path.stem,
            "valid": False,
            "failures": [str(error)],
        }

    if manifest.get("schema_version") != DATASET_MANIFEST_SCHEMA_VERSION:
        failures.append("Unsupported dataset manifest schema version")
    if manifest_path.name != (
        f"{manifest.get('dataset_id')}.manifest.json"
    ):
        failures.append("Dataset manifest filename does not match dataset_id")
    if manifest_hash(manifest) != manifest.get("manifest_content_hash"):
        failures.append("Dataset manifest content hash mismatch")
    registration = manifest.get("registration")
    registration_valid = False
    if not isinstance(registration, dict):
        failures.append("Dataset manifest registration must be an object")
        registration = {}
    else:
        try:
            validate_registration_config(registration)
        except DatasetError as error:
            failures.append(f"Invalid registration config: {error}")
        else:
            registration_valid = True
    if registration_valid and content_hash(registration) != manifest.get(
        "registration_config_hash"
    ):
        failures.append("Dataset registration config hash mismatch")
    if registration_valid:
        registration_fields = {
            "dataset_id": "dataset_id",
            "version": "version",
            "status": "status",
            "study_role": "study_role",
            "domain": "domain",
            "data_classification": "data_classification",
            "contains_private_data": "contains_private_data",
            "source": "source",
            "license": "license",
            "sample_id_column": "sample_id_column",
            "target": "target",
            "allowed_inputs": "allowed_inputs",
            "forbidden_inputs": "forbidden_inputs",
            "group_columns": "group_columns",
            "duplicate_key_columns": "duplicate_key_columns",
            "missing_data_policy": "missing_data_policy",
            "duplicate_policy": "duplicate_policy",
            "label_access_policy": "label_access_policy",
            "iid_split": "iid_split",
            "ood_split": "ood_split",
        }
        for manifest_field, registration_field in registration_fields.items():
            if manifest.get(manifest_field) != registration.get(
                registration_field
            ):
                failures.append(
                    f"Dataset registration mismatch: {manifest_field}"
                )
    commit = str(manifest.get("git_commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        failures.append("Dataset git_commit must be a full hash")
    else:
        commit_exists = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=repository_root.resolve(),
            check=False,
            capture_output=True,
        )
        if commit_exists.returncode != 0:
            failures.append("Dataset git_commit is unavailable")

    inspection: dict[str, Any] | None = None
    if registration_valid:
        try:
            inspection = _inspect_registration(
                registration,
                repository_root.resolve(),
            )
        except (DatasetError, OSError) as error:
            failures.append(str(error))
    if inspection is not None:
        comparisons = {
            "files": inspection["files"],
            "row_count": inspection["row_count"],
            "sample_id_hash": inspection["sample_id_hash"],
            "dataset_content_hash": inspection["dataset_content_hash"],
            "group_values": inspection["group_values"],
            "missing_fractions": inspection["missing_fractions"],
            "duplicate_group_count": len(inspection["duplicate_groups"]),
        }
        for field, expected in comparisons.items():
            if manifest.get(field) != expected:
                failures.append(f"Dataset manifest mismatch: {field}")

    return {
        "dataset_id": manifest.get("dataset_id"),
        "version": manifest.get("version"),
        "valid": not failures,
        "failures": failures,
        "dataset_content_hash": manifest.get("dataset_content_hash"),
        "manifest_content_hash": manifest.get("manifest_content_hash"),
        "row_count": manifest.get("row_count"),
    }


def rows_for_manifest(
    manifest: dict[str, Any],
    repository_root: Path,
) -> list[dict[str, Any]]:
    return load_manifest_rows(manifest, repository_root.resolve())
