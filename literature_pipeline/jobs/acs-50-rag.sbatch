#!/usr/bin/env bash
#SBATCH --job-name=acs50-rag
#SBATCH --partition=a100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPOSITORY="$BASE/code/catalysis-research-platform"
PIPELINE="$REPOSITORY/research/literature_pipeline"
CONFIG="$PIPELINE/configs/acs-50-rag.template.yaml"
VENV="$BASE/envs/py312-rag"
RUN_ID=acs-50-main-si-rag-v1
INDEX="$BASE/workspace/indexes/${RUN_ID}-index"

mkdir -p "$BASE/cache/huggingface" "$BASE/cache/pip" "$BASE/envs" "$BASE/logs"
export HF_HOME="$BASE/cache/huggingface"
export SENTENCE_TRANSFORMERS_HOME="$BASE/cache/huggingface"
export PIP_CACHE_DIR="$BASE/cache/pip"
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

echo "[$(date -Is)] host=$(hostname) job_id=${SLURM_JOB_ID:-none}"
python3 --version

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi

PYTHON="$VENV/bin/python"
if [[ ! -f "$VENV/.acs50-rag-dependencies-v2" ]]; then
  "$PYTHON" -m pip install --upgrade "pip>=24" "setuptools>=68" wheel
  "$PYTHON" -m pip install -e "$PIPELINE"
  "$PYTHON" -m pip install \
    --index-url https://download.pytorch.org/whl/cu121 \
    "torch==2.4.1+cu121"
  "$PYTHON" -m pip install "sentence-transformers==3.1.1"
  touch "$VENV/.acs50-rag-dependencies-v2"
fi

"$PYTHON" -m pip freeze > "$BASE/logs/python-freeze-${SLURM_JOB_ID}.txt"
"$PYTHON" -c "import torch; assert torch.cuda.is_available(); print(torch.cuda.get_device_name(0))"
"$VENV/bin/litpipe" doctor
"$VENV/bin/litpipe" preflight --config "$CONFIG"
"$VENV/bin/litpipe" run \
  --config "$CONFIG" \
  --run-id "$RUN_ID" \
  --confirm-large-run
"$VENV/bin/litpipe" verify \
  --run-id "$RUN_ID" \
  --workspace "$BASE/workspace" \
  > "$BASE/logs/verify-run-${SLURM_JOB_ID}.json"
"$VENV/bin/litpipe" verify \
  --index "$INDEX" \
  > "$BASE/logs/verify-index-${SLURM_JOB_ID}.json"

"$VENV/bin/litpipe" retrieve \
  --index "$INDEX" \
  --query "zeolite hydrothermal synthesis temperature time and structure directing agent" \
  > "$BASE/logs/retrieval-synthesis-${SLURM_JOB_ID}.json"
"$VENV/bin/litpipe" retrieve \
  --index "$INDEX" \
  --query "supporting information experimental characterization XRD NMR adsorption" \
  > "$BASE/logs/retrieval-si-${SLURM_JOB_ID}.json"
"$VENV/bin/litpipe" retrieve \
  --index "$INDEX" \
  --query "Si Al ratio acidity and catalytic performance" \
  > "$BASE/logs/retrieval-acidity-${SLURM_JOB_ID}.json"

echo "[$(date -Is)] completed run_id=$RUN_ID"
