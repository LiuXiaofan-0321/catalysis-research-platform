from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "show-layout":
        print("\n".join(REQUIRED_DIRECTORIES))
        return 0

    status = inspect_layout(args.root)
    print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
