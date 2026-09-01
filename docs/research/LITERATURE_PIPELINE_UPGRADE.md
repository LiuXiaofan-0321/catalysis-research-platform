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

The zeolite extraction campaign has now completed and is frozen as
`zeolite-structured-corpus-v1`: 6,691 papers and 8,927 main/SI documents.
The three extraction batches, cross-campaign document deduplication, main/SI
aggregation, schema/hash verification, and 24-paper stratified review are
complete. `Small-KG-zeolite-v1` is also frozen; historical pilot and campaign
records remain unchanged.

The current production sequence is now:

1. Complete raw-source license and DOI/title/year semantic-dedup sign-off.
2. Build scientific normalization overlay v1.1 without modifying the frozen
   corpus or Small KG v1.
3. Rebuild a raw RAG index from the exact 6,691-paper / 8,927-document frozen
   manifest rather than reusing the older identity-mismatched full-RAG index.
4. Expose raw RAG and KG+RAG through one evidence-bundle contract.
5. Run a frozen 10-20-question retrieval smoke test without generation-model
   calls.
6. Freeze one eligible benchmark and its benchmark-native `D0` baseline before
   any outcome-bearing descriptor run.

The executor uses a bounded worker queue and an append-only per-paper result
journal. Resume reuses the frozen inventory and skips completed papers. A
mixed success/failure attempt stays unfinalized, and hash embeddings cannot be
selected silently in a production configuration.

## Data Boundary

The program accepts only paths supplied explicitly by the operator. It does
not discover private dataset locations. Raw PDFs, parsed text, model
responses, SQLite ledgers and vector indexes remain outside Git. Private
labels and downstream evaluation targets are not part of extraction prompts,
index records or development benchmarks.
