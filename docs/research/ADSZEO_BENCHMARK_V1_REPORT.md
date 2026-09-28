# AdsZeo Benchmark v1：简化审计与三模式初步对比

> **状态：作废并归档（2026-09-28）。** v1 使用预定义描述符目录，属于闭合菜单选择任务，不是开放式模型假设生成。因此本文及其 v1–v4 历史比较不再作为当前 harness、知识模式或开放假设能力的证据；数值仅保留用于审计、故障定位和研究演进追溯。当前开放式结果见 [AdsZeo v5 报告](ADSZEO_V5_NOMINATION_REPORT.md) 和 [v5 单评分集协议](ADSZEO_V5_SINGLE_SCORE_PROTOCOL.md)。

> **2026-09-24 复核：三模式比较存在提示词预算混杂。** 共用的证据编号函数把含有空行的检索上下文误拆为多段，随后按检索条目数重复整段上下文。RAG 与 KG+RAG 实际收到的上下文可能被放大多倍，因此下文的模式排序及“预算完全一致”说法仅是历史记录，不能作为公平的知识模式比较结论。D0、数据审计和不依赖该提示词的 oracle 计算不受此问题影响。修复见 `research/src/catalysis_research/experiments/discovery_loop.py`；修复后的 v5 结果见 [v5 报告](ADSZEO_V5_NOMINATION_REPORT.md)。

状态日期：2026-09-18

运行分类：`EXPLORATORY_BENCHMARK_V1 / EXPLORATORY_NOT_CONFIRMATORY`

## 1. Benchmark 定义

- 数据：AdsZeo v1（`10.5281/zenodo.21445386`，CC BY 4.0），12.4 GB DuckDB，
  md5 `3d100a27429a0dc19708d22618990f56` 已校验；
- 任务：从预吸附框架结构特征预测 298 K 甲烷绝对吸附量（mol/kg framework），
  4775 个 Al 取代含钠沸石结构 × 191 种拓扑 × 13 个压力点（0.1–100 bar）；
- 泄漏控制：适配器永不查询 `positions`（12.4 亿行轨迹）与 `cycle_stats`（结果派生表），
  仅读取 structures、framework_atoms（Al 坐标）、runs、isotherms 的预吸附字段；
- Split：拓扑级 80/10/10（`sha256(seed:topology)` 排序，seed=20260902），
  同一拓扑的全部结构与压力点在同一分区，这是对未见拓扑的 OOD 评估；
- D0 基线：`log_pressure, framework_density, al_fraction, helium_void_fraction,
  cell_volume_per_t, cell_length_anisotropy`（6 个经典预吸附描述符）；
- 下游模型：HistGradientBoosting（log1p 目标，4 组超参在验证集按拓扑 macro-MAE 选一，
  D0+X 复用 D0 选定超参），test 指标为拓扑 macro-MAE（mol/kg）。

## 2. 简化审计结果（2026-09-18）

| 审计项 | 结果 |
| --- | --- |
| License | CC BY 4.0（Zenodo 记录 + README） |
| 数据完整性 | md5 与 Zenodo 一致；preflight 基数全过：4775 结构 / 191 拓扑 / 62075 runs / 62075 甲烷目标，无缺失压力点 |
| 语料泄漏 | AdsZeo 在冻结语料 `papers.jsonl`、`documents.jsonl` 中 0 命中（标题、DOI、zenodo ID 均无）——数据集 2026-07 发布，晚于语料冻结，无直接答案泄漏 |
| 检索 denylist | `github:Rachna-R/AdsZeo` 与 `doi:10.5281/zenodo.21445386` 记录在文档级 benchmark_exclusion；二者不在索引中，索引级仅排除非语料论文 `doi:10.1126/science.ads7290`（r2 配置修正了 9/3 原配置对不存在论文的 fail-closed 排除） |
| 目标泄漏 | D0+X 与 D0 使用同一 ML 管线与超参选择，descriptor 生成阶段不见任何行级标签或测试结果 |
| 索引完整性 | r2 配置通过 fail-closed 校验：6691 papers / 8927 documents / 365643 chunks |

已知限制：未做 benchmark 论文（AdsZeo 预印本）的逐句复述泄漏扫描；未复现原论文
native baseline（该数据集论文定义的是生成任务，未提供回归 benchmark，本任务的
D0/HGB 管线为项目自定义）；`structure_id` 数字部分不可用作 split（idx 后缀分布
退化：4473 个 `idx_0`），已改用拓扑级哈希 split。

