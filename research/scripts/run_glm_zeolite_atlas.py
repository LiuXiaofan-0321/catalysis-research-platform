from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))
sys.path.insert(0, str(RESEARCH_ROOT / "literature_pipeline" / "src"))

from catalysis_research.experiments.zeolite_atlas import DEFAULT_MODEL, run_zeolite_atlas_loop  # noqa: E402
from catalysis_research.retrieval import KnowledgeModeRetriever, RetrievalBudget  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exploratory GLM comparison on Materials Cloud Zeolite Atlas.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--rag-index", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--dataset-root", type=Path, required=True, help="extracted Materials Cloud archive root")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=4500)
    parser.add_argument("--thinking", choices=("disabled", "enabled"), default="enabled")
    parser.add_argument("--reasoning-effort", choices=("low", "high", "max"), default="low")
    parser.add_argument("--replicate-id", type=int)
    parser.add_argument("--mode", action="append", dest="modes")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    service = KnowledgeModeRetriever.from_directories(config_path=args.config, rag_index_directory=args.rag_index, kg_snapshot_directory=args.snapshot, normalization_overlay_directory=args.overlay)
    result = run_zeolite_atlas_loop(service=service, dataset_root=args.dataset_root, output_path=args.output, task=args.task, query=args.query, budget=RetrievalBudget(**config["budget"]), model=args.model, temperature=args.temperature, max_tokens=args.max_tokens, thinking=args.thinking, reasoning_effort=args.reasoning_effort, replicate_id=args.replicate_id, modes=args.modes or ("agent", "rag_agent", "small_kg_rag_agent"))
    print(json.dumps({"output": str(args.output.resolve()), "run_classification": result["run_classification"], "modes": {mode: row.get("status") for mode, row in result["modes"].items()}}, ensure_ascii=False, indent=2))
    return 0 if all(row.get("status") == "completed" for row in result["modes"].values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
