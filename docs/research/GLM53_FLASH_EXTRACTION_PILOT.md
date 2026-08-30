# GLM-5.3-Flash three-paper extraction pilot

Date: 2026-08-30

## Scope

- Provider/model: Zhipu `glm-5.3-flash`
- Frozen selection: 3 ACS papers, each with one main document and one SI document
- Final run: `full-rag-extraction-pilot-3-glm53flash-proxy-v5`
- Slurm job: `3550610`
- Prompt version: `catalysis-paper-extraction-v2.2`
- Reasoning effort: `low`
- Output ceilings: 6,000 tokens for core extraction and 8,000 for data extraction
- Server run directory: `/public/home/xiaohe/lxf/catalysis-rag/workspace-extraction/runs/full-rag-extraction-pilot-3-glm53flash-proxy-v5`

## Result

The final job completed in 11 minutes 21 seconds. All 6 documents completed,
all 12 model calls ended with `finish_reason=stop`, and pipeline verification
reported `valid: true`. No API key was stored in the repository or job logs.

| Metric | Main documents | SI documents | Total |
| --- | ---: | ---: | ---: |
| Documents | 3 | 3 | 6 |
| Prompt tokens | 35,981 | 26,154 | 62,135 |
| Completion tokens | 23,239 | 18,816 | 42,055 |
| Total tokens | 59,220 | 44,970 | 104,190 |
| Evidence records | 115 | 83 | 198 |
| Items needing review | 31 | 20 | 51 |

Evidence validation totals were 140 exact quotes, 26 locally recovered quotes,
and 32 unverified quotes. The extraction produced 55 entity records, 20
experiment records, 48 observation records, 20 claim records, and 7 visual
review items. These are document-level records and must not be interpreted as
deduplicated KG node counts.

## Engineering findings

The development runs before `v5` are not scientific results:

1. Direct compute-node access failed because compute nodes cannot resolve or
   reach the external API.
2. The cluster proxy's 60-second upstream timeout was too short for GLM calls.
   A copy under `lxf/tools/api_proxy_300s.py` changes only this timeout to 300
   seconds; the proxy must run on `login02` and be stopped after the job.
3. `reasoning_effort=max` exhausted small output budgets without producing a
   final JSON response. `low` completed the fixed-schema extraction reliably.
4. GLM occasionally returned evidence as quote strings rather than evidence
   objects. Prompt v2.2 now shows the complete object shape, and the boundary
   normalizer conservatively retains string quotes and flags them for review.
5. Reasoning effort and output ceilings are now included in model-call and
   extraction cache keys to prevent cross-configuration cache reuse.

## Decision

The pilot demonstrates that GLM-5.3-Flash can produce schema-valid,
evidence-linked main-text and SI extraction. It should not yet be scaled to the
full corpus. At the observed average of 17,365 tokens per document, the current
prompt is too expensive for thousands of papers. The next step is a manual
scientific audit of these six artifacts, followed by field and context pruning
and a second small cost-quality pilot. Only then should a larger batched run be
considered.
