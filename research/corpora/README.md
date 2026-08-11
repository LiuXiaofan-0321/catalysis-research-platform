# Frozen Literature Corpora

This directory stores immutable public literature corpus inventories used to
construct research knowledge snapshots.

Each corpus directory contains:

- `manifest.json`: archive identity, Git state, extraction metadata, counts,
  distributions, and artifact hashes.
- `paper_ids.txt`: exact frozen paper IDs.
- `papers.jsonl`: one audit record per source paper, including PDF and
  structured JSON hashes.

Corpus directories are append-only. A correction or expansion requires a new
corpus ID and version. Downstream labels and private data are forbidden inputs
to corpus freezing.
