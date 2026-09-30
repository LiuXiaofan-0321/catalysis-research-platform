"""Read-only reproduction of proposal feasibility and budget diagnostics.

No model API calls, fitting, or server access. The only writes are this report's
JSON. Uses native input values, not score/test labels, for formula diagnostics.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import statistics
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(REPO / "research/src"), str(REPO / "research/scripts")]
from catalysis_research.experiments.jacs_au import FEATURES, load_data, make_split
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from run_jacs_au import evaluate_formula


def audit(data_root: Path) -> dict:
    data = load_data(data_root)
    train = make_split(data)["train"]
    env, _ = formula_environment(data, train)
    result = {
        "method": "Read-only audit: native training features and completed saved trajectories; no new fitting or generation.",
        "train_n": len(train),
        "feature_zero_counts": {},
        "modes": {},
    }
    for name in FEATURES:
        values = env[name][train]
        zeros = values == 0
        result["feature_zero_counts"][name] = {
            "exact_zero": int(zeros.sum()),
            "exact_zero_pct": float(100 * zeros.mean()),
            "abs_below_1e_12": int((np.abs(values) < 1e-12).sum()),
            "minimum": float(values.min()),
            "zero_molecule_counts": dict(Counter(str(data["keys"][i][1]) for i in train[zeros])),
            "zero_framework_counts": dict(Counter(str(data["keys"][i][0]) for i in train[zeros])) if name in ("ASA", "AV") else {},
        }
    root = REPO / "research/reports/jacs_au_kg_v3_repair_20260929/server-results/discovery"
    for mode in ("agent", "rag_agent", "small_kg_rag_agent"):
        trajectories = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(root.glob(mode + "-replicate-*.json"))]
        rounds = [r for d in trajectories for r in d["rounds"]]
        candidates = [c for r in rounds for c in r["candidates"]]
        usages = [u for r in rounds for u in r["usage"]]
        group = {
            "trajectories": len(trajectories),
            "proposals": len(candidates),
            "scored": sum(c["status"] == "scored" for c in candidates),
            "positive_scored": sum(c.get("marginal_improvement", 0) > 0 for c in candidates),
            "retained": sum(c["retained"] for c in candidates),
            "reasons": dict(Counter(c["reason"] for c in candidates if c["status"] == "rejected")),
            "mean_full_request_lexical_tokens": statistics.mean(r["full_request_lexical_tokens"] for r in rounds),
            "api_calls": len(usages),
            "api_token_totals": {k: sum(u.get(k, 0) for u in usages) for k in ("prompt_tokens", "completion_tokens", "total_tokens")},
            "round_mean_gain_d0_percentage_points": {
                str(k): statistics.mean(100 * (r["before_mae_R"] - r["after_mae_R"]) / d["d0_score_mae_R"] for d in trajectories for r in d["rounds"] if r["round"] == k)
                for k in (1, 2, 3)
            },
            "completion_finish_reasons": dict(Counter(a["finish_reason"] for r in rounds for a in r["completion_attempts"])),
            "unstable_reproduction": [],
        }
        for d in trajectories:
            for r in d["rounds"]:
                for c in r["candidates"]:
                    if c.get("reason") != "Formula unstable inside declared physical regime":
                        continue
                    spec = c["scientific_test"]
                    local = {k: v[train].copy() for k, v in env.items()}
                    axis = local[spec["regime_input"]]
                    low, high = np.quantile(axis, spec["regime_train_quantiles"])
                    mask = (axis >= low) & (axis <= high)
                    variable = spec["vary_input"]
                    values = local[variable]
                    step = max(float(np.quantile(values, .9) - np.quantile(values, .1)) * .01, 1e-8)
                    plus = {k: v.copy() for k, v in local.items()}
                    plus[variable] = values + step
                    plus["q_" + variable] = plus[variable] / plus[variable + "_ref"]
                    before = evaluate_formula(c["formula"], local)
                    after = evaluate_formula(c["formula"], plus)
                    bad = mask & ~(np.isfinite(before) & np.isfinite(after))
                    group["unstable_reproduction"].append({
                        "replicate": d["replicate"], "round": r["round"],
                        "name": c["name"], "formula": c["formula"],
                        "regime_input": spec["regime_input"],
                        "regime_quantiles": spec["regime_train_quantiles"],
                        "global_nonfinite_before": int((~np.isfinite(before)).sum()),
                        "regime_n": int(mask.sum()), "nonfinite_regime_n": int(bad.sum()),
                        "nonfinite_regime_pct": float(100 * bad.sum() / mask.sum()),
                        "native_zero_overlap": {name: int(((local[name] == 0) & bad).sum()) for name in FEATURES if ((local[name] == 0) & bad).any()},
                    })
        result["modes"][mode] = group
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("design_audit.json"))
    args = parser.parse_args()
    payload = audit(args.data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "modes": {k: {x: v[x] for x in ("proposals", "scored", "retained", "api_calls")} for k, v in payload["modes"].items()}}, ensure_ascii=False))
