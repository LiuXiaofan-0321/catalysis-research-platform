#!/usr/bin/env bash
# Submit after the array with: sbatch --dependency=afterok:ARRAY_JOB_ID full-rag-merge.sbatch
#SBATCH --job-name=full-rag-merge
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
VENV="$BASE/envs/py312-rag"
WORKSPACE="$BASE/workspace-full"
OUTPUT="$WORKSPACE/indexes/full-rag-v1-index"
indexes=("$WORKSPACE"/indexes/full-rag-v1-shard-*-index)
if [[ ! -d "${indexes[0]}" ]]; then
  echo "No shard indexes found" >&2
  exit 1
fi
expected_shards=$("$VENV/bin/python" -c \
  'import json, pathlib; print(json.loads(pathlib.Path("/public/home/xiaohe/lxf/catalysis-rag/manifests/full-rag-v1/summary.json").read_text())["batch_count"])')
if [[ "${#indexes[@]}" -ne "$expected_shards" ]]; then
  echo "Expected $expected_shards shard indexes, found ${#indexes[@]}" >&2
  exit 2
fi
arguments=()
for index in "${indexes[@]}"; do
  arguments+=(--index "$index")
done

"$VENV/bin/litpipe" merge-indexes \
  "${arguments[@]}" \
  --output "$OUTPUT" \
  --index-id full-rag-v1-index
"$VENV/bin/litpipe" verify --index "$OUTPUT"
