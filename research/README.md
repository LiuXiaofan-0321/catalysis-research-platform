# Research Experiment Layer

当前进展与后续计划见 [研究阶段成果与后续路线（2026-09-27）](../docs/research/RESEARCH_PROGRESS_AND_ROADMAP_20260927.md)，汇总 v5 实验结果及轮数、multi-agent、Jev 的待实施方案。

Harness vNext 的可运行接口、轮数实验设计和 Jev 判定边界见
[`../docs/research/HARNESS_VNEXT_DESIGN.md`](../docs/research/HARNESS_VNEXT_DESIGN.md)。

`research/` is the command-line experiment layer for the evidence-grounded
scientific hypothesis discovery and Model x Knowledge scaling study. It is
intentionally separated from the production web application in `backend/` and
`frontend/`.

The production platform remains responsible for interactive literature
exploration, evidence inspection, research advice, and experiment feedback.
This directory is responsible for reproducible paper experiments, immutable
artifacts, evaluation, and statistical analysis.

## Rules

1. Every paper result must be reproducible without the frontend.
2. Experimental inputs, configurations, prompts, and outputs must be
   machine-readable.
3. Production data may be read through explicit adapters, but research code
   must not mutate production records.
4. Private validation data must not enter development workflows.
5. Failed runs and negative results must be retained.
6. Scientific facts, cross-paper synthesis, model inference, hypotheses, and
   user observations must remain distinguishable.
7. Knowledge quantity and knowledge scope/diversity are separate experimental
   variables and must not share an ambiguous `K` label.

## Layout

| Directory | Responsibility |
| --- | --- |
| `configs/` | Versioned experiment configurations |
| `models/` | Model provider adapters and capability definitions |
| `kg_snapshots/` | Rebuildable knowledge snapshots and metadata |
| `prompts/` | Versioned prompt families |
| `experiments/` | Experiment orchestration |
| `benchmarks/` | Scientific tasks and expected evidence |
| `descriptors/` | Descriptor schemas, generation, validation, and execution |
| `datasets/` | Public dataset adapters and split definitions |
| `runs/` | Immutable run artifacts |
| `evaluation/` | Reasoning, descriptor, prediction, and optimization metrics |
| `statistics/` | Confidence intervals, effect sizes, and scaling models |
| `manifests/` | Dataset, snapshot, run, and freeze manifests |
| `scripts/` | Stable command-line entry points |
| `reports/` | Human-readable reports and figure inputs |

## Commands

From the repository root:

```bash
npm run research:doctor
npm run research:test
```

The `doctor` command validates the directory contract and the six required
methodology documents, then prints a machine-readable JSON report. It does not
access model APIs or mutate data.

Run Manifest commands are available through:

```bash
python research/scripts/research.py run --help
```

Public dataset registry and fixed split commands are available through:

```bash
python research/scripts/research.py dataset --help
```

Frozen literature corpus and nested KG commands are available through:

```bash
python research/scripts/research.py corpus --help
python research/scripts/research.py kg build-nested --help
python research/scripts/research.py kg verify-nested --help
```

Scientific normalization overlays are built and verified without modifying the
frozen KG or corpus:

```bash
python research/scripts/research.py normalization build --help
python research/scripts/research.py normalization verify --help
```

The common retrieval API is in `catalysis_research.retrieval`. It exposes the
same candidate, item, token, per-paper, tokenizer, and formatter budgets for
`none`, `rag`, and `small_kg_rag`. The shuffled mode is reserved and rejected
until a corruption manifest is frozen.

The experiment-facing interface exposes `agent`, `rag_agent`, and
`small_kg_rag_agent`. It reads the historical `full-rag-v1-index` without
rewriting it, excludes `doi:10.1126/science.ads7290` and its 19 chunks before
ranking, verifies the retained 6,691-paper / 8,927-document / 365,643-chunk
scope, and applies the frozen scientific-normalization overlay to retrieval
queries and KG evidence. Any source identity, hash, or count drift fails
closed.

```bash
python research/scripts/research.py retrieve \
  --config research/configs/retrieval/small-kg-hybrid-v1.json \
  --rag-index /path/to/full-rag-v1-index \
  --snapshot /path/to/Small-KG-zeolite-v1 \
  --overlay /path/to/scientific-normalization-Small-KG-zeolite-v1.1 \
  --mode rag_agent \
  --query "MTO conversion over MFI"
```

Changing only `--mode` produces matched-budget evidence bundles for the three
conditions. This command performs retrieval only; it does not call an LLM or
run the hypothesis/descriptor loop.

### Local Python environment

