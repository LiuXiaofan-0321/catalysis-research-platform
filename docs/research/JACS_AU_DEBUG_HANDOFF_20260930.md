# JACS Au 科学假设发现：GitHub调试入口

**2026-10-05 完整结果：** [high 直接加入 V5 完整结果与接口分析](JACS_AU_DIRECT_V5_RESULTS_20261005.md)。30/30 轨迹、150 个 seed 评分记录完成；主降幅 KG 0.926468%、Agent 0.776041%、RAG 0.428412%，差值区间跨零。54/90 槽追加，发现 21 个 proxy_assumptions 列表/字符串接口失败，知识组各9个、Agent3个；无损适配器已测试，未替换本批结果。旧“运行中/阻塞”的段落均为当日早期快照。

**2026-10-04 配额恢复后提交：** 符号对五 seed 与 D0 已完成，工程门槛和计算节点 high API 探针通过。新 V5 生成数组 `3868198` 运行中，最终评分 `3868202`、全量汇总 `3868203` 依赖接续；见 [最新实施报告](JACS_AU_STAGE_REPLAY_AND_DIRECT_V5_20261004.md) 及 [提交清单](../../research/reports/jacs_au_direct_v5_20261004/LAUNCH.json)。尚无新方法排名。

**2026-10-04 最新状态：** [真实阶段回放与直接加入 V5 实施报告](JACS_AU_STAGE_REPLAY_AND_DIRECT_V5_20261004.md)。54/54 原数据 ANN 回放完成、230 次拟合，历史前缀/终稿误差均为 0；新增初稿/复核稿分数见全 162 槽明细。V5 代码、同事实平铺/图对照、30 任务和五 seed 方案已准备，未运行。真实符号对多 seed 诊断被服务器账户 CPU 配额阻止；不要把旧段落的“回放尚未运行”当作最新状态，也不要把当前 V5 准备文件当作结果。

2026-10-01补充：[GPT-6 Pro外部审查核实与采纳顺序](JACS_AU_PRO_REVIEW_ADOPTION_20261001.md)。已核实符号等价公式的历史评分差与方向标旗语义；新ANN回放及直接加入实验仍未运行。

更新：2026-09-30。用途：供外部研究审查者从实际代码、完整轨迹和已有回溯接续分析。主线NMI；Jev、harness和ZeoDiff暂缓。目标KG+RAG > RAG > Agent尚未稳定实现，不能将希望排序作为结果筛选标准。

**先读最新[直接加入协议澄清](JACS_AU_HIGH_DIRECT_ADDITION_ASSESSMENT_20260930.md)。** 用户要每轮直接加入描述符；优先建议high每轮1项、3轮、各组10条新轨迹。该协议尚未实现/运行。旧V4是三个候选经ANN评分后择一，保留为历史开发实验，不能当作新协议结果。

[可直接复制给GPT-6-Pro的完整提示词](GPT6_PRO_RESEARCH_DEBUG_PROMPT_20260930.md)。

## 最新结果

| effort | Agent评分MAE降幅 | RAG | KG+RAG |
| --- | ---: | ---: | ---: |
| low | 6.64% | 6.87% | 4.30% |
| high | 6.98% | 6.42% | 7.16% |

18/18轨迹完整、160/162候选成功评分。每档每组3次完整生成重复，每次3轮×每轮3候选。原论文14项D0、同一ANN4000 epochs/fit seed=3/划分/目标换算。high-KG领先Agent约0.175pp，不能认定稳定优越；原外层已开发查看，独立泛化未确认。HGB冻结公式迁移没有统一收益。

high第一轮全部单式、不择优的探索性均值为KG+0.804%、Agent+0.455%、RAG+0.281%。不能拼接成三轮直接加入成绩，不能相加成多式联合收益。

## 建议阅读顺序

1. [最新协议澄清及无择优单轮诊断](JACS_AU_HIGH_DIRECT_ADDITION_ASSESSMENT_20260930.md)
2. [V4完整结果](JACS_AU_KG_V4_RESULTS_20260930.md)
3. [V4全部轨迹回溯结论](JACS_AU_KG_V4_DIAGNOSIS_20260930.md)
4. [固定候选复核消融与阶段回放设计（尚未执行）](JACS_AU_KG_V4_REVIEW_ABLATION_20260930.md)
5. [V4工程修复、提交与恢复记录](JACS_AU_KG_V4_LOW_HIGH_20260930.md)
6. [V3回溯](JACS_AU_KG_V3_DIAGNOSIS_20260930.md)、[V3结果](JACS_AU_KG_V3_RESULTS_20260930.md)
7. [V2泄漏与根因更正](JACS_AU_KG_V2_DIAGNOSIS_20260929.md)、[结果台账](RESEARCH_RESULTS_LEDGER_20260929.md)

旧V2实际检索含benchmark正文/SI/SHAP结果，受污染；不要把该批排名用于干净的方法比较。V3/V4中的条件迁移、引用充分性和自然语言机制一致性仍可进一步审查。

