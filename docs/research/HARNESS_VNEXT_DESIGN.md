# Harness vNext：可审计的假设发现循环

AdsZeo v1–v4 已归档为闭合描述符目录实验。当前 harness 主线从 v5 的开放式公式提名出发，研究三个问题：

1. 假设增加轮数后，后续候选是否利用了失败原因和验证反馈，还是只重复近似公式；
2. 多个角色分别承担证据、重复性、可执行性和验证计划工作时，是否减少无效计算并提高有用候选召回；
3. Jev 作为可替换的判别/调度器，能否在相同提议预算下正确决定“补充检索、进入计算、修改、暂缓或放弃”。

`research/src/catalysis_research/harness/` 提供了第一版离线可运行骨架。它不把模型输出当作科学结论，程序化执行器和锁定测试集仍然是最终裁决者。

当前骨架已经覆盖角色产物、证据引用校验、公式规范化、锁定测试字段剥离和 Jev 路由接口；全局 token/调用预算、自动追加检索、与 AdsZeo v5 执行器的状态机连接及人工校准集仍属于下一步实现，不能把当前离线基线当作完整闭环结果。

离线回放入口为 `python research/scripts/run_harness.py --input rounds.json --output harness.json`；设置 `--judge jev` 时需要显式提供 `JEV_ENDPOINT` 和 `JEV_API_KEY`。默认 `--judge rule` 用于测试和成本基线。

每个候选必须带稳定的 `candidate_id`、`hypothesis_id`、公式或描述、证据 `E##`、执行状态和验证反馈。harness 按固定顺序运行四个可替换角色：

| 角色 | 必须产出的可检查结果 |
| --- | --- |
| `evidence_critic` | 支持、矛盾或证据不足；缺口和证据 ID |
| `novelty_auditor` | 公式规范化摘要、重复候选 ID、重复判断置信度 |
| `feasibility_auditor` | 可执行、不可执行或退化；失败代码 |
| `validation_planner` | 验证集边际收益、重复次数、split ID |

Jev 接收这些结构化结果，并只输出一个门控建议：

`retrieve_more | compute_validate | revise | defer | abandon`。

建议必须附带证据判断、重复判断、理由、缺失证据或检索问题。Jev 不得添加证据、读取行级标签或锁定测试结果，也不能把“证据支持”写成“假设已证实”。`RuleBasedJev` 是离线基线；`HttpJevClient` 只负责可替换的 JSON 接口，真正的 Jev endpoint、模型版本和提示词哈希需要在冻结正式实验前固定。

## 轮数实验

第一阶段固定数据、模型、检索预算和每轮提议预算，只改变轮数和反馈条件：

- `one_shot`：一次提议，不返回验证反馈；
- `feedback_loop`：每轮返回已保留候选、失败代码和 validation 边际收益；
- `multi_agent_loop`：在同样总 token/call 预算下增加角色审查；
- `jev_loop`：在同样预算下增加 Jev 门控。

每个候选的真实验证收益仍由程序计算。每轮记录可执行率、证据充分率、重复率、角色调用成本、`retrieve_more`/`compute_validate`/`revise`/`defer`/`abandon` 数量、validation 增益和失败分类。测试集只能在所有候选完成决策后访问一次。

主要结果是跨重复的 paired validation/OOD 增益、发现曲线下面积、达到目标增益的调用成本、有用候选召回和错误放弃率。没有独立人工标注时，不能把角色一致率或 Jev 置信度当作科学正确率；应先建立小型人工审计集，再报告校准和误拒绝。

## Jev 判定规则

程序化门控优先于模型意见：

- 证据不足且还有检索预算 → `retrieve_more`；预算耗尽 → `defer`；
- 公式重复 → `abandon`；不安全或输入不支持 → `revise`；零方差、缺失过多或冗余 → `abandon`；
- 通过执行检查且没有证据冲突 → `compute_validate`；验证无边际收益 → `defer` 或 `abandon`；
- 最终保留集合和测试结果由固定验证规则决定，Jev 只能调度下一步。

正式实验需要保留 Jev 请求/响应哈希、模型和版本、延迟、token 成本、检索前后预算、失败处置、验证可用性及所有候选的 hindsight validation 标签，以便计算 precision、recall 和 false-rejection。
