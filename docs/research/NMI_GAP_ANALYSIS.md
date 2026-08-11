# NMI Gap Analysis

状态日期：2026-08-10

## 1. 目标

目标不是继续增加一个多智能体科研平台，而是建立一套可以受控研究以下问题的
实验基础设施：

```text
How do model capability and structured scientific knowledge jointly scale
AI-driven scientific reasoning and descriptor discovery?
```

研究对象为：

```text
Q = f(M, K)
```

- `M`：foundation model capability；
- `K`：scientific knowledge capability；
- `Q`：预先定义的科学发现表现。

核心证据链必须到达：

```text
Literature
  -> Evidence-grounded KG
  -> Hypothesis
  -> Executable Descriptor
  -> Predictive Utility
  -> Optimization Utility
  -> Truly Unseen Validation
```

## 2. 当前总体判断

| 能力 | 当前成熟度 | 判断 |
| --- | --- | --- |
| 结构化论文语料 | 中高 | 可复用，是当前最强资产 |
| Evidence provenance | 中 | 字段较完整，但缺少独立 registry 和评估 |
| KG import | 中 | 可用，但未版本化为实验自变量 |
| Retrieval | 低至中 | 可用于产品，不足以支持严格 ablation |
| Hypothesis generation | 中 | 有结构，但未形成正式科学对象 |
| Experiment planning | 中 | 产品可用，provenance 不完整 |
| Model abstraction | 低 | DeepSeek 硬编码 |
| Descriptor discovery | 缺失 | 论文主线无法成立 |
| Downstream ML | 缺失 | 无法量化 representation utility |
| Public dataset and splits | 低至中 | registry、hash、IID/OOD、label firewall 和 audit 工具已实现，exact dataset 尚未选择 |
| Experiment manifest | 中 | immutable manifest、artifact hash 和 CLI 已实现，尚未接入完整实验流水线 |
| KG scaling | 低至中 | K247 已冻结为首个真实点，nested scaling builder 尚未实现 |
| Statistical analysis | 缺失 | 无法支持 scaling claim |
| Private blind validation | 低 | firewall 协议已冻结，独立 evaluator 和执行工具尚未实现 |
| 自动测试 | 低至中 | research layout、K247 freeze 和 Run Manifest 已覆盖 |

## 3. P0：论文主线成立前必须完成

### P0-1 Frozen Experiment Protocol

当前缺口：

- `Q`、`M`、`K` 没有操作性定义；
- 没有 primary endpoint；
- 没有预先定义 knowledge scaling 成立判据；
- 没有 tuning/freeze 边界；
- 没有 pilot go/no-go 规则。

必须完成：

- `docs/research/EXPERIMENT_PROTOCOL.md`；
- protocol version 和 amendment log；
- primary/secondary endpoints；
- fixed matrix、seeds、budgets、splits 和 statistics；
- private firewall；
- pre-registered success/failure criteria。

验收：

- 在查看 Model x KG outcome 前完成；
- 任何后续变化必须有版本、理由和受影响 run 列表；
- 禁止只因结果不显著而修改 endpoint。

### P0-2 Complete Run Provenance

当前状态：

`research/src/catalysis_research/provenance/run_manifest.py` 已实现
`run_manifest.v1`。每个 run 独立保存 manifest、SHA256-addressed scientific
artifacts 和 `FINALIZED.json`；completed/failed run 终态不可变，dirty Git
默认禁止，CLI 可创建、记录、完成、失败、展示和验证 run。

已记录：

- run ID、time、Git commit、dirty state；
- Git tree/branch、prompt version/hash；
- provider/model/revision；
- temperature、seed、token/reasoning budget；
- KG snapshot ID/hash；
- retrieval configuration 和 evidence IDs；
- raw and parsed outputs；
- hypothesis 和 descriptor artifacts；
- dataset/split identity and hashes；
- downstream model configuration；
- metrics、warnings、errors、manual interventions。

当前验收：

- [x] 一个 run 目录可单独审计；
- [x] completed run 不允许通过 API 原地覆盖；
- [x] failed run 同样保留；
- [x] artifact、manifest 和 finalization 篡改可检测；
- [ ] model、retrieval、descriptor、dataset 和 evaluation modules 全部接入；
- [ ] 实现基于 manifest 的 end-to-end replay。

### P0-3 KG Snapshot and Versioning

当前状态：

- 生产 Workspace 的当前数据库状态不是 snapshot；
- import 不读取 dataset manifest；
- 已实现 immutable Stage 1 corpus inventory freezer；
- 已实现 `proportional_stratified_hash_order.v1` 和单一完整顺序的 exact
  nested prefix builder；
- 已实现 K20 至 K100 snapshot、selection order、corpus 和 nested manifest
  的 hash/strict-nesting verification；
- thermal v1 固定 seed、年份桶、topic source rule、paper type groups 和
  `102/205/307/410/512` absolute counts 已在 protocol/config 中预注册；
- 没有 structure ablation；
- 没有 relevant evidence coverage。

仍必须完成：

