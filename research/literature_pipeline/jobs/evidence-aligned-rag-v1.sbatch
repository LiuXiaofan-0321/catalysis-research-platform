#!/usr/bin/env bash
#SBATCH --job-name=aligned-rag-v1
#SBATCH --partition=cpu_192G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=12:00:00
#SBATCH --output=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.out
#SBATCH --error=/public/home/xiaohe/lxf/catalysis-rag/logs/%x-%j.err

set -euo pipefail
umask 027
unset PYTHONHOME PYTHONPATH

BASE=/public/home/xiaohe/lxf/catalysis-rag
REPO="$BASE/code/catalysis-research-platform"
VENV="$BASE/envs/py312-rag"
CORPUS="$BASE/releases/zeolite-structured-corpus-v1"
OUTPUT="$BASE/indexes/zeolite-evidence-aligned-raw-rag-v1"
CONFIG="$REPO/research/configs/retrieval/evidence-aligned-rag-v1.json"
CODE_COMMIT="${CODE_COMMIT:?Submit with --export=ALL,CODE_COMMIT=<git-commit>}"

mkdir -p "$BASE/logs" "$BASE/indexes"
if [[ -e "$OUTPUT" ]]; then
  echo "Refusing to overwrite existing index: $OUTPUT" >&2
  exit 2
fi

"$VENV/bin/python" - "$REPO" "$CORPUS" "$OUTPUT" "$CONFIG" "$CODE_COMMIT" <<'PY'
import json
import sys
from pathlib import Path

repo, corpus, output, config_path, code_commit = sys.argv[1:]
sys.path.insert(0, str(Path(repo) / "research" / "literature_pipeline" / "src"))

from catalysis_literature.aligned_index import build_evidence_aligned_index
from catalysis_literature.config import IndexConfig
from catalysis_literature.indexing import verify_index

config = json.loads(Path(config_path).read_text(encoding="utf-8"))
embedding = config["embedding"]
retrieval = config["retrieval"]
index_config = IndexConfig(
    backend="portable",
    embedding_model=embedding["model"],
    embedding_revision=embedding["revision"],
    embedding_batch_size=embedding["batch_size"],
    vector_dimensions=embedding["dimensions"],
    allow_hash_embedding_fallback=embedding["allow_hash_fallback"],
    **retrieval,
)
manifest = build_evidence_aligned_index(
    corpus_directory=Path(corpus),
    output_directory=Path(output),
    index_id=config["index_id"],
    index_config=index_config,
    target_tokens=config["chunking"]["target_tokens"],
    overlap_tokens=config["chunking"]["overlap_tokens"],
    code_commit=code_commit,
)
print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
report = verify_index(Path(output))
print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
raise SystemExit(0 if report["valid"] else 1)
PY
