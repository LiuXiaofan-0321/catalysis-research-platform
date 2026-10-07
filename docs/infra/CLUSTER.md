# 集群调用外部 API（华东师大 HPC）

来源：华东师大 HPC 的计算节点调用外部 API 手册（登录 banner 链接，2026-09-24 核对）。

计算节点不能直接访问外网。API 请求必须经过同一集群账号在 **login02**（`59.78.189.133`）上启动的代理。代理绑定 `10.11.100.254`，端口在 `5000-5010` 中自动分配。**不能假定上次用过的端口仍然转发到同一个上游 API。**

`jobs/zeosyn/launch.sh` 已经自动完成下面的全部步骤（启动专用代理、读取端口、在计算节点上探测、所有作业结束后关闭代理），日常运行不需要手动操作。以下内容用于排查问题。

## 手动步骤

1. 在 login02 上启动专用代理。服务器上的 `tools/api_proxy_1800s.py` 是集群脚本的副本，只把上游超时从 60 秒改为 1800 秒（GLM 推理调用需要更长时间）。代理会转发作业请求中的 `Authorization` 头，**不要把 API key 写在代理命令行里**。

   ```bash
   BASE=/public/home/xiaohe/lxf/catalysis-rag
   nohup python -u "$BASE/tools/api_proxy_1800s.py" --target https://open.bigmodel.cn --name <run-name> \
     > "$BASE/logs/<run-name>-proxy.log" 2>&1 &
   grep '绑定地址' "$BASE/logs/<run-name>-proxy.log"
   ```

2. 使用**启动时打印的端口**。客户端 URL 必须包含且只包含一次 GLM API 路径：

   ```bash
   export ZHIPU_PROXY_BASE_URL="http://10.11.100.254:<port>/api/paas/v4"
   ```

   `GlmClient` 会自动追加 `/chat/completions`。代理会把收到的路径拼接到 `--target` 后面；如果 `--target` 写成 `https://open.bigmodel.cn/api/paas/v4`，再配合上面的 URL，路径会重复，返回 404。

3. 正式提交数组作业之前，先**在计算节点上**发一次真实的 GLM 请求，检查模型返回的内容，而不只是代理根路径返回 HTTP 200。代理根路径可能正常响应，但上游转发的却是别的 API。

## 已知故障

- 漏设 `ZHIPU_PROXY_BASE_URL`：计算节点无法解析 `open.bigmodel.cn`。
- 端口被其他用途占用：曾出现 5000 端口实际转发 PubChem，导致 GLM 请求返回 404。
- API key 只能放在进程或 Slurm 环境变量里，不能写进启动记录、归档或日志。所有作业结束后要关闭专用代理。
