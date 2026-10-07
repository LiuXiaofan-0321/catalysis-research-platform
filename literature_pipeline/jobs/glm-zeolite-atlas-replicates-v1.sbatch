#!/usr/bin/env bash
#SBATCH --job-name=glm-zeolite-reps
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=00:30:00
#SBATCH --array=1-5%5
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err

set -euo pipefail
unset PYTHONHOME PYTHONPATH
: "${ZHIPU_API_KEY:?Export ZHIPU_API_KEY before submitting}"
: "${ZHIPU_PROXY_BASE_URL:?Export ZHIPU_PROXY_BASE_URL before submitting}"

BASE=/public/home/xiaohe/lxf/catalysis-rag
CODE=/public/home/xiaohe/lxf/catalysis-rag/code/releases/knowledge-retrieval-dcaa99e-r2
export HF_HOME="$BASE/cache/huggingface"
export HF_HUB_CACHE="$HF_HOME"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export PYTHONPATH="$CODE/research/src:$CODE/research/literature_pipeline/src"

RUN_DIR="$BASE/runs/glm-discovery-zeolite-atlas-v1-replicates-${SLURM_ARRAY_JOB_ID}"
mkdir -p "$RUN_DIR" "$BASE/logs"

TASK='Using only the retrieved zeolite evidence, propose one falsifiable hypothesis about a computable structural descriptor that could improve prediction of framework energy or volume in the Materials Cloud Zeolite Atlas. Keep reported evidence separate from the hypothesis, use only the supplied descriptor catalog, and state what result would falsify it.'
QUERY='zeolite framework topology ring distribution local environment heterogeneity SOAP energy volume descriptor'
OUT=$(printf '%s/replicate-%02d.json' "$RUN_DIR" "$SLURM_ARRAY_TASK_ID")

"$BASE/envs/py312-rag/bin/python" "$CODE/research/scripts/run_glm_zeolite_atlas.py" \
  --config "$CODE/research/configs/retrieval/small-kg-hybrid-zeolite-atlas-v1.json" \
  --rag-index "$BASE/workspace-full/indexes/full-rag-v1-index" \
  --snapshot "$BASE/kg-snapshots/Small-KG-zeolite-v1" \
  --overlay "$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1" \
  --dataset-root "$BASE/benchmarks/materialscloud-2019.0079-v1/extracted" \
  --output "$OUT" \
  --task "$TASK" \
  --query "$QUERY" \
  --model glm-5.3-flash \
  --thinking enabled \
  --reasoning-effort low \
  --replicate-id "$SLURM_ARRAY_TASK_ID"

echo "output=$OUT"
