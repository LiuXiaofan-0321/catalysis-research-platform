#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v4-summary
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err
set -euo pipefail
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
"$PYTHON" -u "$CODE_ROOT/research/scripts/summarize_jacs_au_kg_v4.py" "$JACS_RUN_ROOT"
