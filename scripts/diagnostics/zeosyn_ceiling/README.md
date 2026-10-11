# ZeoSyn knowledge-channel ceiling analysis (diagnostic)

Read-only diagnostics used for the V3 diagnosis (`docs/experiments/ZEOSYN_V3_PLAN.md`).
They do not change any protocol, split, model or data; they only measure how much a
literature-knowledge channel could add under different splits, and how far the current
KG synthesis layer is from that ceiling. Results: `docs/experiments/zeosyn_v3_ceiling/`.

Run from the repository root (about 15 minutes; RandomForest with 60 trees, 2 seeds):

```bash
export PYTHONPATH=src
.venv/bin/python scripts/diagnostics/zeosyn_ceiling/00_prepare.py   # load, splits, imputation (D0 columns only) -> cache/
.venv/bin/python scripts/diagnostics/zeosyn_ceiling/A_structure.py  # dataset structure, OSDA->framework determinism
.venv/bin/python scripts/diagnostics/zeosyn_ceiling/C_kg.py         # reach and accuracy of data/kg_zeolite_v1
.venv/bin/python scripts/diagnostics/zeosyn_ceiling/B_paper.py      # paper split: baselines, 20 hand-made gel ratios
.venv/bin/python scripts/diagnostics/zeosyn_ceiling/B_osda.py       # OSDA split: baselines, oracle literature prior, RF x prior
.venv/bin/python scripts/diagnostics/zeosyn_ceiling/write_report.py # -> REPORT.md
```

`ZEOSYN_CEILING_OUT` overrides the output directory. The imputation here is the loader's
`IterativeImputer` restricted to the 43 D0 columns (the loader imputes 1,314 columns, which
takes minutes per fit); this is a diagnostic shortcut and the numbers are not protocol results.
