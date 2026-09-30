#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v4-repair
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH --array=3,14,16%3
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required}"
: "${JACS_SOURCE_RUN:?Required}"
: "${ZHIPU_API_KEY:?Required}"
: "${ZHIPU_PROXY_BASE_URL:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
modes=(small_kg_rag_agent rag_agent agent)
efforts=(low high)
mode=${modes[$((SLURM_ARRAY_TASK_ID / 2 % 3))]}
effort=${efforts[$((SLURM_ARRAY_TASK_ID % 2))]}
replicate=$((SLURM_ARRAY_TASK_ID / 6 + 1))
"$PYTHON" -u "$CODE_ROOT/research/scripts/run_jacs_au_kg_v4.py" \
  --data "$BASE/benchmarks/jacs-au-2024/Supporting_final_2" \
  --baseline "$BASE/runs/jacs-au-20260928/baseline" \
  --bank "$JACS_SOURCE_RUN/evidence/bank.json" \
  --index "$BASE/workspace-full/indexes/full-rag-v1-index" \
  --config "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v4-$effort.json" \
  --mode "$mode" --replicate "$replicate" \
  --resume-source "$JACS_SOURCE_RUN/$effort/discovery/${mode}-replicate-${replicate}.json" \
  --output "$JACS_RUN_ROOT/$effort/discovery/${mode}-replicate-${replicate}.json"
