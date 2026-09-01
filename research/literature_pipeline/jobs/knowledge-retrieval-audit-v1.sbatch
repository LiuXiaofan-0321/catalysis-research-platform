#!/usr/bin/env bash
#SBATCH --job-name=kg-rag-audit-v1
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=01:30:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
CODE_ROOT="${CODE_ROOT:?Submit with --export=ALL,CODE_ROOT=<versioned-code-directory>}"
VENV="$BASE/envs/py312-rag"
INDEX="$BASE/workspace-full/indexes/full-rag-v1-index"
SNAPSHOT="$BASE/kg-snapshots/Small-KG-zeolite-v1"
OVERLAY="$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1"
CONFIG="$CODE_ROOT/research/configs/retrieval/small-kg-hybrid-v1.json"
QUESTIONS_CONFIG="${QUESTIONS_CONFIG:-zeolite-retrieval-audit-v1.json}"
AUDIT_NAME="${AUDIT_NAME:-zeolite-retrieval-audit-v1}"
QUESTIONS="$CODE_ROOT/research/configs/retrieval/$QUESTIONS_CONFIG"
OUTPUT="$BASE/audits/$AUDIT_NAME-${SLURM_JOB_ID}.json"

mkdir -p "$BASE/logs" "$BASE/audits"
export HF_HOME="$BASE/cache/huggingface"
export SENTENCE_TRANSFORMERS_HOME="$BASE/cache/huggingface"
export HF_HUB_DISABLE_TELEMETRY=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"

"$VENV/bin/python" "$CODE_ROOT/research/scripts/research.py" audit-retrieval \
  --config "$CONFIG" \
  --questions "$QUESTIONS" \
  --rag-index "$INDEX" \
  --snapshot "$SNAPSHOT" \
  --overlay "$OVERLAY" \
  --output "$OUTPUT"

echo "retrieval_audit=$OUTPUT"
