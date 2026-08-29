#!/usr/bin/env bash
#SBATCH --job-name=acs50-si-audit
#SBATCH --partition=a100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --gres=gpu:1
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
VENV="$BASE/envs/py312-rag"
INDEX="$BASE/workspace/indexes/acs-50-main-si-rag-v1-index"

export HF_HOME="$BASE/cache/huggingface"
export SENTENCE_TRANSFORMERS_HOME="$BASE/cache/huggingface"
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false

"$VENV/bin/litpipe" retrieve \
  --index "$INDEX" \
  --query "time-dependent Cu(I) fraction in O2-assisted oxidation XAS rate equation" \
  > "$BASE/logs/retrieval-si-cui-${SLURM_JOB_ID}.json"
"$VENV/bin/litpipe" retrieve \
  --index "$INDEX" \
  --query "Table S1 comparison of probe-assisted NMR methods Bronsted acid location concentration and strength" \
  > "$BASE/logs/retrieval-si-nmr-table-${SLURM_JOB_ID}.json"
"$VENV/bin/litpipe" retrieve \
  --index "$INDEX" \
  --query "downsizing AFX zeolite crystals by post-milling recrystallization experimental procedure" \
  > "$BASE/logs/retrieval-si-afx-${SLURM_JOB_ID}.json"

echo "[$(date -Is)] completed targeted SI retrieval audit"
