"""Read-only reconstruction of KG-v3 formula checks. No fitting or API calls."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from catalysis_research.experiments.jacs_au import FEATURES, load_data, make_split
from catalysis_research.experiments.jacs_au_knowledge import formula_environment, audit_dimensions
from catalysis_research.experiments.jacs_au_kg_v3 import scientific_check

spec = importlib.util.spec_from_file_location("runner_numeric_audit", ROOT / "scripts/run_jacs_au.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def domain_operations(formula, env):
    """Trace exact DSL domain failures to primitive operations, without repair."""
    out = []
    n = len(next(iter(env.values())))

    def array(v):
        return np.broadcast_to(np.asarray(v, dtype=float), (n,))

    def issue(node, kind, mask):
        if np.any(mask):
            out.append({"operation": kind, "subexpression": ast.unparse(node),
                        "mask": np.asarray(mask, dtype=bool)})

    def visit(node):
        if isinstance(node, ast.Constant):
            return float(node.value)
        if isinstance(node, ast.Name):
            return env[node.id]
        if isinstance(node, ast.UnaryOp):
            v = visit(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return a + b
            if isinstance(node.op, ast.Sub): return a - b
            if isinstance(node.op, ast.Mult): return a * b
            if isinstance(node.op, ast.Div):
                issue(node, "zero_denominator", array(b) == 0)
                return np.divide(a, b)
            if isinstance(node.op, ast.Pow):
                values = np.power(a, b)
                issue(node, "power_domain", ~np.isfinite(array(values)) & np.isfinite(array(a)))
                return values
        if isinstance(node, ast.Call):
            args = [visit(a) for a in node.args]
            fname = node.func.id
            if fname in ("log", "log10"):
                issue(node, "nonpositive_log_argument", array(args[0]) <= 0)
            if fname == "sqrt": issue(node, "negative_sqrt_argument", array(args[0]) < 0)
            return runner.FUNCTIONS[fname](*args)
        raise ValueError("Unsupported node")

    with np.errstate(all="ignore"):
        visit(ast.parse(formula, mode="eval").body)
    return out


def main():
    data_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "C:/Users/18963/AppData/Local/Temp/jacs-au-4c00429/Supporting_final_2")
    source = ROOT / "reports/jacs_au_kg_v3_repair_20260929/server-results"
    destination = Path(__file__).parent
    data = load_data(data_root)
    split = make_split(data)
    train = split["train"]
    env, refs = formula_environment(data, train)
    local = {k: np.asarray(v)[train].copy() for k, v in env.items()}
    feature_stats = {}
    for i, name in enumerate(FEATURES):
        v = data["x"][train, i]
        feature_stats[name] = {
            "min": float(v.min()), "max": float(v.max()), "zero": int((v == 0).sum()),
            "negative": int((v < 0).sum()), "small_positive_under_1e12": int(((v > 0) & (v < 1e-12)).sum()),
            "zero_pct": 100 * float((v == 0).mean()), "reference": refs[name],
            "zero_molecules": dict(Counter(str(x[1]) for x in data["keys"][train[v == 0]])),
            "zero_frameworks": dict(Counter(str(x[0]) for x in data["keys"][train[v == 0]])),
        }

    records = []
    all_ref_exact = True
    for folder, label in [("discovery", "main"), ("ablation-flat/discovery", "flat")]:
        for path in sorted((source / folder).glob("*.json")):
            run = json.loads(path.read_text(encoding="utf-8"))
            all_ref_exact &= refs == run["training_references"]
            retained_values = []
            for rnd in run["rounds"]:
                reference_matrix = np.column_stack([data["x"]] + retained_values)
                winner = None
                for ci, candidate in enumerate(rnd["candidates"]):
                    c = candidate
                    rec = {"group": label, "mode": run["mode"], "replicate": run["replicate"],
                           "round": rnd["round"], "candidate_index": ci, "name": c["name"],
                           "formula": c["formula"], "status": c["status"], "reason": c.get("reason"),
                           "retained": c["retained"], "scientific_test": c["scientific_test"],
                           "score": c.get("score"), "marginal_improvement": c.get("marginal_improvement")}
                    try:
                        audit_dimensions(c["formula"])
                        with np.errstate(all="ignore"):
                            scientific_check(c, env, train, data["entropy"], runner.evaluate_formula)
                        runner.checked_feature(c["formula"], env, reference_matrix, train)
                        reproduced = "scored"
                    except (ValueError, SyntaxError, FloatingPointError, OverflowError) as error:
                        reproduced = str(error)
                    rec["reproduced_check_result"] = reproduced
                    rec["result_matches"] = reproduced == ("scored" if c["status"] == "scored" else c["reason"])
                    try:
                        values = runner.evaluate_formula(c["formula"], env)
                        st = c["scientific_test"]
                        low, high = np.quantile(local[st["regime_input"]], st["regime_train_quantiles"])
                        mask = (local[st["regime_input"]] >= low) & (local[st["regime_input"]] <= high)
                        variable = st["vary_input"]
                        step = max(float(np.quantile(local[variable], .9) - np.quantile(local[variable], .1)) * .01, 1e-8)
                        plus = {k: v.copy() for k, v in local.items()}
                        plus[variable] += step
                        plus["q_" + variable] = plus[variable] / plus[variable + "_ref"]
                        before = values[train]
                        after = runner.evaluate_formula(c["formula"], plus)
                        finite = mask & np.isfinite(before) & np.isfinite(after)
                        rec.update(regime_n=int(mask.sum()), native_regime_bounds=[float(low), float(high)],
                                   nonfinite_before_regime=int((mask & ~np.isfinite(before)).sum()),
                                   nonfinite_after_regime=int((mask & ~np.isfinite(after)).sum()),
                                   nonfinite_union_regime=int((mask & ~finite).sum()),
                                   nonfinite_union_regime_pct=100 * float((mask & ~finite).sum()) / mask.sum(),
                                   nonfinite_global_train=int((~np.isfinite(before)).sum()),
                                   nonfinite_global_train_pct=100 * float((~np.isfinite(before)).mean()),
                                   perturbation=step,
                                   perturbation_only_failure_n=int((mask & np.isfinite(before) & ~np.isfinite(after)).sum()))
                        sign = 1 if st["descriptor_direction"] == "increasing" else -1
                        delta = after[finite] - before[finite]
                        tol = 1e-10 * max(1., float(np.std(before[finite])))
                        rec["direction_opposite_n"] = int((sign * delta < -tol).sum())
                        rec["direction_positive_n"] = int((sign * delta > tol).sum())
                        rec["direction_neutral_n"] = int((np.abs(delta) <= tol).sum())
                        rec["finite_n"] = int(finite.sum())
                        operations = domain_operations(c["formula"], local)
                        rec["domain_operations"] = [
                            {"operation": op["operation"], "subexpression": op["subexpression"],
                             "n_train": int(op["mask"].sum()), "n_regime": int((op["mask"] & mask).sum())}
                            for op in operations]
                        rec["bad_zero_native_inputs"] = {
                            name: int(((local[name] == 0) & mask & ~finite).sum())
                            for name in FEATURES if np.any((local[name] == 0) & mask & ~finite)
                        }
                        try:
                            runner.checked_feature(c["formula"], env, reference_matrix, train)
                            rec["feature_without_scientific_check"] = "would_pass"
                        except ValueError as error:
                            rec["feature_without_scientific_check"] = str(error)
                        if c["retained"]:
                            winner = runner.checked_feature(c["formula"], env, reference_matrix, train)
                    except (ValueError, KeyError, SyntaxError) as error:
                        rec["numeric_trace_error"] = str(error)
                    tree = ast.parse(c["formula"], mode="eval")
                    rec["has_log"] = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                                         and n.func.id in ("log", "log10") for n in ast.walk(tree))
                    records.append(rec)
                if winner is not None: retained_values.append(winner)

    groups = defaultdict(list)
    for rec in records: groups[rec["group"] + "/" + rec["mode"]].append(rec)
    summaries = {}
    for name, rows in groups.items():
        unstable = [r for r in rows if r["reason"] == "Formula unstable inside declared physical regime"]
        summaries[name] = {
            "candidate_n": len(rows), "scored_n": sum(r["status"] == "scored" for r in rows),
            "retained_n": sum(r["retained"] for r in rows),
            "positive_n": sum((r["marginal_improvement"] or 0) > 1e-10 for r in rows),
            "reasons": dict(Counter(r["reason"] for r in rows if r["status"] == "rejected")),
            "log_n": sum(r["has_log"] for r in rows),
            "unstable_n": len(unstable),
            "unstable_would_pass_old_feature_gate": sum(r.get("feature_without_scientific_check") == "would_pass" for r in unstable),
            "unstable_would_pass_95pct_regime_and_direction_gate": int(sum(
                r.get("nonfinite_union_regime_pct", 100) <= 5
                and r.get("direction_opposite_n", 1) == 0
                and r.get("direction_positive_n", 0) >= .5 * r.get("finite_n", 1)
                and r.get("feature_without_scientific_check") == "would_pass" for r in unstable)),
            "unstable_perturbation_only": sum(r.get("perturbation_only_failure_n", 0) > 0 for r in unstable),
            "unstable_domain_operation_counts": dict(Counter(op["operation"] for r in unstable for op in r.get("domain_operations", []) if op["n_regime"] > 0)),
        }
    payload = {"input_data": str(data_root), "training_n": len(train), "split": {k: len(v) for k, v in split.items()},
               "references_equal_all_runs": all_ref_exact,
               "all_check_results_reproduced": all(r["result_matches"] for r in records),
               "feature_stats": feature_stats, "summaries": summaries, "candidates": records}
    (destination / "numeric-audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("training_n", "references_equal_all_runs", "all_check_results_reproduced", "summaries")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
