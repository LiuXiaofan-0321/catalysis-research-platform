# 当前进展

本文件只保留一份，有进展时直接修改，不再另建带日期的进度文档。最后更新：2026-10-09。

## 已完成：ZeoSyn V1

结果与机制分析：[experiments/ZEOSYN_V1_RESULTS.md](experiments/ZEOSYN_V1_RESULTS.md)。Agent +0.54 pp，RAG +0.10，KG+RAG +0.17；知识条件显著低于 Agent，开发集复查排序相同。

## 进行中：ZeoSyn V2（运行前的工作已完成，尚未正式运行）

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
- 冒烟测试中的发现（详见开发日志）：KG 组目前没有主动使用文献特征；在冒烟配置下，只加文献特征带来的提升很小。完整开发集运行会用分层诊断来检验。

## 下一步

1. 在台式机上按运行手册跑开发集第 1 轮，把结果推送到 GitHub。
2. 根据开发集结果决定预注册中待确认的事项：主指标、每组轨迹数、是否加平铺对照、LLM 不使用文献特征时的处理方式。
3. 冻结协议，在测试集上做唯一一次正式评估。

## 运行环境

- 台式机（R7-9700X）：V1、V2 都在这里运行。凡是需要载入 KG 或 RAG 的步骤都在这里做。
- 华东师大集群：系统 Git 1.8.3，不能访问 GitHub，队列拥挤；V1 的流程见根目录 `AGENTS.md`。
- 知识库已作为 GitHub release `knowledge-zeolite-v1-20261008` 发布，各文件均有 SHA256 校验。

## 之后的计划

1. 第二个 benchmark：OCM（北海道大学 CADS 公开数据；Schmack 2019 的专家结论可作为“重新发现”评测）。
2. 按目标任务定义 Small/Medium/Large KG，在数量匹配的条件下比较。
3. 投稿前补充不使用领域知识的 baseline（CAAFE、LLM-FE）。
