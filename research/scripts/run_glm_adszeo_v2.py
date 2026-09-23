from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))
sys.path.insert(0, str(RESEARCH_ROOT / "literature_pipeline" / "src"))

from catalysis_research.experiments.adszeo_v2 import (  # noqa: E402
    DEFAULT_MODEL,
    EVIDENCE_FAMILY_QUERIES,
    run_adszeo_v2_loop,
)
from catalysis_research.experiments.adszeo_nomination import run_adszeo_nomination_loop  # noqa: E402
from catalysis_research.retrieval import KnowledgeModeRetriever, RetrievalBudget  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the AdsZeo v2 geometry-catalog three-mode benchmark.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--rag-index", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--geometry-csv", type=Path, required=True)
    parser.add_argument("--database-sha256", help="Precomputed SHA256 of the DuckDB database.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task")
    parser.add_argument("--query")
    parser.add_argument("--model")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--thinking", choices=("disabled", "enabled"))
    parser.add_argument("--reasoning-effort", choices=("none", "low", "high", "max"))
    parser.add_argument("--replicate-id", type=int)
    parser.add_argument("--rounds", type=int)
    parser.add_argument("--purified-evidence", action="store_true",
                        help="Retrieve per evidence family (topology/pore/composition) and merge under the same budgets.")
    parser.add_argument("--open-nomination", action="store_true",
                        help="Free-form descriptor nomination with the restricted DSL executor (no candidate catalog).")
    parser.add_argument("--mode", action="append", dest="modes")
    args = parser.parse_args()
    if args.database_sha256 is not None:
        value = args.database_sha256.strip().lower()
        if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            parser.error("--database-sha256 must be 64 hexadecimal characters")
        args.database_sha256 = value

    config = json.loads(args.config.read_text(encoding="utf-8"))
    experiment = config["experiment"]
    service = KnowledgeModeRetriever.from_directories(
        config_path=args.config,
        rag_index_directory=args.rag_index,
        kg_snapshot_directory=args.snapshot,
        normalization_overlay_directory=args.overlay,
    )
    common = dict(
        service=service,
        database_path=args.database,
        geometry_csv=args.geometry_csv,
        output_path=args.output,
        task=args.task or experiment["task"],
        query=args.query or experiment["query"],
        budget=RetrievalBudget(**config["budget"]),
        model=args.model or experiment["model"],
        temperature=args.temperature if args.temperature is not None else experiment["temperature"],
        max_tokens=args.max_tokens or experiment["max_tokens"],
        thinking=args.thinking or experiment["thinking"],
        reasoning_effort=(None if (args.reasoning_effort or experiment["reasoning_effort"]) == "none"
                          else (args.reasoning_effort or experiment["reasoning_effort"])),
        replicate_id=args.replicate_id,
        rounds=args.rounds or experiment.get("rounds", 3),
        database_sha256=args.database_sha256,
    )
    if args.open_nomination:
        result = run_adszeo_nomination_loop(
            modes=args.modes or ("agent", "rag_agent", "small_kg_rag_agent"),
            proposal_count=experiment.get("selected_descriptor_count", 3),
            **common,
        )
    else:
        result = run_adszeo_v2_loop(
            modes=args.modes or ("agent", "rag_agent", "small_kg_rag_agent"),
            selected_descriptor_count=experiment["selected_descriptor_count"],
            evidence_queries=EVIDENCE_FAMILY_QUERIES if args.purified_evidence else None,
            **common,
        )
    statuses = {mode: row.get("status") for mode, row in result["modes"].items()}
    print(json.dumps({"output": str(args.output.resolve()), "modes": statuses}, ensure_ascii=False, indent=2))
    return 0 if all(status == "completed" for status in statuses.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