Python 3.11 or newer is required. The current Windows workstation uses Python
3.12.10 and a repository-local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r research\requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install -e research --no-deps
```

The TheMeCat + DeepSeek runner is an exploratory pipeline check. It is not an
activated or confirmatory protocol run:

```powershell
$env:DEEPSEEK_API_KEY = "<local-secret>"
.\.venv\Scripts\python.exe research\scripts\run_themecat_pilot.py
Remove-Item Env:DEEPSEEK_API_KEY
```

The raw `TheMeCat_v1.csv` file must be placed in `research/datasets/raw/` and
is intentionally ignored by Git. The result is retained under
`research/runs/themecat-deepseek-exploratory-v1/`, which is also ignored by
Git. Neither location may contain private data.

### GLM evidence-to-descriptor pilot

The active first benchmark is Materials Cloud **Zeolite Atlas v1**
(`10.24435/materialscloud:2019.0079/v1`, CC BY 4.0). Its 1k view contains
structure-level aggregates of the source Angles, Distances, King ring and
SOAP-KPCA descriptors with the source energy/volume contributions. The
exploratory GLM runner compares the three matched knowledge conditions
(`agent`, `rag_agent`, `small_kg_rag_agent`) with one prompt, one inference
budget and one descriptor budget. It preserves the evidence chain, falsifiable
hypothesis and descriptor provenance, then evaluates fixed classical `D0`
against catalog-only `D0+X` descriptors:

```powershell
$env:ZHIPU_API_KEY = "<local-secret>"
$env:ZHIPU_PROXY_BASE_URL = "<existing-GLM-compatible-endpoint>"
\.venv\Scripts\python.exe research\scripts\run_glm_zeolite_atlas.py `
  --config research\configs\retrieval\small-kg-hybrid-v1.json `
  --rag-index <full-rag-v1-index> `
  --snapshot <Small-KG-zeolite-v1> `
  --overlay <scientific-normalization-Small-KG-zeolite-v1.1> `
  --dataset-root <extracted-materialscloud-2019.0079-v1> `
  --output research\runs\glm-discovery-zeolite-atlas-v1\result.json `
  --task "<frozen task text>" `
  --query "<frozen retrieval query>"
Remove-Item Env:ZHIPU_API_KEY
Remove-Item Env:ZHIPU_PROXY_BASE_URL
```

The default model is `glm-5.3-flash`. The run is explicitly
`EXPLORATORY_NOT_CONFIRMATORY`: source units and native-model reproduction must
still be signed off, and locked-test outcomes must not be used to revise the
generated descriptors. The old TheMeCat adapter remains in the repository only
for historical reproducibility and is not an active benchmark.

Large-scale PDF extraction and KG-aware retrieval live in the independent
`literature_pipeline/` package. It uses content-addressed parsing and model
call caches, produces Stage-1-compatible artifacts, and builds versioned
portable or LanceDB indexes:

```bash
npm run literature:doctor
npm run literature:test
python research/literature_pipeline/scripts/litpipe.py run --config <config.yaml>
```

### AdsZeo open-nomination benchmark (v5)

The second active benchmark is **AdsZeo v1** (`10.5281/zenodo.21445386`,
CC BY 4.0): 4,775 aluminium-substituted sodium zeolite structures x 191
topologies x 13 methane pressures from RASPA GCMC simulations. The adapter
is leakage-aware (the `positions` and `cycle_stats` tables are never read)
and the split is topology-level 80/10/10, so generalization is measured on
unseen framework topologies.

The experiment line iterated through four protocols (see
`../docs/research/ADSZEO_BENCHMARK_V1_REPORT.md` and
`../docs/research/ADSZEO_V2_GEOMETRY_REPORT.md`). A 2026-09-24 audit found
that a shared evidence-labeling helper amplified RAG/KG context whenever a
retrieved quote contained blank lines. Historical cross-mode rankings in
v1-v4 are therefore exploratory records, not fair knowledge-mode comparisons.
The D0 baseline and non-LLM oracle diagnostics are unaffected:

1. **v1** — the 9/3 frozen 25-descriptor catalog exposed strong descriptor
   collinearity with D0.
2. **v2** — geometry-extended 42-descriptor catalog (ring-size distribution,
   coordination sequences, bond geometry, Al second shell; precomputed by
   `scripts/adszeo_geometry_features.py`) + 3-round validation-only feedback.
3. **v3** — blinded catalog (rationales removed for every mode) at n=40;
   its historical mode comparison needs a corrected replication.
4. **v5** — cumulative open-ended nomination
   (`src/catalysis_research/experiments/adszeo_nomination.py`): no candidate
   catalog; the model nominates three DSL formulas in each of three rounds.
   A whitelisted AST executor rejects unsafe, non-computable, degenerate, or
   redundant proposals with recorded failure codes (`unsafe_expression`,
   `unsupported_input`, `zero_variance`, `redundant`, ...). All three candidates
   are scored for marginal validation benefit beyond `D0` plus the previously
   retained descriptors. At most one positive-benefit candidate is retained
   per round, giving a final budget of zero to three added descriptors.
   If a round has no beneficial candidate, the retained set is unchanged.
   The held-out test is evaluated only after all three knowledge modes finish
   their validation decisions. Executability, failure taxonomy, novelty,
   provenance, and topology macro-MAE are recorded. The corrected 10-repeat
   GLM-5.3-Flash result is reported in
   [`../docs/research/ADSZEO_V5_NOMINATION_REPORT.md`](../docs/research/ADSZEO_V5_NOMINATION_REPORT.md):
   RAG improved in 8/10 repeats but all three mean effects have intervals
   crossing zero, and KG+RAG did not consistently exceed RAG.
   A separate [single-score search protocol](../docs/research/ADSZEO_V5_SINGLE_SCORE_PROTOCOL.md)
   uses the former validation topologies for both selection and the reported
   adaptive search score; invoke it with `--open-nomination --score-only`.
   Its score is not a held-out test estimate.

```bash
python research/scripts/run_glm_adszeo_v2.py \
  --config research/configs/retrieval/small-kg-hybrid-adszeo-v5.json \
  --rag-index <full-rag-v1-index> \
  --snapshot <Small-KG-zeolite-v1> \
  --overlay <scientific-normalization-Small-KG-zeolite-v1.1> \
  --database <AdsZeo_data.duckdb> \
  --geometry-csv <geometry-features-v1.csv> \
  --output <run.json> \
  --open-nomination
