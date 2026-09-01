#!/usr/bin/env bash
#SBATCH --job-name=norm-v1.1
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
CORPUS="$BASE/releases/zeolite-structured-corpus-v1"
SNAPSHOT="$BASE/kg-snapshots/Small-KG-zeolite-v1"
OUTPUT="$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1"
CONFIG="$REPO/research/configs/normalization/scientific-normalization-v1.1.json"
CODE_COMMIT="${CODE_COMMIT:?Submit with --export=ALL,CODE_COMMIT=<git-commit>}"
EXPECTED_SNAPSHOT_HASH=07925455449dfe13cc78b9b958dd71d5e4d77aee2ad54fcd8a312ce4f1bf9f43

mkdir -p "$BASE/logs" "$BASE/releases"

if [[ -e "$OUTPUT" ]]; then
  echo "Refusing to overwrite existing normalization output: $OUTPUT" >&2
  exit 2
fi

"$VENV/bin/python" - "$REPO" "$SNAPSHOT" "$CORPUS" "$OUTPUT" "$CONFIG" "$CODE_COMMIT" "$EXPECTED_SNAPSHOT_HASH" <<'PY'
import json
import sys
from pathlib import Path

repo, snapshot, corpus, output, config, code_commit, expected_hash = sys.argv[1:]
sys.path.insert(0, str(Path(repo) / "research" / "src"))

from catalysis_research.normalization import (
    build_normalization_overlay,
    verify_normalization_overlay,
)

snapshot_manifest = json.loads(
    (Path(snapshot) / "manifest.json").read_text(encoding="utf-8")
)
actual_hash = snapshot_manifest.get("snapshot_content_hash")
if actual_hash != expected_hash:
    raise SystemExit(
        f"Unexpected Small KG snapshot hash: {actual_hash} != {expected_hash}"
    )

manifest = build_normalization_overlay(
    snapshot_directory=Path(snapshot),
    corpus_directory=Path(corpus),
    output_directory=Path(output),
    config_path=Path(config),
    code_commit=code_commit,
)
print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))

report = verify_normalization_overlay(
    overlay_directory=Path(output),
    snapshot_directory=Path(snapshot),
    corpus_directory=Path(corpus),
)
print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
raise SystemExit(0 if report["valid"] else 1)
PY