- task-level evidence coverage；
- real、raw、entity、evidence、shuffled 等结构模式；
- exact public predictive dataset freeze 后绑定 task coverage。

验收：

- 同一输入和配置生成相同 snapshot hash；
- K20 是 K40 的严格子集，依次嵌套；
- selected snapshot 只从对应 source JSON records 重建，不从 K100 过滤；
- shuffled control 保持节点、文本和 token budget 可比；
- snapshot 不依赖手工复制数据库。

### P0-4 Model Provider Abstraction

当前缺口：

- DeepSeek provider 和 API shape 写死；
- `AI_RESEARCH_PROVIDER` 未生效；
- 缺少 model revision、seed、reasoning budget、prompt hash。

必须完成：

- `ScientificModelProvider`；
- provider-neutral request/response；
- capability registry；
- retry/timeout/concurrency policy；
- raw response；
- structured output validation；
- deterministic request hash。

验收：

- 替换模型不修改 hypothesis/descriptor 核心逻辑；
- M1/M2/M3 使用相同 experiment interface；
- provider 不支持的参数明确记录为 unsupported，不能静默忽略。

### P0-5 DescriptorSpecification

当前缺口：

没有 descriptor 代码或 schema。

必须完成：

- stable descriptor ID；
- hypothesis 和 mechanistic rationale；
- physical meaning；
- mathematical definition/formula；
- required inputs；
- units；
- expected relationship；
- applicable domain；
- evidence/claim IDs；
- assumptions/confounders；
- falsification condition；
- computation method；
- novelty rationale；
- confidence。

验收：

- JSON Schema validation；
- evidence ID 必须存在于当前 snapshot；
- 缺少计算定义的自然语言概念不能进入 executable stage；
- 所有 rejection 都记录原因。

### P0-6 Executable Descriptor Pipeline

当前缺口：

无法把模型建议转成 dataset column。

必须完成：

- controlled expression or code generation；
- sandboxed execution；
- allowed input registry；
- units validation；
- numerical sanity checks；
- missing data policy；
- variance check；
- redundancy/correlation check；
- failure ledger；
- code and environment hash。

验收：

- 无人工秘密修正；
- 相同 descriptor 和 dataset 产生相同 column hash；
- invalid、non-computable、zero-variance 等失败均保留；
- 任意人工 intervention 显式进入 manifest。

### P0-7 Public Dataset and Fixed Splits

当前状态：

基础设施已实现：

- `dataset_manifest.v1` 和 `split_manifest.v1`；
- public-only registration 和 raw file SHA256；
- fixed seed `20260810` 的 deterministic `60/20/20` IID split；
- pre-registered group-aware OOD folds；
- sample、duplicate group 和 split hash；
- descriptor generation / computation / downstream training / evaluator
  label-access boundary；
- structural leakage audit 和 CLI。

剩余缺口：

- exact eligible public thermocatalysis dataset 尚未选择；
- `public-registry.v1.json` 仍为空并保持 `ACTIVATION_BLOCKED`；
- real license、source、version、checksum 尚未登记；
- real target、allowed inputs、group rationale 尚未冻结；
- 尚未生成真实 IID/OOD manifests；
- semantic target-proxy 和 corpus contamination 仍需人工审计。

验收：

- exact dataset 和 split 在第一个 outcome-bearing run 前冻结；
- test labels 不进入 descriptor generation 和 selection；
- OOD group 有科学解释，不只是随机划分。

### P0-8 Fair Baseline and Downstream ML

当前缺口：

没有 conventional、LLM-only、RAG、KG、shuffled 或 oracle baseline，也没有
统一 ML pipeline。

必须完成：

- fixed descriptor budget；
- identical preprocessing；
- identical split and seeds；
- identical hyperparameter search budget；
- primary Ridge pipeline；
- secondary nonlinear models；
- failure-safe fixed feature slots。

验收：

- condition 之间唯一有意变化是 Model、Knowledge 或预注册的 structure；
- feature 数量一致；
- test 不参与 tuning；
- 所有 baseline 使用相同 evaluator。

### P0-9 Model x Knowledge Pilot

当前缺口：

没有二维实验矩阵和 pilot 判据。

必须完成：

- 3 models x 3 KG scales pilot；
- LLM-only、Raw RAG、Evidence KG、Shuffled KG；
- fixed prompts、descriptor budget、splits 和 seeds；
- pilot report；
- failure mode distribution。

验收：

- 结果可由单个 CLI workflow 重建；
- 生成真实而非示意图；
- 根据预注册 go/no-go 判据决定是否扩展；
- 没有趋势时优先 debug，不直接扩库。

### P0-10 Private Data Blind Protocol

当前缺口：

没有访问控制、freeze bundle、独立 evaluator 或 one-shot 规则。

必须完成：

- AI team 和 data-generation team 权限隔离；
- private labels 不进入 repository；
- pre-blind freeze manifest；
- independent evaluation runner；
- aggregate-only result release；
- access and rerun log。

验收：

- blind test 前所有方法和 hash 已冻结；
- AI team 不查看 raw labels；
- 查看 private performance 后修改方法会被明确标记为失去 pristine blind status。

