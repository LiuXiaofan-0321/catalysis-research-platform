# 当前进展

本文件只保留一份，有进展时直接修改，不再另建带日期的进度文档。最后更新：2026-10-10。

## 已完成：ZeoSyn V1

结果与机制分析：[experiments/ZEOSYN_V1_RESULTS.md](experiments/ZEOSYN_V1_RESULTS.md)。Agent +0.54 pp，RAG +0.10，KG+RAG +0.17；知识条件显著低于 Agent，开发集复查排序相同。

## 进行中：ZeoSyn V2（开发集第 1 轮已完成，测试集未评估）

- 方案：[experiments/ZEOSYN_V2_PLAN.md](experiments/ZEOSYN_V2_PLAN.md)；预注册草稿：[experiments/ZEOSYN_V2_PREREG.md](experiments/ZEOSYN_V2_PREREG.md)；开发日志：[experiments/ZEOSYN_V2_ITERATIONS.md](experiments/ZEOSYN_V2_ITERATIONS.md)；运行手册：[experiments/ZEOSYN_V2_RUNBOOK.md](experiments/ZEOSYN_V2_RUNBOOK.md)。
- **关卡 1 通过**：KG 中 4,656 条合成实验链接到 161 种 ZeoSyn OSDA，训练集配方覆盖率 53.9%。
- 已实现：
  - KG 合成知识层和文献特征（含本文排除、评估论文排除、时间截断版和外部版）；
  - 打乱 KG 对照、相同事实平铺对照；
  - 模型自主检索的三步流程，KG 证据以可读形式呈现；
  - RAG 合成白名单（47,440 个文本块）；
  - 开发集 / 测试集划分，测试集需协议冻结后才能评估；
  - 分层、只加文献特征、HGB、检索审计、直接答案审计等分析；
  - 台式机运行脚本。

  测试 84 项全部通过；Agent 和各 KG 组在开发集上的端到端冒烟测试已跑通（不计入结果）。
- **开发集第 1 轮已完成**（`results/zeosyn_v2_dev_1/`，分析见开发日志“第 1 轮”）：
  - 准确率相对 D0：Agent +0.19，RAG +0.18，KG +0.00，打乱 KG +0.07（百分点），区间全部跨 0。H1、H2 都不成立。
  - 所有组都没有使用文献特征（0/30）。只加文献特征 −0.03。
  - KG 检索相关率 64.4%，RAG 52.0%。
  - 原因诊断：按论文划分时，KG 能补充新信息的验证配方只有 0.5%；新 OSDA 留出时，KG 只覆盖少数高频 OSDA，而且不含凝胶组成。

## 下一步

开发集第 1 轮之后暂停，测试集未评估，预注册未冻结。

2026-10-10 完成了对整个框架的诊断和 V3 方案：[experiments/ZEOSYN_V3_PLAN.md](experiments/ZEOSYN_V3_PLAN.md)（上限分析见 [experiments/zeosyn_v3_ceiling/REPORT.md](experiments/zeosyn_v3_ceiling/REPORT.md)）。核心判断：公式再表达通道的上限约 0.5 pp；按 OSDA 留出并以“合成记录 KG × 原生 RF”合并，可达 +11 到 +14 pp；KG 需按合成记录重建。

## 运行环境

- 台式机（R7-9700X）：V1、V2 都在这里运行。凡是需要载入 KG 或 RAG 的步骤都在这里做。
- 华东师大集群：系统 Git 1.8.3，不能访问 GitHub，队列拥挤；V1 的流程见根目录 `AGENTS.md`。
- 知识库已作为 GitHub release `knowledge-zeolite-v1-20261008` 发布，各文件均有 SHA256 校验。

## 之后的计划

1. 第二个 benchmark：OCM（北海道大学 CADS 公开数据；Schmack 2019 的专家结论可作为“重新发现”评测）。
2. 按目标任务定义 Small/Medium/Large KG，在数量匹配的条件下比较。
3. 投稿前补充不使用领域知识的 baseline（CAAFE、LLM-FE）。
