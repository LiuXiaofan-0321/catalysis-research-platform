"""Final statistics: pooled v3 (n=40) ordering test + purified-evidence comparison."""
import json
import random
from pathlib import Path

import numpy as np
from scipy import stats

BASE = Path("/public/home/xiaohe/lxf/catalysis-rag/runs")
V3_OLD = BASE / "glm-discovery-adszeo-v2-3693194"
V3_EXT = BASE / "glm-discovery-adszeo-v2-3693359"
V4_PUR = BASE / "glm-discovery-adszeo-v4-3693360"
GEOM = {"ring4_frac", "ring5_frac", "ring6_frac", "ring7_frac", "ring8_frac",
        "ring10_frac", "ring12_frac", "ring13p_frac", "ring_mean", "ring_entropy",
        "cs2_mean", "cs3_mean", "tt_bond_mean", "tt_bond_std",
        "otot_angle_mean", "otot_angle_std", "al_second_shell_al_frac"}


def collect(dirs, modes=None):
    out = {}
    failures = {}
    for d in dirs:
        for p in sorted(Path(d).glob("replicate-*.json")):
            data = json.loads(p.read_text(encoding="utf-8"))
            for mode, row in data["modes"].items():
                if modes and mode not in modes:
                    continue
                if row.get("status") != "completed":
                    out.setdefault(mode, [])
                    failures.setdefault(mode, []).append((data.get("replicate_id"), str(row.get("error"))[:80]))
                    continue
                out.setdefault(mode, []).append({
                    "imp": row["downstream"]["topology_macro_mae_relative_improvement"],
                    "geom": bool(GEOM & set(row["final_selection"])),
                    "run": p.parent.name,
                    "rep": data.get("replicate_id"),
                })
    return out, failures


def boot_ci(xs, n=20000, seed=7):
    rng = random.Random(seed)
    ms = sorted(sum(rng.choices(xs, k=len(xs))) / len(xs) for _ in range(n))
    return ms[int(n * 0.025)], ms[int(n * 0.975)]


def boot_ci_diff(xs, ys, n=20000, seed=11):
    rng = random.Random(seed)
    ds = []
    for _ in range(n):
        rx = rng.choices(xs, k=len(xs))
        ry = rng.choices(ys, k=len(ys))
        ds.append(sum(rx) / len(rx) - sum(ry) / len(ry))
    ds.sort()
    return ds[int(n * 0.025)], ds[int(n * 0.975)]


def summarize(rows, label):
    xs = np.array([r["imp"] * 100 for r in rows])
    lo, hi = boot_ci(list(xs))
    geom = sum(1 for r in rows if r["geom"])
    print(f"  {label}: n={len(xs)} mean={xs.mean():+.2f}% sd={xs.std(ddof=1):.2f} "
          f"boot95=[{lo:+.2f},{hi:+.2f}] positive={int((xs > 0).sum())}/{len(xs)} "
          f"geometry_picks={geom}/{len(xs)}")
    return xs


print("== RUN A: pooled v3 blinded, single frozen query ==")
pool_a, fail_a = collect([V3_OLD, V3_EXT])
xa = {}
for mode in ("agent", "rag_agent", "small_kg_rag_agent"):
    xa[mode] = summarize(pool_a[mode], mode)
    if fail_a.get(mode):
        print(f"    failures: {fail_a[mode]}")

print("\n  Mann-Whitney U (two-sided) + mean difference bootstrap CI:")
for a, b in (("small_kg_rag_agent", "agent"), ("agent", "rag_agent"), ("small_kg_rag_agent", "rag_agent")):
    u, p = stats.mannwhitneyu(xa[a], xa[b], alternative="two-sided")
    dlo, dhi = boot_ci_diff(list(xa[a]), list(xa[b]))
    print(f"    {a} vs {b}: mean_diff={xa[a].mean() - xa[b].mean():+.2f}% boot95=[{dlo:+.2f},{dhi:+.2f}] U={u} p={p:.4f}")

print("\n== RUN B: purified three-family evidence (knowledge modes only) ==")
pool_b, fail_b = collect([V4_PUR], modes={"rag_agent", "small_kg_rag_agent"})
for mode in ("rag_agent", "small_kg_rag_agent"):
    summarize(pool_b[mode], f"{mode} (purified)")
    if fail_b.get(mode):
        print(f"    failures: {fail_b[mode]}")

print("\n  Purified vs single-query (same mode, Mann-Whitney) and purified vs agent:")
for mode in ("rag_agent", "small_kg_rag_agent"):
    xb = np.array([r["imp"] * 100 for r in pool_b[mode]])
    u1, p1 = stats.mannwhitneyu(xb, xa[mode], alternative="two-sided")
    u2, p2 = stats.mannwhitneyu(xb, xa["agent"], alternative="two-sided")
    print(f"    {mode}: purified {xb.mean():+.2f}% vs single {xa[mode].mean():+.2f}% (p={p1:.4f}); "
          f"vs agent {xa['agent'].mean():+.2f}% (p={p2:.4f})")

print("\n== variance comparison (sd) ==")
for mode in ("rag_agent", "small_kg_rag_agent"):
    xb = np.array([r["imp"] * 100 for r in pool_b[mode]])
    print(f"  {mode}: single sd={xa[mode].std(ddof=1):.2f} -> purified sd={xb.std(ddof=1):.2f}")
print("DONE")
