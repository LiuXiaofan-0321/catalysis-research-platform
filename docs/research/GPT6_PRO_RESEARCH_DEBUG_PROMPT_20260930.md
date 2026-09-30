# 给网页端 GPT-6-Pro 的研究调试提示词

以下正文可以直接复制。仓库入口：[研究调试索引](https://github.com/LiuXiaofan-0321/catalysis-research-platform/blob/main/docs/research/JACS_AU_DEBUG_HANDOFF_20260930.md)。不要只看仓库根README的历史路线。

---

请作为科学假设发现、知识图谱/RAG、机器学习实验设计的独立审查者，接续已有研究，诊断为什么现有方法尚未稳定实现 KG+RAG > RAG > Agent，并给出可执行的修复与公平实验方案。目标排名是待检验假设，不是必须制造的结论。请认真读取实际代码和轨迹，不从零泛泛设计新项目。

仓库：https://github.com/LiuXiaofan-0321/catalysis-research-platform

先读：

1. `docs/research/JACS_AU_DEBUG_HANDOFF_20260930.md`：最新状态、文件地图、历史协议与当前用户意图。
2. `docs/research/JACS_AU_HIGH_DIRECT_ADDITION_ASSESSMENT_20260930.md`：最新协议澄清，优先于旧文档中的候选择优方案。
3. `docs/research/JACS_AU_KG_V4_RESULTS_20260930.md`、`JACS_AU_KG_V4_DIAGNOSIS_20260930.md`、`JACS_AU_KG_V4_REVIEW_ABLATION_20260930.md`。
4. `docs/research/JACS_AU_KG_V3_DIAGNOSIS_20260930.md`、`JACS_AU_KG_V2_DIAGNOSIS_20260929.md`、`RESEARCH_RESULTS_LEDGER_20260929.md`。

研究主线是NMI科学假设发现，JACS Au论文10.1021/jacsau.4c00429为benchmark。Jev/harness/ZeoDiff暂缓。D0必须保持原论文14个原生输入；提出开放公式假设，不使用预设描述符菜单。公式只重表达D0，不提供新观测信息，也不自动证明机制。

务必区分两种协议：

- 已运行V4：每条完整轨迹3轮，每轮生成3个公式候选，分别ANN评分后只保留一个最佳改善者；无改善则停留。每个effort/方法有3条完整生成重复，不是只有3个候选。low/high两档×3方法×3重复=18条完整轨迹、162候选槽，160槽成功评分。
- 用户最新意图：每轮直接加入提出的描述符，不根据评分择优。优先建议high、每轮只输出并加入1个、连续3轮：D0→D0+X1→D0+X1+X2→D0+X1+X2+X3；即使评分变差也不回退。每轮加入2/3个可作为预先冻结的单独协议。新协议尚未实现和运行，计划各组10条新完整轨迹，不能与旧V4混算。请审查这个设计，包括知识是否应在生成之前进入、是否排除MAE及训练标签关联反馈、技术失败如何公平处理。

V4模型glm-5.3-flash，temperature=0.2，ANN4000 epochs、fit seed=3，同一D0/划分/目标换算；相对D0的评分MAE平均降幅：

| effort | Agent | RAG | KG+RAG |
| --- | ---: | ---: | ---: |
| low | 6.64% | 6.87% | 4.30% |
| high | 6.98% | 6.42% | 7.16% |

high三条最终轨迹分别是：Agent [3.876,7.998,9.079]%，RAG [7.107,6.160,6.006]%，KG [7.526,7.469,6.483]%。KG仅比Agent高约0.175个百分点，不能凭3次认定稳定优越。high外层开发诊断为Agent2.61%、RAG3.38%、KG4.32%，但数据已经开发查看，不能作为独立验证或替代评分排名。冻结ANN所选公式迁移HGB没有统一收益。

不按评分择优、纳入high第一轮每组全部9个单独公式的探索性平均为KG+0.804%、Agent+0.455%、RAG+0.281%；这不是新协议三轮最终成绩，也不是同时加入三个公式的成绩，不能把单式MAE降幅相加。不能事后挑h3位置来获得希望排名。

请重点核查以下问题，引用具体路径、轨迹/轮次/slot、公式和初稿→复核→修复变化：

1. high-RAG均值低于Agent是生成波动、有效候选价值不足、历史冗余、复核表达变化，还是证据/机制覆盖限制？区分已经有证据的原因与需要消融的解释，不把“模型太强/太新/token不够”当默认答案。
2. KG是否真正产生了额外机制组合？现有代码中三个方法都先盲生成，RAG与KG复核获得相同来源锚点和6张机制卡，所有组共享可执行precheck；图主要连接机制、共享代理与定义规则。high-KG6个胜者中5个保持初稿公式。检查是否错误地把共享检查和随机初稿优势算成图贡献。
3. 复核的科学锁定是否有漏洞？low-KG-1/R3/h1把已通过的孔径差改成上一轮已评分无改善的乘积；low-KG-3/R2/h3将AV替换成Dif，锁定hypothesis仍说AV，最终+6.103pp；high-KG-3/R1/h1删MW并翻符号，导数声明冲突后又翻回，rationale未同步。请独立核实，不把这些诊断当不可挑战的事实。
4. 目标方向、训练关联与物理预测是否混淆？核对实际entropy loss/R定义与s_ads/s_gas，检查通过翻符号或单调变换让训练相关性标签一致是否被误报为机制修正。局部导数测试、训练相关性、ANN增益和物理机制分别评价。
5. 正确处理native重原子PMI/SPAN/GeDi合法零值、single-site/linear/nonlinear分支、固定探针AV的质量比单位、Df/lsd_f与Dif/lsd_p角色、q_X=X/X_ref。不要把Df当全局腔径Di，不把AV/Vol当分子真实自由体积，不用任意epsilon冒充物理边界。
6. 原论文正文、SI及已有描述符答案是否确实被排除？V2曾受benchmark SHAP泄漏污染，必须隔离，不将其排名用于干净对照。V3/V4的来源身份/条件审查是否还有缺口？引用编号存在不等于来源支持当前代理或机制。
7. 缓存或恢复回放是否影响重复实验？旧high首轮9个相同请求返回9份不同结构化输出，输入缓存命中不等于答案缓存。旧失败响应正文/usage有不可追回部分。检查追踪、成本与失败处理，不用改变科学提示或反复重抽强迫生成不同公式。

重点代码：

- `research/scripts/run_jacs_au_kg_v4.py`：真实prompt、partial updates、字段锁、复核、修复、评分与逐轮保留。
- `research/src/catalysis_research/experiments/jacs_au_kg_v4.py`：输入定义、图路径、来源检索、训练域、precheck。
- `research/src/catalysis_research/experiments/jacs_au.py`、`jacs_au_knowledge.py`、`jacs_au_kg_v3.py`、`jacs_au_sources.py`：数据/目标/模型、DSL与引用排除。
- `research/src/catalysis_research/models/glm.py`、`research/scripts/merge_jacs_au_kg_v4_recovery.py`、`summarize_jacs_au_kg_v4.py`：请求参数、失败与汇总。
- `research/scripts/diagnose_jacs_au_kg_v4.py`、`replay_jacs_au_kg_v4_candidates.py`、`audit_jacs_au_high_no_selection.py`：已有回溯与尚未执行的离线阶段回放。

完整轨迹：`research/reports/jacs_au_kg_v4_20260930/complete-server-results/`，含low/high各9条、summary.json和recovery-manifest.json。详细回溯：`research/reports/jacs_au_kg_v4_diagnosis_20260930/`，含ALL_TRAJECTORIES.md、candidate-audit.json、fixed-review-blocks.json、high-first-round-no-selection.json、cache-audit.json。大JSON无法读取时，先用调试索引链接的逐轨迹Markdown，再按需读取对应原始JSON或小块资料；若无法访问明确说明，不声称已经读完。

请输出：

1. 你实际读了哪些文件/轨迹，以及哪些未能访问。
2. 证据表：观察→具体轨迹/代码→解释→事实/推测→最小验证；按对结论的影响排序。
3. 真正代码bug、协议偏离用户意图、统计不确定性、知识贡献不足、机制解释不自洽分别列出。
4. 新“high每轮直接加入一个”主协议的精确设计、需要修改的函数/schema、失败处理、冻结/预算/信息边界，以及每组10次能回答和不能回答的问题。
5. 固定初稿的self/source/同事实flat-graph/graph复核消融，如何隔离生成差异、图额外事实、训练标签反馈及评分搜索。科学主协议与历史局部消融不要混算。
6. 不依赖希望排名的验收标准，以及新划分稳健性和真正独立评估的计划；包括负结果怎样报告。

不要为了得到KG > RAG > Agent挑随机种子、slot、重复次数、模型档位、指标或挑最好的几条轨迹。允许结论是“知识组织增量很小”或“现有设计还未检验该主张”。不得将预测增益当成物理机制发现。不要恢复/清理历史语料删除，不索要或输出密码/API密钥，不重复提交旧服务器作业。先审查，再提出具体、可复查的修复。
