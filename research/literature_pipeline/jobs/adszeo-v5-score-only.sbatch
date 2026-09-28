#!/usr/bin/env bash
#SBATCH --job-name=adszeo-v5-score
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=03:00:00
#SBATCH --array=1-10%5
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%A_%a.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${ZHIPU_API_KEY:?Export ZHIPU_API_KEY before submitting}"
: "${ZHIPU_PROXY_BASE_URL:?Export the server GLM proxy endpoint before submitting}"

BASE=/public/home/xiaohe/lxf/catalysis-rag
CODE_ROOT="${CODE_ROOT:?Submit with CODE_ROOT set to the versioned code directory}"
DATABASE="${ADSZEO_DATABASE:-$BASE/benchmarks/adszeo-v1/AdsZeo_data.duckdb}"
GEOMETRY_CSV="${ADSZEO_GEOMETRY_CSV:-$BASE/benchmarks/adszeo-v1/geometry-features-v1.csv}"
VENV="${ADSZEO_VENV:-$BASE/envs/py312-rag}"
SHA256_FILE="$DATABASE.sha256"

test -s "$DATABASE"
test -s "$SHA256_FILE"
test -s "$GEOMETRY_CSV"
DATABASE_SHA256=$(tr -d '[:space:]' < "$SHA256_FILE")
test "${#DATABASE_SHA256}" -eq 64

# py312-rag python symlinks to miniconda; duckdb 1.5.5 needs a newer libstdc++
# than miniconda ships, and the executable RPATH wins over LD_LIBRARY_PATH,
# so preload the compatible library explicitly.
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
export HF_HOME="$BASE/cache/huggingface"
export HF_HUB_CACHE="$HF_HOME"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"

RUN_DIR="$BASE/runs/glm-discovery-adszeo-v5-score-only-${SLURM_ARRAY_JOB_ID}"
mkdir -p "$RUN_DIR" "$BASE/logs"
OUT=$(printf '%s/replicate-%02d.json' "$RUN_DIR" "$SLURM_ARRAY_TASK_ID")

"$VENV/bin/python" "$CODE_ROOT/research/scripts/run_glm_adszeo_v2.py" \
  --config "$CODE_ROOT/research/configs/retrieval/small-kg-hybrid-adszeo-v5.json" \
  --rag-index "$BASE/workspace-full/indexes/full-rag-v1-index" \
  --snapshot "$BASE/kg-snapshots/Small-KG-zeolite-v1" \
  --overlay "$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1" \
  --database "$DATABASE" \
  --geometry-csv "$GEOMETRY_CSV" \
  --database-sha256 "$DATABASE_SHA256" \
  --output "$OUT" \
  --replicate-id "$SLURM_ARRAY_TASK_ID" \
  --open-nomination \
  --score-only

echo "output=$OUT"
