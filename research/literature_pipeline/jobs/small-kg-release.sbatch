#!/usr/bin/env bash
#SBATCH --job-name=small-kg-v1
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=08:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
CAMPAIGNS="$BASE/workspace-extraction-production/campaigns"
CORPUS="$BASE/releases/zeolite-structured-corpus-v1"
STAGE1="$BASE/releases/zeolite-small-kg-stage1-v1.zip"
SNAPSHOT="$BASE/kg-snapshots/Small-KG-zeolite-v1"
CODE_COMMIT="${CODE_COMMIT:?Submit with --export=ALL,CODE_COMMIT=<git-commit>}"

mkdir -p "$BASE/logs" "$BASE/releases" "$BASE/kg-snapshots"

if [[ ! -f "$CORPUS/manifest.json" ]]; then
  "$VENV/bin/python" \
    "$REPO/research/literature_pipeline/scripts/freeze_structured_corpus.py" \
    --campaign-directory "$CAMPAIGNS/glm53-extraction-batch-0001" \
    --campaign-directory "$CAMPAIGNS/glm53-extraction-batch-0002" \
    --campaign-directory "$CAMPAIGNS/glm53-extraction-batch-0003" \
    --output-directory "$CORPUS" \
    --corpus-id zeolite-structured-corpus-v1 \
    --expected-documents 8927 \
    --review-sample-size 24
fi

arguments=()
if [[ -f "$STAGE1" ]]; then
  arguments+=(--reuse-stage1-archive)
fi

if [[ ! -f "$SNAPSHOT/manifest.json" ]]; then
  "$VENV/bin/python" \
    "$REPO/research/literature_pipeline/scripts/build_small_kg_from_corpus.py" \
    --corpus-directory "$CORPUS" \
    --stage1-archive "$STAGE1" \
    --snapshot-directory "$SNAPSHOT" \
    --repository-root "$REPO" \
    --expected-documents 8927 \
    --expected-papers 6691 \
    --code-commit "$CODE_COMMIT" \
    "${arguments[@]}"
fi

"$VENV/bin/python" -c \
  "import json,sys; sys.path.insert(0, '$REPO/research/src'); from pathlib import Path; from catalysis_research.kg.freeze_stage1 import verify_snapshot; result=verify_snapshot(Path('$SNAPSHOT')); print(json.dumps(result, indent=2)); raise SystemExit(0 if result['valid'] else 1)"
