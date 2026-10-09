# ZeoSyn V2 台式机运行手册

适用于 Windows 台式机（V1 就在这台机器上运行）。命令以 PowerShell 为例；Linux 下把 `$env:X = "..."` 换成 `export X=...`，把反引号换行换成 `\` 即可。所有命令都在仓库根目录执行。

## 0. 一次性准备

1. 拉取代码：`git checkout main; git pull`。
2. Python 3.11 或更高版本。安装依赖：`pip install -e ".[knowledge,test]"`，并安装 CPU 版 PyTorch。不需要 RDKit 和 Java，KG 层已经构建好并随仓库提供。
3. 知识库沿用 V1 时下载的 release `knowledge-zeolite-v1-20261008`。把下面三个路径换成你本机的实际位置：

   ```powershell
   $RAG = "D:\knowledge\rag\full-rag-v1-index"
   $OVERLAY = "D:\knowledge\normalization\scientific-normalization-Small-KG-zeolite-v1.1"
   $env:HF_HOME = "D:\knowledge\cache\huggingface"; $env:HF_HUB_OFFLINE = "1"
   ```

4. 运行测试：`python -m pytest -q`，应当全部通过。
5. 每次运行前设置 GLM key：`$env:ZHIPU_API_KEY = "<key>"`。key 不要写进任何文件。

## 1. 开发集运行（第 1 轮）

```powershell
$RUN = "runs\zeosyn-v2-dev-1"
python scripts/run_zeosyn_v2.py prepare --split dev --run-dir $RUN `
  --reuse-matrices results/zeosyn_direct_v1_local_20261008/prepared/matrices.npz `
  --reuse-matrices-manifest results/zeosyn_direct_v1_local_20261008/prepared/data-manifest.json
python scripts/run_zeosyn_v2.py prepare-rag --run-dir $RUN --rag-index $RAG
python scripts/run_zeosyn_v2.py generate --run-dir $RUN --rag-index $RAG --overlay $OVERLAY --workers 5
python scripts/run_zeosyn_v2.py evaluate --run-dir $RUN --hgb
python scripts/run_zeosyn_v2.py audit-retrieval --run-dir $RUN --rag-index $RAG --overlay $OVERLAY --modes rag kg --output $RUN\retrieval-audit.json
python scripts/run_zeosyn_v2.py direct-answer-audit --run-dir $RUN
python scripts/run_zeosyn_v2.py summarize --run-dir $RUN
python scripts/run_zeosyn_v2.py collect --run-dir $RUN --name zeosyn_v2_dev_1
git add results/zeosyn_v2_dev_1; git commit -m "results: ZeoSyn V2 dev iteration 1"; git push
```

说明：
- `--reuse-matrices` 复用 V1 的数据矩阵。它和 V1 的划分完全相同，会先按 hash 校验；也可以去掉这两个参数，现场重新计算（较慢，峰值内存约 2 GB）。
- `generate` 可以断点续跑：中途因网络或 API 出错时，重新执行同一条命令，只会补跑缺失的轨迹，已完成的不会重跑。
- 只想先跑部分组时，可以加 `--modes agent kg` 或 `--replicates 1-3`。
- 估计耗时：生成约 40 条轨迹 × 6 次调用，5 个并发，约 40–60 分钟；RandomForest 评分约 1 小时；HGB 敏感性分析约 1–2 小时，可以加 `--hgb` 留到最后再跑。
- 峰值内存：RAG 组生成时需要载入 RAG 索引，约 4–6 GB；其他步骤都在 2 GB 以内。每个命令结束时会打印峰值内存（Windows 下不打印）。

## 2. 开发集结果讨论

开发集结果推送后，先看以下内容，再决定是否需要第 2、3 轮开发迭代（最多 3 轮，每轮记入 `ZEOSYN_V2_ITERATIONS.md`）：
- `summary.json` 里的 `contrasts.kg-agent`，以及打乱 KG 的对照；
- 只加文献特征的分层结果；
- KG 组使用文献特征的比例；
- 检索审计的相关率。

关卡 2：最后一轮开发集上 KG 没有优于 Agent，就不做测试集正式评估。

## 3. 冻结协议

1. 把 `docs/experiments/ZEOSYN_V2_PREREG.md` 中所有 “TO BE CONFIRMED” 改成确定的内容，并把最终设置同步到 `configs/experiments/zeosyn-v2.json`（例如每组轨迹数、实验组列表）。
2. 执行 `python scripts/run_zeosyn_v2.py freeze`，然后提交配置文件和预注册文档并推送。此后这两个文件不能再改。

## 4. 测试集正式运行（只做一次）

```powershell
$RUN = "runs\zeosyn-v2-test"
python scripts/run_zeosyn_v2.py prepare --split test --run-dir $RUN `
  --reuse-matrices results/zeosyn_direct_v1_local_20261008/prepared/matrices.npz `
  --reuse-matrices-manifest results/zeosyn_direct_v1_local_20261008/prepared/data-manifest.json
python scripts/run_zeosyn_v2.py prepare-rag --run-dir $RUN --rag-index $RAG
python scripts/run_zeosyn_v2.py generate --run-dir $RUN --rag-index $RAG --overlay $OVERLAY --workers 5
python scripts/run_zeosyn_v2.py evaluate --run-dir $RUN --confirmatory --hgb
python scripts/run_zeosyn_v2.py audit-retrieval --run-dir $RUN --rag-index $RAG --overlay $OVERLAY --modes rag kg --output $RUN\retrieval-audit.json
python scripts/run_zeosyn_v2.py direct-answer-audit --run-dir $RUN
python scripts/run_zeosyn_v2.py summarize --run-dir $RUN
python scripts/run_zeosyn_v2.py collect --run-dir $RUN --name zeosyn_v2_test
git add results/zeosyn_v2_test; git commit -m "results: ZeoSyn V2 confirmatory test"; git push
```

测试集评估必须带 `--confirmatory`，并且协议已经冻结、预注册文档的 hash 与配置一致，否则会拒绝运行。

## 5. 重新构建 KG 层（一般不需要）

只有修改了实体链接规则，才需要重新构建。这一步需要 RDKit 和 Java（`pip install rdkit jdk4py`，OPSIN 2.8.0 jar 从 GitHub release 下载）：

```powershell
python scripts/run_zeosyn_v2.py build-kg --kg-dir D:\knowledge\kg\Small-KG-zeolite-v1 --opsin-jar <opsin.jar> --java <java路径> --pubchem cache
python scripts/run_zeosyn_v2.py probe
python scripts/run_zeosyn_v2.py rag-allowlist --rag-index $RAG
```

重新构建后会产生新的 `data/kg_zeolite_v1/manifest.json`。所有已经准备好的运行目录都会因为 hash 变化而拒绝继续，需要重新执行 `prepare`。
