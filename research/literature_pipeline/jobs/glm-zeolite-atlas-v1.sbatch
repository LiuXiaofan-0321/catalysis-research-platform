#!/usr/bin/env bash
#SBATCH --job-name=glm-zeolite-atlas-v1
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=00:30:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
unset PYTHONHOME PYTHONPATH
: "${ZHIPU_API_KEY:?Export ZHIPU_API_KEY before submitting}"
: "${ZHIPU_PROXY_BASE_URL:?Export ZHIPU_PROXY_BASE_URL before submitting}"

BASE=/public/home/xiaohe/lxf/catalysis-rag
CODE=/public/home/xiaohe/lxf/catalysis-rag/code/releases/knowledge-retrieval-dcaa99e-r2
export PYTHONPATH="$CODE/research/src:$CODE/research/literature_pipeline/src"
mkdir -p "$BASE/runs" "$BASE/logs"

TASK='Using only the retrieved zeolite evidence, propose one falsifiable hypothesis about a computable structural descriptor that could improve prediction of framework energy or volume in the Materials Cloud Zeolite Atlas. Keep reported evidence separate from the hypothesis, use only the supplied descriptor catalog, and state what result would falsify it.'
QUERY='zeolite framework topology ring distribution local environment heterogeneity SOAP energy volume descriptor'
OUT="$BASE/runs/glm-discovery-zeolite-atlas-v1-${SLURM_JOB_ID}.json"

"$BASE/envs/py312-rag/bin/python" "$CODE/research/scripts/run_glm_zeolite_atlas.py" \
  --config "$CODE/research/configs/retrieval/small-kg-hybrid-v1.json" \
  --rag-index "$BASE/workspace-full/indexes/full-rag-v1-index" \
  --snapshot "$BASE/kg-snapshots/Small-KG-zeolite-v1" \
  --overlay "$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1" \
  --dataset-root "$BASE/benchmarks/materialscloud-2019.0079-v1/extracted" \
  --output "$OUT" \
  --task "$TASK" \
  --query "$QUERY"

echo "output=$OUT"