## 4. P1：强烈建议完成

### P1-1 Full 3 x 5 Scaling Study

- M1/M2/M3；
- K20/K40/K60/K80/K100；
- multiple seeds；
- task-balanced analysis；
- effect sizes 和 confidence intervals。

### P1-2 Knowledge Structure Ablation

- no knowledge；
- raw RAG；
- entity KG；
- experiment KG；
- evidence KG；
- shuffled KG；
- optional component removal。

目的不是证明“更多 token 更好”，而是区分 size、coverage、structure 和
provenance 的贡献。

### P1-3 Retrieval Evaluation

- recall@k；
- evidence precision；
- task coverage；
- oracle evidence；
- retrieval failure 与 reasoning failure 分离。

### P1-4 Scientific Reasoning Evaluation

- evidence grounding；
- claim correctness；
- mechanistic consistency；
- cross-paper reasoning；
- falsifiability；
- descriptor executability。

需要自动指标和盲态专家评价相结合，并记录 reviewer agreement。

### P1-5 Data Efficiency and OOD

- 10%、20%、40%、60%、100% training fractions；
- fixed subsample seeds；
- family/reaction/material OOD；
- learning curves；
- uncertainty intervals。

### P1-6 Descriptor Novelty x Utility

- novelty rubric；
- nearest known descriptor；
- utility delta；
- feature ablation；
- success/failure quadrants；
- 不只挑选成功案例。

### P1-7 Optimization Benchmark

- top-k enrichment；
- hit rate；
- best-found value；
- normalized regret；
- samples to target；
- fixed acquisition budget。

### P1-8 Statistical Analysis

至少包含：

```text
Performance ~ Model
            + Knowledge
            + Model:Knowledge
            + KnowledgeStructure
            + Task
```

报告：

- marginal effects；
- interaction；
- bootstrap confidence interval；
- effect size；
- sensitivity analysis；
- multiplicity correction。

## 5. P2：可以后续扩展

- 更大规模语料；
- 更多 foundation models；
- 更复杂 agent topology；
- vector database 或 distributed graph；
- 前端研究 dashboard；
- 人类协作实验设计；
- 自动实验设备集成；
- 多领域迁移；
- 产品级审计和组织权限。

这些能力不应抢占 P0 的复现、descriptor 和严格实验设计工作。

## 6. 主要 Validity Threats

### 6.1 Construct Validity

风险：

- 用节点数代表 knowledge capability；
- 用自然语言“合理性”代表 descriptor utility；
- 用单一 benchmark 表示 scientific discovery。

控制：

- 明确定义 M、K、Q；
- primary endpoint 冻结；
- size、coverage、structure 分离；
- descriptor 必须 executable。

### 6.2 Internal Validity

风险：

- 不同 condition 使用不同 prompt 或 token budget；
- KG condition 生成更多 descriptors；
- downstream tuning budget 不同；
- test feedback 进入方法修改。

控制：

- condition-matched budgets；
- fixed feature slots；
- shared evaluator；
- immutable manifests；
- freeze gate。

### 6.3 Statistical Validity

风险：

- 只报告最好 seed；
- 多指标中挑显著结果；
- task 当作独立样本但忽略重复结构；
- interaction power 不足。

控制：

- primary endpoint；
- all-seed reporting；
- hierarchical analysis；
- confidence intervals 和 effect sizes；
- pilot 只作 go/no-go，不作最终显著性结论。

### 6.4 External Validity

风险：

- 只在随机划分上有效；
- 模型记忆了公开文献；
- public benchmark 过拟合；
- 只在一个催化体系成立。

控制：

- domain-aware OOD；
- temporal evaluation 只作 secondary；
- private unseen thermocatalysis blind test；
- secondary cross-domain transfer。

### 6.5 Contamination Risk

风险：

- private labels 被 AI team 查看；
- private results 被用于调 descriptor；
- KG 中意外加入 private records；
- public test 被反复使用。

控制：

- physical and logical firewall；
- freeze bundle；
- one-shot evaluator；
- access log；
- dataset hash audit。

## 7. 最小侵入式改造边界

应保留：

- 现有生产前后端；
- 用户、Workspace 和 Profile；
- Stage 1 extraction artifacts；
- evidence-rich import；
- 生产图谱浏览和实验反馈。

新科研能力优先放入 `research/`。

只有以下情况才修改 production backend：

1. 增加只读、版本化的数据导出；
2. 修复影响 evidence correctness 的错误；
3. 提供稳定 adapter，而不是让 research 直接依赖内部 mutable table；
4. 修改后有 production regression tests。

## 8. 当前阻塞项

在正式 Model x KG run 前必须解决：

1. 精确选择 public predictive dataset；
2. 确认 target、allowed raw inputs 和 OOD grouping；
3. 确认 M1/M2/M3 的具体模型和 revision；
4. 确认推理成本预算；
5. 确认私有数据的组织权限和独立 evaluator；
6. 完成 protocol freeze。

这些阻塞项不能在结果出来后再补写。
