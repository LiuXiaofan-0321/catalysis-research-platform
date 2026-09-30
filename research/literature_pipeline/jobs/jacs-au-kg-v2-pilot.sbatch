#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v2
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=02:00:00
#SBATCH --array=0-8%3
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required}"
: "${ZHIPU_API_KEY:?Required}"
: "${ZHIPU_PROXY_BASE_URL:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
BASELINE="${JACS_BASELINE_ROOT:-$BASE/runs/jacs-au-20260928/baseline}"
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export HF_HOME="$BASE/cache/huggingface" HF_HUB_CACHE="$BASE/cache/huggingface"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
modes=(agent rag_agent small_kg_rag_agent)
mode=${modes[$((SLURM_ARRAY_TASK_ID % 3))]}
replicate=$((SLURM_ARRAY_TASK_ID / 3 + 1))
"$PYTHON" -u "$CODE_ROOT/research/scripts/run_jacs_au.py" discover \
  --data "$BASE/benchmarks/jacs-au-2024/Supporting_final_2" \
  --baseline "$BASELINE" --knowledge-bank "$JACS_RUN_ROOT/evidence/bank.json" \
  --config "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v2-pilot.json" \
  --mode "$mode" --replicate "$replicate" \
  --output "$JACS_RUN_ROOT/discovery/${mode}-replicate-${replicate}.json"
