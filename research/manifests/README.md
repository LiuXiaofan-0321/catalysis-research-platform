# Research Manifests

This directory contains versioned schemas and frozen provenance records.

## Run Manifest Lifecycle

```text
run create
  -> status: running
  -> record retrieved evidence
  -> record hypothesis
  -> record descriptors
  -> record raw model output
  -> record structured output
  -> complete or fail
  -> FINALIZED.json
```

A finalized run cannot be changed through the Run Manifest API.

Every scientific artifact is stored as a separate file with:

- relative path;
- SHA256;
- byte count;
- media type.

The manifest itself has a canonical content hash. `FINALIZED.json` records the
final manifest hash, so later changes are detectable.

This is repository-local integrity protection, not a cryptographic signature or
an external append-only ledger. Publication runs should additionally archive
the finalized run directory in access-controlled, versioned storage.

## Required Traceability

Every run records:

- exact Git commit and tree state;
- model provider, name, version, temperature, seed, and reasoning budget;
- prompt version and optional prompt hash;
- KG snapshot and content hash;
- retrieval mode, configuration, and retrieved evidence;
- hypothesis and descriptors;
- raw and structured model outputs;
- dataset and split;
- downstream model and hyperparameters;
- metrics, errors, runtime, and manual interventions.

## CLI

Create:

```bash
python research/scripts/research.py run create \
  --config research/configs/runs/example-run-spec.json
```

Record an artifact:

```bash
python research/scripts/research.py run record \
  --run research/runs/<run_id> \
  --field descriptors \
  --input descriptors.json
```

Finalize:

```bash
python research/scripts/research.py run complete \
  --run research/runs/<run_id> \
  --metrics metrics.json
```

Verify:

```bash
python research/scripts/research.py run verify \
  --run research/runs/<run_id>
```

The example config contains placeholders and must not be used unchanged for an
outcome-bearing experiment.

## Public Dataset and Split Manifests

Public predictive datasets use two integrity layers:

- `dataset_manifest.v1` freezes source/license metadata, raw file SHA256,
  sample identity, target, allowed/forbidden inputs, duplicate and missingness
  policies, OOD rationale, and label-access rules.
- `split_manifest.v1` freezes deterministic IID membership or pre-registered
  group-aware OOD folds and records a recomputable split hash.

Registration configs and dataset manifests must be committed before the next
freeze stage. Raw public files may remain outside Git under
`research/datasets/raw/`, but their exact bytes are anchored by SHA256.

The public registry is intentionally empty until an eligible thermocatalysis
predictive dataset is selected. Infrastructure availability does not activate
the experiment protocol.

## Corpus and Nested KG Manifests

`stage1_corpus.v1` freezes a committed literature archive as an exact paper
inventory with PDF hashes, structured JSON hashes, extraction metadata,
distributions, and Git provenance.

`nested_kg_manifest.v1` records one deterministic full paper order and the
strict K20/K40/K60/K80/K100 prefixes derived from it. Each level references its
immutable snapshot content hash. Selection is forbidden from reading
downstream labels or model/descriptor outcomes; task coverage remains
`not_measured` until an eligible public predictive dataset is frozen.
