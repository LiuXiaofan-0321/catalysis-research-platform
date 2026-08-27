# Literature Pipeline Upgrade

## Baseline

The previous extraction flow was scientifically careful but operationally
monolithic. It scanned and hashed every PDF on each invocation, used
index-based output names, sent the complete paper to two prompts, rewrote a
growing JSON manifest after every paper, and cached only the final combined
artifact. The production evidence search used wildcard matching over SQLite
JSON fields.

For the existing thermal run, successful papers averaged about 38,267 total
tokens. A direct 6000-paper extension would therefore approach 230 million
tokens before retries.

## New Architecture

`research/literature_pipeline/` is an independent Python package with these
stages:

1. **Inventory**: SHA-256 identity, deterministic deduplication, source
   manifest support.
2. **Parse**: PyMuPDF fast path, pypdf fallback, optional Docling quality
   fallback, page-aware structured cache.
3. **Chunk**: section-aware chunks with stable IDs and reference exclusion.
4. **Extract**: compact core and quantitative contexts, independent model-call
   caches, strict v2 schema and local evidence validation.
5. **Index**: papers, chunks and evidence records with bilingual lexical text
   and dense vectors; LanceDB is optional and the portable NumPy index remains
   rebuildable.
6. **Retrieve**: dense and lexical recall, reciprocal-rank fusion, evidence
   quality weighting, same-paper expansion, diversity limits and a fixed
   context budget.
7. **Export**: Stage-1-compatible JSON directories for existing graph
   importers and future immutable KG freezes.

## Reproducibility

Every paper and stage has a content-derived cache key. A run manifest records
the source inventory hash, Git commit, parser and model versions, prompt
hashes, selected chunk IDs, token use, artifacts, errors and runtime. A
finalized run cannot be updated through the pipeline. Index manifests record
their logical content hash and exact embedding configuration.

Existing frozen corpora and KG snapshots are never rewritten. Re-extracting
the same papers with this pipeline produces a new extraction version and must
later be frozen under a new corpus and snapshot ID.

## Data Boundary

The program accepts only paths supplied explicitly by the operator. It does
not discover private dataset locations. Raw PDFs, parsed text, model
responses, SQLite ledgers and vector indexes remain outside Git. Private
labels and downstream evaluation targets are not part of extraction prompts,
index records or development benchmarks.