## 3. 三模式 5 次重复结果

Slurm array 3691096（r4 作业脚本，LD_PRELOAD libstdc++ 修复计算节点 duckdb 1.5.5
加载），模型 `glm-5.3-flash`，thinking enabled / reasoning_effort low，
单次 1 轮假设 + 3 个新增 descriptor，预算与 prompt 三模式完全一致。

D0（全部重复共用）：拓扑 macro-MAE 0.23511，row RMSE 0.37152，row R² 0.9246。

| 模式 | 有效/总数 | MAE 改善均值 | MAE 改善范围 | 平均 tokens |
| --- | --- | ---: | --- | ---: |
| Agent | 4/5 | −0.97% | −3.52% ~ +3.60% | ~2,579 |
| RAG+Agent | 5/5 | −2.51% | −4.71% ~ −0.28% | ~48,036 |
| Small KG+RAG+Agent | 5/5 | −1.45% | −2.80% ~ −0.33% | ~41,004 |

（正值 = MAE 降低 = 改善；负值 = 变差。三模式均值均为负或近零，差异远小于
单次波动，不能区分任何模式。）

无效输出：Agent rep1 输出 descriptor 数量不符被严格校验拒绝（保留为固定预算下的
实验结果，不追加重试）。

Descriptor 选择频次（跨重复）：

- `al_per_void_volume`：Agent 4/4、RAG 5/5、Small KG+RAG 2/5；
- `void_volume_per_t`：Agent 3/4、RAG 3/5、Small KG+RAG 4/5；
- `al_close_pair_fraction_5a`：Small KG+RAG 4/5；
- `al_clustering_index`：RAG 2/5、Small KG+RAG 2/5。

## 4. 当前判断

1. 本轮证明 AdsZeo benchmark 三模式闭环端到端可运行，链路含：泄漏感知数据加载 →
   检索 → 假设 → descriptor 生成 → 同管线 D0 vs D0+X 验证。
2. 三模式间差异远小于重复间波动（模式均值差 ~1–2.5%，单次重复波动 ±3.5%），
   **不能据此宣称任何模式优于其他**。
3. 值得注意的负结果：所有 14 个有效 D0+X 组合中 12 个不优于 D0（HGB 在 4775×13
   数据上已接近该特征空间的性能上限，R² 0.9246），且新增 descriptor 与 D0 高度
   相关（都是 Al/孔隙率的函数），ML 端缺乏可挖掘的正交信息。
4. Small KG+RAG 的 row RMSE 在 5 次中 5 次低于 D0（0.362–0.371 vs 0.372），
   与拓扑 macro-MAE 方向不一致，提示以 row 指标做次要诊断时可能给出不同印象，
   正式结论必须只用预注册的拓扑 macro-MAE。
5. Agent 模式 rep1 的失败是 schema 违规（输出 2 个 descriptor 而非 3 个），
   与 Zeolite Atlas 轮次的 Agent 不稳定现象一致。

## 5. 下一步

1. 扩大重复到 ≥10 或加入 seed 扰动，把模式间差异与重复间波动区分开；
2. Descriptor 冗余审计：量化候选 catalog 与 D0 的相关性，考虑引入几何/拓扑类
   正交特征（环分布、孔径、环构成）扩展 catalog；
3. 引入 token-matched shuffled KG 对照，满足正式对比的 knowledge-structure 控制；
4. 将本报告与 r2 配置、r4 作业脚本回传 GitHub 仓库。

## 6. 可追溯信息

- 运行目录：`/public/home/xiaohe/lxf/catalysis-rag/runs/glm-discovery-adszeo-v1-3691096/`
- 作业脚本：`/tmp/adszeo-v1-replicates-r4.sbatch`（LD_PRELOAD 修复版）
- 检索配置：`code/releases/adszeo-v1-20260903/research/configs/retrieval/small-kg-hybrid-adszeo-v1-r2.json`
- Preflight 报告：`benchmarks/adszeo-v1/preflight/preflight-3690920.json`
- 数据：`benchmarks/adszeo-v1/AdsZeo_data.duckdb`（sha256 文件同目录）
- 环境：`envs/py312-rag`（+duckdb 1.5.5 wheel + LD_PRELOAD libstdc++.so.6.0.36）
