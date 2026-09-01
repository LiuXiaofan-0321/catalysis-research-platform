#!/usr/bin/env bash
#SBATCH --job-name=norm-review-v1
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
OVERLAY="$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1"
OUTPUT="$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1-review"

if [[ -e "$OUTPUT" ]]; then
  echo "Refusing to overwrite existing review output: $OUTPUT" >&2
  exit 2
fi

"$VENV/bin/python" - "$REPO" "$OVERLAY" "$OUTPUT" <<'PY'
import json
import sys
from pathlib import Path

repo, overlay, output = sys.argv[1:]
sys.path.insert(0, str(Path(repo) / "research" / "src"))

from catalysis_research.normalization import summarize_unresolved

manifest = summarize_unresolved(
    overlay_directory=Path(overlay),
    output_directory=Path(output),
    top_n=50,
    sample_per_reason=20,
)
print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
PY
