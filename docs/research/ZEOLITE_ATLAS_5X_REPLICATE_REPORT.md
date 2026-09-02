# Zeolite Atlas 三模式五次重复报告

## 实验设置

- Benchmark：Materials Cloud Zeolite Atlas v1；
- 模型：`glm-5.3-flash`；
- 模式：`Agent / RAG+Agent / Small KG+RAG+Agent`；
- 重复：每种模式 5 次独立调用，共 15 次；
- 单次预算：1 轮假设生成、3 个新增 descriptor、`reasoning_effort=low`；
- ML：固定 structure-ID modulo-5 split、相同 Ridge 和 alpha grid；
- Slurm array：`3585436`，五个子作业并发运行；
- 单个子作业耗时：4 分 24 秒至 4 分 42 秒。

## 原始论文排除

Zeolite Atlas 原始论文 `doi:10.1063/1.5119751` 已冻结为 benchmark 专用排除项，
同时从 RAG 和 Small KG 检索路径中排除。原索引及向量未修改。

该论文在原索引中对应 1 paper、1 document 和 33 chunks。加上通用排除项
`doi:10.1126/science.ads7290` 后，实际检索视图为：

- 6690 papers；
- 8926 documents；
- 365610 chunks；
- 52 条排除记录。

五次结果中原始论文证据泄漏数为 0。

## 汇总结果

| 模式 | 有效输出 | Energy RMSE 平均改善 | Volume RMSE 平均改善 | 有效调用已知 tokens |
|---|---:|---:|---:|---:|
| Agent | 3/5 | 1.45% | 2.35% | 10,357 |
| RAG+Agent | 5/5 | 1.34% | 3.27% | 237,443 |
| Small KG+RAG+Agent | 4/5 | 1.70% | 3.54% | 168,395 |

无效输出也作为固定预算下的实验结果保留，不追加重试：

- Agent 两次错误引用了外部证据，因此被严格校验拒绝；
- Small KG+RAG 一次缺少顶层 `falsification_criteria`；
- RAG 五次均通过结构化输出校验。

## Descriptor 稳定性

- `ring_entropy`：所有有效输出均选择；
- `soap6_variability`：Agent 3/3、RAG 4/5、Small KG+RAG 3/4；
- `soap6_pc1_std`：Agent 2/3、RAG 3/5、Small KG+RAG 2/4；
- `soap6_pc1_mean`：RAG 3/5、Small KG+RAG 3/4；
- `ring_nonzero_fraction`：Agent 1/3、RAG 1/5。

三种模式仍集中到少数相似 descriptor，说明当前 descriptor catalog 对选择结果有较强
约束。Small KG+RAG 的有效样本平均改善略高，但只有 4 个有效重复，且模式间差异
小于重复间波动，目前不能宣称 KG 显著优于 RAG 或 Agent。

## 逐重复结果

| 重复 | Agent | RAG+Agent | Small KG+RAG+Agent |
|---|---|---|---|
| 1 | E 1.44%，V 2.13% | E 2.48%，V 4.37% | schema 失败 |
| 2 | E 1.49%，V 2.78% | E 1.44%，V 2.13% | E 0.41%，V 3.29% |
| 3 | schema 失败 | E 0.41%，V 3.29% | E 2.48%，V 4.37% |
| 4 | schema 失败 | E -0.09%，V 2.21% | E 2.48%，V 4.37% |
| 5 | E 1.44%，V 2.13% | E 2.48%，V 4.37% | E 1.44%，V 2.13% |

`E` 和 `V` 分别表示 Energy 与 Volume test RMSE 相对 D0 的改善比例；正值表示
RMSE 降低。失败调用的 token usage 未被当前结果格式保留，因此 token 合计仅覆盖
12 个通过校验的调用。

## 当前判断

本轮证明：原论文可以在不重建索引的情况下被严格排除；重复实验也证实单次结果不足以
判断 KG 收益。下一步不应立即增加迭代轮数，而应先确认当前新增 descriptor 是否只是
重复 benchmark 已知表示，并复现原论文 native baseline、单位和 split。完成后再决定
是否扩大重复数或进入固定 3 轮的 validation-only 迭代。

## 结果位置

- 服务器：`/public/home/xiaohe/lxf/catalysis-rag/runs/glm-discovery-zeolite-atlas-v1-replicates-3585436/`
- 本地：`research/runs/glm-discovery-zeolite-atlas-v1/replicates-3585436/`
