#!/usr/bin/env bash
# Submit with: sbatch --array=1-N%6 full-rag-array.sbatch
#SBATCH --job-name=full-rag
#SBATCH --partition=a100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=02:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
VENV="$BASE/envs/py312-rag"
SHARD_NUMBER=$(printf '%04d' "${SLURM_ARRAY_TASK_ID:?missing array task id}")
SHARD_ID="shard-${SHARD_NUMBER}"
CONFIG="$BASE/configs/full-rag-v1/${SHARD_ID}.yaml"
RUN_ID="full-rag-v1-${SHARD_ID}"
INDEX="$BASE/workspace-full/indexes/${RUN_ID}-index"

export HF_HOME="$BASE/cache/huggingface"
export SENTENCE_TRANSFORMERS_HOME="$BASE/cache/huggingface"
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

"$VENV/bin/python" -c \
  "import torch; assert torch.cuda.is_available(); print(torch.cuda.get_device_name(0))"
if [[ -d "$BASE/workspace-full/runs/$RUN_ID" ]]; then
  "$VENV/bin/litpipe" resume \
    --workspace "$BASE/workspace-full" \
    --run-id "$RUN_ID" \
    --confirm-large-run
else
  "$VENV/bin/litpipe" run \
    --config "$CONFIG" \
    --run-id "$RUN_ID" \
    --confirm-large-run
fi
"$VENV/bin/litpipe" verify \
  --run-id "$RUN_ID" \
  --workspace "$BASE/workspace-full"
if [[ ! -f "$INDEX/manifest.json" ]]; then
  echo "Shard run is partial and has no index: $RUN_ID" >&2
  exit 2
fi
"$VENV/bin/litpipe" verify --index "$INDEX"
