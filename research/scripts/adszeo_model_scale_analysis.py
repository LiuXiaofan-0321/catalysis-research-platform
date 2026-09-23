"""Model-scale ablation: glm-4-flash (n=20) vs glm-5.3-flash (n=40), v3 blinded protocol."""
import json
import random
from pathlib import Path

import numpy as np
from scipy import stats

BASE = Path("/public/home/xiaohe/lxf/catalysis-rag/runs")
G53 = [BASE / "glm-discovery-adszeo-v2-3693194", BASE / "glm-discovery-adszeo-v2-3693359"]
G4F = [BASE / "glm-discovery-adszeo-v3-glm4f-3695325"]
GEOM = {"ring4_frac", "ring5_frac", "ring6_frac", "ring7_frac", "ring8_frac",
        "ring10_frac", "ring12_frac", "ring13p_frac", "ring_mean", "ring_entropy",
        "cs2_mean", "cs3_mean", "tt_bond_mean", "tt_bond_std",
        "otot_angle_mean", "otot_angle_std", "al_second_shell_al_frac"}
MODES = ("agent", "rag_agent", "small_kg_rag_agent")


def collect(dirs):
    out, fails = {}, []
    for d in dirs:
        for p in sorted(Path(d).glob("replicate-*.json")):
            data = json.loads(p.read_text(encoding="utf-8"))
            for mode, row in data["modes"].items():
                if row.get("status") != "completed":
                    fails.append((mode, data.get("replicate_id"), str(row.get("error"))[:70]))
                    continue
                out.setdefault(mode, []).append({
                    "imp": row["downstream"]["topology_macro_mae_relative_improvement"],
                    "geom": bool(GEOM & set(row["final_selection"])),
                })
    return out, fails


def boot_ci(xs, n=20000, seed=7):
    rng = random.Random(seed)
    ms = sorted(sum(rng.choices(xs, k=len(xs))) / len(xs) for _ in range(n))
    return ms[int(n * 0.025)], ms[int(n * 0.975)]


g53, f53 = collect(G53)
g4f, f4f = collect(G4F)

print("== per-model, per-mode ==")
xs_by = {}
for label, pool in (("glm-5.3-flash", g53), ("glm-4-flash", g4f)):
    for mode in MODES:
        rows = pool.get(mode, [])
        xs = np.array([r["imp"] * 100 for r in rows])
        xs_by[(label, mode)] = xs
        if len(xs) == 0:
            print(f"  {label} {mode}: NO DATA")
            continue
        lo, hi = boot_ci(list(xs))
        geom = sum(1 for r in rows if r["geom"])
        print(f"  {label} {mode}: n={len(xs)} mean={xs.mean():+.2f}% sd={xs.std(ddof=1):.2f} "
              f"boot95=[{lo:+.2f},{hi:+.2f}] positive={int((xs > 0).sum())}/{len(xs)} geom={geom}/{len(xs)}")

print("\n== failures ==")
print("  glm-4-flash:", f4f if f4f else "none")

print("\n== KG-Agent gap by model (the 'model too strong' test) ==")
for label, pool in (("glm-5.3-flash", g53), ("glm-4-flash", g4f)):
    ka = np.array([r["imp"] * 100 for r in pool.get("small_kg_rag_agent", [])])
    ag = np.array([r["imp"] * 100 for r in pool.get("agent", [])])
    if len(ka) and len(ag):
        u, p = stats.mannwhitneyu(ka, ag, alternative="two-sided")
        print(f"  {label}: gap(kg-agent)={ka.mean() - ag.mean():+.2f}%  Mann-Whitney p={p:.4f}")

print("\n== agent capability drop across models ==")
a53, a4f = xs_by.get(("glm-5.3-flash", "agent")), xs_by.get(("glm-4-flash", "agent"))
if a53 is not None and a4f is not None and len(a4f):
    u, p = stats.mannwhitneyu(a4f, a53, alternative="two-sided")
    print(f"  agent: glm-4-flash {a4f.mean():+.2f}% vs glm-5.3-flash {a53.mean():+.2f}% (p={p:.4f})")
k53, k4f = xs_by.get(("glm-5.3-flash", "small_kg_rag_agent")), xs_by.get(("glm-4-flash", "small_kg_rag_agent"))
if k53 is not None and k4f is not None and len(k4f):
    u, p = stats.mannwhitneyu(k4f, k53, alternative="two-sided")
    print(f"  kg:    glm-4-flash {k4f.mean():+.2f}% vs glm-5.3-flash {k53.mean():+.2f}% (p={p:.4f})")
print("DONE")
