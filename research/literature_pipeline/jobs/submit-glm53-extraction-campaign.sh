#!/usr/bin/env bash
set -euo pipefail

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
CAMPAIGN_ID="${1:?usage: submit-glm53-extraction-campaign.sh CAMPAIGN_ID [MAX_PARALLEL]}"
MAX_PARALLEL="${2:-3}"
SUMMARY="$BASE/manifests/glm53-extraction/$CAMPAIGN_ID/summary.json"

: "${ZHIPU_API_KEY:?Export ZHIPU_API_KEY before submitting}"
: "${ZHIPU_PROXY_BASE_URL:?Export ZHIPU_PROXY_BASE_URL before submitting}"
if [[ ! -f "$SUMMARY" ]]; then
  echo "Campaign summary not found: $SUMMARY" >&2
  exit 2
fi
if ! [[ "$MAX_PARALLEL" =~ ^[1-9][0-9]*$ ]]; then
  echo "MAX_PARALLEL must be a positive integer" >&2
  exit 2
fi

SHARD_COUNT=$(
  "$BASE/envs/py312-rag/bin/python" -c \
    'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["shard_count"])' \
    "$SUMMARY"
)
ARRAY_JOB_ID=$(sbatch --parsable \
  --array="1-${SHARD_COUNT}%${MAX_PARALLEL}" \
  --export="ALL,CAMPAIGN_ID=$CAMPAIGN_ID" \
  "$REPO/research/literature_pipeline/jobs/glm53-extraction-array.sbatch")
FINALIZE_JOB_ID=$(sbatch --parsable \
  --dependency="afterok:${ARRAY_JOB_ID}" \
  --export="ALL,CAMPAIGN_ID=$CAMPAIGN_ID" \
  "$REPO/research/literature_pipeline/jobs/glm53-extraction-finalize.sbatch")

printf 'campaign_id=%s\narray_job_id=%s\nfinalize_job_id=%s\nshard_count=%s\nmax_parallel=%s\n' \
  "$CAMPAIGN_ID" "$ARRAY_JOB_ID" "$FINALIZE_JOB_ID" "$SHARD_COUNT" "$MAX_PARALLEL"
