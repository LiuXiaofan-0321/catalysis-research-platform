# Full RAG Retrieval Audit and Three-Paper Extraction Pilot

## Frozen Index

- Index: `full-rag-v1-index`
- Logical hash: `7da20ce475e04c185fdc27e271d417883c81525ca3cd527b67b74f477670bbcf16`
- Contents: 6,692 papers, 8,928 unique documents, and 365,662 chunks
- Retrieval audit job: `3550308`, completed with exit code `0:0`
- DeepSeek calls: zero

## Three-Question Audit

| Question | Pre-registered target | Result |
| --- | --- | --- |
| Cu(I)/XAS kinetic rate equation | `doi:10.1021/acs.accounts.0c00328`, SI | Failed: target absent from Top-8 |
| Probe-assisted NMR mapping of H-MOR acid sites | `doi:10.1021/acs.accounts.1c00069`, main | Passed: target rank 1 |
| AFX post-milling recrystallization procedure | `doi:10.1021/acs.cgd.6b00365`, SI | Failed: target main rank 3, target SI absent |

The strict pass rate is therefore 1/3. All three query contexts contained
topically related terms, but term overlap alone produced false positives for
the two SI questions. A target paper and target document type must match in the
same retrieved record.

## SI Coverage Finding

The two missing target SI files exist in the public ACS source tree and were
present in the earlier ACS-50 index. They were absent from the full-corpus
master manifest. The full-corpus discovery code treated DOI-like directories
under `si-output` (for example `10.1021_xxx_supporting`) as separate papers and
then excluded them as SI-only orphan bundles.

The discovery rule is fixed and covered by a regression test. The frozen v1
index remains unchanged for provenance. A corrected manifest and SI supplement
index should be created as a new version rather than overwriting v1.

Candidate-manifest job `3550331` completed without API calls. The corrected
selection keeps the same 6,693 papers and 6,693 main documents while increasing
SI coverage from 2,239 to 4,209 documents (+1,970). SI-only orphan documents
drop from 1,976 to 3. The candidate contains 10,902 paths and has selection hash
`0f631b11300ed71ea1d2f7ba18d5f2f93731f31c127a4b8072c3a8d6e3d35616`.

Because the main-document set is unchanged, the efficient correction is to
index only the 1,970 newly recovered SI documents and merge that supplement
with v1 under a new v2 index ID. The v1 artifacts should remain immutable.

## Three-Paper Extraction Pilot

The pilot deliberately covers three different extraction behaviors:

1. `doi:10.1021/acs.accounts.0c00328`: quantitative Cu/XAS kinetics with SI.
2. `doi:10.1021/acs.accounts.1c00069`: acid-site characterization review; the
   extractor should avoid inventing paper-owned experiments.
3. `doi:10.1021/acs.cgd.6b00365`: AFX synthesis procedure with SI.

The frozen pilot contains three main documents and three SI documents.

- Selection hash: `1c41cbc74db225f1e83d60f79842e96bc77f52e1423da1277f357f8a33cca1a9e`
- Preflight config hash: `1a882b437fe2c53fe0865516cf29525f49d22c1b53684aa37eafe63c6cf6baee`
- Model calls: 12 maximum (two stages per document)
- Configured maximum: 68,400 tokens over all six documents
- Preflight: ready, no missing paths, no warnings

The former limit was 30,000 tokens per document. The pilot limit is 11,400,
a 62% reduction. It also caps record counts, omits abstract translation,
preserves observation basis and normalization, and injects main/SI provenance
programmatically. No extraction job has been submitted; the API key is still
required through the job environment.
