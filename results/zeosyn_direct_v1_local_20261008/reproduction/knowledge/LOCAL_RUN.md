# 本地 KG / RAG 与 ZeoSyn 运行

工作目录：`C:\scientific_research\catalysis-research-platform`。

Release：`knowledge-zeolite-v1-20261008`；匹配代码：`3bfc543b8cc89439bfb76f0c6407f3d328ca8902`。
全部四个归档和 36 个文件已校验 SHA256。压缩包保存在 `.local-knowledge/knowledge-zeolite-v1-20261008/`，解压资产保存在 `knowledge/`；两处仅在本机忽略，不进入 Git。

## 快速连续查询（离线，无 GLM 调用）

在 PowerShell 中执行：

```powershell
.\.venv\Scripts\python.exe knowledge\run_local.py query --interactive
```

知识库和嵌入模型只加载一次，每个问题同时返回 RAG 与 KG+RAG 的证据包。输入空行退出。完整证据 JSON 写入 `.local-knowledge/knowledge-zeolite-v1-20261008/queries/`，每次查询保留独立文件。

只查询一种模式：

```powershell
.\.venv\Scripts\python.exe knowledge\run_local.py query --mode small_kg_rag_agent --query "How does OSDA molecular size influence zeolite framework selectivity?"
```

查询使用已冻结的 ZeoSyn 测试论文排除配置；495 个测试 DOI 中有 205 个出现在索引里，已经排除。所有证据仍受原来的每篇论文、条数和 token 预算约束。

## 本地正式实验

数据准备、测试论文排除、六个证据包与五个 seed 的 D0 已完成，保存在 `runs/zeosyn-local-v1-20261008/`。D0 mean accuracy = `0.43314415437003406`，macro-F1 = `0.31122416330749564`。

```powershell
.\.venv\Scripts\python.exe knowledge\run_local.py status
.\.venv\Scripts\python.exe knowledge\run_local.py run
```

`run` 会在终端隐藏提示输入 `ZHIPU_API_KEY`；也可以从当前终端环境读取该变量。密钥仅保留在内存中并传给子进程。默认连接 `https://open.bigmodel.cn/api/paas/v4`，如果使用自己的兼容端点，可设置 `ZHIPU_BASE_URL`。生成阶段会调用 GLM，产生 API 用量。

加速采用 5 条生成轨迹并行、随机森林 8 线程。完整配置保持每组 10 条、每条 3 轮、GLM-5.3-Flash high、原始五个 fit seed 和测试划分；没有减少科学预算。所有生成先完成并冻结，之后才评分。没有 NVIDIA CUDA GPU；检索和随机森林在 CPU 上运行，GLM 在 API 服务端运行，生成速度仍取决于服务端延迟与并发限制。

调整资源占用（不改变实验配置）：

```powershell
.\.venv\Scripts\python.exe knowledge\run_local.py run --workers 3 --rf-jobs 8
```

结果保存在 `runs/zeosyn-local-v1-20261008/`，包含 `prepared/`、`d0.json`、`generation/`、`evaluation/`、`summary.json` 和 `local-logs/`。已有生成与评分文件不会覆盖。启动器只调用官方 Python 入口，没有修改受 Git 跟踪的代码或配置。

当前使用已有 `.venv`，没有降级或重装依赖。实际版本见 `local-validation.json`；Release 的源服务器依赖版本见 `requirements-portable.txt`。如果要另建严格匹配的环境，请使用 Release README 的安装步骤。

## 资产目录

- RAG：`knowledge/rag/full-rag-v1-index/`
- KG：`knowledge/kg/Small-KG-zeolite-v1/`
- 归一化层：`knowledge/normalization/scientific-normalization-Small-KG-zeolite-v1.1/`
- 固定嵌入模型：`knowledge/cache/huggingface/`（384 维多语言 MiniLM，revision 与索引完全一致）

官方工具与许可文件：`.local-knowledge/knowledge-zeolite-v1-20261008/tools/`。
