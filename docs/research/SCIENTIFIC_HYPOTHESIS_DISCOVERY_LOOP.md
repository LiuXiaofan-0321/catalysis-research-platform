# Evidence-grounded Scientific Hypothesis Discovery Loop

状态日期：2026-09-01

状态：`SMALL_KG_V1_FROZEN / RETRIEVAL_AND_BENCHMARK_PENDING`

本文定义项目当前的科学主线。Small KG 第一版的精确冻结结果、hash、质量统计、
已知限制和下一阶段目标见 `SMALL_KG_V1_STATUS.md`。当前冻结结果不等于 raw-source
license/semantic-dedup sign-off，也不表示任何 Model x Knowledge outcome 已产生。

## 1. 核心科学问题

我们研究的不是 KG 能否让问答更流畅，而是：

> 当 AI 可访问的外部科学知识从单一目标领域扩展到邻近领域，再扩展到跨领域
> 异构知识时，它是否更容易提出能够被真实材料数据验证的科学假设？

目标因果链为：

```text
Knowledge scope and diversity
  -> Evidence-chain quality
  -> Hypothesis quality
  -> Executable descriptor quality
  -> Empirical and OOD utility
  -> Scientific discovery ability
```

我们不预设知识越多结果一定越好，也不把论文数、节点数或问答分数单独视为
scientific discovery。

## 2. 科学发现闭环

```text
Existing ML study
  -> Existing dataset, descriptors and scientific conclusions
  -> KG evidence retrieval and evidence chains
  -> Evidence-grounded scientific hypothesis
  -> Computable and falsifiable descriptor
  -> Same downstream ML and frozen split
  -> Supported / rejected / revised
  -> Feedback to the next hypothesis
```

KG+LLM 不直接替代 property predictor，也不允许随机枚举数学组合做 AutoML。
每个新增 descriptor 必须同时具有：

- scientific hypothesis；
- supporting and contradicting evidence；
- physical or chemical meaning；
- mathematical definition and required raw inputs；
- applicable domain、assumptions 和 confounders；
- falsifiable expected effect；
- empirical validation result。

失败假设必须保留。`rejected` 和 `revised` 与 `supported` 一样进入完整实验轨迹和
统计 denominator。

## 3. Knowledge scope 的三个层级

### 3.1 Small KG - Local / domain-specific

Small KG 仅包含分子筛/zeolite 目标材料体系知识。当前冻结实例包含 6691 篇论文、
8927 个结构化文档，其中 main 6691 个、SI 2236 个。全部 6691 篇共同构成
`Small-KG-zeolite-v1`，不再用 500/2000/6691 表示 Small/Medium/Large。

它回答：

> 当 AI 只掌握目标体系内部知识时，能否完成 Evidence -> Hypothesis ->
> Descriptor -> Validation 的最小闭环？

已经冻结的工程与数据成果：

1. 三批结构化抽取结果按 `document_id` 去重，并按 `paper_id` 聚合 main/SI；
2. 结构化 schema、artifact hash、三批统计和 24 篇分层复核样本已验证；
3. 6691-paper / 8927-document corpus manifest 已冻结；
4. evidence-grounded `Small-KG-zeolite-v1` snapshot 已构建并通过严格证据审计。

以下治理项仍需在 outcome-bearing benchmark 前完成或签字确认：

1. 完成原始文件来源、许可和只读 inventory 审计；
2. 完成 DOI/title/year/version 级 semantic duplicate sign-off；
3. 冻结 research article、review、perspective 和无效记录的纳入/排除规则；
4. 建立 benchmark literature leakage 和 direct-answer leakage audit。

论文、图表和 config 应使用 6691 papers / 8927 documents 及对应冻结 hash，不再使用
`5000-6000` 估计值描述当前 Small KG。

### 3.2 Medium KG - Domain-expanded

Medium KG 包含 Small KG，并加入与目标性质直接相关的邻近领域：

- MOF；
- COF 和其他多孔材料；
- adsorption；
- host-guest interaction；
- confinement、pore chemistry 和 diffusion；
- adsorption thermodynamics。

它用于检验 AI 是否能从邻近材料体系迁移机制。

### 3.3 Large KG - Cross-domain

Large KG 包含 Small/Medium KG，并加入可能提供可迁移机制的跨领域知识：

- catalysis、photocatalysis 和 thermal catalysis；
- surface science 和 reaction chemistry；
- local coordination、strain 和 electronic effects；
- thermodynamics、kinetics 和 transport。

它用于检验跨领域 evidence chain 是否能产生目标领域内没有直接提出过、但可计算
和可验证的 hypothesis/descriptor。

## 4. KG scaling 的操作性定义

新的核心变量不是单一 size：

```text
K = (quantity, domain diversity, task coverage, structure, provenance)
```

正式实验必须区分：

- Quantity：论文、有效 evidence 和 token 数量；
- Diversity：source domain、relation type 和 mechanism family 的覆盖；
- Coverage：对冻结 benchmark scientific question 的相关证据覆盖；
- Structure：raw RAG、entity KG、evidence KG、shuffled KG；
- Provenance：证据能否解析回论文、位置和原始 quote。

在资源允许时增加固定数量对照，例如：

| Condition | Example composition | Purpose |
| --- | --- | --- |
| Local-6k | 6000 zeolite | Local-domain reference |
| Mixed-6k | 3000 zeolite + 3000 MOF | Diversity at matched quantity |
| Cross-6k | 2000 zeolite + 2000 MOF + 2000 catalysis | Cross-domain diversity at matched quantity |

这些数值是设计示例，最终 composition 必须在 outcome-bearing run 前根据 inventory
和预算冻结。现有 `K20/K40/K60/K80/K100` 热催化快照继续作为 within-corpus
quantity infrastructure 和辅助 ablation，不等同于新的 Local/Expanded/Cross-domain
主变量。

