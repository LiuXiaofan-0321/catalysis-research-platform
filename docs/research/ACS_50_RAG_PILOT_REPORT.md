# ACS 50-Paper RAG Pilot

## Scope

- Source: the first 50 article directories in `ACS/file/batch_001`, sorted
  case-insensitively by directory name.
- Frozen selection: 50 papers, 50 main-text Markdown documents, and 26 SI
  Markdown documents; 76 documents total with no missing paths.
- Selection hash:
  `b2c6f42f376780ea5900f36ea43bfbdf33bf66add48d943927d5d00450dfd6b1`.
- The shared corpus was read only. Generated artifacts are under
  `/public/home/xiaohe/lxf/catalysis-rag`.

## Result

- Slurm build job: `3547732`, `COMPLETED`, exit code `0`, elapsed `00:01:37`.
- Index verification job: `3547755`, `COMPLETED`.
- Output: 50 paper records, 76 document records, and 2450 chunks.
- Embedding model:
  `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, revision
  `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`, 384 dimensions.
- Hash fallback was disabled. DeepSeek extraction was disabled, so the run made
  no model calls and did not create structured KG facts.
- Frozen index logical hash:
  `1f57dbcce2bd9c9a381501d31efa7f1a2d193fd5a717a5832ef79332d71a9fbc`.

## SI Retrieval Check

Targeted audit job `3547779` completed on `gpu9` in 22 seconds with exit code
`0`. Two SI-specific questions ranked the correct SI document first:

- Cu(I) fraction and oxygen-assisted XAS rate equation: SI rank 1.
- AFX post-milling recrystallization procedure: SI rank 1.

A generic query containing "supporting information" ranked an SI document only
ninth because main articles frequently contain that phrase. A targeted NMR
Table S1 query also selected two main-text chunks from the same paper before its
SI chunk. The data and provenance chain are therefore working, but retrieval
still needs document-type-aware evaluation or diversification before SI ranking
quality can be treated as solved.

## Next Gate

Keep the current index as the frozen ingestion baseline. Before scaling the
full corpus, add a small fixed query set with expected main/SI sources and
measure Recall@k and MRR by document type. Corpus expansion can then proceed in
restartable 50- or 100-paper batches while retrieval changes are evaluated
against the same frozen pilot.
