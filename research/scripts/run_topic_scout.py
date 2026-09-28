"""Run the reproducible hot-topic scout on a frozen record artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.harness import JevTopicScout, RuleBasedTopicScout  # noqa: E402


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSON list or object containing records")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cutoff", required=True, help="Frozen ISO date used as the as-of boundary")
    parser.add_argument("--corpus-hash", help="Pinned corpus hash; defaults to SHA256 of --input")
    parser.add_argument("--scout", choices=("rule", "jev"), default="rule")
    parser.add_argument("--window-days", type=int, default=365)
    parser.add_argument("--half-life-days", type=float, default=365.0)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    records = payload.get("records", payload) if isinstance(payload, dict) else payload
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        parser.error("input must be a JSON list of records or an object with a records list")
    corpus_hash = args.corpus_hash or _sha256(args.input)
    if args.scout == "rule":
        scout = RuleBasedTopicScout(window_days=args.window_days, half_life_days=args.half_life_days)
    else:
        scout = JevTopicScout()
    result = scout.scout(records, cutoff=args.cutoff, corpus_hash=corpus_hash)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
