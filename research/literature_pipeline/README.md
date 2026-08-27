# Literature Extraction and KG-RAG Pipeline

This package is the independent literature-processing layer for large
catalysis corpora. It does not modify the frozen K247 or thermal K20-K100
snapshots and does not read private evaluation data.

## What Changed

The previous Stage-1 program sent the full PDF text to the model twice and
cached only the final paper JSON. This implementation:

- identifies papers by PDF SHA-256 rather than directory order;
- parses and chunks each PDF once;
- uses compact, section-targeted core and quantitative prompts;
- caches each model call independently;
- stores task state in a SQLite WAL ledger;
- creates immutable run and RAG-index manifests;
- exports the existing Stage-1 JSON shape;
- builds portable dense plus lexical retrieval, with optional LanceDB tables.

## Install

```powershell
cd research/literature_pipeline
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

For the complete indexing and document-layout stack:

```powershell
pip install -e ".[index,docling]"
```

PyMuPDF is the preferred parser. If it is unavailable, the program uses
`pypdf`. Docling is invoked only when the initial parse fails the configured
quality gate.

## Run

Copy `configs/example.yaml` and set `source` to a public PDF directory or a
source manifest. API credentials remain environment variables:

```powershell
$env:DEEPSEEK_API_KEY = "<key>"
litpipe doctor
litpipe preflight --config .\configs\my-run.yaml
litpipe run --config .\configs\my-run.yaml --limit 20 --run-id smoke-mock-001
```

For a DeepSeek smoke test, use 20-50 papers and audit extraction quality before
freezing the production config. A run selecting more than 100 papers requires
an explicit confirmation after preflight:

```powershell
litpipe run --config .\configs\production.yaml --run-id zeolite-6000-v1 --confirm-large-run
```

The command prints the generated `run_id`. Resume and query with:

```powershell
litpipe resume --run-id <run_id> --workspace <workspace>
litpipe retrieve --index <workspace>\indexes\<run_id>-index --query "甲醇选择性与酸位关系"
litpipe export-stage1 --run-id <run_id> --workspace <workspace> --output <new-output-directory>
litpipe verify --run-id <run_id> --workspace <workspace>
```

The inventory is frozen inside the run and reused on resume. Use
`--refresh-inventory` only when intentionally changing the source corpus.
Per-paper outcomes are appended to `paper-results.journal.jsonl`, so an
interrupted process resumes only missing or failed papers. A run is finalized
and indexed automatically only when every selected paper succeeds. To stop
retrying known failures, explicitly seal the partial run before indexing:

```powershell
litpipe finalize-partial --run-id <run_id> --workspace <workspace>
litpipe build-index --run-id <run_id> --workspace <workspace>
```

Partial finalization is an exception path and remains labelled `partial`; it
never appears as a complete corpus.

For production, set `parser.fail_on_low_quality: true`. PDFs that still fail
the text-quality gate after optional Docling fallback then remain retryable
failures instead of entering the RAG index as apparently successful papers.

`provider: mock`, `hash-embedding-v1`, and `backend: portable` are available
for offline tests. Production configs must pin a real embedding revision and
keep `allow_hash_embedding_fallback: false`.
Production manifests always record the actual parser, embedding backend,
model, prompt hashes, source hashes, token use, cache hits, errors, and Git
commit.

## Generated Data

The workspace contains PDFs only by reference. Parsed text, model responses,
extractions, indexes, SQLite ledgers, and manifests are generated below the
configured workspace and are excluded from Git. Only code, prompts, schemas,
configuration examples, tests, and documentation belong in the repository.
