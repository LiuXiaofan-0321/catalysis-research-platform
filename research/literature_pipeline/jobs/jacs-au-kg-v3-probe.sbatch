#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v3-probe
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
: "${JACS_RUN_ROOT:?Required}"
: "${ZHIPU_API_KEY:?Required}"
: "${ZHIPU_PROXY_BASE_URL:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
export PYTHONPATH="$CODE_ROOT/research/src:$CODE_ROOT/research/literature_pipeline/src"
"$PYTHON" -u "$CODE_ROOT/research/scripts/probe_jacs_au_kg_v3_api.py" \
  --output "$JACS_RUN_ROOT/api-probe-result.json"