```

Diagnostics live in `scripts/adszeo_oracle_diagnostic.py` (noise floor +
catalog oracle ceiling), `scripts/adszeo_final_stats.py` (bootstrap CIs +
Mann-Whitney tests), and `scripts/adszeo_model_scale_analysis.py`
(model-scale ablation). Slurm jobs are under
`literature_pipeline/jobs/adszeo-v*.sbatch`.
For compute-node GLM access, see
[`../docs/research/CLUSTER_EXTERNAL_API.md`](../docs/research/CLUSTER_EXTERNAL_API.md);
the proxy port is assigned dynamically and must be checked before submission.

Large-scale PDF extraction and KG-aware retrieval live in the independent
`literature_pipeline/` package. It uses content-addressed parsing and model
call caches, produces Stage-1-compatible artifacts, and builds versioned
portable or LanceDB indexes:

```bash
npm run literature:doctor
npm run literature:test
python research/literature_pipeline/scripts/litpipe.py run --config <config.yaml>
```

See `literature_pipeline/README.md` and
`../docs/research/LITERATURE_PIPELINE_UPGRADE.md`.

## Immediate Milestone: Small KG

The current scientific direction is defined in
`../docs/research/SCIENTIFIC_HYPOTHESIS_DISCOVERY_LOOP.md`. The exact frozen
results, limitations, and next goals are summarized in
`../docs/research/SMALL_KG_V1_STATUS.md`. The first Small/Local KG now contains
6,691 zeolite papers represented by 8,927 main/SI structured documents. The
next milestone is to run one complete public-benchmark loop:

```text
zeolite-structured-corpus-v1
  -> Small-KG-zeolite-v1
  -> scientific normalization overlay v1.1
  -> matched KG/RAG retrieval
  -> falsifiable hypothesis
  -> executable descriptor
  -> benchmark-native D0 vs D0 + X validation
  -> supported / rejected / revised feedback
```

For each benchmark, the primary empirical comparison reproduces the original
paper's model and evaluation framework and changes only the added descriptor
set. A common Ridge `D0` versus `D0 + X` run is retained only as a secondary
cross-benchmark representation diagnostic.

The corpus and graph identities, hashes, evidence audit, and lightweight QA
sample are frozen. Before any outcome-bearing Small-KG run, raw-source license
review, DOI/title/year semantic-dedup sign-off, benchmark leakage audit,
normalization, and benchmark activation gates must still be completed. No
private data may be included.

## Current Scope

The research boundary, repository-level experiment protocol, K247 knowledge
snapshot, immutable Run Manifest, public dataset registration, deterministic
IID/OOD splitting, label-access controls, and structural leakage audit
infrastructure are implemented. The thermal nested KG builder freezes one
label-independent, stratified full paper order and constructs K20/K40/K60/K80/
K100 as exact prefixes. Each selected graph is rebuilt from its own Stage 1
source records. The public registry intentionally remains empty until an exact
eligible dataset is selected and reviewed.

The 247/512-paper snapshots remain immutable infrastructure and secondary
within-corpus quantity ablations. They do not constitute the frozen 6,691-paper
Small KG and must not be relabeled or overwritten. Local/Domain-expanded/
Cross-domain scope experiments require new corpus and snapshot IDs plus matched
quantity and structure controls.

The frozen protocol is maintained in
`../docs/research/EXPERIMENT_PROTOCOL.md`. It remains blocked from activation
until the exact public predictive dataset, model registry, splits, prompts, KG
snapshots, benchmark-native baseline, and downstream configuration are
registered and locked. The current small ablation is LLM-only, raw RAG, and
Small KG + RAG with a single Agent; Multi-Agent is deferred.

Private unseen thermocatalysis validation is governed by
`../docs/research/PRIVATE_DATA_PROTOCOL.md`. Research development code must not
read or locate private data.
