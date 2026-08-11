from __future__ import annotations

from pathlib import Path
from typing import Any

from .loader import index_rows, is_missing, load_manifest_rows
from .registry import load_dataset_manifest, verify_dataset_manifest
from .schema import DatasetError, content_hash
from .split import load_split_manifest, verify_split_manifest


def _normalized_name(value: str) -> str:
    return "".join(character for character in value.lower() if character.isalnum())


def _partition_map(
    partitions: dict[str, list[str]],
) -> tuple[dict[str, str], list[str]]:
    mapping: dict[str, str] = {}
    duplicates: list[str] = []
    for partition, identifiers in partitions.items():
        for identifier in identifiers:
            identifier = str(identifier)
            if identifier in mapping:
                duplicates.append(identifier)
            mapping[identifier] = partition
    return mapping, sorted(set(duplicates))


def _duplicate_key(
    row: dict[str, Any],
    columns: list[str],
) -> tuple[str, ...]:
    return tuple(str(row.get(column, "")).strip() for column in columns)


def _audit_partitions(
    *,
    rows_by_id: dict[str, dict[str, Any]],
    partitions: dict[str, list[str]],
    duplicate_columns: list[str],
    ood_group_column: str | None = None,
) -> list[str]:
    failures: list[str] = []
    mapping, duplicate_membership = _partition_map(partitions)
    if duplicate_membership:
        failures.append(
            "Sample IDs occur in multiple partitions: "
            + ", ".join(duplicate_membership)
        )
    expected_ids = set(rows_by_id)
    actual_ids = set(mapping)
    missing_ids = sorted(expected_ids - actual_ids)
    unknown_ids = sorted(actual_ids - expected_ids)
    if missing_ids:
        failures.append(
            "Split omits sample IDs: " + ", ".join(missing_ids)
        )
    if unknown_ids:
        failures.append(
            "Split contains unknown sample IDs: " + ", ".join(unknown_ids)
        )

    duplicate_partitions: dict[tuple[str, ...], set[str]] = {}
    for identifier, partition in mapping.items():
        row = rows_by_id.get(identifier)
        if row is None:
            continue
        key = _duplicate_key(row, duplicate_columns)
        duplicate_partitions.setdefault(key, set()).add(partition)
    crossing_duplicates = sum(
        1
        for memberships in duplicate_partitions.values()
        if len(memberships) > 1
    )
    if crossing_duplicates:
        failures.append(
            f"{crossing_duplicates} duplicate groups cross split boundaries"
        )

    if ood_group_column:
        group_partitions: dict[str, set[str]] = {}
        for identifier, partition in mapping.items():
            row = rows_by_id.get(identifier)
            if row is None:
                continue
            group = str(row.get(ood_group_column, "")).strip()
            group_partitions.setdefault(group, set()).add(partition)
        crossing_groups = sorted(
            group
            for group, memberships in group_partitions.items()
            if len(memberships) > 1
        )
        if crossing_groups:
            failures.append(
                "OOD groups cross split boundaries: "
                + ", ".join(crossing_groups)
            )
    return failures


