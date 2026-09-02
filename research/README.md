# Research Experiment Layer

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
