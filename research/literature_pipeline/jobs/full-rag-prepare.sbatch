#!/usr/bin/env bash
#SBATCH --job-name=rag-prepare
#SBATCH --partition=cpu_96G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPOSITORY="$BASE/code/catalysis-research-platform"
PIPELINE="$REPOSITORY/research/literature_pipeline"
VENV="$BASE/envs/py312-rag"

"$VENV/bin/python" "$PIPELINE/scripts/build_full_corpus_manifests.py" \
  --corpus-root /public/home/xiaohe/zwan/zya/paper_all \
  --output-directory "$BASE/manifests/full-rag-v1" \
  --batch-size 200 \
  --config-template "$PIPELINE/configs/full-rag-shard.template.yaml" \
  --config-output-directory "$BASE/configs/full-rag-v1" \
  --workspace "$BASE/workspace-full" \
  --overwrite
