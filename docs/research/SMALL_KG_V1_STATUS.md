# Small KG v1：冻结结果与下一阶段目标

状态日期：2026-09-01

状态：`SMALL_KG_V1_FROZEN / RETRIEVAL_AND_BENCHMARK_PENDING`

本文记录分子筛 Small KG 第一版已经完成的可验证结果、已知限制和下一阶段目标。
它是当前进度的权威摘要，但不替代
`SCIENTIFIC_HYPOTHESIS_DISCOVERY_LOOP.md` 和 `EXPERIMENT_PROTOCOL.md` 中的科学
定义与预注册约束。

## 1. 研究目标

科学主线面向 Nature Machine Intelligence：研究外部科学知识从 Local 扩展到
Domain-expanded 和 Cross-domain 后，是否能提高 AI 提出可验证科学假设和可执行
descriptor 的能力。

核心闭环保持为：

```text
Knowledge
  -> Evidence
  -> Hypothesis
  -> Executable descriptor
  -> Frozen-data validation
  -> Supported / rejected / revised
  -> Next hypothesis
```

当前 6691 篇分子筛论文共同构成一个完整的 `Small/Local KG`。500、2000 和
6691 不是 Small/Medium/Large 三个等级。Medium 和 Large 必须通过增加邻近领域与
跨领域知识定义，而不是仅增加同领域论文数量。

## 2. 三批结构化抽取

| Campaign | Papers | Documents |
| --- | ---: | ---: |
| `glm53-extraction-batch-0001` | 500 | 855 |
| `glm53-extraction-batch-0002` | 1500 | 1806 |
| `glm53-extraction-batch-0003` | 4691 | 6266 |
| **Total** | **6691** | **8927** |

最终文档组成：

- main：6691；
- SI：2236；
- failed/missing：0；
- 一个缺少主文的 orphan SI 在 campaign selection 阶段记录并排除；
- 三批结果按 `document_id` 做跨批去重，每个 `paper_id` 必须且只能有一个 main。

抽取模型为 `glm-5.3-flash`，抽取 schema 为
`catalysis_paper_extraction.v2.1`，prompt version 为
`catalysis-paper-extraction-v2.2`。

## 3. 冻结结构化语料

Corpus ID：`zeolite-structured-corpus-v1`

Schema：`structured_extraction_corpus.v1`

关键不可变身份：

| Identity | SHA256 / content hash |
| --- | --- |
| Document content | `fbc1543bcaa79e1c4e468ff380a627524b79f9dfb753f2b2ae2ee95005aee8bbc` |
| Paper content | `ef86fcbe530b13be8f51ea09b0927c498982db9acae6a4cc20a09dbb2b274cffd` |
| `structured-documents.zip` | `8bcb2d0ca8e7f00cae778058979631f91d237dac3efcbc32ef781edf287499ccc` |

冻结目录包含：

- `manifest.json`：版本、来源、三批统计和 artifact hashes；
- `documents.jsonl`：8927 个文档的来源、hash、模型和 ZIP entry；
- `papers.jsonl`：6691 个按 `paper_id` 聚合的主文/SI关系；
- `quality-summary.json`：全量自动质量统计；
- `review-sample.jsonl` 和 `review-sample.md`：24 篇确定性分层复核样本；
- `structured-documents.zip`：通过 schema 与 artifact hash 校验的原始结构化结果。

## 4. 轻量质量验收

全量 schema/hash 验证通过。结构化记录统计为：

| Record | Count |
| --- | ---: |
| Entities | 74306 |
| Experiments | 34006 |
| Observations | 80550 |
| Claims | 31816 |
| Evidence records | 307386 |

质量标记：

- 边界规范化涉及 1319 个文档，占 14.78%；
- `unverified` evidence 为 33321 条，占全部 evidence 的 10.84%；
- 7026 个文档至少含一条 `unverified` evidence，占 78.71%；
- 5695 个文档含 visual-review 标记，占 63.80%；
- 24 篇样本覆盖三批、main/SI 和 clean/normalized/review/unverified 风险层。

24 篇快速人工复核的主要结论：

