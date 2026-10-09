# Instructions for coding agents running experiments

Two setups exist: the ZeoSyn V1 cluster workflow (below) and the ZeoSyn V2 desktop
workflow (section "ZeoSyn V2 on the desktop" at the end). The rules apply to Codex or
any other agent operating this repository, for V1 on the
ECNU cluster (`/public/home/xiaohe/lxf/catalysis-rag`, login node `login2`,
also reachable as login02 / 59.78.189.133). The agent's job is to
**run and report**, not to change science.

## Workflow

The cluster cannot reach GitHub, so code goes up as a snapshot and results come
back as an archive.

1. **Local machine:** `git checkout main && git pull`. Make a fresh shallow clone
   of `main` (it must include `.git`), upload it to
   `$BASE/code/catalysis-research-<first 12 characters of the commit>/` and check
   that `git rev-parse HEAD` there prints the same commit. Never edit it on the server.
2. **Cluster, from that directory, on login2:**

   ```bash
   bash jobs/zeosyn/launch.sh --dry-run         # checks only; must end with "dry run: all checks passed"
   bash jobs/zeosyn/launch.sh                   # submit a new run (prints RUN_DIR)
   bash jobs/zeosyn/launch.sh --status RUN_DIR  # progress
   bash jobs/zeosyn/launch.sh --resume RUN_DIR  # only if --status lists missing tasks
   bash jobs/zeosyn/collect.sh RUN_DIR          # after summary.json exists
   ```

3. **Local machine:** download `results/<name>.tar.gz` printed by `collect.sh`,
   extract it into `results/` of the local clone, then
   `git add results/<name> && git commit -m "results: <name>" && git push`.

Read-only inspection (`cat`, `ls`, `tail`, `squeue`, `sinfo`, `sacct`, `git log`,
`git status`) is always fine.

## Forbidden

- Do not edit, create or delete any file in the repository (code, configs,
  data, docs, tests), locally or on the server. `launch.sh` refuses to run with
  uncommitted code changes. The only files added are the `results/` folders
  produced by `collect.sh`.
- Do not work around a failing check with environment overrides
  (`ALLOW_NON_LOGIN02`, `LD_PRELOAD`, `PYTHONPATH`, another Python environment)
  or by changing code, thresholds, seeds, queries, splits, models or retries.
  Stop and report instead.
- Do not rerun, delete or overwrite finished generations or evaluations to
  obtain a different result. Failed slots, zero-append and negative
  trajectories are results and must be kept.
- Do not start a second run because the first one looks bad.
- Never print, log, commit or paste the API key. It is read from
  `$ZHIPU_API_KEY` or `/public/home/xiaohe/lxf/catalysis-rag/.secrets/zhipu_api_key`.

## When something fails

Report, without modifying anything:

1. the exact command and its full error output;
2. `bash jobs/zeosyn/launch.sh --status RUN_DIR` (if a run was submitted);
3. `sacct -j <job ids from RUN_DIR/LAUNCH.log> --format=JobID,JobName,Partition,State,ExitCode,Elapsed,MaxRSS,Reason`;
4. the last 50 lines of the relevant `RUN_DIR/logs/zeosyn-*.err` and `.out` files;
5. for jobs that stay pending: `squeue -u $USER -o '%.12i %.20j %.8T %.10M %R'` and
   `sinfo -p cpu_96G,cpu_192G`.

If only some generation tasks are missing because of API/network errors
(the job log shows `GlmError`), `--resume RUN_DIR` is allowed once. If the
`knowledge`, `prepare` or `baseline` stage fails, do not resume; report.

When the run finishes, collect and push the results as in step 3, then report
the commit hash and the `per_mode` block of `summary.json`.

## ZeoSyn V2 on the desktop

Follow `docs/experiments/ZEOSYN_V2_RUNBOOK.md` exactly; it lists every allowed
command (`scripts/run_zeosyn_v2.py` prepare, prepare-rag, generate, evaluate,
audit-retrieval, direct-answer-audit, summarize, status, collect) and the
`git add/commit/push` of the collected `results/` folder. In addition to the rules above:

- Development runs use `--split dev`. Never prepare, generate or evaluate
  `--split test` unless the user says the protocol has been frozen; never pass
  `--confirmatory` on your own.
- Never run `build-kg`, `rag-allowlist` or `freeze`, and never edit
  `docs/experiments/ZEOSYN_V2_PREREG.md` or `configs/experiments/zeosyn-v2.json`.
- If `generate` stops with API/network errors, rerunning the same command is
  allowed (it only fills in missing trajectories). Any other failure: stop and
  report the command, its full output and `run_zeosyn_v2.py status --run-dir RUN`.
