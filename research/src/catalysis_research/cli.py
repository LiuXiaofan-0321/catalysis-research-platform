from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .kg.freeze_stage1 import freeze_stage1_archive, verify_snapshot
from .layout import REQUIRED_DIRECTORIES, inspect_layout


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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "show-layout":
        print("\n".join(REQUIRED_DIRECTORIES))
        return 0

    if args.command == "kg":
        if args.kg_command == "freeze-stage1":
            repository_root = Path(__file__).resolve().parents[3]
            manifest = freeze_stage1_archive(
                archive_path=args.input,
                output_directory=args.output,
                snapshot_id=args.snapshot_id,
                knowledge_level=args.knowledge_level,
                domain=args.domain,
                expected_papers=args.expected_papers,
                allowed_systems=set(args.allowed_systems),
                repository_root=repository_root,
            )
            print(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        report = verify_snapshot(args.snapshot)
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if report["valid"] else 1

    status = inspect_layout(args.root)
    print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
