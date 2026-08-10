# Research Experiment Layer

`research/` is the command-line experiment layer for the Model x Knowledge
scaling study. It is intentionally separated from the production web
application in `backend/` and `frontend/`.

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

The `doctor` command validates the directory contract and the four required
methodology documents, then prints a machine-readable JSON report. It does not
access model APIs or mutate data.

## Current Scope

This first scaffold establishes the research boundary and repository-level
experiment protocol. Run provenance, KG snapshot versioning, model providers,
descriptors, benchmarks, and evaluation pipelines will be implemented as
separate reviewed modules.

The frozen protocol is maintained in `../EXPERIMENT_PROTOCOL.md`. It remains
blocked from activation until the exact public predictive dataset, model
registry, splits, prompts, KG snapshots, and downstream configuration are
registered and locked.

Private unseen thermocatalysis validation is governed by
`../PRIVATE_DATA_PROTOCOL.md`. Research development code must not read or
locate private data.
