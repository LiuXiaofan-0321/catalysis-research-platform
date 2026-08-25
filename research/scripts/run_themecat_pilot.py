from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.experiments.themecat_pilot import run_pilot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the explicitly exploratory TheMeCat + DeepSeek pilot."
    )
    parser.add_argument(
        "--raw",
        type=Path,
        default=RESEARCH_ROOT / "datasets" / "raw" / "TheMeCat_v1.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=RESEARCH_ROOT / "runs" / "themecat-deepseek-exploratory-v1" / "result.json",
    )
    parser.add_argument("--model", default="deepseek-v4-flash")
    args = parser.parse_args()
    result = run_pilot(raw_path=args.raw, output_path=args.output, model=args.model)
    summary = {
        "run_classification": result["run_classification"],
        "output": str(args.output.resolve()),
        "model": result["model"]["provider_model"],
        "selected_descriptor_ids": result["generation"]["selected_descriptor_ids"],
        "baseline_macro_ood_rmse": result["downstream"]["baseline"]["macro_test_rmse"],
        "deepseek_macro_ood_rmse": result["downstream"]["deepseek_descriptors"]["macro_test_rmse"],
        "exploratory_normalized_rmse_improvement": result["downstream"]["exploratory_normalized_rmse_improvement"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
