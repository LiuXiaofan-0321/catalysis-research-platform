# ZeoSyn V1/V2 trajectory forensics (diagnostic)

Read-only scripts that rebuild, slot by slot, what GLM-5.3-Flash produced in
`results/zeosyn_v2_dev_1/` (120 descriptor slots) and `results/zeosyn_direct_v1_local_20261008/`,
regenerate the KG evidence the model saw (hash-verified against the stored contexts), and
re-score every distinct formula on its own with the repository's scorer and the five official
fit seeds. Outputs and the report are in `docs/experiments/zeosyn_v2_forensics/`. They change
no protocol, split, model or data and are referenced from `docs/experiments/ZEOSYN_V3_PLAN.md` §1.5.

Run from the repository root with `PYTHONPATH=src:scripts:literature_pipeline/src`; the
single-descriptor re-scoring (`single_descriptor_eval.py <out.json>`) fits 100-tree forests for
90 formulas x 5 seeds plus cumulative k = 1, 2 per trajectory and takes about two hours.
