#!/usr/bin/env bash
#SBATCH --job-name=jacs-kg-v2-audit
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:05:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err
set -euo pipefail
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
"$BASE/envs/py312-rag/bin/python" -u "$CODE_ROOT/research/scripts/audit_jacs_au_kg_v2_bank.py" \
  --run "$JACS_RUN_ROOT" --base "$BASE" \
  --config "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v2-pilot.json"
