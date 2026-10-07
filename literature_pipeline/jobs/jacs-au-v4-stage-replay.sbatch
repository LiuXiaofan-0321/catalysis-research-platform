#!/usr/bin/env bash
#SBATCH --job-name=jacs-v4-stage-replay
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=04:00:00
#SBATCH --array=0-53%4
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${REPLAY_RUN:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/scripts"
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
"$PYTHON" -u "$CODE_ROOT/research/scripts/replay_jacs_au_kg_v4_candidates.py" \
  --data "$BASE/benchmarks/jacs-au-2024/Supporting_final_2" \
  --baseline "$BASE/runs/jacs-au-20260928/baseline" \
  --source "$BASE/runs/jacs-au-kg-v4-20260930c-complete" \
  --blocks "$CODE_ROOT/research/reports/jacs_au_kg_v4_diagnosis_20260930/fixed-review-blocks.json" \
  --block-index "$SLURM_ARRAY_TASK_ID" \
  --output "$REPLAY_RUN/blocks/block-$SLURM_ARRAY_TASK_ID.json"
