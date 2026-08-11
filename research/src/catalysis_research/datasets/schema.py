from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


DATASET_REGISTRATION_SCHEMA_VERSION = "dataset_registration.v1"
DATASET_MANIFEST_SCHEMA_VERSION = "dataset_manifest.v1"
SPLIT_MANIFEST_SCHEMA_VERSION = "split_manifest.v1"
DATASET_REGISTRY_SCHEMA_VERSION = "public_dataset_registry.v1"
IID_SPLIT_SEED = 20260810
IID_SPLIT_RATIOS = {
    "train": 0.6,
    "validation": 0.2,
    "test": 0.2,
}


class DatasetError(RuntimeError):
    """Raised when public dataset rules or frozen artifacts are invalid."""


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DatasetError(f"{field} must be a non-empty string")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise DatasetError(
            f"{field} may contain only letters, numbers, dot, underscore, and dash"
        )
    if value in {".", ".."}:
        raise DatasetError(f"{field} must not be a relative path marker")
    return value


def require_string(mapping: dict[str, Any], field: str) -> str:
    value = mapping.get(field)
    if not isinstance(value, str) or not value.strip():
        raise DatasetError(f"{field} must be a non-empty string")
    return value


def _require_object(mapping: dict[str, Any], field: str) -> dict[str, Any]:
    value = mapping.get(field)
    if not isinstance(value, dict):
        raise DatasetError(f"{field} must be an object")
    return value


def _require_object_list(
    mapping: dict[str, Any],
    field: str,
    *,
    allow_empty: bool = False,
) -> list[dict[str, Any]]:
    value = mapping.get(field)
    if not isinstance(value, list) or (
        not allow_empty and not value
    ):
        qualifier = "a list" if allow_empty else "a non-empty list"
        raise DatasetError(f"{field} must be {qualifier}")
    if not all(isinstance(item, dict) for item in value):
        raise DatasetError(f"{field} entries must be objects")
    return value


def _validate_named_entries(
    entries: list[dict[str, Any]],
    field: str,
    *,
    require_reason: bool,
) -> set[str]:
    names: set[str] = set()
    for index, entry in enumerate(entries):
        name = require_string(entry, "name")
        if name in names:
            raise DatasetError(f"Duplicate {field} name: {name}")
        names.add(name)
        if require_reason:
            require_string(entry, "reason")
        else:
            require_string(entry, "description")
            require_string(entry, "dtype")
            if "units" not in entry:
                raise DatasetError(
                    f"{field}[{index}].units must be present, using null if unitless"
                )
    return names


