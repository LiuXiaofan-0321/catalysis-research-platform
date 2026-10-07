#!/usr/bin/env bash
# One-command launcher for the ZeoSyn Agent / RAG / KG+RAG experiment on the ECNU cluster.
#
#   bash research/jobs/zeosyn/launch.sh                 # new run (run on login02)
#   bash research/jobs/zeosyn/launch.sh --status RUN    # progress of a run
#   bash research/jobs/zeosyn/launch.sh --resume RUN    # resubmit missing generations/evaluations
#   bash research/jobs/zeosyn/launch.sh --dry-run       # checks only, submits nothing
#
# The GLM key is read from $ZHIPU_API_KEY or, if unset, from $ZHIPU_KEY_FILE
# (default $BASE/.secrets/zhipu_api_key). It is never written to any file here.
set -euo pipefail
umask 027

BASE="${BASE:-/public/home/xiaohe/lxf/catalysis-rag}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
BASE_PYTHON="${BASE_PYTHON:-$BASE/envs/py312-rag/bin/python}"
ZEOSYN_ENV="${ZEOSYN_ENV:-$BASE/envs/zeosyn-py312}"
RAG_INDEX="${RAG_INDEX:-$BASE/workspace-full/indexes/full-rag-v1-index}"
KG_SNAPSHOT="${KG_SNAPSHOT:-$BASE/kg-snapshots/Small-KG-zeolite-v1}"
KG_OVERLAY="${KG_OVERLAY:-$BASE/releases/scientific-normalization-Small-KG-zeolite-v1.1}"
HF_HOME="${HF_HOME:-$BASE/cache/huggingface}"
PROXY_SCRIPT="${PROXY_SCRIPT:-$BASE/tools/api_proxy_1800s.py}"
PROXY_PYTHON="${PROXY_PYTHON:-python3}"
PROXY_HOST="${PROXY_HOST:-10.11.100.254}"
PARTITION="${PARTITION:-cpu_96G,cpu_192G}"
MAX_PARALLEL="${MAX_PARALLEL:-5}"
ZHIPU_KEY_FILE="${ZHIPU_KEY_FILE:-$BASE/.secrets/zhipu_api_key}"
SBATCH_FILE_REL="research/literature_pipeline/jobs/zeosyn-direct.sbatch"

die() { echo "ERROR: $*" >&2; exit 1; }
say() { echo "[zeosyn] $*"; }

MODE=new; RUN_DIR=""; DRY=0
case "${1:-}" in
  --status) MODE=status; RUN_DIR="${2:?--status RUN_DIR}" ;;
  --resume) MODE=resume; RUN_DIR="${2:?--resume RUN_DIR}" ;;
  --dry-run) DRY=1 ;;
  "") ;;
  *) die "unknown argument $1" ;;
esac

if [[ "$MODE" == status ]]; then
  [[ -f "$RUN_DIR/LAUNCH.env" ]] || die "$RUN_DIR/LAUNCH.env not found"
  # shellcheck disable=SC1090,SC1091
  source "$RUN_DIR/LAUNCH.env"
  PYTHONPATH="$CODE_ROOT/research/src" "$ZEOSYN_PYTHON" -W ignore "$CODE_ROOT/research/scripts/run_zeosyn.py" status --run-dir "$RUN_DIR"
  squeue -u "$USER" -o '%.12i %.20j %.8T %.10M %R' 2>/dev/null | grep -E "zeosyn|JOBID" || true
  [[ -f "$RUN_DIR/summary.json" ]] && say "summary: $RUN_DIR/summary.json"
  exit 0
fi

# ------------------------------------------------------------------ checks
command -v sbatch >/dev/null || die "sbatch not found; run this on the cluster login node"
[[ "$(hostname)" == *login02* || -n "${ALLOW_NON_LOGIN02:-}" ]] || die "start on login02 (proxy requirement); set ALLOW_NON_LOGIN02=1 to override"
if [[ -z "${ZHIPU_API_KEY:-}" ]]; then
  [[ -r "$ZHIPU_KEY_FILE" ]] || die "set ZHIPU_API_KEY or create $ZHIPU_KEY_FILE (chmod 600)"
  ZHIPU_API_KEY="$(tr -d '[:space:]' < "$ZHIPU_KEY_FILE")"
fi
export ZHIPU_API_KEY
for p in "$RAG_INDEX" "$KG_SNAPSHOT" "$KG_OVERLAY" "$HF_HOME"; do [[ -e "$p" ]] || die "missing $p"; done
[[ -f "$PROXY_SCRIPT" ]] || die "missing proxy script $PROXY_SCRIPT"
[[ -x "$BASE_PYTHON" ]] || die "missing base python $BASE_PYTHON"

