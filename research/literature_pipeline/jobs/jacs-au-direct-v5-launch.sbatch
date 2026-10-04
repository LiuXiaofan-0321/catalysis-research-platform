#!/usr/bin/env bash
#SBATCH --job-name=jacs-direct-v5
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=10:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required frozen scientific release}"
: "${AUX_ROOT:?Required launch-only release}"
: "${DIRECT_RUN:?Required}"
: "${DIRECT_PHASE:?probe, generate, evaluate or summarize}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="$BASE/envs/py312-rag/bin/python"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}"
export PYTHONPATH="$CODE_ROOT/research/src"
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
if [[ "$DIRECT_PHASE" == probe ]]; then
  : "${ZHIPU_API_KEY:?Private environment required}"
  : "${ZHIPU_PROXY_BASE_URL:?Dedicated login02 proxy required}"
  "$PYTHON" -u "$AUX_ROOT/research/scripts/probe_jacs_au_direct_api.py" \
    --config "$DIRECT_RUN/prepared/config.json" --output "$DIRECT_RUN/api-probe.json"
elif [[ "$DIRECT_PHASE" == summarize ]]; then
  unset ZHIPU_API_KEY
  "$PYTHON" -u "$CODE_ROOT/research/scripts/manage_jacs_au_direct.py" summarize \
    --plan "$DIRECT_RUN/scheduling-tasks.json" --generations "$DIRECT_RUN/generation" \
    --evaluations "$DIRECT_RUN/evaluation" --output "$DIRECT_RUN/summary.json"
elif [[ "$DIRECT_PHASE" == generate || "$DIRECT_PHASE" == evaluate ]]; then
  : "${SLURM_ARRAY_TASK_ID:?Required array 0-29}"
  read -r MODE REP < <("$PYTHON" -c 'import json,sys; p=json.load(open(sys.argv[1])); t=p["tasks"][int(sys.argv[2])]; assert t["index"]==int(sys.argv[2]); print(t["mode"],t["replicate"])' "$DIRECT_RUN/scheduling-tasks.json" "$SLURM_ARRAY_TASK_ID")
  NAME="$MODE-replicate-$REP"
  COMMON=(--data "$BASE/benchmarks/jacs-au-2024/Supporting_final_2" --baseline "$BASE/runs/jacs-au-20260928/baseline" --config "$DIRECT_RUN/prepared/config.json")
  if [[ "$DIRECT_PHASE" == generate ]]; then
    : "${ZHIPU_API_KEY:?Private environment required}"
    : "${ZHIPU_PROXY_BASE_URL:?Dedicated login02 proxy required}"
    "$PYTHON" -u "$CODE_ROOT/research/scripts/run_jacs_au_direct.py" generate "${COMMON[@]}" \
      --knowledge "$DIRECT_RUN/prepared/knowledge.json" --gate "$DIRECT_RUN/gate.json" \
      --mode "$MODE" --replicate "$REP" --output "$DIRECT_RUN/generation/$NAME.json"
  else
    unset ZHIPU_API_KEY
    "$PYTHON" -u "$CODE_ROOT/research/scripts/run_jacs_au_direct.py" evaluate "${COMMON[@]}" \
      --multi-seed-baseline "$DIRECT_RUN/d0" --frozen "$DIRECT_RUN/generation/$NAME.json" \
      --output "$DIRECT_RUN/evaluation/$NAME.json"
  fi
else
  echo 'Unsupported DIRECT_PHASE' >&2
  exit 2
fi