- 大部分 quote 含可读的科学事实、数值或实验条件；
- 模糊表格数字和不完整 caption 通常已进入 `unverified` 或 `needs_review`；
- 一个抽样 SI 只有结构坐标表，没有抽取出结构化记录；
- 部分 SI 的 title 被图片、表格、期刊页眉或通用 Supplementary Information 文本
  污染；
- KG 按 `paper_id` 合并 main/SI，并以 main metadata 构建 paper node，因此上述 SI
  title 问题不会替换论文主标题。

这些结果支持进入 Small KG MVP 的检索与 benchmark 阶段，但不表示所有记录都已
人工核验，也不构成模型效果结论。

## 5. Small KG v1

Snapshot ID：`Small-KG-zeolite-v1`

Ontology：`catalysis_evidence_graph.v2`

Stage-1 archive SHA256：
`a1185bdd4ac16b1722de274bdf84b328c62d527b03190ddee129586efcdddb00d`

Snapshot content hash：
`07925455449dfe13cc78b9b958dd71d5e4d77aee2ad54fcd8a312ce4f1bf9f43`

图规模：

| Node type | Count |
| --- | ---: |
| Paper | 6691 |
| Entity | 33120 |
| Keyword | 31608 |
| Experiment | 34002 |
| Observation | 80541 |
| Claim | 31796 |
| Reaction | 1143 |
| Condition | 32448 |
| Metric | 61112 |
| **All nodes** | **312461** |

总边数为 701204。严格证据模式删除 302 条缺少完整 provenance 的候选边，保留边
必须含：

- `source_paper_id`；
- 至少一个原始 `document_id`；
- `pdf_page_index`；
- 非空原文 `quote`。

最终验证结果：

- grounded edge rate：100%；
- dangling edges：0；
- ungrounded edges：0；
- source archive hash verification：通过；
- main/SI 局部 ID 在聚合前按 `document_id` namespace，避免跨文档误连接。

## 6. 已知限制

1. `v2` 的实体、反应、条件和指标节点完成了确定性字符串规范化，但尚未完成
   ontology-level synonym/canonical mapping；中英文、缩写和近义反应仍可能形成多个
   节点。
2. `paper_type`、年份和 reaction category 存在抽取变体或异常值，不能直接作为
   confirmatory covariate。
3. visual-review 文档比例较高，视觉表格/图片中的关键数值仍需在具体 benchmark
   evidence universe 中针对性复核。
4. 语料已经按 `document_id` 去重并按 `paper_id` 聚合，但原始库的 license 审计和
   DOI/title/year 级 semantic duplicate sign-off 尚未完成。
5. benchmark literature leakage、direct-answer leakage 和 task-level evidence
   coverage 尚未测量。
6. 当前没有任何 Model x Knowledge outcome，不能声称 KG、RAG、Agent 或
   Multi-Agent 已带来科学性能提升。

## 7. 下一阶段目标

### 7.1 科学规范化映射层 v1.1

2026-09-02 本地实现状态：immutable overlay builder/verifier、CLI、v1.1 规则配置、
deterministic hash、unresolved queue 和合成测试已完成。6691-paper 全量 artifact
尚未在集群物化，高频映射与高风险 metadata repair 也尚未人工签核。

保持 Small KG v1 不变，另建可追溯 mapping overlay：

- zeolite framework、catalyst sample、reaction 和 metric 的 canonical mapping；
- 温度、压力、时间、flow、WHSV/GHSV 和性能单位规范化；
- 中英文、缩写、大小写和拼写变体合并；
- 每条 mapping 保留 raw value、canonical value、rule/version 和人工复核状态；
- 异常年份、碎片化 paper type 和 SI title 污染进入单独质量修复层。

### 7.2 KG+RAG 混合检索

2026-09-02 实现状态：common EvidenceBundle、matched budgets、严格 provenance、
frozen KG 0-2 hop retriever、科学规范化 overlay 接入，以及统一的 `agent` /
`rag_agent` / `small_kg_rag_agent` 接口均已完成并通过离线测试。Raw RAG 以只读方式
复用历史 `full-rag-v1-index`，在排序前排除唯一多余论文及其 19 chunks，并校验过滤后
恰为 6691 papers / 8927 documents / 365643 chunks，不重建或改写原索引。10-20 问题
smoke test 尚未完成，因此这里仍不包含任何模型或检索效果结论。

