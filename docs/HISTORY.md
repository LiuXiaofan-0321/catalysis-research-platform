# 历史研究线（2026-08 至 2026-10）

下列研究线的代码、配置、Slurm 脚本、完整轨迹和报告都已从 main 移除，但完整保存在 tag **`archive/full-2026-10-07`** 中。

```bash
git show archive/full-2026-10-07:docs/research/JACS_AU_DIRECT_V5_RESULTS_20261005.md   # 查看某个旧文件
git checkout archive/full-2026-10-07 -- research/reports/jacs_au_direct_v5_20261005   # 把旧目录恢复到工作区
```

存档中的文件路径都是重组前的旧路径（`research/...`、`docs/research/...`）。

## 知识库建设（2026-08）

结果仍在使用，即服务器上的 Small KG 和 RAG 索引，说明见 [infra/KNOWLEDGE_BASE.md](infra/KNOWLEDGE_BASE.md)。

- 先做了 ACS 50 篇论文的 RAG 试点，以及 GLM-5.3-Flash 三篇论文的结构化抽取试跑，随后分三批抽取 6,691 篇分子筛论文（8,927 份主文/SI）。
- `full-rag-v1-index` 检索审计：3 个预注册问题中严格通过 1 个。
- 归档文档：`ACS_50_RAG_PILOT_REPORT.md`、`GLM53_FLASH_EXTRACTION_PILOT*.md`、`FULL_RAG_RETRIEVAL_AUDIT.md`、`LITERATURE_PIPELINE_UPGRADE.md`。

## TheMeCat、Zeolite Atlas（2026-08 至 09）

- TheMeCat + DeepSeek 只用于跑通流程，后来退出 benchmark 候选。
- Zeolite Atlas（Materials Cloud，1000 个结构，预测能量/体积，统一用 Ridge）：Agent、RAG、KG+RAG 三组都跑通了“证据 → 假设 → 3 个描述符”，结论为 `EXPLORATORY_NOT_CONFIRMATORY`。

## AdsZeo v1–v5（2026-09）

- 预测 4,775 个铝取代沸石的甲烷吸附量，按拓扑划分训练/测试。v1–v4 的做法是从预设的描述符目录里选择，v5 改为开放式公式提名（3 轮 × 3 个公式，保留验证集上有提升的）。
- 审计发现证据编号函数有 bug，会把 RAG/KG 的上下文重复多遍，v1–v4 及 v5 首批的组间比较因此作废。
- v5 修正批次（10 次重复）在测试集上：Agent −1.96%，RAG +0.25%，KG+RAG −0.21%，三组的区间都跨 0。
- 教训：D0 是我们自己设计的，不是原论文的；描述符目录与 D0 高度共线。

## JACS Au 吸附熵（2026-09-28 至 10-05）

- 原论文 14 项 D0 加原生 ANN，公开权重复现 MAE 0.567R。

| 版本 | 协议 | Agent | RAG | KG+RAG | 说明 |
|---|---|---:|---:|---:|---|
| V1 | 3 轮 × 3 候选，按评分择优 | +6.24% | +5.79% | +5.86% | 只有 6/90 个候选引用了 KG |
| V2 | 改进图关系 | — | — | — | 漏排了原论文正文/SI，结果被污染，作废 |
| V3 | 修复来源排除、图去重 | +6.61% | +2.18% | +5.55% | |
| V4 high | 同上，3×3 择优 | 6.98% | 6.42% | 7.16% | KG 只比 Agent 高约 0.175 个百分点 |
| V5 | 每轮直接加入 1 个，无标签，5 个 seed | 0.776% | 0.428% | 0.926% | 差值区间跨 0；90 个槽只成功加入 54 个 |

- V5 的主要问题：
  - `proxy_assumptions` 字段的列表/字符串接口不兼容，导致 21 个槽失败，其中知识组占 18 个；
  - 单个 seed 就能改变组间排序（seed 内的标准差约 2.8 个百分点）；
  - 成功加入的公式大多是 D0 内部的几何比值，各组之间高度重合。
- 结论：这个任务只能对已有的 14 列重新组合，没有新信息进入模型；LLM 自身先验已经足够，所以知识组不可能显示出优势。改用 ZeoSyn 的原因就在这里。

## ZeoDiff（2026-09-29）

- Nature Communications 2026 的烷烃扩散工作：原生 9 项 D0，公开权重回放得到 R² 0.914。完成了数据审查，暂缓开展实验。

## Jev / harness（2026-09）

- 多角色审查和 Jev 调度的离线框架，已暂缓，设计见 `HARNESS_VNEXT_DESIGN.md`。

## 其他已移除的内容

- K20–K100 热催化嵌套 KG 和 K247 光催化 KG 快照（同一语料内的数量消融），热催化 Stage-1 语料。
- 通用的数据集注册、划分、泄漏审计和 Run Manifest 工具，以及 `research.py` 命令行。知识库相关的命令现在由 `scripts/knowledge.py` 提供。
- 网页平台（backend、frontend、数据包、部署文档）：已迁移到 [catalysis-web](https://github.com/LiuXiaofan-0321/catalysis-web)，并保留了它的提交历史。
