"""Oracle diagnostic for the v2 geometry-extended catalog (no LLM calls).

For each geometry descriptor: validation-selected? no - fixed D0 hyperparams,
test-set topology macro-MAE when added to D0 individually. Then best-3 combined
and full catalog. Decides whether the v2 LLM run is worth launching.
"""
import json
import sys
import time
from pathlib import Path

CODE = Path("/public/home/xiaohe/lxf/catalysis-rag/code/releases/adszeo-v1-20260903")
sys.path.insert(0, str(CODE / "research" / "src"))

from catalysis_research.datasets.adszeo import load_adszeo  # noqa: E402
from catalysis_research.experiments.adszeo import (  # noqa: E402
    D0_DESCRIPTOR_IDS,
    evaluate_adszeo,
)
from catalysis_research.experiments.adszeo_v2 import (  # noqa: E402
    GEOMETRY_RATIONALES,
    adszeo_v2_catalog,
    load_geometry,
)

DB = Path("/public/home/xiaohe/lxf/catalysis-rag/benchmarks/adszeo-v1/AdsZeo_data.duckdb")
GEOMETRY = Path("/public/home/xiaohe/lxf/catalysis-rag/benchmarks/adszeo-v1/geometry-features-v1.csv")

t0 = time.time()
dataset = load_adszeo(DB)
geometry_columns, geometry_map = load_geometry(GEOMETRY)
for row in dataset.rows:
    row.update(geometry_map[row["structure_id"]])
catalog = adszeo_v2_catalog(geometry_columns)
print(f"loaded rows={len(dataset.rows)} catalog={len(catalog)} in {time.time() - t0:.0f}s", flush=True)

baseline = evaluate_adszeo(dataset, D0_DESCRIPTOR_IDS, catalog)
params = baseline["selected_parameters"]
base_mae = baseline["test"]["topology_macro_mae_mol_kg"]
print(f"D0: macro_mae={base_mae:.5f}", flush=True)

singles = {}
for did in geometry_columns:
    r = evaluate_adszeo(dataset, (*D0_DESCRIPTOR_IDS, did), catalog, fixed_parameters=params)
    singles[did] = r["test"]["topology_macro_mae_mol_kg"]
    print(f"  D0+{did}: {singles[did]:.5f} ({100 * (base_mae - singles[did]) / base_mae:+.2f}%)", flush=True)

ranked = sorted(singles.items(), key=lambda kv: kv[1])
best3 = tuple(k for k, _ in ranked[:3])
r = evaluate_adszeo(dataset, (*D0_DESCRIPTOR_IDS, *best3), catalog, fixed_parameters=params)
print(f"GEOM_BEST3 {list(best3)}: mae={r['test']['topology_macro_mae_mol_kg']:.5f} "
      f"({100 * (base_mae - r['test']['topology_macro_mae_mol_kg']) / base_mae:+.2f}%)", flush=True)
# v1 winner for reference
r = evaluate_adszeo(dataset, (*D0_DESCRIPTOR_IDS, "t_count"), catalog, fixed_parameters=params)
print(f"D0+t_count reference: mae={r['test']['topology_macro_mae_mol_kg']:.5f}", flush=True)
r = evaluate_adszeo(dataset, (*D0_DESCRIPTOR_IDS, *best3, "t_count"), catalog, fixed_parameters=params)
print(f"D0+geom_best3+t_count: mae={r['test']['topology_macro_mae_mol_kg']:.5f}", flush=True)
full = tuple(catalog.keys())
r = evaluate_adszeo(dataset, full, catalog, fixed_parameters=params)
print(f"FULL_CATALOG_42: mae={r['test']['topology_macro_mae_mol_kg']:.5f} "
      f"({100 * (base_mae - r['test']['topology_macro_mae_mol_kg']) / base_mae:+.2f}%)", flush=True)
print("V2_ORACLE_DONE", flush=True)
