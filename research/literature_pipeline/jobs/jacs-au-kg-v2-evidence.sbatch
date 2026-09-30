#!/usr/bin/env bash
#SBATCH --job-name=jacs-au-kg-v2-evidence
#SBATCH --partition=cpu_96G,cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
#SBATCH --time=01:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err
set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH
: "${CODE_ROOT:?Required}"
: "${JACS_RUN_ROOT:?Required}"
BASE=/public/home/xiaohe/lxf/catalysis-rag
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
export HF_HOME="$BASE/cache/huggingface" HF_HUB_CACHE="$BASE/cache/huggingface"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6${LD_PRELOAD:+:$LD_PRELOAD}"
PYTHON="${JACS_PYTHON:-$BASE/envs/py312-rag/bin/python}"
"$PYTHON" -u "$CODE_ROOT/research/scripts/run_jacs_au.py" evidence-bank \
  --base "$BASE" --output "$JACS_RUN_ROOT/evidence" \
  --config "$CODE_ROOT/research/configs/experiments/jacs-au-kg-v2-pilot.json"
