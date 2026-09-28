"""Replay a harness artifact at one-shot and multiple feedback-loop lengths."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.harness import (  # noqa: E402
    HarnessController,
    HttpJevClient,
    RuleBasedJev,
    run_round_prefix_experiment,
)
from catalysis_research.harness.types import RoundInput  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, required=True,
        help="JSON with run_id, rounds and optional run_context (same input as run_harness.py)",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--rounds", default="1,3,5",
        help="Comma-separated prefix lengths, or one-shot; defaults to 1,3,5",
    )
    parser.add_argument("--judge", choices=("rule", "jev"), default="rule")
    parser.add_argument(
        "--oracle-key", default="useful",
        help="Optional boolean candidate field used for recall/false-rejection metrics",
    )
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    rounds = [RoundInput(**item) for item in payload.get("rounds", [])]
    judge = RuleBasedJev() if args.judge == "rule" else HttpJevClient()
    result = run_round_prefix_experiment(
        controller=HarnessController(judge=judge),
        run_id=str(payload.get("run_id") or "harness-round-experiment"),
        rounds=rounds,
        round_counts=args.rounds,
        run_context=payload.get("run_context") or {},
        oracle_key=args.oracle_key,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
