#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v4-evidence
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required new V4 run directory}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
"$PYTHON" -X utf8 -m unittest discover -s "$CODE_ROOT/research/tests" \
  -p 'test_jacs_au*.py' -q > "$JACS_RUN_ROOT/logs/preflight-tests.txt" 2>&1
"$PYTHON" -X utf8 -m unittest discover -s "$CODE_ROOT/research/tests" \
  -p 'test_glm.py' -q > "$JACS_RUN_ROOT/logs/glm-tests.txt" 2>&1
"$PYTHON" -u "$CODE_ROOT/research/scripts/prepare_jacs_au_kg_v4.py" \
  --source "$BASE/runs/jacs-au-kg-v3-20260929/evidence/bank.json" \
  --config "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v4-low.json" \
  --data "$BASE/benchmarks/jacs-au-2024/Supporting_final_2" \
  --index "$BASE/workspace-full/indexes/full-rag-v1-index" \
  --output "$JACS_RUN_ROOT/evidence"
