# Cluster access to external APIs

Source: ECNU HPC's [计算节点调用外部 API manual](http://59.78.189.195/#s/ECM6xlXC), linked from the login banner (checked 2026-09-24).

Compute nodes do not have direct internet access. API calls must go through a proxy started under the same cluster account on **login02** (`59.78.189.133`). The service binds to `10.11.100.254` and automatically selects an available port in `5000-5010`. Do not assume that a previously used port still serves the same upstream API.

## GLM workflow for AdsZeo

1. On login02, start a dedicated proxy. The server already has `tools/api_proxy_300s.py`, a copy of the cluster script whose only change is the upstream request timeout from 60 to 300 seconds. The longer timeout is needed for GLM reasoning calls. The script forwards the job's `Authorization` header; do not put the API key in the proxy command line.

   ```bash
   BASE=/public/home/xiaohe/lxf/catalysis-rag
   nohup python -u "$BASE/tools/api_proxy_300s.py" \
     --target https://open.bigmodel.cn \
     --name adszeo-v5-glm \
     > "$BASE/logs/adszeo-v5-glm-proxy.log" 2>&1 &
   grep '绑定地址' "$BASE/logs/adszeo-v5-glm-proxy.log"
   ```

2. Use the **port printed at startup**. With this target, the client URL must include the GLM API path exactly once:

   ```bash
   BASE=/public/home/xiaohe/lxf/catalysis-rag
   export ZHIPU_PROXY_BASE_URL="http://10.11.100.254:<allocated-port>/api/paas/v4"
   export ZHIPU_API_KEY="<load from a private credential source>"
   export CODE_ROOT="<versioned AdsZeo code release>"
   sbatch --export=ALL,CODE_ROOT="$CODE_ROOT" \
     "$CODE_ROOT/research/literature_pipeline/jobs/adszeo-v5-nomination.sbatch"
   ```

   The `GlmClient` appends `/chat/completions`. The proxy appends the incoming path to its `--target`; using `--target https://open.bigmodel.cn/api/paas/v4` **and** the URL above would duplicate the path and return 404.

3. Before a full array, run a small GLM request **on a compute node** through the selected proxy. Check the model response, not just an HTTP 200 from the proxy root. The proxy can respond at `/` even when its upstream is a different API. With `BASE`, `CODE_ROOT`, `ZHIPU_API_KEY`, and `ZHIPU_PROXY_BASE_URL` already set in the submitting shell:

   ```bash
   srun --partition=cpu_192G --nodes=1 --ntasks=1 --cpus-per-task=1 \
     --mem=2G --time=00:03:00 \
     env PYTHONPATH="$CODE_ROOT/research/src" "$BASE/envs/py312-rag/bin/python" -c \
     'from catalysis_research.models.glm import GlmClient; r=GlmClient(retries=0).chat_json(model="glm-5.3-flash", system="Return JSON only.", user="Return a JSON object with ok set to true.", max_tokens=128, thinking="enabled", reasoning_effort="low"); print(r.model, r.structured.get("ok"))'
   ```

   Keep the API key in the Slurm environment, never in a repository file or command argument. When all runs finish, stop the dedicated proxy as the cluster manual requests.

The first v5 array (`3739039`) failed because it lacked `ZHIPU_PROXY_BASE_URL`; compute nodes could not resolve `open.bigmodel.cn`. A follow-up connectivity probe reached port 5000, but that port then served PubChem and returned 404 to GLM. These were connectivity failures, not scientific outcomes. The v5 Slurm script now requires `ZHIPU_PROXY_BASE_URL` at startup.

The cluster manual also specifies the login02 requirement, automatic port allocation, account-level access control, and `10.11.100.254` as the only supported service address. Recheck the manual if the cluster changes its proxy policy.

## JACS Au V4 low/high (2026-09-30)

Use a separate `tools/api_proxy_1800s.py` copy, changing only the old upstream `timeout=300` to `timeout=1800`. Preserve the original. Start on login02 with the run directory name as `--name`, record PID and printed port, and use the same `/api/paas/v4` client path above. High's client waits 1800 seconds; low waits 600 seconds. The V4 probe tests both full configured payloads on a compute node before the array.

The cleanup watcher waits for preflight, probe, array and summary to terminate. Before signaling it checks the owner, exact run name, and `api_proxy_300s.py` or `api_proxy_1800s.py` suffix. Credentials stay in process/Slurm environment, never launch records, archives or logs. See [V4 protocol](JACS_AU_KG_V4_LOW_HIGH_20260930.md).
