# ZeoSyn direct V1: complete local run (2026-10-08)

Completed Windows CPU run at code commit `3bfc543b8cc89439bfb76f0c6407f3d328ca8902`.
Release assets: [knowledge-zeolite-v1-20261008](https://github.com/LiuXiaofan-0321/catalysis-research-platform/releases/tag/knowledge-zeolite-v1-20261008).

The complete original run is retained here: 102 original files, including the prepared matrix, frozen configuration and evidence, all 30 generations, all 30 five-seed evaluations, API probe, baseline, summary, 30 generation logs, execution record and report. `ARTIFACTS.json` records SHA256 and sizes. Folder-local `.gitattributes` preserves exact bytes so frozen hashes survive cloning.

- Model: GLM-5.3-Flash, high reasoning; Agent / RAG / KG+RAG, 10 trajectories each, 3 rounds each.
- Generation concurrency: 5; RandomForest CPU threads: 8; all original five fit seeds retained.
- Split: DOI-grouped, seed 20261007; 17,567 training rows and 4,405 test rows. Held-out publications were excluded from retrieval.
- D0 accuracy: 43.3144%. Mean accuracy gains in percentage points: Agent +0.5403, RAG +0.1049, KG+RAG +0.1684.
- All 90 slots appended; 3 technical repair calls; no failed slots. All negative trajectories retained.
- KG+RAG minus RAG: +0.0636 percentage points, 97.5% bootstrap interval [-0.2125, +0.3215]; this run does not establish a KG advantage. Agent exceeded both knowledge conditions on this fixed setup.

Read [LOCAL_REPORT.md](LOCAL_REPORT.md) for analysis and [summary.json](summary.json) for the authoritative machine-readable statistics. This is a fixed-split comparison; trajectory intervals do not capture alternative data splits, and no same-facts flattened control was included.

## Contents

| Path | Contents |
| --- | --- |
| `prepared/` | Source hashes, exact experiment configuration, held-out retrieval configuration, six evidence bundles, tasks, matrices.npz |
| `generation/` | All structured responses, usage, evidence citations, formula checks, technical repairs and final formulas |
| `evaluation/` | Per-seed metrics and paired changes versus D0 for every trajectory |
| `local-logs/` | All 30 original generation logs (intentionally included despite the global *.log ignore rule) |
| `d0.json`, `api-probe.json`, `summary.json` | Baseline, actual API connectivity probe and final statistics |
| `local-execution.json`, `LOCAL_REPORT.md`, `make_local_report.py` | Execution timing, report and exact original reporting helper |
| `reproduction/` | Exact local launcher snapshot, actual package versions, dependency lists and release manifest |

## Inspect and verify

From the repository root:

```bash
python results/zeosyn_direct_v1_local_20261008/verify_artifacts.py
python scripts/run_zeosyn.py status --run-dir results/zeosyn_direct_v1_local_20261008
```

The source run remains at `runs/zeosyn-local-v1-20261008` on the original workstation. Large KG/RAG/model assets are downloaded separately from the matching Release and are identified in `reproduction/knowledge-release-manifest.json`.

`reproduction/knowledge/run_local.py` is an exact snapshot intended for its original location, `<repository>/knowledge/run_local.py`; restore it there to use the original launcher. Its reference inputs also include `reproduction/local-validation.json` (originally `.local-knowledge/knowledge-zeolite-v1-20261008/local-validation.json`). Source code should match the recorded commit. Actual local package versions are in `reproduction/environment.json` and `requirements-local.txt`; they differ from the release's source-server versions in `requirements-portable.txt`.

No API keys or environment-variable dumps are included. Generation needs a separately configured `ZHIPU_API_KEY`. Completed generation/evaluation files are preserved and must not be overwritten or regenerated to improve outcomes.
