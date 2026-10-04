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
: "${CODE_ROOT:?Required versioned code release}"
: "${DIRECT_RUN:?Required new run directory}"
: "${DIRECT_PHASE:?baseline, generate or evaluate}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export PYTHONPATH="$CODE_ROOT/research/src"
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
COMMON=(--data "$BASE/benchmarks/jacs-au-2024/Supporting_final_2" --baseline "$BASE/runs/jacs-au-20260928/baseline" --config "$DIRECT_RUN/prepared/config.json")
if [[ "$DIRECT_PHASE" == baseline ]]; then
  "$PYTHON" -u "$CODE_ROOT/research/scripts/manage_jacs_au_direct.py" baseline "${COMMON[@]}" --output "$DIRECT_RUN/d0"
elif [[ "$DIRECT_PHASE" == generate || "$DIRECT_PHASE" == evaluate ]]; then
  : "${SLURM_ARRAY_TASK_ID:?Required array 0-29}"
  TASK="$SLURM_ARRAY_TASK_ID"
  # The prepared manifest is the authoritative mapping; do not reroll an index.
  read -r MODE REP < <("$PYTHON" -c 'import json,sys; p=json.load(open(sys.argv[1])); t=p["tasks"][int(sys.argv[2])]; assert t["index"]==int(sys.argv[2]); print(t["mode"],t["replicate"])' "$DIRECT_RUN/prepared/tasks.json" "$TASK")
  NAME="$MODE-replicate-$REP"
  if [[ "$DIRECT_PHASE" == generate ]]; then
    : "${ZHIPU_API_KEY:?Load in private submitting environment}"
    : "${ZHIPU_PROXY_BASE_URL:?Verify dedicated login02 proxy on a compute node first}"
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
