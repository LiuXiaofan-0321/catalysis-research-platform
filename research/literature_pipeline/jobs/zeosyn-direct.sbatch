#!/usr/bin/env bash
#SBATCH --job-name=zeosyn-direct
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=03:00:00
# Submitted only by research/jobs/zeosyn/launch.sh, which sets per-phase
# resources, --output/--error and the exported variables below.
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?frozen code release}"
: "${RUN_DIR:?run directory}"
: "${PHASE:?prepare|knowledge|baseline|probe|generate|evaluate|summarize}"
: "${ZEOSYN_PYTHON:?python with numpy, pandas, scikit-learn, openpyxl, rdkit}"
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"
N="${SLURM_CPUS_PER_TASK:-1}"
export OMP_NUM_THREADS="$N" MKL_NUM_THREADS="$N" OPENBLAS_NUM_THREADS="$N"
if [[ -n "${ZEOSYN_LD_PRELOAD:-}" ]]; then export LD_PRELOAD="$ZEOSYN_LD_PRELOAD${LD_PRELOAD:+:$LD_PRELOAD}"; fi
RUN=("$ZEOSYN_PYTHON" -u -W ignore "$CODE_ROOT/research/scripts/run_zeosyn.py")
echo "phase=$PHASE task=${SLURM_ARRAY_TASK_ID:-none} host=$(hostname) start=$(date -Is)"
case "$PHASE" in
  prepare)
    unset ZHIPU_API_KEY
    "${RUN[@]}" prepare --data-root "$CODE_ROOT/research/datasets/zeosyn" --run-dir "$RUN_DIR" \
      --config "$CODE_ROOT/research/configs/experiments/zeosyn-direct-v1.json" ;;
  knowledge)
    unset ZHIPU_API_KEY
    : "${RAG_INDEX:?}" "${KG_SNAPSHOT:?}" "${KG_OVERLAY:?}" "${HF_HOME:?}"
    export HF_HUB_CACHE="$HF_HOME" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
    "${RUN[@]}" knowledge --run-dir "$RUN_DIR" \
      --base-retrieval-config "$CODE_ROOT/research/configs/retrieval/small-kg-hybrid-v1.json" \
      --rag-index "$RAG_INDEX" --snapshot "$KG_SNAPSHOT" --overlay "$KG_OVERLAY" ;;
  baseline)
    unset ZHIPU_API_KEY
    "${RUN[@]}" baseline --run-dir "$RUN_DIR" --n-jobs "$N" ;;
  probe)
    : "${ZHIPU_API_KEY:?}" "${ZHIPU_PROXY_BASE_URL:?}"
    "${RUN[@]}" probe --run-dir "$RUN_DIR" ;;
  generate)
    : "${ZHIPU_API_KEY:?}" "${ZHIPU_PROXY_BASE_URL:?}" "${SLURM_ARRAY_TASK_ID:?}"
    "${RUN[@]}" generate --run-dir "$RUN_DIR" --task-index "$SLURM_ARRAY_TASK_ID" ;;
  evaluate)
    unset ZHIPU_API_KEY
    : "${SLURM_ARRAY_TASK_ID:?}"
    "${RUN[@]}" evaluate --run-dir "$RUN_DIR" --task-index "$SLURM_ARRAY_TASK_ID" --n-jobs "$N" ;;
  summarize)
    unset ZHIPU_API_KEY
    "${RUN[@]}" summarize --run-dir "$RUN_DIR" ;;
  *) echo "Unsupported PHASE=$PHASE" >&2; exit 2 ;;
esac
echo "phase=$PHASE end=$(date -Is)"
