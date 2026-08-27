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

For the 5000-6000 paper zeolite corpus, the production sequence is fixed as:

1. Freeze and inspect the SHA-256 inventory.
2. Run the complete mock path on 20 papers.
3. Run DeepSeek extraction on 20-50 papers and manually audit evidence,
   schema validity, parser quality, and token use.
4. Pin the prompt, model, parser, and embedding revisions.
5. Review preflight counts and explicitly confirm the full run.
6. Resume failed papers until complete, or explicitly finalize a documented
   partial corpus; only then build the RAG index and freeze its manifest.

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
