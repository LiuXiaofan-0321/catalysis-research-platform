#!/usr/bin/env bash
# Submit only after the three-paper manifest is frozen and ZHIPU_API_KEY is exported.
#SBATCH --job-name=rag-extract-3
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
CONFIG_TEMPLATE="$REPO/research/literature_pipeline/configs/full-rag-extraction-pilot-3.template.yaml"
WORKSPACE="$BASE/workspace-extraction"
RUN_ID=full-rag-extraction-pilot-3-glm53flash-proxy-v2
CONFIG="$BASE/configs/$RUN_ID.yaml"

: "${ZHIPU_API_KEY:?Export ZHIPU_API_KEY before submitting this job}"
: "${ZHIPU_PROXY_BASE_URL:?Export the login02 proxy API base URL before submitting}"

mkdir -p "$BASE/configs"
sed "s|^  base_url: .*$|  base_url: ${ZHIPU_PROXY_BASE_URL%/}|" \
  "$CONFIG_TEMPLATE" > "$CONFIG"

"$VENV/bin/litpipe" preflight --config "$CONFIG"
if [[ -d "$WORKSPACE/runs/$RUN_ID" ]]; then
  "$VENV/bin/litpipe" resume --workspace "$WORKSPACE" --run-id "$RUN_ID"
else
  "$VENV/bin/litpipe" run --config "$CONFIG" --run-id "$RUN_ID"
fi
"$VENV/bin/litpipe" verify --workspace "$WORKSPACE" --run-id "$RUN_ID"
