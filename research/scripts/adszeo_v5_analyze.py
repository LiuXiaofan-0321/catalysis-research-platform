"""Summarize a completed AdsZeo v5 array with paired replicate comparisons."""

from __future__ import annotations

import argparse
import itertools
import json
import random
import statistics
from collections import Counter
from pathlib import Path


MODES = ("agent", "rag_agent", "small_kg_rag_agent")
PAIRS = (
    ("rag_agent", "agent"),
    ("small_kg_rag_agent", "rag_agent"),
    ("small_kg_rag_agent", "agent"),
)


def mean_ci(values: list[float], *, seed: int = 17, draws: int = 20_000) -> list[float]:
    rng = random.Random(seed)
    n = len(values)
    draws_sorted = sorted(statistics.mean(rng.choices(values, k=n)) for _ in range(draws))
    return [draws_sorted[int(0.025 * draws)], draws_sorted[int(0.975 * draws)]]


def sign_flip_p(values: list[float]) -> float:
    observed = abs(statistics.mean(values))
    tolerance = 1e-12
    more_extreme = sum(
        abs(statistics.mean(sign * value for sign, value in zip(signs, values)))
        >= observed - tolerance
        for signs in itertools.product((-1, 1), repeat=len(values))
    )
    return more_extreme / (2 ** len(values))