def validate_registration_config(config: dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise DatasetError("Dataset registration config must be an object")
    if config.get("schema_version") != DATASET_REGISTRATION_SCHEMA_VERSION:
        raise DatasetError("Unsupported dataset registration schema version")

    validate_identifier(config.get("dataset_id"), "dataset_id")
    validate_identifier(config.get("version"), "version")
    study_role = require_string(config, "study_role")
    if study_role not in {"primary", "secondary"}:
        raise DatasetError("study_role must be primary or secondary")
    domain = require_string(config, "domain")
    if study_role == "primary" and domain != "thermal_catalysis":
        raise DatasetError(
            "Primary public datasets must use domain thermal_catalysis"
        )
    if config.get("data_classification") != "public":
        raise DatasetError(
            "Only explicitly public data may enter the public dataset registry"
        )
    if config.get("contains_private_data") is not False:
        raise DatasetError("contains_private_data must be explicitly false")
    if config.get("status") not in {"candidate", "frozen"}:
        raise DatasetError("status must be candidate or frozen")

    source = _require_object(config, "source")
    for field in ("name", "url", "citation", "accessed_at"):
        require_string(source, field)

    license_record = _require_object(config, "license")
    for field in ("name", "url"):
        require_string(license_record, field)
    for field in (
        "allows_research",
        "allows_publication",
        "allows_redistribution",
    ):
        if not isinstance(license_record.get(field), bool):
            raise DatasetError(f"license.{field} must be boolean")
    if not license_record["allows_research"]:
        raise DatasetError("Dataset license must allow research")
    if not license_record["allows_publication"]:
        raise DatasetError("Dataset license must allow publication")

    files = _require_object_list(config, "files")
    seen_paths: set[str] = set()
    for item in files:
        path = require_string(item, "path")
        if path in seen_paths:
            raise DatasetError(f"Duplicate dataset file path: {path}")
        seen_paths.add(path)
        if item.get("format") not in {"csv", "tsv", "jsonl"}:
            raise DatasetError(
                "Dataset file format must be csv, tsv, or jsonl"
            )
        require_string(item, "role")

    sample_id_column = require_string(config, "sample_id_column")
    target = _require_object(config, "target")
    for field in ("name", "column", "definition", "units", "task_type"):
        require_string(target, field)
    if target["task_type"] not in {"regression", "classification"}:
        raise DatasetError(
            "target.task_type must be regression or classification"
        )

    allowed_inputs = _require_object_list(config, "allowed_inputs")
    allowed_names = _validate_named_entries(
        allowed_inputs,
        "allowed_inputs",
        require_reason=False,
    )
    forbidden_inputs = _require_object_list(
        config,
        "forbidden_inputs",
        allow_empty=True,
    )
    forbidden_names = _validate_named_entries(
        forbidden_inputs,
        "forbidden_inputs",
        require_reason=True,
    )
    overlap = sorted(allowed_names & forbidden_names)
    if overlap:
        raise DatasetError(
            "Columns cannot be both allowed and forbidden: "
            + ", ".join(overlap)
        )
    if target["column"] in allowed_names:
        raise DatasetError("Target column must not be an allowed input")
    if target["column"] not in forbidden_names:
        raise DatasetError(
            "Target column must be declared in forbidden_inputs"
        )
    if sample_id_column in allowed_names:
        raise DatasetError("Sample ID column must not be an allowed input")

    group_columns = _require_object_list(config, "group_columns")
    group_names: set[str] = set()
    priorities: set[int] = set()
    for entry in group_columns:
        name = require_string(entry, "name")
        require_string(entry, "rationale")
        priority = entry.get("priority")
        if isinstance(priority, bool) or not isinstance(priority, int):
            raise DatasetError("group_columns.priority must be an integer")
        if priority < 1 or priority in priorities:
            raise DatasetError(
                "group_columns.priority must be unique and at least 1"
            )
        if name in group_names:
            raise DatasetError(f"Duplicate group column: {name}")
        if name == target["column"]:
            raise DatasetError("Target column cannot define OOD groups")
        group_names.add(name)
        priorities.add(priority)

    duplicate_keys = config.get("duplicate_key_columns")
    if not isinstance(duplicate_keys, list) or not duplicate_keys:
        raise DatasetError(
            "duplicate_key_columns must be a non-empty list"
        )
    if (
        not all(isinstance(item, str) and item.strip() for item in duplicate_keys)
        or len(set(duplicate_keys)) != len(duplicate_keys)
    ):
        raise DatasetError(
            "duplicate_key_columns must contain unique non-empty strings"
        )
    if target["column"] in duplicate_keys:
        raise DatasetError(
            "Target column cannot define duplicate identity"
        )

    missing_policy = _require_object(config, "missing_data_policy")
    require_string(missing_policy, "strategy")
    maximum_fraction = missing_policy.get("maximum_allowed_fraction")
    if (
        isinstance(maximum_fraction, bool)
        or not isinstance(maximum_fraction, (int, float))
        or not 0 <= maximum_fraction <= 1
    ):
        raise DatasetError(
            "missing_data_policy.maximum_allowed_fraction must be in [0, 1]"
        )

    duplicate_policy = _require_object(config, "duplicate_policy")
    if duplicate_policy.get("action") not in {
        "reject",
        "keep_together",
        "aggregate_before_registration",
    }:
        raise DatasetError("Unsupported duplicate_policy.action")
    require_string(duplicate_policy, "rationale")

    label_policy = _require_object(config, "label_access_policy")
    for field in (
        "descriptor_generation",
        "descriptor_computation",
        "downstream_training",
        "evaluation",
    ):
        require_string(label_policy, field)

    iid = _require_object(config, "iid_split")
    if iid.get("seed") != IID_SPLIT_SEED:
        raise DatasetError(f"iid_split.seed must be {IID_SPLIT_SEED}")
    ratios = _require_object(iid, "ratios")
    for partition, expected in IID_SPLIT_RATIOS.items():
        value = ratios.get(partition)
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isclose(value, expected, abs_tol=1e-12)
        ):
            raise DatasetError(
                f"iid_split.ratios.{partition} must be {expected}"
            )
    quantiles = iid.get("stratify_target_quantiles")
    if quantiles is not None and (
        isinstance(quantiles, bool)
        or not isinstance(quantiles, int)
        or quantiles < 2
    ):
        raise DatasetError(
            "iid_split.stratify_target_quantiles must be null or >= 2"
        )
    if target["task_type"] == "classification" and quantiles is not None:
        raise DatasetError(
            "Classification datasets must use null target quantiles"
        )

    ood = _require_object(config, "ood_split")
    group_column = require_string(ood, "group_column")
    if group_column not in group_names:
        raise DatasetError(
            "ood_split.group_column must be registered in group_columns"
        )
    folds = _require_object_list(ood, "folds")
    fold_ids: set[str] = set()
    for fold in folds:
        fold_id = validate_identifier(fold.get("fold_id"), "fold_id")
        if fold_id in fold_ids:
            raise DatasetError(f"Duplicate OOD fold_id: {fold_id}")
        fold_ids.add(fold_id)
        test_groups = fold.get("test_groups")
        validation_groups = fold.get("validation_groups")
        for field, values in (
            ("test_groups", test_groups),
            ("validation_groups", validation_groups),
        ):
            if not isinstance(values, list) or not values:
                raise DatasetError(
                    f"ood_split.{field} must be a non-empty list"
                )
            if len({str(value) for value in values}) != len(values):
                raise DatasetError(
                    f"ood_split.{field} must not contain duplicates"
                )
        overlap_groups = {
            str(value) for value in test_groups
        } & {str(value) for value in validation_groups}
        if overlap_groups:
            raise DatasetError(
                f"OOD fold {fold_id} has overlapping validation/test groups"
            )

def manifest_hash(manifest: dict[str, Any]) -> str:
    value = dict(manifest)
    value.pop("manifest_content_hash", None)
    return content_hash(value)


def split_hash(manifest: dict[str, Any]) -> str:
    identity = {
        "schema_version": manifest.get("schema_version"),
        "split_id": manifest.get("split_id"),
        "dataset_id": manifest.get("dataset_id"),
        "dataset_version": manifest.get("dataset_version"),
        "dataset_content_hash": manifest.get("dataset_content_hash"),
        "strategy": manifest.get("strategy"),
        "algorithm_version": manifest.get("algorithm_version"),
        "configuration": manifest.get("configuration"),
        "partitions": manifest.get("partitions"),
        "folds": manifest.get("folds"),
    }
    return content_hash(identity)