def leakage_audit(
    *,
    dataset_manifest_path: Path,
    repository_root: Path,
    split_manifest_path: Path | None = None,
) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    manual_review_required: list[str] = [
        "Confirm allowed inputs cannot deterministically reconstruct the target.",
        "Confirm source publications do not duplicate benchmark test records.",
        "Confirm OOD grouping was selected without observing model outcomes.",
    ]

    dataset_report = verify_dataset_manifest(
        dataset_manifest_path,
        repository_root,
    )
    if not dataset_report["valid"]:
        failures.extend(dataset_report["failures"])
        return {
            "dataset_id": dataset_report.get("dataset_id"),
            "valid": False,
            "failures": failures,
            "warnings": warnings,
            "manual_review_required": manual_review_required,
            "audit_hash": content_hash(
                {
                    "failures": failures,
                    "warnings": warnings,
                    "manual_review_required": manual_review_required,
                }
            ),
        }
    try:
        manifest = load_dataset_manifest(dataset_manifest_path)
        rows = load_manifest_rows(manifest, repository_root.resolve())
        rows_by_id = index_rows(rows, manifest["sample_id_column"])
    except DatasetError as error:
        failures.append(str(error))
        return {
            "dataset_id": dataset_report.get("dataset_id"),
            "valid": False,
            "failures": failures,
            "warnings": warnings,
            "manual_review_required": manual_review_required,
            "audit_hash": content_hash(
                {
                    "failures": failures,
                    "warnings": warnings,
                    "manual_review_required": manual_review_required,
                }
            ),
        }

    allowed_names = {
        entry["name"] for entry in manifest["allowed_inputs"]
    }
    forbidden_names = {
        entry["name"] for entry in manifest["forbidden_inputs"]
    }
    target_column = manifest["target"]["column"]
    sample_column = manifest["sample_id_column"]
    if allowed_names & forbidden_names:
        failures.append("Allowed and forbidden input registries overlap")
    if target_column in allowed_names:
        failures.append("Target column is exposed as an allowed input")
    if sample_column in allowed_names:
        failures.append("Sample ID is exposed as an allowed input")

    target_tokens = {
        _normalized_name(target_column),
        _normalized_name(manifest["target"]["name"]),
    }
    suspicious_names = sorted(
        name
        for name in allowed_names
        if _normalized_name(name) in target_tokens
        or any(
            token
            and token in _normalized_name(name)
            for token in target_tokens
        )
    )
    if suspicious_names:
        warnings.append(
            "Allowed input names require target-proxy review: "
            + ", ".join(suspicious_names)
        )

    all_columns = {
        str(column)
        for row in rows
        for column in row
    }
    undeclared_columns = sorted(
        all_columns
        - allowed_names
        - forbidden_names
        - {
            target_column,
            sample_column,
            *(
                entry["name"]
                for entry in manifest["group_columns"]
            ),
            *manifest["duplicate_key_columns"],
        }
    )
    if undeclared_columns:
        warnings.append(
            "Columns are present but absent from allowed/forbidden registries: "
            + ", ".join(undeclared_columns)
        )

    if split_manifest_path is not None:
        split_report = verify_split_manifest(
            split_manifest_path=split_manifest_path,
            dataset_manifest_path=dataset_manifest_path,
            repository_root=repository_root,
        )
        if not split_report["valid"]:
            failures.extend(split_report["failures"])
        try:
            split_manifest = load_split_manifest(split_manifest_path)
        except DatasetError as error:
            failures.append(str(error))
        else:
            if split_manifest.get("strategy") == "iid":
                failures.extend(
                    _audit_partitions(
                        rows_by_id=rows_by_id,
                        partitions=split_manifest.get("partitions") or {},
                        duplicate_columns=manifest[
                            "duplicate_key_columns"
                        ],
                    )
                )
            elif split_manifest.get("strategy") == "ood":
                for fold in split_manifest.get("folds") or []:
                    fold_failures = _audit_partitions(
                        rows_by_id=rows_by_id,
                        partitions=fold.get("partitions") or {},
                        duplicate_columns=manifest[
                            "duplicate_key_columns"
                        ],
                        ood_group_column=manifest["ood_split"][
                            "group_column"
                        ],
                    )
                    failures.extend(
                        f"{fold.get('fold_id')}: {failure}"
                        for failure in fold_failures
                    )
            else:
                failures.append("Unsupported split strategy in leakage audit")

    target_missing = sum(
        1
        for row in rows
        if is_missing(row.get(target_column))
    )
    if target_missing:
        failures.append(f"{target_missing} rows have missing targets")

    audit_identity = {
        "dataset_content_hash": manifest.get("dataset_content_hash"),
        "split_hash": (
            split_report.get("split_hash")
            if split_manifest_path is not None
            else None
        ),
        "failures": failures,
        "warnings": warnings,
        "manual_review_required": manual_review_required,
    }
    return {
        "dataset_id": manifest["dataset_id"],
        "valid": not failures,
        "failures": failures,
        "warnings": warnings,
        "manual_review_required": manual_review_required,
        "row_count": len(rows_by_id),
        "audit_hash": content_hash(audit_identity),
    }