def summarize(directory: Path) -> dict:
    paths = sorted(directory.glob("replicate-*.json"))
    if not paths:
        raise ValueError(f"No replicate results in {directory}")
    runs = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    ids = [run["replicate_id"] for run in runs]
    if sorted(ids) != list(range(1, len(ids) + 1)) or len(set(ids)) != len(ids):
        raise ValueError(f"Replicate IDs are missing or duplicated: {ids}")
    runs.sort(key=lambda run: run["replicate_id"])
    for run in runs:
        if run["rounds"] != 3 or run["proposal_count"] != 3:
            raise ValueError(f"Unexpected protocol in replicate {run['replicate_id']}")
        if run["protocol_status"] != "FROZEN_BEFORE_OUTCOME_RUN":
            raise ValueError(f"Unexpected protocol status in replicate {run['replicate_id']}")
        if set(run["modes"]) != set(MODES):
            raise ValueError(f"Missing mode in replicate {run['replicate_id']}")
        for mode in MODES:
            row = run["modes"][mode]
            if row["status"] != "completed" or len(row["rounds"]) != 3:
                raise ValueError(f"Incomplete {mode} in replicate {run['replicate_id']}")
            if row["model"]["requested_model"] != "glm-5.3-flash" or row["model"]["model"] != "glm-5.3-flash":
                raise ValueError(f"Unexpected model for {mode} in replicate {run['replicate_id']}")
            if any(len(round_row["execution_feedback"]) != 3 for round_row in row["rounds"]):
                raise ValueError(f"Unexpected proposal count for {mode} in replicate {run['replicate_id']}")
            if any(sum(bool(entry.get("retained")) for entry in round_row["execution_feedback"]) > 1
                   for round_row in row["rounds"]):
                raise ValueError(f"Multiple candidates retained in one round for {mode} in replicate {run['replicate_id']}")

    d0 = [run["modes"][mode]["downstream"]["D0"]["test"]["topology_macro_mae_mol_kg"]
          for run in runs for mode in MODES]
    if max(d0) - min(d0) > 1e-10:
        raise ValueError("D0 test MAE changed across replicates")

    result: dict = {
        "replicate_ids": ids,
        "n": len(runs),
        "d0_test_topology_macro_mae_mol_kg": d0[0],
        "modes": {},
        "paired": {},
    }
    improvements: dict[str, list[float]] = {}
    for mode in MODES:
        rows = [run["modes"][mode] for run in runs]
        imp = [100 * row["topology_macro_mae_relative_improvement"] for row in rows]
        improvements[mode] = imp
        test_mae = [row["downstream"]["D0_plus_X"]["test"]["topology_macro_mae_mol_kg"] for row in rows]
        val_imp = [
            100 * (row["rounds"][0]["validation_before_topology_macro_mae_mol_kg"]
                   - row["rounds"][-1]["validation_after_topology_macro_mae_mol_kg"])
            / row["rounds"][0]["validation_before_topology_macro_mae_mol_kg"]
            for row in rows
        ]
        retained = [len(row["final_executed_descriptor_ids"]) for row in rows]
        feedback = [entry for row in rows for round_row in row["rounds"] for entry in round_row["execution_feedback"]]
        statuses = Counter(entry["status"] for entry in feedback)
        failures = Counter(entry.get("failure_code") for entry in feedback if entry["status"] == "failed")
        selected_formulas = [item["formula"] for row in rows for item in row["accepted_catalog"].values()]
        prompt_tokens = sum(row["model"]["total_usage"].get("prompt_tokens", 0) for row in rows)
        completion_tokens = sum(row["model"]["total_usage"].get("completion_tokens", 0) for row in rows)
        result["modes"][mode] = {
            "test_improvement_pct_by_replicate": imp,
            "test_improvement_pct_mean": statistics.mean(imp),
            "test_improvement_pct_sd": statistics.stdev(imp),
            "test_improvement_pct_median": statistics.median(imp),
            "test_improvement_pct_mean_bootstrap_95_ci": mean_ci(imp),
            "test_improvement_exact_two_sided_sign_flip_p": sign_flip_p(imp),
            "test_improvement_positive_count": sum(value > 0 for value in imp),
            "test_topology_macro_mae_mol_kg_mean": statistics.mean(test_mae),
            "validation_improvement_pct_mean": statistics.mean(val_imp),
            "validation_improvement_positive_count": sum(value > 0 for value in val_imp),
            "retained_descriptor_count_by_replicate": retained,
            "retained_descriptor_count_mean": statistics.mean(retained),
            "retained_descriptor_count_histogram": dict(sorted(Counter(retained).items())),
            "proposal_feedback_count": len(feedback),
            "proposal_status_counts": dict(statuses),
            "proposal_execution_rate": statuses["executed"] / len(feedback),
            "failure_taxonomy_counts": dict(failures),
            "selected_formula_count": len(selected_formulas),
            "selected_formula_unique_count": len(set(selected_formulas)),
            "retrieved_items_mean": statistics.mean(len(row["bundle"]["items"]) for row in rows),
            "retrieved_context_chars_mean": statistics.mean(len(row["bundle"]["context"]) for row in rows),
            "model_prompt_tokens": prompt_tokens,
            "model_prompt_tokens_per_round_mean": prompt_tokens / (3 * len(rows)),
            "model_completion_tokens": completion_tokens,
            "model_total_tokens": sum(row["model"]["total_usage"].get("total_tokens", 0) for row in rows),
        }

    for better, worse in PAIRS:
        diff = [a - b for a, b in zip(improvements[better], improvements[worse])]
        result["paired"][f"{better}_minus_{worse}"] = {
            "percentage_points_by_replicate": diff,
            "mean_percentage_points": statistics.mean(diff),
            "mean_bootstrap_95_ci": mean_ci(diff, seed=23),
            "count_better": sum(value > 0 for value in diff),
            "exact_two_sided_sign_flip_p": sign_flip_p(diff),
        }
    result["ordered_counts"] = {
        "kg_greater_rag_greater_agent": sum(
            improvements["small_kg_rag_agent"][i] > improvements["rag_agent"][i] > improvements["agent"][i]
            for i in range(len(runs))
        ),
        "agent_greater_rag_greater_kg": sum(
            improvements["agent"][i] > improvements["rag_agent"][i] > improvements["small_kg_rag_agent"][i]
            for i in range(len(runs))
        ),
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.run_directory), ensure_ascii=False, indent=2))
