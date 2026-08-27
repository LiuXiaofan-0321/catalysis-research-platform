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

This runner is a `K-none` formula-selection and execution check. It does not
retrieve from any frozen KG, does not implement the evidence-chain hypothesis
loop, and must not be used as evidence for Small-KG utility.

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
`../docs/research/SCIENTIFIC_HYPOTHESIS_DISCOVERY_LOOP.md`. The next milestone
is to turn the already downloaded candidate collection of approximately
5,000-6,000 zeolite papers into an auditable local/domain-specific Small KG,
then run one complete public-benchmark loop:

```text
candidate files
  -> read-only inventory and deduplication
  -> frozen Small corpus
  -> evidence-grounded Small KG
  -> evidence retrieval
  -> falsifiable hypothesis
  -> executable descriptor
  -> fixed downstream validation
  -> supported / rejected / revised feedback
```

The approximate paper count is planning metadata only. Before any
outcome-bearing Small-KG run, the exact unique count, file hashes, licenses,
inclusion/exclusion decisions, extraction failures, paper IDs, graph hashes,
ontology, and benchmark leakage audit must be frozen. No private data may be
discovered or included during inventory.

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
within-corpus quantity ablations. They do not constitute the pending Small KG
and must not be relabeled or overwritten. Local/Domain-expanded/Cross-domain
scope experiments require new corpus and snapshot IDs plus matched quantity
and structure controls.

The frozen protocol is maintained in
`../docs/research/EXPERIMENT_PROTOCOL.md`. It remains blocked from activation
until the exact public predictive dataset, model registry, splits, prompts, KG
snapshots, and downstream configuration are registered and locked.

Private unseen thermocatalysis validation is governed by
`../docs/research/PRIVATE_DATA_PROTOCOL.md`. Research development code must not
read or locate private data.
