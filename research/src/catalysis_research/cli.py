from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Sequence

from .corpora.stage1 import (
    CorpusError,
    freeze_stage1_corpus,
    verify_stage1_corpus,
)
from .datasets.leakage import leakage_audit
from .datasets.loader import generation_context
from .datasets.registry import (
    load_dataset_manifest,
    register_dataset,
    verify_dataset_manifest,
)
from .datasets.schema import DatasetError
from .datasets.split import create_split, verify_split_manifest
from .kg.freeze_stage1 import freeze_stage1_archive, verify_snapshot
from .kg.nested import (
    NestedSnapshotError,
    build_nested_snapshots,
    verify_nested_snapshots,
)
from .kg.selection import SelectionError
from .layout import REQUIRED_DIRECTORIES, inspect_layout
from .normalization import (
    NormalizationError,
    build_normalization_overlay,
    verify_normalization_overlay,
)
from .provenance.run_manifest import (
    OUTPUT_FIELDS,
    RunManifestError,
    complete_run,
    create_run,
    fail_run,
    load_manifest,
    record_artifact,
    record_error,
    verify_run,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="catalysis-research",
        description="Command-line entry point for reproducible research experiments.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Override the research root used for layout inspection.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "doctor",
        help="Validate the research directory contract and print JSON.",
    )
    subparsers.add_parser(
        "show-layout",
        help="Print the required research directories.",
    )
    kg_parser = subparsers.add_parser(
        "kg",
        help="Build and verify immutable knowledge graph snapshots.",
    )
    kg_subparsers = kg_parser.add_subparsers(dest="kg_command", required=True)
    freeze_parser = kg_subparsers.add_parser(
        "freeze-stage1",
        help="Freeze a Stage 1 ZIP archive as a deterministic KG snapshot.",
    )
    freeze_parser.add_argument("--input", type=Path, required=True)
    freeze_parser.add_argument("--output", type=Path, required=True)
    freeze_parser.add_argument("--snapshot-id", required=True)
    freeze_parser.add_argument("--knowledge-level", required=True)
    freeze_parser.add_argument("--domain", required=True)
    freeze_parser.add_argument("--expected-papers", type=int, required=True)
    freeze_parser.add_argument(
        "--allowed-system",
        action="append",
        required=True,
        dest="allowed_systems",
    )
    verify_parser = kg_subparsers.add_parser(
        "verify",
        help="Verify all frozen snapshot artifact hashes.",
    )
    verify_parser.add_argument("--snapshot", type=Path, required=True)
    nested_build_parser = kg_subparsers.add_parser(
        "build-nested",
        help="Build immutable nested Stage 1 KG snapshots from a frozen corpus.",
    )
    nested_build_parser.add_argument("--config", type=Path, required=True)
    nested_build_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )
    nested_build_parser.add_argument("--allow-dirty", action="store_true")
    nested_verify_parser = kg_subparsers.add_parser(
        "verify-nested",
        help="Verify strict nesting and all nested snapshot artifacts.",
    )
    nested_verify_parser.add_argument("--manifest", type=Path, required=True)
    nested_verify_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )

    corpus_parser = subparsers.add_parser(
        "corpus",
        help="Freeze and verify immutable public literature corpora.",
    )
    corpus_subparsers = corpus_parser.add_subparsers(
        dest="corpus_command",
        required=True,
    )
    corpus_freeze_parser = corpus_subparsers.add_parser(
        "freeze-stage1",
        help="Freeze a committed Stage 1 archive inventory.",
    )
    corpus_freeze_parser.add_argument("--input", type=Path, required=True)
    corpus_freeze_parser.add_argument("--output", type=Path, required=True)
    corpus_freeze_parser.add_argument("--corpus-id", required=True)
    corpus_freeze_parser.add_argument("--domain", required=True)
    corpus_freeze_parser.add_argument(
        "--expected-papers",
        type=int,
        required=True,
    )
    corpus_freeze_parser.add_argument("--expected-sha256")
    corpus_freeze_parser.add_argument(
        "--allowed-system",
        action="append",
        required=True,
        dest="allowed_systems",
    )
    corpus_freeze_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )
    corpus_freeze_parser.add_argument("--allow-dirty", action="store_true")
    corpus_verify_parser = corpus_subparsers.add_parser(
        "verify",
        help="Verify a frozen corpus and its source archive.",
    )
    corpus_verify_parser.add_argument(
        "--corpus",
        type=Path,
        required=True,
    )
    run_parser = subparsers.add_parser(
        "run",
        help="Create, update, finalize, and verify immutable run manifests.",
    )
    run_subparsers = run_parser.add_subparsers(
        dest="run_command",
        required=True,
    )
    create_parser = run_subparsers.add_parser(
        "create",
        help="Create a new running manifest from a JSON run spec.",
    )
    create_parser.add_argument("--config", type=Path, required=True)
    create_parser.add_argument(
        "--runs-root",
        type=Path,
        default=Path("research/runs"),
    )
    create_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )
    create_parser.add_argument("--run-id")
    create_parser.add_argument("--allow-dirty", action="store_true")

    record_parser = run_subparsers.add_parser(
        "record",
        help="Record one immutable run artifact.",
    )
    record_parser.add_argument("--run", type=Path, required=True)
    record_parser.add_argument(
        "--field",
        choices=sorted(OUTPUT_FIELDS),
        required=True,
    )
    record_parser.add_argument("--input", type=Path, required=True)
    record_parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
    )

    error_parser = run_subparsers.add_parser(
        "error",
        help="Append a non-final error to a running manifest.",
    )
    error_parser.add_argument("--run", type=Path, required=True)
    error_parser.add_argument("--stage", required=True)
    error_parser.add_argument("--type", default="RunError")
    error_parser.add_argument("--message", required=True)

    complete_parser = run_subparsers.add_parser(
        "complete",
        help="Finalize a run as completed using a metrics JSON file.",
    )
    complete_parser.add_argument("--run", type=Path, required=True)
    complete_parser.add_argument("--metrics", type=Path, required=True)

    fail_parser = run_subparsers.add_parser(
        "fail",
        help="Finalize a run as failed.",
    )
    fail_parser.add_argument("--run", type=Path, required=True)
    fail_parser.add_argument("--stage", required=True)
    fail_parser.add_argument("--type", default="RunError")
    fail_parser.add_argument("--message", required=True)

    run_verify_parser = run_subparsers.add_parser(
        "verify",
        help="Verify manifest, finalization, and artifact hashes.",
    )
    run_verify_parser.add_argument("--run", type=Path, required=True)

    show_parser = run_subparsers.add_parser(
        "show",
        help="Print a run manifest.",
    )
    show_parser.add_argument("--run", type=Path, required=True)

    dataset_parser = subparsers.add_parser(
        "dataset",
        help="Register, split, audit, and verify public predictive datasets.",
    )
    dataset_subparsers = dataset_parser.add_subparsers(
        dest="dataset_command",
        required=True,
    )
    dataset_register_parser = dataset_subparsers.add_parser(
        "register",
        help="Freeze one public dataset registration manifest.",
    )
    dataset_register_parser.add_argument(
        "--config",
        type=Path,
        required=True,
    )
    dataset_register_parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("research/manifests/datasets"),
    )
    dataset_register_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )
    dataset_register_parser.add_argument(
        "--allow-dirty",
        action="store_true",
    )

    dataset_split_parser = dataset_subparsers.add_parser(
        "split",
        help="Create an immutable IID or OOD split manifest.",
    )
    dataset_split_parser.add_argument("--dataset", required=True)
    dataset_split_parser.add_argument(
        "--strategy",
        choices=("iid", "ood"),
        required=True,
    )
    dataset_split_parser.add_argument(
        "--dataset-manifests-root",
        type=Path,
        default=Path("research/manifests/datasets"),
    )
    dataset_split_parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("research/manifests/splits"),
    )
    dataset_split_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )
    dataset_split_parser.add_argument(
        "--allow-dirty",
        action="store_true",
    )

    dataset_verify_parser = dataset_subparsers.add_parser(
        "verify",
        help="Recompute and verify a frozen dataset manifest.",
    )
    dataset_verify_parser.add_argument(
        "--manifest",
        type=Path,
        required=True,
    )
    dataset_verify_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )

    split_verify_parser = dataset_subparsers.add_parser(
        "verify-split",
        help="Recompute and verify a frozen split manifest.",
    )
    split_verify_parser.add_argument(
        "--split",
        type=Path,
        required=True,
    )
    split_verify_parser.add_argument(
        "--dataset-manifest",
        type=Path,
        required=True,
    )
    split_verify_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )

    audit_parser = dataset_subparsers.add_parser(
        "leakage-audit",
        help="Audit label exposure, duplicate crossing, and OOD isolation.",
    )
    audit_parser.add_argument("--dataset", required=True)
    audit_parser.add_argument(
        "--dataset-manifests-root",
        type=Path,
        default=Path("research/manifests/datasets"),
    )
    audit_parser.add_argument("--split", type=Path)
    audit_parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )

    context_parser = dataset_subparsers.add_parser(
        "generation-context",
        help="Print the label-free descriptor-generation dataset context.",
    )
    context_parser.add_argument("--dataset", required=True)
    context_parser.add_argument(
        "--dataset-manifests-root",
        type=Path,
        default=Path("research/manifests/datasets"),
    )
    normalization_parser = subparsers.add_parser(
        "normalization",
        help="Build and verify immutable scientific normalization overlays.",
    )
    normalization_subparsers = normalization_parser.add_subparsers(
        dest="normalization_command",
        required=True,
    )
    normalization_build_parser = normalization_subparsers.add_parser(
        "build",
        help="Build a normalization overlay without modifying frozen inputs.",
    )
    normalization_build_parser.add_argument("--snapshot", type=Path, required=True)
    normalization_build_parser.add_argument("--corpus", type=Path, required=True)
    normalization_build_parser.add_argument("--output", type=Path, required=True)
    normalization_build_parser.add_argument("--config", type=Path, required=True)
    normalization_verify_parser = normalization_subparsers.add_parser(
        "verify",
        help="Verify overlay artifacts and frozen input identities.",
    )
    normalization_verify_parser.add_argument("--overlay", type=Path, required=True)
    normalization_verify_parser.add_argument("--snapshot", type=Path, required=True)
    normalization_verify_parser.add_argument("--corpus", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "show-layout":
        print("\n".join(REQUIRED_DIRECTORIES))
        return 0

    if args.command == "kg":
        try:
            if args.kg_command == "freeze-stage1":
                repository_root = Path(__file__).resolve().parents[3]
                output = freeze_stage1_archive(
                    archive_path=args.input,
                    output_directory=args.output,
                    snapshot_id=args.snapshot_id,
                    knowledge_level=args.knowledge_level,
                    domain=args.domain,
                    expected_papers=args.expected_papers,
                    allowed_systems=set(args.allowed_systems),
                    repository_root=repository_root,
                )
            elif args.kg_command == "build-nested":
                output = build_nested_snapshots(
                    config_path=args.config,
                    repository_root=args.repository_root,
                    allow_dirty=args.allow_dirty,
                )
            elif args.kg_command == "verify-nested":
                output = verify_nested_snapshots(
                    manifest_path=args.manifest,
                    repository_root=args.repository_root,
                )
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
            else:
                output = verify_snapshot(args.snapshot)
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
        except (
            NestedSnapshotError,
            SelectionError,
            OSError,
            ValueError,
            json.JSONDecodeError,
        ) as error:
            print(
                json.dumps(
                    {"ok": False, "error": str(error)},
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1
        print(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.command == "corpus":
        try:
            if args.corpus_command == "freeze-stage1":
                output = freeze_stage1_corpus(
                    archive_path=args.input,
                    output_directory=args.output,
                    corpus_id=args.corpus_id,
                    domain=args.domain,
                    expected_papers=args.expected_papers,
                    allowed_systems=set(args.allowed_systems),
                    repository_root=args.repository_root,
                    expected_archive_sha256=args.expected_sha256,
                    allow_dirty=args.allow_dirty,
                )
            else:
                output = verify_stage1_corpus(args.corpus)
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
        except (
            CorpusError,
            OSError,
            ValueError,
            json.JSONDecodeError,
        ) as error:
            print(
                json.dumps(
                    {"ok": False, "error": str(error)},
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1
        print(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.command == "normalization":
        try:
            if args.normalization_command == "build":
                output = build_normalization_overlay(
                    snapshot_directory=args.snapshot,
                    corpus_directory=args.corpus,
                    output_directory=args.output,
                    config_path=args.config,
                )
            else:
                output = verify_normalization_overlay(
                    overlay_directory=args.overlay,
                    snapshot_directory=args.snapshot,
                    corpus_directory=args.corpus,
                )
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
        except (
            NormalizationError,
            OSError,
            ValueError,
            KeyError,
            json.JSONDecodeError,
            zipfile.BadZipFile,
        ) as error:
            print(
                json.dumps(
                    {"ok": False, "error": str(error)},
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1
        print(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.command == "run":
        try:
            if args.run_command == "create":
                spec = json.loads(
                    args.config.read_text(encoding="utf-8")
                )
                result = create_run(
                    runs_root=args.runs_root,
                    spec=spec,
                    repository_root=args.repository_root,
                    allow_dirty=args.allow_dirty,
                    run_id=args.run_id,
                )
                output = {
                    "run_id": result["run_id"],
                    "run_directory": result["run_directory"],
                    "manifest_content_hash": result["manifest"][
                        "manifest_content_hash"
                    ],
                }
            elif args.run_command == "record":
                if args.format == "json":
                    value = json.loads(
                        args.input.read_text(encoding="utf-8")
                    )
                    media_type = "application/json"
                else:
                    value = args.input.read_text(encoding="utf-8")
                    media_type = "text/plain"
                output = record_artifact(
                    run_directory=args.run,
                    field=args.field,
                    value=value,
                    media_type=media_type,
                )
            elif args.run_command == "error":
                output = record_error(
                    run_directory=args.run,
                    stage=args.stage,
                    error_type=args.type,
                    message=args.message,
                )
            elif args.run_command == "complete":
                output = complete_run(
                    run_directory=args.run,
                    metrics=json.loads(
                        args.metrics.read_text(encoding="utf-8")
                    ),
                )
            elif args.run_command == "fail":
                output = fail_run(
                    run_directory=args.run,
                    stage=args.stage,
                    error_type=args.type,
                    message=args.message,
                )
            elif args.run_command == "show":
                output = load_manifest(args.run)
            else:
                output = verify_run(args.run)
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
        except (RunManifestError, OSError, json.JSONDecodeError) as error:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": str(error),
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1
        print(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.command == "dataset":
        try:
            if args.dataset_command == "register":
                result = register_dataset(
                    config_path=args.config,
                    output_root=args.output_root,
                    repository_root=args.repository_root,
                    allow_dirty=args.allow_dirty,
                )
                output = {
                    "dataset_id": result["dataset_id"],
                    "manifest_path": result["manifest_path"],
                    "dataset_content_hash": result["manifest"][
                        "dataset_content_hash"
                    ],
                    "manifest_content_hash": result["manifest"][
                        "manifest_content_hash"
                    ],
                }
            elif args.dataset_command == "split":
                dataset_manifest_path = (
                    args.dataset_manifests_root
                    / f"{args.dataset}.manifest.json"
                )
                result = create_split(
                    dataset_manifest_path=dataset_manifest_path,
                    strategy=args.strategy,
                    output_root=args.output_root,
                    repository_root=args.repository_root,
                    allow_dirty=args.allow_dirty,
                )
                output = {
                    "split_id": result["split_id"],
                    "split_path": result["split_path"],
                    "split_hash": result["manifest"]["split_hash"],
                }
            elif args.dataset_command == "verify":
                output = verify_dataset_manifest(
                    args.manifest,
                    args.repository_root,
                )
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
            elif args.dataset_command == "verify-split":
                output = verify_split_manifest(
                    split_manifest_path=args.split,
                    dataset_manifest_path=args.dataset_manifest,
                    repository_root=args.repository_root,
                )
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
            elif args.dataset_command == "leakage-audit":
                dataset_manifest_path = (
                    args.dataset_manifests_root
                    / f"{args.dataset}.manifest.json"
                )
                output = leakage_audit(
                    dataset_manifest_path=dataset_manifest_path,
                    repository_root=args.repository_root,
                    split_manifest_path=args.split,
                )
                print(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0 if output["valid"] else 1
            else:
                dataset_manifest_path = (
                    args.dataset_manifests_root
                    / f"{args.dataset}.manifest.json"
                )
                output = generation_context(
                    load_dataset_manifest(dataset_manifest_path)
                )
        except (
            DatasetError,
            OSError,
            json.JSONDecodeError,
        ) as error:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": str(error),
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1
        print(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    status = inspect_layout(args.root)
    print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
