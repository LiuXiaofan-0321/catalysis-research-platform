#!/usr/bin/env bash
# Submit only after the three-paper manifest is frozen and DEEPSEEK_API_KEY is exported.
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
CONFIG="$REPO/research/literature_pipeline/configs/full-rag-extraction-pilot-3.template.yaml"
WORKSPACE="$BASE/workspace-extraction"
RUN_ID=full-rag-extraction-pilot-3-v1

: "${DEEPSEEK_API_KEY:?Export DEEPSEEK_API_KEY before submitting this job}"

"$VENV/bin/litpipe" preflight --config "$CONFIG"
if [[ -d "$WORKSPACE/runs/$RUN_ID" ]]; then
  "$VENV/bin/litpipe" resume --workspace "$WORKSPACE" --run-id "$RUN_ID"
else
  "$VENV/bin/litpipe" run --config "$CONFIG" --run-id "$RUN_ID"
fi
"$VENV/bin/litpipe" verify --workspace "$WORKSPACE" --run-id "$RUN_ID"
