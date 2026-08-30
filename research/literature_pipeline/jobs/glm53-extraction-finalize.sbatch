#!/usr/bin/env bash
# Submitted automatically with an afterok dependency on the extraction array.
#SBATCH --job-name=glm53-finalize
#SBATCH --partition=cpu_96G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
WORKSPACE="$BASE/workspace-extraction-production"
CAMPAIGN_ID="${CAMPAIGN_ID:?CAMPAIGN_ID was not exported by the submitter}"
CAMPAIGN_DIR="$BASE/manifests/glm53-extraction/$CAMPAIGN_ID"

"$VENV/bin/python" \
  "$REPO/research/literature_pipeline/scripts/finalize_extraction_campaign.py" \
  --summary "$CAMPAIGN_DIR/summary.json" \
  --workspace "$WORKSPACE" \
  --output-directory "$WORKSPACE/campaigns/$CAMPAIGN_ID"
