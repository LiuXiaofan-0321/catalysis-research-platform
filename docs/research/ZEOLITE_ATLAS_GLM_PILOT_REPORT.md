# Zeolite Atlas 三模式探索性评测报告

## 结论

第一轮 benchmark 已从弃用的 TheMeCat 切换为 Materials Cloud Zeolite Atlas v1：

- 数据来源：`10.24435/materialscloud:2019.0079/v1`；
- 许可证：CC BY 4.0；
- 数据规模：1000 个结构、52686 个 Si 原子；
- 预测目标：结构级 energy 和 volume；
- 模型：`glm-5.3-flash`，`thinking=enabled`，`reasoning_effort=low`；
- 对比模式：`Agent / RAG+Agent / Small KG+RAG+Agent`；
- 作业：Slurm `3579959`，`COMPLETED`，耗时 4 分 56 秒；
- 结果分类：`EXPLORATORY_NOT_CONFIRMATORY`。

三个模式均完成了“证据链 -> 假设 -> 3 个新增描述符 -> 同一 Ridge ML 流水线”流程，
且使用相同 prompt、检索预算、descriptor 数量、split 和超参数搜索预算。

## 探索性结果

| 模式 | 新增描述符 | Energy RMSE：D0 -> D0+X | Volume RMSE：D0 -> D0+X | 总 tokens |
|---|---|---:|---:|---:|
| Agent | `soap6_variability`, `ring_entropy`, `soap6_pc1_mean` | 254.772 -> 248.452（-2.48%） | 1505.036 -> 1439.292（-4.37%） | 3,404 |
| RAG+Agent | `soap6_variability`, `soap6_pc1_std`, `ring_entropy` | 254.772 -> 251.108（-1.44%） | 1505.036 -> 1473.033（-2.13%） | 49,803 |
| Small KG+RAG+Agent | `soap6_variability`, `soap6_pc1_mean`, `ring_entropy` | 254.772 -> 248.452（-2.48%） | 1505.036 -> 1439.292（-4.37%） | 36,959 |

当前结果只证明端到端链路可运行。三种模式都得到正向的探索性 RMSE 变化，但
Small KG+RAG 没有超过 Agent，并且 Agent 与 Small KG+RAG 选择了相同描述符。

## 不能作为正式结论的原因

RAG 和 Small KG+RAG 都检索到了 Zeolite Atlas 的原始论文
`doi:10.1063/1.5119751`。该论文直接报告 SOAP 对 energy/volume 的预测优于
angles、distances 和 rings，因此当前检索包含 benchmark 直接答案泄漏。
检索结果还出现了复述该结论的后续论文，正式比较前也需要纳入污染审计。

此外，当前 `D0` 是统一 Ridge 下的 classical descriptor 诊断基线，原论文 native
model、单位和原始 split 尚未完成复现签字。因此不能把本次 RMSE 作为论文主结果，
也不能据此宣称 KG 有效或无效。

## 下一步

1. 冻结 benchmark contamination denylist，至少排除原始论文及直接复述答案的文献，
   不修改原有 8927 文档及向量。
2. 用同一模型、prompt、三轮调用、descriptor 预算和 ML pipeline 重跑三模式。
3. 人工检查新证据是否仍直接泄露 benchmark 已知答案；通过后才把结果升级为可比较
   的 exploratory run。
4. 并行复现原论文 native baseline 和单位；完成前不进入 confirmatory locked test。

SorbMetaML 保留为第二候选。它更适合后续 hydrogen adsorption 任务，但仓库许可证、
材料结构映射和原始 split 仍需确认，所以本轮不替换 Zeolite Atlas。

## 可追溯信息

- 服务器结果：`/public/home/xiaohe/lxf/catalysis-rag/runs/glm-discovery-zeolite-atlas-v1-3579959.json`
- 本地结果：`research/runs/glm-discovery-zeolite-atlas-v1/result-3579959.json`
- 结果 SHA-256：`09c9f3d7b128f94704463d18680d7d50f4b76ee3888a048e11f704f864fcf94f`
- 数据归档 SHA-256：`d704adbccbfee6d5736abf0a5d68d5893c85bbab43483c37a5be525587d7b4e4`
