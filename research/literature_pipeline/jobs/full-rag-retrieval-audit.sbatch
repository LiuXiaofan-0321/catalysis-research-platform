#!/usr/bin/env bash
#SBATCH --job-name=full-rag-audit
#SBATCH --partition=a100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=12G
#SBATCH --time=00:20:00
#SBATCH --gres=gpu:1
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
INDEX="$BASE/workspace-full/indexes/full-rag-v1-index"
QUESTIONS="$REPO/research/literature_pipeline/configs/full-rag-retrieval-audit-v1.json"
OUTPUT="$BASE/logs/full-rag-retrieval-audit-${SLURM_JOB_ID}.json"

export HF_HOME="$BASE/cache/huggingface"
export SENTENCE_TRANSFORMERS_HOME="$BASE/cache/huggingface"
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false

"$VENV/bin/litpipe" audit-retrieval \
  --index "$INDEX" \
  --questions "$QUESTIONS" \
  --top-k 8 \
  --context-token-budget 4000 \
  > "$OUTPUT"

echo "retrieval_audit=$OUTPUT"