## 5. Benchmark 的角色

Benchmark 是 hypothesis 的实验台和裁判，不向 LLM 暴露 locked-test labels。

每个候选 benchmark 必须满足：

1. public raw data、license 和固定版本可获得；
2. target、单位和 sample identity 明确；
3. 原始 descriptor set 和 scientific conclusion 可复现；
4. 有足够结构/组成输入计算新 descriptor；
5. 原论文或统一 baseline 可复现；
6. 能构造 train/validation/locked-test；
7. 最好支持 scientifically meaningful OOD split；
8. 能审计 benchmark paper 和答案是否已存在于 KG。

当前候选：

- **Zeolite Atlas**：优先评估其结构、原 descriptor、energy/volume target 和
  baseline 是否足以支持 structure-property hypothesis；
- **SorbMetaML**：优先评估结构映射、统一 descriptor 计算和 IZA/PCOD/MOF OOD
  条件；如果无法形成完整 hypothesis-descriptor loop，则不强行采用。

候选名称不是预注册结论。完成数据可用性、许可、结构映射、baseline reproduction
和 leakage audit 后，才能激活其中一个 benchmark。

## 6. Small KG 最小可行实验

第一阶段只证明闭环可以严谨运行，不直接声称完整 knowledge-diversity scaling。

### 6.1 条件

- `D0`：原论文 descriptor baseline；
- `LLM-only`：给定原论文、descriptor 定义和 dataset metadata，不提供 KG；
- `Small-KG + LLM`：提供冻结 Small KG 的 evidence retrieval；
- `Small-RAG + LLM`：使用相同语料和近似 token budget 的 raw retrieval；
- `Small-shuffled + LLM`：保留文本/预算但打乱预注册关系，用作结构诊断。

### 6.2 固定变量

- 同一个 LLM、prompt family 和 inference budget；
- 同一个 hypothesis/descriptor proposal budget；
- 同一个 downstream ML、preprocessing 和 hyperparameter budget；
- 同一个 train/validation/locked-test split；
- 同一组 random seeds；
- test labels 在 descriptor 冻结前不可见。

### 6.3 单轮闭环

```text
D0 baseline reproduction
  -> retrieve evidence
  -> generate H1
  -> compile descriptor X1
  -> D1 = D0 + X1
  -> validation-set comparison
  -> supported / rejected / revised
  -> feedback artifact
```

仅当 H*、descriptor code、selection rule 和所有 hashes 冻结后，才允许一次 locked
test。不得采用 `test -> 改 descriptor -> 再 test`。

### 6.4 MVP 验收

- 至少一个真实 public benchmark 的 baseline 可复现；
- 至少一个 hypothesis 带完整 evidence chain；
- descriptor 可以从 allowed raw inputs 确定性计算；
- supported、rejected 和 execution failure 全部保留；
- LLM-only、RAG 和 Small KG 使用匹配预算；
- run manifest 可以单独验证并重放关键 artifacts；
- 无 benchmark target、原答案或 locked-test outcome 泄漏到生成阶段。

MVP 通过只证明 pipeline readiness。Small/Medium/Large scaling claim 需要后续冻结
的多 scope、多 task 和统计实验。

## 7. 主要评价指标

### Scientific generation

- hypothesis hit rate；
- evidence grounding 和 citation correctness；
- falsifiability 和 descriptor executability；
- unsupported hypothesis rate；
- strengthen/revise/challenge outcome distribution。

### Empirical utility

- paired delta RMSE/MAE/R2 或 benchmark 原指标；
- OOD gain；
- multiple-seed confidence interval；
- feature-importance change 和 proxy relationship；
- best-of-N gain 和 iterative discovery curve。

### Knowledge mechanism

- evidence-chain length 和 relation types；
- direct/indirect/conflicting evidence；
- source-domain distribution；
- cross-domain transfer rate；
- quantity-matched diversity effect。

## 8. Leakage controls

每个 benchmark 至少生成两个可审计标记：

- `benchmark-paper-present`：原论文是否在 KG；
- `direct-answer-present`：目标 descriptor 或结论是否已被 KG 文献直接给出。

必要时构建 leakage-controlled KG，排除：

- benchmark 原论文；
- 明确引用并总结其核心结论的论文；
- 明确提出待评估 descriptor 的论文。

Temporal evaluation 只能作为辅助证据，因为基础模型可能在预训练阶段见过未来
论文。最强验证仍然来自 post-training、unpublished 或其他真正 unseen data。

## 9. 研究问题

- **RQ1**：KG 是否比 LLM-only 提高 validated hypothesis rate？
- **RQ2**：Local -> Domain-expanded -> Cross-domain 是否提高 hypothesis/descriptor utility？
- **RQ3**：增益来自 quantity 还是 domain diversity？
- **RQ4**：跨领域证据能否产生目标领域未直接提出的有效 descriptor？
- **RQ5**：增益是否迁移到 OOD，而不只改善 interpolation？
- **RQ6**：系统能否 strengthen、revise 或 challenge 已有 scientific conclusion？
- **RQ7**：更广知识是否提高 iterative scientific discovery rate？

## 10. 当前阶段边界

当前立即目标是：

```text
Frozen Small corpus and Small-KG-zeolite-v1
  -> Scientific normalization overlay v1.1
  -> KG/RAG common retrieval contract
  -> One eligible benchmark
  -> One complete hypothesis-descriptor-validation-feedback loop
```

在 Small KG MVP 通过前，不启动 Medium/Large KG 的大规模构建，也不根据早期结果
修改 locked test、endpoint 或 benchmark。生产平台继续作为交互界面；所有
outcome-bearing pipeline、manifest 和 evaluation 优先实现于 `research/`。