## 原始与分析文件

| 内容 | 仓库路径 |
| --- | --- |
| V4全部18条原始完成轨迹 | [complete-server-results](../../research/reports/jacs_au_kg_v4_20260930/complete-server-results/) |
| V4汇总 | [summary.json](../../research/reports/jacs_au_kg_v4_20260930/complete-server-results/summary.json) |
| 三条失败的恢复来源 | [recovery-manifest.json](../../research/reports/jacs_au_kg_v4_20260930/complete-server-results/recovery-manifest.json) |
| V4原提交和补跑 | [LAUNCH.json](../../research/reports/jacs_au_kg_v4_20260930/LAUNCH.json)、[RECOVERY_LAUNCH.json](../../research/reports/jacs_au_kg_v4_20260930/RECOVERY_LAUNCH.json) |
| 全部162槽的公式与最终评分 | [ALL_TRAJECTORIES.md](../../research/reports/jacs_au_kg_v4_diagnosis_20260930/ALL_TRAJECTORIES.md) |
| 逐轨迹完整阶段内容（网页阅读） | [web-review/README.md](../../research/reports/jacs_au_kg_v4_diagnosis_20260930/web-review/README.md) |
| 全部候选对象与原检索 | [candidate-audit.json](../../research/reports/jacs_au_kg_v4_diagnosis_20260930/candidate-audit.json) |
| 54个固定复核批次，未跑 | [fixed-review-blocks.json](../../research/reports/jacs_au_kg_v4_diagnosis_20260930/fixed-review-blocks.json) |
| 无择优第一轮27式 | [high-first-round-no-selection.json](../../research/reports/jacs_au_kg_v4_diagnosis_20260930/high-first-round-no-selection.json) |
| API缓存回溯 | [cache-audit.json](../../research/reports/jacs_au_kg_v4_diagnosis_20260930/cache-audit.json) |
| V3图组织9条与平铺3条 | [server-results](../../research/reports/jacs_au_kg_v3_repair_20260929/server-results/) |
| V3数值/证据/设计回溯 | [jacs_au_kg_v3_diagnosis_20260930](../../research/reports/jacs_au_kg_v3_diagnosis_20260930/) |
| V3已审查来源库 | [evidence-final/bank.json](../../research/reports/jacs_au_kg_v3_repair_20260929/evidence-final/bank.json) |
| V2原轨迹和污染回溯 | [jacs_au_kg_v2_20260929](../../research/reports/jacs_au_kg_v2_20260929/) |
| 最初JACS 30条轨迹及基线预测/划分 | [jacs_au_20260929](../../research/reports/jacs_au_20260929/) |

大JSON在GitHub界面或网页工具可能不能一次读完。逐轨迹Markdown保存三个阶段的完整候选与检查，并链接原JSON；全轨迹公式清单可先用于定位问题。候选分析中的counterfactual_blind_ann_score为空是因为未训练，不能自行填成已有分数。

## 代码入口与复现边界

- [真实V4调度、提示和更新协议](../../research/scripts/run_jacs_au_kg_v4.py)
- [V4图、定义、检索与预检](../../research/src/catalysis_research/experiments/jacs_au_kg_v4.py)
- [数据、目标和ANN适配](../../research/src/catalysis_research/experiments/jacs_au.py)
- [原公式/单位与假设检查](../../research/src/catalysis_research/experiments/jacs_au_knowledge.py)
- [来源排除](../../research/src/catalysis_research/experiments/jacs_au_sources.py)
- [GLM客户端](../../research/src/catalysis_research/models/glm.py)
- [结果汇总](../../research/scripts/summarize_jacs_au_kg_v4.py)、[恢复合并](../../research/scripts/merge_jacs_au_kg_v4_recovery.py)
- [全轨迹诊断导出](../../research/scripts/diagnose_jacs_au_kg_v4.py)
- [阶段固定组合ANN回放（未执行）](../../research/scripts/replay_jacs_au_kg_v4_candidates.py)

原始Supporting_final_2数据及完整检索索引在服务器，未随本次GitHub同步；因此仓库可审查代码、复核轨迹和复算已有评分统计，但仅靠仓库文件不能宣称已经重训原ANN。基线预测和split.json保留，原论文公开数据入口是[论文与SI](https://pubs.acs.org/doi/10.1021/jacsau.4c00429)。不存在的新协议结果、固定候选ANN回放结果不能被报告为已完成。

旧不可解析失败响应的正文与usage未落盘，不能追回。补跑复用成功事件、恢复失败阶段，原失败文件保留；合并记录usage与恢复耗时有账目局限。cached_tokens表示输入计算复用，现有high首轮九次相同请求返回九份不同结构化答案；无法据此保证所有未来接口行为。

本次同步聚焦JACS研究资料、依赖代码及回溯。既有语料删除没有恢复或纳入本次提交；`.env`、私有凭据、服务器原始数据和完整索引不发布。不得向网页模型提供密码/API密钥或要求它重新提交已结束的服务器作业。
