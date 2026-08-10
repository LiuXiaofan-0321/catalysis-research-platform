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