# ------------------------------------------------------------------ frozen code release
if [[ "$MODE" == new ]]; then
  git -C "$REPO" diff --quiet HEAD -- research || die "uncommitted changes under research/; do not edit code on the server"
  COMMIT="$(git -C "$REPO" rev-parse HEAD)"
  CODE_ROOT="$BASE/code/releases/zeosyn-direct-v1-${COMMIT:0:12}"
  if [[ ! -d "$CODE_ROOT" ]]; then
    mkdir -p "$CODE_ROOT"
    git -C "$REPO" archive "$COMMIT" research | tar -x -C "$CODE_ROOT"
  fi
else
  # shellcheck disable=SC1090,SC1091
  source "$RUN_DIR/LAUNCH.env"
fi

# ------------------------------------------------------------------ python environment
if [[ ! -x "$ZEOSYN_ENV/bin/python" ]]; then
  say "creating $ZEOSYN_ENV (inherits $BASE_PYTHON site-packages)"
  "$BASE_PYTHON" -m venv --system-site-packages "$ZEOSYN_ENV"
fi
ZEOSYN_PYTHON="$ZEOSYN_ENV/bin/python"
missing="$("$ZEOSYN_PYTHON" - <<'EOF'
import importlib.util as u
print(' '.join(p for m, p in (('numpy','numpy'),('pandas','pandas'),('sklearn','scikit-learn'),('openpyxl','openpyxl'),('rdkit','rdkit'),('scipy','scipy')) if u.find_spec(m) is None))
EOF
)"
if [[ -n "$missing" ]]; then
  say "installing into $ZEOSYN_ENV: $missing"
  "$ZEOSYN_PYTHON" -m pip install ${PIP_INDEX_URL:+--index-url "$PIP_INDEX_URL"} $missing
fi
PYTHONPATH="${CODE_ROOT:-$REPO}/research/src:${CODE_ROOT:-$REPO}/research/literature_pipeline/src" "$ZEOSYN_PYTHON" -c \
  'import numpy, pandas, sklearn, openpyxl, rdkit, catalysis_research.experiments.zeosyn_direct, catalysis_literature.retrieval' \
  || die "python environment check failed"
ZEOSYN_LD_PRELOAD=""
[[ -f "$BASE/envs/adszeo-py312/lib/libstdc++.so.6" ]] && ZEOSYN_LD_PRELOAD="$BASE/envs/adszeo-py312/lib/libstdc++.so.6"

if [[ "$MODE" == new ]]; then
  RUN_DIR="$BASE/runs/zeosyn-direct-v1-$(date +%Y%m%d-%H%M%S)"
fi
say "code release: $CODE_ROOT"
say "run directory: $RUN_DIR"
if [[ "$DRY" == 1 ]]; then say "dry run: all checks passed, nothing submitted"; exit 0; fi
mkdir -p "$RUN_DIR/logs"

