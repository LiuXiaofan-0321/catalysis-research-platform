# Instructions for coding agents running experiments on the cluster

These rules apply to Codex or any other agent operating this repository on the
ECNU cluster (`/public/home/xiaohe/lxf/catalysis-rag`). The agent's job is to
**run and report**, not to change science.

## Allowed

Only these commands, from the repository root, on **login02**:

```bash
git pull                                     # update to the branch you were told to use
bash jobs/zeosyn/launch.sh --dry-run         # checks only
bash jobs/zeosyn/launch.sh                   # submit a new run (prints RUN_DIR)
bash jobs/zeosyn/launch.sh --status RUN_DIR  # progress
bash jobs/zeosyn/launch.sh --resume RUN_DIR  # only if --status lists missing tasks
bash jobs/zeosyn/collect.sh RUN_DIR          # after summary.json exists
git push                                     # push the commit made by collect.sh
```

Read-only inspection (`cat`, `ls`, `tail`, `squeue`, `sacct`) is always fine.

## Forbidden

- Do not edit, create or delete any file in the repository (code, configs,
  data, docs, tests). `launch.sh` refuses to run with uncommitted code changes.
  The only files added to the repository are the ones `collect.sh` copies into
  `results/` and commits.
- Do not "fix" a failing stage by changing code, thresholds, seeds, queries,
  splits, models or retries. Stop and report instead.
- Do not rerun, delete or overwrite finished generations or evaluations to
  obtain a different result. Failed slots, zero-append and negative
  trajectories are results and must be kept.
- Do not start a second run because the first one looks bad.
- Never print, log, commit or paste the API key. It is read from
  `$ZHIPU_API_KEY` or `/public/home/xiaohe/lxf/catalysis-rag/.secrets/zhipu_api_key`.

## When something fails

Report, without modifying anything:

1. the exact command and its full error output;
2. `bash jobs/zeosyn/launch.sh --status RUN_DIR`;
3. `sacct -j <job ids from RUN_DIR/LAUNCH.log> --format=JobID,JobName,State,ExitCode,Elapsed,MaxRSS`;
4. the last 50 lines of the relevant `RUN_DIR/logs/zeosyn-*.err` and `.out` files.

If only some generation tasks are missing because of API/network errors
(the job log shows `GlmError`), `--resume RUN_DIR` is allowed once. If the
`knowledge`, `prepare` or `baseline` stage fails, do not resume; report.

If the run finishes, run `collect.sh RUN_DIR` and `git push`, then report the
commit hash and the `per_mode` block of `summary.json`.
