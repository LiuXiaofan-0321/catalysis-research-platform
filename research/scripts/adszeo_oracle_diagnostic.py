"""Oracle diagnostic: is the AdsZeo catalog information-saturated?

Answers three questions with numbers:
1. Noise floor: how much of the residual is GCMC stochastic noise?
2. Oracle ceiling: best possible feature selection from the current catalog vs D0.
3. Where the information is: D0 ablations + value of 'discovering' HVF from a
   composition-only baseline.
"""
import json
import sys
import time
from pathlib import Path

CODE = Path("/public/home/xiaohe/lxf/catalysis-rag/code/releases/adszeo-v1-20260903")
sys.path.insert(0, str(CODE / "research" / "src"))

import duckdb  # noqa: E402
import numpy as np  # noqa: E402

from catalysis_research.datasets.adszeo import load_adszeo  # noqa: E402
from catalysis_research.experiments.adszeo import (  # noqa: E402
    D0_DESCRIPTOR_IDS,
    adszeo_descriptor_catalog,
    evaluate_adszeo,
)

DB = Path("/public/home/xiaohe/lxf/catalysis-rag/benchmarks/adszeo-v1/AdsZeo_data.duckdb")

t0 = time.time()
ds = load_adszeo(DB)
catalog = adszeo_descriptor_catalog()
print(f"dataset_load_seconds={time.time() - t0:.0f} rows={len(ds.rows)}", flush=True)

baseline = evaluate_adszeo(ds, D0_DESCRIPTOR_IDS, catalog)
params = baseline["selected_parameters"]
base_mae = baseline["test"]["topology_macro_mae_mol_kg"]
base_r2 = baseline["test"]["row_r2"]
print(f"D0: macro_mae={base_mae:.5f} row_r2={base_r2:.4f} params={params}", flush=True)

# --- 1) oracle: best single feature added to D0 (fixed D0 hyperparams) ---
singles = {}
for did in catalog:
    if did in D0_DESCRIPTOR_IDS:
        continue
    r = evaluate_adszeo(ds, (*D0_DESCRIPTOR_IDS, did), catalog, fixed_parameters=params)
    singles[did] = r["test"]["topology_macro_mae_mol_kg"]
    print(f"  D0+{did}: {singles[did]:.5f}", flush=True)
ranked = sorted(singles.items(), key=lambda kv: kv[1])
best_id, best_mae = ranked[0]
print(f"ORACLE_BEST_SINGLE: {best_id} mae={best_mae:.5f} "
      f"improvement={100 * (base_mae - best_mae) / base_mae:+.2f}%", flush=True)

# --- 2) top-3 combined and full catalog ---
top3 = tuple(k for k, _ in ranked[:3])
r = evaluate_adszeo(ds, (*D0_DESCRIPTOR_IDS, *top3), catalog, fixed_parameters=params)
print(f"ORACLE_TOP3 {list(top3)}: mae={r['test']['topology_macro_mae_mol_kg']:.5f} "
      f"improvement={100 * (base_mae - r['test']['topology_macro_mae_mol_kg']) / base_mae:+.2f}%", flush=True)
r = evaluate_adszeo(ds, tuple(catalog.keys()), catalog, fixed_parameters=params)
print(f"FULL_CATALOG_25: mae={r['test']['topology_macro_mae_mol_kg']:.5f} "
      f"improvement={100 * (base_mae - r['test']['topology_macro_mae_mol_kg']) / base_mae:+.2f}%", flush=True)

# --- 3) information location: ablations ---
comp_only = tuple(d for d in D0_DESCRIPTOR_IDS if d != "helium_void_fraction")
r = evaluate_adszeo(ds, comp_only, catalog, fixed_parameters=params)
comp_mae = r["test"]["topology_macro_mae_mol_kg"]
print(f"D0_minus_hvf (composition+pressure only): mae={comp_mae:.5f} "
      f"worse_by={100 * (comp_mae - base_mae) / base_mae:+.2f}%", flush=True)
r = evaluate_adszeo(ds, (*comp_only, "helium_void_fraction"), catalog, fixed_parameters=params)
print(f"composition_D0 + DISCOVERED hvf: mae={r['test']['topology_macro_mae_mol_kg']:.5f} "
      f"gain_over_comp_only={100 * (comp_mae - r['test']['topology_macro_mae_mol_kg']) / comp_mae:+.2f}%", flush=True)
r = evaluate_adszeo(ds, ("log_pressure", "helium_void_fraction"), catalog, fixed_parameters=params)
print(f"minimal(logP+hvf): mae={r['test']['topology_macro_mae_mol_kg']:.5f}", flush=True)

# --- 4) noise floor from GCMC uncertainties ---
con = duckdb.connect(str(DB), read_only=True)
vals = con.execute(
    "SELECT value, uncertainty FROM isotherms "
    "WHERE lower(component)='methane' AND loading_type='absolute' "
    "AND unit='mol/kg framework'"
).fetchall()
con.close()
rel = np.array([u / v for v, u in vals if v and u and u > 0], dtype=float)
print(f"NOISE_FLOOR: rows={len(vals)} with_uncertainty={len(rel)} "
      f"({100 * len(rel) / max(len(vals), 1):.1f}%) "
      f"median_rel_unc={100 * float(np.median(rel)):.2f}% "
      f"p90_rel_unc={100 * float(np.percentile(rel, 90)):.2f}%", flush=True)
print("DIAGNOSTIC_DONE", flush=True)