# ------------------------------------------------------------------ dedicated GLM proxy on login02
PROXY_NAME="zeosyn-$(basename "$RUN_DIR")-$(date +%H%M%S)"
PROXY_LOG="$RUN_DIR/logs/proxy-$(date +%Y%m%d-%H%M%S).log"
nohup "$PROXY_PYTHON" -u "$PROXY_SCRIPT" --target https://open.bigmodel.cn --name "$PROXY_NAME" > "$PROXY_LOG" 2>&1 &
PROXY_PID=$!
PORT=""
for _ in $(seq 1 30); do
  PORT="$(grep -oE "${PROXY_HOST//./\\.}:[0-9]{4,5}" "$PROXY_LOG" 2>/dev/null | head -1 | cut -d: -f2 || true)"
  [[ -n "$PORT" ]] && break
  kill -0 "$PROXY_PID" 2>/dev/null || { cat "$PROXY_LOG" >&2; die "proxy exited"; }
  sleep 1
done
[[ -n "$PORT" ]] || { kill "$PROXY_PID" 2>/dev/null || true; cat "$PROXY_LOG" >&2; die "could not read the proxy port from $PROXY_LOG"; }
export ZHIPU_PROXY_BASE_URL="http://$PROXY_HOST:$PORT/api/paas/v4"
say "proxy pid $PROXY_PID at $ZHIPU_PROXY_BASE_URL"
JOBS=()
abort_submission() {  # a failed submission leaves no orphan jobs or proxy behind
  if ((${#JOBS[@]})); then scancel "${JOBS[@]}" 2>/dev/null || true; echo "cancelled ${JOBS[*]}" >&2; fi
  kill "$PROXY_PID" 2>/dev/null || true
}
trap abort_submission EXIT

# ------------------------------------------------------------------ submission helpers
export CODE_ROOT RUN_DIR ZEOSYN_PYTHON ZEOSYN_LD_PRELOAD RAG_INDEX KG_SNAPSHOT KG_OVERLAY HF_HOME
SBATCH_FILE="$CODE_ROOT/$SBATCH_FILE_REL"
LAST=""
submit() {  # submit NAME PHASE DEPENDENCY CPUS MEM TIME [ARRAY]; sets $LAST (no subshell, so JOBS is kept)
  local name=$1 phase=$2 dep=$3 cpus=$4 mem=$5 time=$6 array=${7:-}
  local args=(--parsable --job-name "zeosyn-$name" --partition "$PARTITION" --cpus-per-task "$cpus" --mem "$mem"
              --time "$time" --kill-on-invalid-dep=yes --export "ALL,PHASE=$phase"
              --output "$RUN_DIR/logs/%x-%A_%a.out" --error "$RUN_DIR/logs/%x-%A_%a.err")
  [[ -n "$dep" ]] && args+=(--dependency "$dep")
  [[ -n "$array" ]] && args+=(--array "$array")
  local id
  id="$(sbatch "${args[@]}" "$SBATCH_FILE")"
  id="${id%%;*}"
  JOBS+=("$id")
  LAST="$id"
  say "submitted $name: $id${dep:+ ($dep)}"
}
missing_list() {  # missing_list generation|evaluation -> "0,3,7" or ""
  PYTHONPATH="$CODE_ROOT/research/src" "$ZEOSYN_PYTHON" -W ignore "$CODE_ROOT/research/scripts/run_zeosyn.py" status --run-dir "$RUN_DIR" \
    | "$ZEOSYN_PYTHON" -c "import json,sys; print(','.join(map(str, json.load(sys.stdin)['missing_$1_task_indexes'])))"
}

if [[ "$MODE" == new ]]; then
  submit prepare prepare "" 2 16G 01:00:00; PREP=$LAST
  submit knowledge knowledge "afterok:$PREP" 2 32G 03:00:00; KNOW=$LAST
  submit baseline baseline "afterok:$PREP" 8 16G 02:00:00; BASEJ=$LAST
  submit probe probe "afterok:$KNOW" 1 2G 00:30:00; PROBE=$LAST
  # Smoke: first replicate of each condition, generated and evaluated before the full array is released.
  submit smoke-gen generate "afterok:$PROBE" 1 4G 03:00:00 "0,10,20"; SGEN=$LAST
  submit smoke-eval evaluate "afterok:$SGEN:$BASEJ" 4 16G 01:00:00 "0,10,20"; SEVAL=$LAST
  submit gen generate "afterok:$SEVAL" 1 4G 04:00:00 "1-9,11-19,21-29%$MAX_PARALLEL"; GEN=$LAST
  submit eval evaluate "afterany:$GEN" 4 16G 02:00:00 "0-29%10"; EVAL=$LAST
  submit summarize summarize "afterany:$EVAL" 1 2G 00:30:00
else
  GEN_MISSING="$(missing_list generation)"
  DEP=""
  if [[ -n "$GEN_MISSING" ]]; then
    submit gen-resume generate "" 1 4G 04:00:00 "$GEN_MISSING%$MAX_PARALLEL"; GEN=$LAST; DEP="afterany:$GEN"
  fi
  submit eval-resume evaluate "$DEP" 4 16G 02:00:00 "0-29%10"; EVAL=$LAST
  submit summarize summarize "afterany:$EVAL" 1 2G 00:30:00
fi

# ------------------------------------------------------------------ proxy cleanup watcher (login02)
JOB_LIST="$(IFS=,; echo "${JOBS[*]}")"
nohup bash -c '
  while squeue -h -j "$1" 2>/dev/null | grep -q .; do sleep 60; done
  if tr "\0" " " < /proc/$2/cmdline 2>/dev/null | grep -q -- "--name $3"; then kill "$2"; echo "proxy $2 stopped $(date -Is)"; fi
' _ "$JOB_LIST" "$PROXY_PID" "$PROXY_NAME" >> "$RUN_DIR/logs/proxy-watcher.log" 2>&1 &
trap - EXIT

cat > "$RUN_DIR/LAUNCH.env" <<EOF
CODE_ROOT=$CODE_ROOT
ZEOSYN_PYTHON=$ZEOSYN_PYTHON
EOF
cat >> "$RUN_DIR/LAUNCH.log" <<EOF
$(date -Is) mode=$MODE commit=$(basename "$CODE_ROOT") jobs=$JOB_LIST proxy_pid=$PROXY_PID port=$PORT
EOF
say "submitted jobs: $JOB_LIST"
say "progress:  bash research/jobs/zeosyn/launch.sh --status $RUN_DIR"
say "when summary.json exists:  bash research/jobs/zeosyn/collect.sh $RUN_DIR && git push"