构建同一接口下的可切换 knowledge modes：

```text
Agent / no external knowledge
RAG + Agent
Small KG + RAG + Agent
Token-matched shuffled KG
```

统一输出 evidence bundle，并保留 `paper_id + document_id + page + quote`。Raw RAG、
Evidence KG 和 Shuffled KG 必须匹配 model-visible token/retrieval budget。

### 7.3 MVP benchmark

继续客观评估 Zeolite Atlas 与 SorbMetaML，不因已经讨论过就默认采用。激活前必须
完成：

- raw data、license、structure 和 target identity；
- 原 descriptor、模型与 split 的 baseline reproduction；
- 新 descriptor 的 required inputs 可计算性；
- IID/OOD split 与 locked test；
- benchmark-paper 和 direct-answer leakage audit。

截至 2026-09-02 的 benchmark feasibility 判断：

- Zeolite Atlas 的 Materials Cloud v1 记录为 CC BY 4.0，包含 1k/10k DEEM 的
  SOAP、angle、distance、ring descriptor 及 energy/volume 相关数据，优先进入
  baseline review；仍需确认 archive 是否包含计算新 descriptor 所需的非泄漏原始结构。
- SorbMetaML 提供 IZA、PCOD、MOF、HCP 等材料的 hydrogen adsorption state points
  和 few-shot subsets，但仓库当前没有明确 license，暂不激活。

当前第一轮 benchmark 选择 **Materials Cloud Zeolite Atlas v1**
（`10.24435/materialscloud:2019.0079/v1`，CC BY 4.0）。用户工作区已下载并校验
归档（SHA-256 `d704adbccbfee6d5736abf0a5d68d5893c85bbab43483c37a5be525587d7b4e4`），
解压 1k 子集得到 1000 个结构、52686 个 Si 原子；Angles/Distances 为 4 维，King
ring 为 20 维，SOAP-KPCA 为 100 维，energy/volume 为逐原子贡献。适配器通过
`ids_natoms_1k.dat` 做结构级聚合，固定结构 ID modulo-5 split，并将原始 classical
descriptor 作为 `D0`，GLM 仅能从可计算 catalog 中选择新增 `X`。源单位、原论文
native model 和 split 复现仍待签字，因此当前结果仍标记为 exploratory。

评价以 benchmark 原始模型、原始 primary metric 和冻结 protocol 为准。主分析在
同一个 benchmark-native pipeline 中比较原 descriptor `D0` 与 `D0 + X`；统一
Ridge 仅作为跨 benchmark 的 secondary representation diagnostic。答案正确率、
检索召回、幻觉率、token、费用和延迟只作为系统诊断，不能替代真实
hypothesis/descriptor validation。

### 7.4 第一组系统对比

当前小规模消融在同一底座模型、prompt、预算、split 和 benchmark-native
downstream pipeline 下比较：

1. 单独 LLM Agent；
2. RAG；
3. Small KG + RAG + Single-Agent。

Multi-Agent 暂不进入当前消融。正式结构性结论后续仍必须加入 token-matched
shuffled KG；进入 Multi-Agent 阶段时再冻结角色、最大调用次数和总 token budget。

### 7.5 Knowledge-scope 对比

Small MVP 通过后再构建：

1. Small KG + RAG + Multi-Agent；
2. Medium KG + RAG + Multi-Agent；
3. Large KG + RAG + Multi-Agent。

Medium 增加 MOF、COF、adsorption、confinement、diffusion 和邻近多孔材料知识；
Large 再增加广义 catalysis、surface science、coordination、strain、thermodynamics、
kinetics 和 transport。正式比较必须增加 quantity-matched diversity controls。

## 8. 当前最近一步

```text
Small KG v1 frozen
  -> normalization overlay v1.1
  -> KG/RAG common retrieval contract
  -> 10-20 question retrieval smoke test
  -> benchmark feasibility and baseline freeze
  -> one complete hypothesis-descriptor-validation-feedback loop
```

在用户明确批准并提供模型配置前，不启动付费模型的全量 Agent 评测。
