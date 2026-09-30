#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v3-evidence
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required new V3 run directory}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
SOURCE_BANK="${JACS_SOURCE_BANK:-$BASE/runs/jacs-au-kg-v2-20260929/evidence/bank.json}"
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"
"$PYTHON" -X utf8 -m unittest discover -s "$CODE_ROOT/research/tests" \
  -p 'test_jacs_au*.py' -q > "$JACS_RUN_ROOT/logs/preflight-tests.txt" 2>&1
"$PYTHON" -u "$CODE_ROOT/research/scripts/prepare_jacs_au_kg_v3.py" \
  --source-bank "$SOURCE_BANK" \
  --review "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v3-source-review.json" \
  --config "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v3-pilot.json" \
  --output "$JACS_RUN_ROOT/evidence"
