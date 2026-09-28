"""Summarize a completed AdsZeo v5 single-adaptive-score array."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

from adszeo_v5_analyze import mean_ci, sign_flip_p


MODES = ("agent", "rag_agent", "small_kg_rag_agent")
PAIRS = (("rag_agent", "agent"),
         ("small_kg_rag_agent", "rag_agent"),
         ("small_kg_rag_agent", "agent"))


def summarize(directory: Path) -> dict:
    paths = sorted(directory.glob("replicate-*.json"))
    if len(paths) != 10:
        raise ValueError(f"Expected 10 result files, found {len(paths)}")
    runs = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    runs.sort(key=lambda row: row["replicate_id"])
    if [row["replicate_id"] for row in runs] != list(range(1, 11)):
        raise ValueError("Replicate IDs are incomplete or duplicated")
    baseline_scores: list[float] = []
    values: dict[str, list[float]] = {mode: [] for mode in MODES}
    result = {"n": len(runs), "outcome": "adaptive_validation_score_not_independent_test",
              "modes": {}, "paired": {}}
    for run in runs:
        if (run["evaluation_protocol"] != "single_adaptive_score"
                or run["outcome_split"] != "validation" or run["test_evaluated"] is not False
                or run["rounds"] != 3 or run["proposal_count"] != 3):
            raise ValueError(f"Unexpected protocol in replicate {run['replicate_id']}")
        if set(run["modes"]) != set(MODES):
            raise ValueError(f"Missing knowledge mode in replicate {run['replicate_id']}")
        for mode in MODES:
            row = run["modes"][mode]
            if (row["status"] != "completed" or len(row["rounds"]) != 3
                    or row["model"]["model"] != "glm-5.3-flash"):
                raise ValueError(f"Incomplete {mode} in replicate {run['replicate_id']}")
            if any(len(item["execution_feedback"]) != 3 for item in row["rounds"]):
                raise ValueError(f"Incorrect proposal budget in replicate {run['replicate_id']}")
            outcome = row["downstream"]
            if outcome["test_evaluated"] is not False or outcome["outcome_split"] != "validation":
                raise ValueError(f"Test outcome unexpectedly present in replicate {run['replicate_id']}")
            if "test" in outcome["D0"] or "test" in outcome["D0_plus_X"]:
                raise ValueError(f"Test metrics unexpectedly present in replicate {run['replicate_id']}")
            d0 = outcome["D0"]["validation_topology_macro_mae_mol_kg"]
            final = outcome["D0_plus_X"]["validation_topology_macro_mae_mol_kg"]
            if abs(final - row["rounds"][-1]["validation_after_topology_macro_mae_mol_kg"]) > 1e-10:
                raise ValueError(f"Final score mismatch in replicate {run['replicate_id']}")
            improvement = 100 * (d0 - final) / d0
            if improvement < -1e-9 or abs(improvement - 100 * row["topology_macro_mae_relative_improvement"]) > 1e-9:
                raise ValueError(f"Improvement mismatch in replicate {run['replicate_id']}")
            baseline_scores.append(d0)
            values[mode].append(improvement)
    if max(baseline_scores) - min(baseline_scores) > 1e-10:
        raise ValueError("D0 score differs across modes or replicates")
    result["d0_score_topology_macro_mae_mol_kg"] = baseline_scores[0]
    for mode in MODES:
        rows = [run["modes"][mode] for run in runs]
        scores = values[mode]
        feedback = [entry for row in rows for item in row["rounds"] for entry in item["execution_feedback"]]
        statuses = Counter(entry["status"] for entry in feedback)
        result["modes"][mode] = {
            "improvement_pct_by_replicate": scores,
            "improvement_pct_mean": statistics.mean(scores),
            "improvement_pct_median": statistics.median(scores),
            "improvement_pct_sd": statistics.stdev(scores),
            "improvement_pct_mean_bootstrap_95_ci": mean_ci(scores),
            "improvement_positive_count": sum(value > 0 for value in scores),
            "final_score_mean_mol_kg": statistics.mean(
                row["downstream"]["D0_plus_X"]["validation_topology_macro_mae_mol_kg"] for row in rows),
            "retained_descriptors_mean": statistics.mean(len(row["final_executed_descriptor_ids"]) for row in rows),
            "proposal_status_counts": dict(statuses),
            "prompt_tokens_per_round_mean": sum(row["model"]["total_usage"].get("prompt_tokens", 0)
                                                for row in rows) / (3 * len(rows)),
        }
    for better, worse in PAIRS:
        differences = [a - b for a, b in zip(values[better], values[worse])]
        result["paired"][f"{better}_minus_{worse}"] = {
            "mean_percentage_points": statistics.mean(differences),
            "mean_bootstrap_95_ci": mean_ci(differences, seed=23),
            "positive_count": sum(value > 0 for value in differences),
            "exact_two_sided_sign_flip_p": sign_flip_p(differences),
        }
    result["kg_greater_rag_greater_agent_count"] = sum(
        values["small_kg_rag_agent"][i] > values["rag_agent"][i] > values["agent"][i]
        for i in range(len(runs))
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.run_directory), ensure_ascii=False, indent=2))
