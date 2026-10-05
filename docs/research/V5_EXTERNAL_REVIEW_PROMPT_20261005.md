# V5 外部模型分析提示词

以下内容可直接复制给可读取 GitHub 的模型。完整 V5 结果已经发布；这是审查请求，不是要求制造 KG > RAG > Agent 的排序。

---

请分析这个催化科学假设发现研究仓库的 **V5 完整结果**：

https://github.com/LiuXiaofan-0321/catalysis-research-platform

研究主线是 NMI，基准来自 JACS Au 原论文 DOI `10.1021/jacsau.4c00429`。请重点回答：为什么这批最终 MAE 平均降幅只有约 0.4%–0.9%，比旧 V4 约 6%–7% 低很多；为什么 RAG 仍低于 Agent；为什么 KG 优势很小；哪些问题属于实现缺陷，哪些属于实验设计、训练波动或知识使用方式。希望排序是 KG+RAG > RAG > Agent，但请依证据分析，不要以恢复该排序为成功标准。

## 先读取最新记录

1. [V5 完整报告](https://github.com/LiuXiaofan-0321/catalysis-research-platform/blob/main/docs/research/JACS_AU_DIRECT_V5_RESULTS_20261005.md)
2. [全部 30 条轨迹及 90 槽清单](https://github.com/LiuXiaofan-0321/catalysis-research-platform/blob/main/research/reports/jacs_au_direct_v5_20261005/analysis/ALL_TRAJECTORIES.md)
3. `research/reports/jacs_au_direct_v5_20261005/analysis/diagnostic.json`
4. 同目录 `all-30-traces.json`、`all-90-slots.json`、`verified-summary.json`
5. `research/reports/jacs_au_direct_v5_20261005/complete-server-results/summary.json`
6. 同目录 `prepared/config.json`、`prepared/knowledge.json`，以及 `generation/`、`evaluation/` 各 30 个 JSON。具体结论须回查这些原始记录，不能只复述报告。

完整实验结果提交为 `9617cba`；后续审查文档更新不会改变这批原始记录。GitHub 若不能展示大 JSON，可使用 Raw 或逐个轨迹文件。若无法读取，请列出实际读到与未读到的文件；不要把未读取内容当作已经核实。

## 当前实验实际做了什么

- 模型 `glm-5.3-flash`，thinking enabled，reasoning_effort high，temperature 0.2。
- 三组 Agent、RAG、KG+RAG，每组十条新的生成轨迹，共 30 条。
- 每条从同一个原生 14 输入 D0 开始，连续三轮，每轮提出一个描述符。成功通过技术流程后直接追加，即 D0 → D0+X → D0+X+Y → D0+X+Y+Z。
- 失败槽跳过、没有新假设重抽；最终可能不足三个新增描述符。不是每轮三个候选择优，也不是把同一个公式重复三次。
- 不提供标签、相关性或 MAE 反馈；整个生成数组结束、组合冻结之后才评分，中间组合没有训练评分。
- ANN 4000 epochs，固定 fit seeds `[3,7,11,17,23]`。先求每条相对同 seed D0 的五 seed 平均降幅，再平均十条轨迹；所有失败、零追加和负收益轨迹均纳入。
- 附加列使用训练特征限定的仿射/符号规范化，不选择最好符号或 seed。原 D0、划分、目标换算和 ANN 预测器保持一致。
- RAG 获得同一已审查知识库的全部图事实平铺，KG 获得同一事实的节点/边结构；原论文正文、SI 和描述符答案从检索证据排除。
- 新公式重表达 D0，不增加测量信息。可执行公式和预测改善均不自动证明机制。

主评分为 Agent **0.776041%**、RAG **0.428412%**、KG **0.926468%**，顺序 KG > Agent > RAG。KG−Agent 只有 **0.150427 个百分点**。预声明 KG−RAG 与 RAG−Agent 的 97.5% bootstrap 差值区间均跨 0；统计单位为十条生成轨迹，不能把五个训练 seed 算成五十条独立发现。外层数据已在开发中看过，其诊断降幅 Agent 0.323158%、RAG 0.438576%、KG −0.084041%，不能当作独立验证。

## 已发现的接口问题，请独立检查

90 槽中仅 54 个成功追加，23 个提出阶段失败，13 个技术阶段失败。旧程序要求 `proxy_assumptions` 是非空字符串，但模型常返回有实际内容的字符串列表；格式恢复又把列表转字符串判成改写受锁科学字段。

首次列表类型失败 Agent 3 个、RAG 9 个、KG 9 个，共 21 个。在派生副本中将原列表保序换行拼接后，19 个能通过原 schema 校验；剩余两例有其他字段问题。**schema 通过不等于执行或 ANN 成功。** 无损适配器已新增并测试，但未接入本批冻结 release、未修改原轨迹或主排名。

请检查：错误究竟怎样发生、是否确实只改变表示、恢复提示和锁定比较是否存在冲突，以及其他失败是否也存在类似契约问题。不能把所有科学字段改动都作为格式恢复放行，也不能假定补回 19 个槽就会改善排名。

## 代码入口

- `research/configs/experiments/jacs-au-direct-v5-high.json`
- `research/scripts/run_jacs_au_direct.py`：生成、复核、技术修复、冻结与评分流程。
- `research/src/catalysis_research/experiments/jacs_au_direct.py`：提示、候选结构、知识控制与检查。
- `research/src/catalysis_research/experiments/jacs_au_direct_interface.py`：新独立无损适配器，尚未替换原流程。
- `research/src/catalysis_research/experiments/jacs_au.py`：D0、数据划分、目标和 ANN。
- `research/src/catalysis_research/models/glm.py`：请求参数、解析、usage 与恢复。
- `research/scripts/manage_jacs_au_direct.py`、`research/scripts/diagnose_jacs_au_direct.py`：汇总及全量审计。
- `research/tests/test_jacs_au_direct.py`、`test_jacs_au_direct_pipeline.py`、`test_jacs_au_direct_interface.py`。

原始训练数据及完整检索索引不在 GitHub。因此可以检查实现、原始生成记录与已保存评分，不能仅凭仓库文件宣称完成重新训练或新实验。

## 希望得到的分析

1. **新旧低值的可比性。** 读取 `docs/research/JACS_AU_KG_V4_RESULTS_20260930.md` 和 `JACS_AU_STAGE_REPLAY_AND_DIRECT_V5_20261004.md`。旧 V4 每轮三个候选、评分择优保留，V5 每轮一个、无标签直接加入，同时还有其他变化。区分“移除评分选择后指标含义改变”与真正的实现/知识退化，不把多项同时变化当单一因果消融。
2. **公平性与失败影响。** 分方法、重复、轮次检查失败和实际新增数量。总体比较保留全部轨迹；成功子集或新增数量条件分析只能作为诊断，不能替代主排名。评估固定候选消融能识别什么、不能识别什么。
3. **具体公式和知识使用。** 结合正负、零追加及跨组重合案例，核查公式来源、代理条件、定义和复核前后变化。哪些证据实际推动组合，哪些只是文字装饰或合规审查？图结构是否比平铺事实提供了可观察的推理帮助？不要凭有引用就认定知识有效。
4. **训练与表示。** 检查同一组合五 seed 的波动、符号/仿射等价、非线性变换和冗余输入。最终组合分数不能归因到某一个新增式，因为中间组合没有评分。D0 强、信息没有增加是可检验解释，不是现成结论。
5. **方案是否过度保守。** 是否有有价值初稿被不必要的契约/方向/定义检查丢弃？哪些是真正不成立的科学声明？修复须保留科学内容，不能为了得分更换公式或事后方向。
6. **可执行修复与对照。** 按优先级提出最小修复、固定候选审计、静态 ANN 消融和下一批 fresh 无标签实验；说明每项的判据、全样本失败处理、预算和冻结规则。修复补入旧槽会改变后续提示历史，所以静态组合消融不等于真实闭环重跑。判断应扩大生成重复、增加训练 seed，还是先改善实现/知识工具；不要保证更多重复会提高均值。

每个主要结论请给出仓库文件位置、方法/重复/轮次、原始与最终公式或字段及相关分数，并标记“已确认事实 / 有证据但尚未隔离的解释 / 待实验假设”。输出优先级问题表和公平实验方案。不要仅凭均值归因于模型太强、token 不够或缓存；本批科学请求 237 次均 stop、response ID 不重复，仍应以实际记录为依据。

不得筛选 seed、重复次数、成功子集或评分指标制造排序；不得将已看过开发诊断称独立测试；不得虚构未执行评分。请指出本报告自身如有错误，并给出可核实的修正依据。
