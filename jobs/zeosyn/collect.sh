#!/usr/bin/env bash
# Copy a finished ZeoSyn run into results/ of this checkout.
#   bash jobs/zeosyn/collect.sh RUN_DIR [--partial] [--commit]
# --partial  collect a run whose summary.json is missing (for debugging a failure)
# --commit   also git-commit the copied folder (use where this checkout can push to GitHub)
# The cluster cannot reach GitHub: copy results/<folder> back to a local clone and commit there.
set -euo pipefail
RUN_DIR="${1:?RUN_DIR}"; shift
PARTIAL=0; COMMIT=0
for a in "$@"; do
  case "$a" in --partial) PARTIAL=1 ;; --commit) COMMIT=1 ;; *) echo "unknown option $a" >&2; exit 2 ;; esac
done
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[[ -f "$RUN_DIR/summary.json" || "$PARTIAL" == 1 ]] || { echo "summary.json missing; use --partial to collect anyway" >&2; exit 1; }
NAME="zeosyn_direct_v1_$(basename "$RUN_DIR" | sed 's/^zeosyn-direct-v1-//')"
DEST="$REPO/results/$NAME"
mkdir -p "$DEST/prepared" "$DEST/logs"
for f in config.json data-manifest.json tasks.json retrieval-config.json knowledge.json; do
  if [[ -f "$RUN_DIR/prepared/$f" ]]; then cp "$RUN_DIR/prepared/$f" "$DEST/prepared/"; fi
done
for f in d0.json api-probe.json summary.json; do
  if [[ -f "$RUN_DIR/$f" ]]; then cp "$RUN_DIR/$f" "$DEST/"; fi
done
if [[ -f "$RUN_DIR/LAUNCH.log" ]]; then cp "$RUN_DIR/LAUNCH.log" "$DEST/LAUNCH.txt"; fi  # *.log is gitignored
for d in generation evaluation; do
  if [[ -d "$RUN_DIR/$d" ]]; then mkdir -p "$DEST/$d"; cp "$RUN_DIR/$d"/*.json "$DEST/$d/" 2>/dev/null || true; fi
done
# Slurm job logs only; proxy logs are not copied.
find "$RUN_DIR/logs" -maxdepth 1 -name 'zeosyn-*' \( -name '*.out' -o -name '*.err' \) -exec cp {} "$DEST/logs/" \;
BASE="${BASE:-/public/home/xiaohe/lxf/catalysis-rag}"
KEY="${ZHIPU_API_KEY:-$(tr -d '[:space:]' < "${ZHIPU_KEY_FILE:-$BASE/.secrets/zhipu_api_key}" 2>/dev/null || true)}"
if { [[ -n "$KEY" ]] && grep -rqsF -- "$KEY" "$DEST"; } || grep -rqs "Bearer " "$DEST"; then
  rm -rf "$DEST"; echo "credential-like text found in the run; nothing collected" >&2; exit 1
fi
(cd "$REPO/results" && tar -czf "$NAME.tar.gz" "$NAME")
echo "collected $DEST"
echo "archive   $REPO/results/$NAME.tar.gz  (download this, extract into results/ of a local clone)"
if [[ "$COMMIT" == 1 ]]; then
  (cd "$REPO" && git add "results/$NAME" && git commit -m "results: ZeoSyn direct-v1 run $(basename "$RUN_DIR")" -- "results/$NAME")
  echo "committed results/$NAME; now run: git push"
fi
