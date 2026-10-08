# 当前进展

本文件只保留一份，有进展时直接修改，不再另建带日期的进度文档。最后更新：2026-10-09。

## 已完成：ZeoSyn V1

协议：[experiments/ZEOSYN_V1.md](experiments/ZEOSYN_V1.md)。结果：`results/zeosyn_direct_v1_local_20261008/`（2026-10-08 在台式机上完成）。

- 原论文 D0 + RandomForest 已精确复现：准确率 0.7358361774744028，与作者 notebook 逐位一致。
- 主实验按 DOI 分组划分，测试集 D0 准确率 43.31%。三组各 10 条轨迹，90 个槽位全部成功加入描述符。
- 相对 D0 的准确率增益：**Agent +0.54**，RAG +0.10，KG+RAG +0.17 个百分点。RAG−Agent 和 KG−Agent 的区间都不跨 0，即知识组显著低于 Agent。
- 在开发集上复查，排序相同（Agent > KG+RAG > RAG），说明这不是偶然现象。
- 原因分析见 [experiments/ZEOSYN_V2_PLAN.md](experiments/ZEOSYN_V2_PLAN.md) 第一节：固定检索词把知识组带向同一类公式、检索质量低、KG 结构对模型不可见、提示词要求“依据证据”，以及知识没有提供模型缺少的信息。

## 下一步：ZeoSyn V2

方案：[experiments/ZEOSYN_V2_PLAN.md](experiments/ZEOSYN_V2_PLAN.md)。**尚未实施。**

- 目标：H1 Agent > D0（V1 已观察到）；H2（主假设）KG > Agent；H3（次要）KG > RAG。
- 核心改动：为 KG 建立文献统计特征通道；模型自主决定检索内容；KG 以可读的汇总事实呈现；加入打乱 KG 对照。
- 第一个关卡：在台式机上做 KG 实体链接的可行性探测，训练集配方覆盖率 ≥ 40% 才继续。
- 从现在起，设计调整只在开发集上评估；V1 的测试集只在 V2 协议冻结后再评估一次。

## 待决定事项

见 V2 方案第六节：是否接受文献特征通道、时间截断的定位、主指标、每组轨迹数、是否加相同事实平铺对照。

## 运行环境

- 华东师大集群：系统 Git 1.8.3，不能访问 GitHub，队列拥挤，流程见根目录 `AGENTS.md`。
- 台式机（R7-9700X）：V1 在这里完成。凡是需要载入 KG 或 RAG 的步骤，都在这里运行。
- 知识库已作为 GitHub release `knowledge-zeolite-v1-20261008` 发布（RAG、Small KG、归一化 overlay、embedding 模型，均有 SHA256 校验）。

## 之后的计划

1. ZeoSyn V2（上面）。
2. 第二个 benchmark：OCM（北海道大学 CADS 公开数据；Schmack 2019 的专家结论可作为“重新发现”评测）。需要先建 OCM/氧化物领域的知识库。
3. 按目标任务定义 Small/Medium/Large KG：建一个带领域标签的并集 KG，按任务过滤，并在数量匹配的条件下比较。
4. 投稿前补充不使用领域知识的 baseline（CAAFE、LLM-FE 等 LLM 特征工程方法）。
