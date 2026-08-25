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

## Pending Zeolite Small Corpus

The already downloaded collection of approximately 5,000-6,000 zeolite papers
is a candidate source collection, not a registered corpus. Its location and
contents must not be inferred by broad filesystem scanning. An explicitly
provided source root must first produce a read-only inventory containing at
least:

- source and license status;
- relative file identity and SHA256;
- DOI, title, year, and version metadata when available;
- parsing and extraction status;
- deterministic DOI/title/year/file-hash duplicate groups;
- inclusion/exclusion decisions and reasons;
- exact unique paper count and paper-ID hash.

Only a reviewed inventory may be frozen as a new versioned corpus such as
`zeolite-small-corpus-v1`. The existing `thermal-catalysis-stage1-v1` corpus of
512 papers remains immutable and is not renamed, expanded in place, or treated
as the new Small corpus.
