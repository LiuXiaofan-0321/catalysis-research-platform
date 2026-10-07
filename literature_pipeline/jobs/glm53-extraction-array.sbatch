#!/usr/bin/env bash
# Submit through submit-glm53-extraction-campaign.sh.
# The array range is supplied at submission time from the frozen campaign summary.
#SBATCH --job-name=glm53-extract
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=06:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
WORKSPACE="$BASE/workspace-extraction-production"
CAMPAIGN_ID="${CAMPAIGN_ID:?CAMPAIGN_ID was not exported by the submitter}"
CAMPAIGN_DIR="$BASE/manifests/glm53-extraction/$CAMPAIGN_ID"
SHARD_NUMBER=$(printf '%04d' "${SLURM_ARRAY_TASK_ID:?missing array task id}")
SHARD_ID="shard-${SHARD_NUMBER}"
SOURCE_CONFIG="$CAMPAIGN_DIR/configs/${SHARD_ID}.yaml"
RUNTIME_CONFIG="$BASE/configs/glm53-extraction/$CAMPAIGN_ID/${SHARD_ID}.yaml"
RUN_ID="${CAMPAIGN_ID}-${SHARD_ID}"

: "${ZHIPU_API_KEY:?Export ZHIPU_API_KEY before submitting}"
: "${ZHIPU_PROXY_BASE_URL:?Export the login02 proxy API base URL before submitting}"

mkdir -p "$(dirname "$RUNTIME_CONFIG")"
sed "s|^  base_url: .*$|  base_url: ${ZHIPU_PROXY_BASE_URL%/}|" \
  "$SOURCE_CONFIG" > "$RUNTIME_CONFIG"

"$VENV/bin/litpipe" preflight --config "$RUNTIME_CONFIG"
if [[ -d "$WORKSPACE/runs/$RUN_ID" ]]; then
  "$VENV/bin/litpipe" resume \
    --workspace "$WORKSPACE" \
    --run-id "$RUN_ID" \
    --confirm-large-run
else
  "$VENV/bin/litpipe" run \
    --config "$RUNTIME_CONFIG" \
    --run-id "$RUN_ID" \
    --confirm-large-run
fi
"$VENV/bin/litpipe" verify --workspace "$WORKSPACE" --run-id "$RUN_ID"
