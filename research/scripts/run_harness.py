"""Run the offline harness or a configured Jev endpoint on JSON rounds."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.harness import HarnessController, HttpJevClient, RuleBasedJev
from catalysis_research.harness.types import RoundInput


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSON with run_id, rounds and optional run_context")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--judge", choices=("rule", "jev"), default="rule")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    rounds = [RoundInput(**item) for item in payload.get("rounds", [])]
    judge = RuleBasedJev() if args.judge == "rule" else HttpJevClient()
    result = HarnessController(judge=judge).run(
        run_id=str(payload.get("run_id") or "harness-run"),
        rounds=rounds,
        run_context=payload.get("run_context") or {},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
