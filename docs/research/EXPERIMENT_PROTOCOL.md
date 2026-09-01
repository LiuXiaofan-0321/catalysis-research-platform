# Experiment Protocol

Protocol ID：`catalysis-model-knowledge-scaling.v1`

规则冻结日期：2026-08-10

状态：`V1.6 RULES_FROZEN / V2 SCOPE AMENDMENT REQUIRED / ACTIVATION_BLOCKED`

`RULES_FROZEN` 表示本文中的研究问题、变量定义、endpoint、预算、公平性规则、
统计判据和 firewall 已冻结。

`ACTIVATION_BLOCKED` 表示仓库尚未包含可用于下游预测的 public AI-ready dataset，
且 M1/M2/M3 的具体模型 revision 尚未登记。在完成本文定义的 activation gate
以前，不允许开始任何 outcome-bearing Model x Knowledge run。

2026-08-25 项目进一步明确：primary scientific question 将从单一 corpus 内的
paper-fraction scaling，扩展为 Local / Domain-expanded / Cross-domain 的 knowledge
scope and diversity scaling。新方向由
`docs/research/SCIENTIFIC_HYPOTHESIS_DISCOVERY_LOOP.md` 定义。现有 v1 的
K20/K40/K60/K80/K100 规则继续有效地约束旧 snapshot 和 within-corpus quantity
ablation，但在 v2 protocol 冻结前，不得直接用它们代表新的 Small/Medium/Large
主变量或启动新方向的 outcome-bearing run。

2026-09-01 进一步冻结 benchmark validation 原则：每个 benchmark 的主分析必须
复现原论文模型与评价框架，在相同 preprocessing、split、hyperparameter budget
和 metric 下比较原 descriptor `D0` 与 `D0 + X`。统一 Ridge 不再作为主分析，
仅作为跨 benchmark 的 secondary representation diagnostic。该修订发生在任何
Model x Knowledge outcome 产生之前。

Private unseen thermocatalysis validation 的访问控制和盲测执行细则由
`docs/research/PRIVATE_DATA_PROTOCOL.md` 管理。两份协议发生冲突时，private data 访问采用更
严格的规则。

## 1. Protocol Governance

### 1.1 Outcome-bearing run

满足任意条件的运行视为 outcome-bearing：

- 生成将进入论文比较的 hypothesis 或 descriptor；
- 使用 benchmark target label；
- 计算 validation、test 或 OOD performance；
- 用结果决定 prompt、KG、descriptor 或模型配置；
- 进入 pilot/full-study figure 或 statistical analysis。

纯 schema、mock provider、synthetic data 和无 target label 的单元测试不属于
outcome-bearing run。

### 1.2 Amendment rule

冻结后如需修改本文中的任何规则，必须：

1. 新增 protocol version；
2. 在 amendment log 中记录日期、原因和负责人；
3. 说明是否已查看任何 validation/test/private outcome；
4. 列出受影响 runs；
5. 对所有受影响 conditions 重新运行；
6. 旧结果和旧 protocol 不得删除。

以下理由不能单独成为 amendment 原因：

- 当前结果不显著；
- 某个模型表现不如预期；
- 某个 metric 更有利；
- 某个 seed 结果不好；
- private test 表现不佳。

### 1.3 Protocol violation

以下任一情况构成 critical protocol violation：

- test/private labels 进入 descriptor generation；
- 查看 test/private outcome 后修改 descriptor 或 prompt；
- condition 使用不同 descriptor 数量而未预注册；
- 删除失败 descriptor 或失败 runs；
- 未记录的人工修复；
- 修改 frozen split、KG snapshot、model revision 或 endpoint；
- hidden hyperparameter tuning；
- raw result 被覆盖。

发生 critical violation 后，受影响结果不能作为 confirmatory evidence，只能作为
exploratory analysis，并必须在报告中显式标记。

## 2. Primary Research Question

主研究问题：

> How do foundation model capability and structured scientific knowledge
> jointly determine the utility of AI-generated scientific descriptors for
> catalysis prediction and generalization?

形式化表示：

```text
Q = f(M, K)
```

本文不预设：

- knowledge 一定比 model 更重要；
- stronger model 一定在所有 K 下更好；
- larger KG 一定单调提升表现；
- interaction 一定为正。

### 2.1 v2 scope amendment requirement

下一版 protocol 必须在任何新 outcome-bearing run 前操作化定义：

```text
K = (quantity, domain diversity, task coverage, structure, provenance)
```

并冻结：

- `Small`：当前冻结的 6691 篇分子筛论文（8927 个 main/SI 结构化文档）；
- `Medium`：Small 加 MOF/COF/adsorption 等邻近领域；
- `Large`：Medium 加 catalysis/surface science/coordination/strain/transport 等
  跨领域知识；
- quantity-matched diversity controls；
- No-KG、LLM-only、raw RAG、evidence KG 和 shuffled KG baselines；
- benchmark literature leakage 和 direct-answer leakage controls；
- hypothesis hit rate、descriptor gain、OOD gain、evidence quality 和
  cross-domain transfer endpoints。

当前 Small corpus 的 exact count 和 hashes 已冻结；raw-source license 与
DOI/title/year semantic-dedup 仍需签字确认。Small KG MVP 先跑通一个 public
benchmark 的完整 Evidence -> Hypothesis -> Descriptor -> Validation -> Feedback
闭环；它是 pipeline go/no-go，不足以单独支持 knowledge-diversity scaling claim。

## 3. Pre-registered Hypotheses

### H-K：Knowledge Scope and Diversity Effect

在 quantity、retrieval 和 inference budget 可比时，知识从 Small/Local 扩展到
Medium/Domain-expanded 和 Large/Cross-domain 会改变并可能提高 primary endpoint。

```text
Q(Large) - Q(Small) != 0
```

方向不预设为必然正向；within-corpus paper quantity 是 secondary effect。

### H-M：Model Capability Effect

在 K 固定时，更高 capability tier 的模型会产生更有用的 descriptor。

```text
dQ/dM > 0
```

### H-MK：Model x Knowledge Interaction

模型从知识中提取科学价值的能力随 model tier 改变。

```text
d2Q/(dM dK) != 0
```

interaction 可以为正或负，不预注册方向。

### H-S：Knowledge Structure Effect

在 approximate token、node、text 和 descriptor budgets 匹配时，真实
evidence-grounded KG 优于 shuffled/corrupted KG。

### H-C：Weak Model Compensation

更强 K 是否可以部分补偿较弱 M，作为 secondary hypothesis。

### H-OOD：Scientific Generalization

Model x Knowledge 产生的 descriptor utility 能迁移到科学合理的 OOD split，
并最终迁移到 private unseen thermocatalysis data。

## 4. Definition of M

`M` 表示 foundation model capability tier，不表示 API 价格或参数量本身。

主实验固定三个 tier：

| Tier | 定义 |
| --- | --- |
| `M1` | weaker/cheaper but instruction-capable model |
| `M2` | intermediate general reasoning model |
| `M3` | stronger reasoning model |

### 4.1 Model selection rule

具体模型必须在 outcome-bearing run 前写入：

```text
research/configs/models/model-registry.v1.json
```

每个模型必须冻结：

- provider；
- model ID；
- model revision 或 provider-visible version；
- API endpoint；
- context limit；
- structured output mode；
- seed support；
- reasoning budget support；
- release/access date；
- capability tier rationale；
- cost accounting method。

Tier 顺序必须在查看本项目 descriptor utility 以前确定。允许参考与本项目
downstream targets 无关的独立 reasoning evidence，但禁止根据本项目结果重新
排序 M1/M2/M3。

### 4.2 Model replacement

provider 停止服务或模型 revision 无法继续访问时：

1. 原 model registry 保留；
2. 创建新的 protocol/model registry version；
3. 替换模型不得只重跑部分有利 condition；
4. 新旧模型结果分开报告。

## 5. Definition of K

`K` 不等同于 KG 节点数量。K 至少由五个维度描述：

```text
K = (quantity, domain diversity, task coverage, structure, provenance)
```

### 5.1 Primary K variable：Knowledge Scope and Diversity

| Scope | Frozen operational meaning |
| --- | --- |
| `Small` | 当前 6691 篇 zeolite local corpus 和 `Small-KG-zeolite-v1` |
| `Medium` | Small 加 MOF、COF、adsorption、confinement、diffusion 等邻近领域 |
| `Large` | Medium 加广义 catalysis、surface science、coordination、strain、thermodynamics、kinetics、transport |

Medium/Large 的 exact inventory、hash 和 inclusion rules 尚未冻结，因此当前不得
运行 scope outcome。正式 v2 必须增加 quantity-matched Local/Mixed/Cross-domain
controls，分离 domain diversity 与更多 papers/tokens 的作用。

### 5.2 Secondary K variable：Legacy Within-corpus Quantity

以下 K20-K100 规则继续约束已冻结的 512-paper thermal infrastructure，但不再是
当前 NMI 主 scaling variable：

| Level | Paper fraction |
| --- | ---: |
| `K20` | 20% |
| `K40` | 40% |
| `K60` | 60% |
| `K80` | 80% |
| `K100` | 100% |

必须满足：

```text
K20 subset K40 subset K60 subset K80 subset K100
```

Nested paper selection 必须：

- 使用固定 selection seed；
- 对 year、topic/domain 和 paper type 进行预注册的 deterministic
  stratification；
- 不读取 downstream target labels；
- 不根据 descriptor performance 调整 paper order；
- 保存 paper list 和 hash。

Thermal Stage 1 nested selection v1 在任何 outcome-bearing run 前进一步冻结为：

```text
corpus: thermal-catalysis-stage1-v1
paper count: 512
selection seed: 20260810
absolute counts: K20=102, K40=205, K60=307, K80=410, K100=512
topic source: first directory after Reaction in source_path
year bins:
  unknown
  pre-1980
  1980-1989
  1990-1999
  2000-2009
  2010-2014
  2015-present
paper type groups:
  research_article
  review_perspective = review + perspective
  other = book_chapter + communication + conference + other + unknown
```

选择算法固定为 `proportional_stratified_hash_order.v1`：

1. 以 `topic source x year bin x paper type group` 定义 stratum；
2. 在每个 stratum 内，以固定 seed、paper ID、archive entry、PDF hash 和
   structured JSON hash 生成 deterministic hash order；
3. 以 stratum 内 fractional rank 进行 proportional interleaving；
4. `K20/K40/K60/K80/K100` 分别取同一个完整顺序的前
   `102/205/307/410/512` 篇。

禁止以 coverage、descriptor、model、validation/test metric 或 private outcome
重新排序。Coverage 在 exact public predictive dataset 冻结前记录为
`not_measured`，不能作为 selection input。

该 legacy quantity corpus 的 domain 为 `thermal_catalysis`。它服务于辅助
within-corpus quantity analysis，不决定当前 public benchmark 或 Small/Medium/Large
scope 的 domain。

Photocatalysis 作为 secondary cross-domain/transfer analysis，不进入 primary
knowledge-scaling endpoint，除非在第一个 outcome-bearing run 前通过 protocol
amendment 明确提升为 co-primary。

当前已冻结第一个绝对知识规模锚点：

```text
K247-photocatalysis-v1
paper count: 247
```

该 snapshot 是后续 absolute-size infrastructure 的冻结锚点，不允许被
更大或更新的光催化语料覆盖。任何修正必须创建新的 snapshot version。

`K20/K40/K60/K80/K100` 是 within-corpus nested fraction aliases。所有论文图表
同时报告 exact absolute paper count 和 snapshot ID，不能只报告模糊的百分比。

### 5.3 Knowledge Coverage

Coverage 是被测量的 mediator，不是根据 test outcome 优化的变量。

每个 benchmark task 记录：

- relevant evidence universe；
- snapshot 中相关 evidence 数量；
- evidence recall/coverage；
- retrieval recall@k；
- missing evidence categories。

禁止仅用总论文数作为 coverage 的替代指标。

### 5.4 Knowledge Structure

Structure ablation 至少包含：

| Code | Condition |
| --- | --- |
| `K-none` | No external knowledge |
| `K-rag` | Raw text / standard RAG |
| `K-entity` | Entity-level KG |
| `K-experiment` | Experiment/observation KG |
| `K-evidence` | Evidence-grounded KG |
| `K-shuffled` | Token-matched shuffled KG |
| `K-oracle` | Oracle evidence, secondary diagnostic only |

当前 Small MVP 使用 `K-none`、`K-rag` 和 `K-evidence`；`K-shuffled` 在任何
structure claim 前必须加入。K20-K100 structure ablation 只属于 legacy secondary
quantity analysis。

## 6. Definition of Q

Q 是分层指标集合，但 confirmatory claim 只使用预注册 primary endpoint。

### 6.1 Primary Endpoint

每个 benchmark 的 primary endpoint 是其原论文 primary metric 上，
benchmark-native pipeline 使用 `D0 + X` 相对于原 descriptor baseline `D0` 的
paired normalized improvement。模型、preprocessing、split、tuning budget 和
metric implementation 在两组之间保持一致。

对于 lower-is-better error metric：

```text
Q_primary =
  (Error_D0,locked - Error_D0+X,locked)
  / Error_D0,locked
```

对于 higher-is-better score：

```text
Q_primary =
  (Score_D0+X,locked - Score_D0,locked)
  / abs(Score_D0,locked)
```

解释：

- `Q_primary > 0`：`D0 + X` 优于原论文 `D0` baseline；
- `Q_primary = 0`：与原论文 `D0` baseline 相同；
- `Q_primary < 0`：condition 更差；
- higher is better。

每个 task、split 和 seed 使用配对 `D0` baseline。跨 task 聚合时每个 task
权重相同，不按样本量加权。

Primary endpoint 使用 benchmark-native locked test。若原论文或冻结 benchmark
支持科学合理 OOD split，则 OOD 是优先 primary view；否则不得为追求 OOD 标签而
偏离原 benchmark，IID/其他 native test 与 OOD secondary view 必须事先登记。

### 6.2 Secondary Endpoints

Prediction：

- benchmark-native primary metric；
- OOD MAE；
- OOD R2；
- OOD Spearman；
- OOD Pearson；
- IID RMSE/MAE/R2/Spearman/Pearson；
- uncertainty calibration when applicable。

Descriptor：

- schema validity rate；
- executable rate；
- evidence grounding rate；
- unsupported hypothesis rate；
- invalid formula rate；
- unit validation rate；
- missingness；
- zero-variance rate；
- redundancy rate；
- utility contribution；
- novelty x utility quadrant。

Common-model diagnostic：

- 统一 Ridge 上的 paired `D0` vs `D0 + X` delta；
- descriptor-only 与 `D0 + X` 两种 feature views；
- 该诊断不得替代 benchmark-native primary conclusion。

Scientific reasoning：

- claim correctness；
- mechanistic consistency；
- cross-paper reasoning；
- falsifiability；
- contradiction handling。

Data efficiency：

- 10%、20%、40%、60%、100% training fractions；
- learning-curve area；
- small-data delta。

Optimization：

- top-k enrichment；
- hit rate；
- best-found value；
- normalized regret；
- samples required to reach target。

Private validation：

- 与 public primary endpoint 相同的 locked metric；
- supplementary MAE、R2 和 ranking metrics；
- 不在看到 private outcome 后更换 primary metric。

### 6.3 Prohibited endpoint behavior

禁止：

- 从 secondary metrics 中挑一个显著结果代替 primary；
- 只报告最好模型、最好 K 或最好 seed；
- 在 test outcome 后改变 `D0` baseline 或 benchmark-native model；
- 删除 negative Q；
- 把 descriptor validity 当作 predictive utility；
- 把 temporal benchmark 当作 contamination-resistant proof。

## 7. Public Dataset Freeze

### 7.1 Current blocking fact

当前仓库的两个 ZIP 是 literature corpora，不是包含 downstream target 的
AI-ready predictive datasets。

因此 exact public dataset 尚不能从当前仓库事实中指定。禁止把 literature
observation 节点临时拼成 prediction dataset 后直接用于 confirmatory analysis，
除非该构建过程单独经过 dataset protocol、deduplication 和 leakage audit。

### 7.2 Activation requirement

开始任何 outcome-bearing run 前，必须创建并锁定：

```text
research/configs/datasets/public-registry.v1.json
research/manifests/datasets/<dataset_id>.manifest.json
research/manifests/splits/<dataset_id>-iid-v1.json
research/manifests/splits/<dataset_id>-ood-v1.json
```

每个 primary public dataset 必须冻结：

- dataset ID 和 version；
- source 和 license；
- raw file SHA256；
- sample ID；
- target name、definition、units；
- allowed raw inputs；
- forbidden/leaky inputs；
- catalyst/reaction/material grouping；
- missing data policy；
- duplicate policy；
- IID split；
- OOD split；
- split hashes。

Full confirmatory study 至少需要 3 个 eligible primary tasks。Task 可以是不同
公开数据集，也可以是同一公开数据集中预注册的不同 target/reaction-family
任务，但必须在 descriptor generation 前定义。少于 3 个 tasks 时可以运行
pilot 或 case study，但不能满足本文 17.2 中的跨 task knowledge-scope scaling 判据。

### 7.3 Dataset eligibility

Primary public dataset 必须：

- 属于已注册的 zeolite、porous materials、adsorption 或 catalysis scientific scope；
- 有机器可读 target；
- 有 descriptor computation 所需原始输入；
- 样本身份可稳定定义；
- 足以构造科学合理 OOD group；
- license 允许研究和结果发布；
- 不包含 private unseen data；
- 不与 literature corpus 的抽取错误形成明显 label leakage。

Exact dataset 未登记前，protocol 保持 `ACTIVATION_BLOCKED`。

## 8. Train / Validation / Test Policy

### 8.1 IID split

Secondary IID analysis 使用：

```text
train:      60%
validation: 20%
test:       20%
```

要求：

- 按稳定 sample ID 划分；
- 必要时按 target quantile stratify；
- 同源重复样本不得跨 split；
- split seed 固定为 `20260810`；
- membership 写入 manifest。

### 8.2 OOD split

Primary analysis 使用 group-aware OOD split。

优先 grouping 顺序：

1. catalyst/material family；
2. reaction family；
3. framework/composition family；
4. laboratory/source batch。

具体 grouping 由 dataset registry 冻结，禁止根据 model performance 选择最有利
的 OOD definition。

每个 OOD fold：

- held-out group 作为 test；
- 其余 group 中再固定一个 validation group 或 group-aware validation split；
- 所有 preprocessing 只 fit 在 train；
- task 数量足够时使用多个预注册 held-out groups，并等权聚合。

### 8.3 Label visibility

Descriptor generation 模型可以看到：

- scientific task description；
- target name、definition 和 units；
- allowed input column dictionary；
- input units；
- public literature/KG context；
- train input 的非标签 schema 和预注册 summary。

Descriptor generation 模型不能看到：

- validation labels；
- test labels；
- private labels；
- test performance；
- row-level target values；
- `D0` baseline test metrics。

Training labels只能由 downstream training/selection code 访问。

## 9. Descriptor Budget and Selection

### 9.1 Fixed budgets

每个 Model x Knowledge condition、task、generation seed：

```text
candidate descriptor budget: 30
selected descriptor budget:  10
```

所有 baseline 也必须提供 10 个 descriptor slots。

### 9.2 Validation and selection

流程固定为：

```text
generate <= 30 candidates
  -> schema validation
  -> evidence validation
  -> safe compilation
  -> train-only numerical validation
  -> deterministic ranking
  -> select 10 slots
```

Deterministic ranking 在 outcome-bearing run 前冻结。允许的 ranking signals：

- schema completeness；
- evidence support；
- physical interpretability；
- executable status；
- train-only missingness；
- train-only variance；
- train-only redundancy；
- optional train-CV utility，若使用必须对所有 conditions 相同。

### 9.3 Failed descriptor slots

如果 candidate budget 用尽后不足 10 个 valid descriptors：

- 不允许人工补写；
- 不允许继续无限生成；
- 缺失 slot 使用固定 null feature；
- null feature 在 downstream preprocessing 后保持常量；
- failure type 进入 manifest；
- condition 仍进入 intention-to-generate analysis。

这样可以保持 10 个 nominal slots，并让 descriptor generation/execution failure
自然降低 condition utility。

### 9.4 Benchmark D0 descriptors

原论文 `D0` descriptor baseline 必须：

- 在 Model x KG outcome 前冻结；
- 完整复现原论文使用的 descriptor set，不受 AI descriptor 10-slot budget 限制；
- 每个有定义、单位、input mapping，以及可验证的 code/artifact identity；
- 不使用 test/private outcome 选择；
- 由 domain experts 审核并保留版本。

## 10. Model x Knowledge Matrices

### 10.1 Current Small KG MVP

当前先使用一个冻结的 foundation model 和 Single-Agent，比较：

```text
Knowledge: LLM-only, Raw RAG, Small KG + RAG
Seeds:     17, 43, 101
Benchmark: one frozen eligible public benchmark
Downstream: benchmark-native D0 vs D0 + X
```

Multi-Agent 暂缓。Shuffled KG 在形成任何 knowledge-structure claim 前必须加入，
但不阻塞前三条件的 pipeline smoke/pilot。

### 10.2 Scope expansion matrix

Small MVP 通过后，v2 protocol 必须在 outcome 前冻结：

```text
Knowledge scope: Small, Medium, Large
Models:          registered M1, M2, M3 or a justified frozen subset
Seeds:           17, 29, 43, 71, 101
Controls:        quantity-matched Local/Mixed/Cross-domain and shuffled KG
```

Small/Medium/Large 表示 domain scope，不表示 500/2000/6691 papers。Multi-Agent
是否进入 scope matrix 必须单独预注册角色、调用次数和总 token budget。

### 10.3 Legacy within-corpus quantity matrix

`K20/K40/K60/K80/K100` 仅保留为 512-paper thermal corpus 的 secondary
within-corpus quantity infrastructure，不是当前 Small/Medium/Large 主变量。Oracle
evidence 只用于区分 retrieval failure 和 reasoning failure，不作为现实 system
performance baseline。

## 11. Prompt and Inference Budget

### 11.1 Shared prompt rule

所有 M/K conditions 必须使用相同：

- prompt family；
- prompt version；
- output schema；
- task wording；
- descriptor candidate/selection budget；
- evidence formatting；
- safety and epistemic instructions。

只能变化：

- registered model；
- registered knowledge condition；
- seed；
- task-specific frozen inputs。

### 11.2 Frozen default budget

Descriptor generation 默认预算：

```text
temperature:               0.20
max output tokens:         8000
retrieval candidate top-k: 30
model-visible evidence:    <= 18 evidence items
canonical evidence budget: 12000 tokens
transport retry limit:     2
schema repair limit:       2
responses per seed:        1
```

Canonical tokenizer 的名称和 revision 必须在 prompt registry 中冻结。各 provider
实际 input/output token 数同时记录。

Raw RAG、Evidence KG 和 Shuffled KG 的 model-visible evidence token 数差异必须
控制在 canonical budget 的 `+/- 2%` 内。

### 11.3 Reasoning budget

统一使用 registry 中的 `standard` reasoning budget class。

每个 provider 必须把 `standard` 映射为明确参数或声明 unsupported。禁止根据
单个 condition 的表现临时提高 reasoning budget。

### 11.4 Retry rule

允许 retry：

- network error；
- timeout；
- provider 5xx；
- empty response；
- invalid JSON/schema。

不允许因以下原因 retry：

- descriptor 看起来不新颖；
- utility 预期不高；
- hypothesis 不符合研究者偏好；
- 模型结论与期望不符。

所有 attempts 均保存。

## 12. Downstream ML

### 12.1 Primary model

Primary downstream model 是每个 benchmark 原论文的模型或严格登记的等价复现。
其模型 family、software revision、preprocessing、split、hyperparameter search
space、selection metric 和计算预算必须在 outcome-bearing run 前冻结。`D0` 与
`D0 + X` 只能改变新增 descriptor，不得改变其他训练条件。

### 12.2 Primary feature analysis

Primary incremental analysis 使用：

```text
D0 benchmark descriptors
+
condition-specific descriptor slots X
```

并与同一 benchmark-native pipeline 的 `D0` 配对比较。这直接检验新 descriptor
能否改变原研究的预测或科学结论。

Secondary descriptor-only analysis 使用：

```text
condition-specific descriptor slots X only
```

用于诊断 X 的独立信息，但不替代 primary incremental result。所有 knowledge
conditions 使用相同 D0、slot 数和 null-feature failure policy。

### 12.3 Preprocessing

必须在 train-only fit：

- numeric median imputation；
- frozen missing indicator policy；
- categorical one-hot encoding；
- benchmark-native scaling/encoding policy；
- no target-derived preprocessing；
- no test distribution fitting。

### 12.4 Hyperparameter tuning

Benchmark-native hyperparameter space 和 tuning budget 在 outcome-bearing run
前冻结。所有 conditions：

- 使用同一 grid；
- 使用同一 validation split；
- 使用同一 trial 数；
- 使用同一 selection metric；
- 不在 test 上选择 hyperparameters。

### 12.5 Common-model diagnostic

统一 Ridge 是预注册的 secondary representation diagnostic。它使用相同的
train-only preprocessing、alpha grid、split、seeds 和 metric implementation，
比较 `D0` 与 `D0 + X`，用于判断 descriptor utility 是否依赖 benchmark 原模型。
它不替代 benchmark-native primary conclusion。其他 secondary model 只有在
public dataset registry 冻结后、查看 outcome 前预注册才可启用。

## 13. Seeds and Repetition

### 13.1 Full study seeds

```text
17, 29, 43, 71, 101
```

同一个 seed index 控制：

- model seed when supported；
- KG corruption；
- descriptor tie-breaking；
- downstream model；
- data-efficiency subsampling。

### 13.2 Unsupported model seed

如果 provider 不支持 seed：

- request 中不伪造 seed；
- manifest 标记 unsupported；
- 使用五次独立 API calls 作为 stochastic replicates；
- provider request IDs 和 timestamps 保留。

### 13.3 Reporting

必须报告：

- 所有 seeds；
- mean、standard deviation；
- confidence interval；
- failure count；
- 不只报告 best seed。

## 14. KG Scale Construction

### 14.1 Source corpus

当前 primary literature corpus 候选为：

```text
data/thermal-catalysis-stage1.zip
SHA256:
f0161fb2ee27a643831fb57392d304a1f6c139175b16ffd446c3f0d8921b5af5
```

在 snapshot 构建前必须重新验证 archive hash 和每个 JSON record hash。

### 14.2 Selection

Paper selection algorithm：

1. 建立稳定 paper ID；
2. deduplicate DOI/SHA/title-year；
3. 按 frozen strata 分组；
4. 在每个 stratum 内使用 hash-based deterministic order；
5. 按累计 20/40/60/80/100% 取 nested prefixes；
6. 生成 paper list hash；
7. 构建 snapshot；
8. 计算 coverage，但不据此重排。

### 14.3 Snapshot manifest

每个 snapshot 必须保存：

- snapshot ID；
- corpus ID/hash；
- exact paper list；
- paper list hash；
- node/edge counts；
- relation distribution；
- topic/domain distribution；
- year distribution；
- evidence validation distribution；
- task coverage；
- generation config/hash；
- code commit；
- snapshot hash。

### 14.4 Shuffled KG

Shuffled KG 必须保留：

- node records；
- evidence text；
- node type distribution；
- edge count；
- approximate token count。

仅随机预注册 relation endpoints/associations。必须保存 permutation mapping 和 seed。

禁止通过明显破坏文本可读性制造过弱的负对照。

## 15. Tuning Policy

### 15.1 Freeze 前允许

只使用 development-only tasks 和 train/validation data 时允许：

- 修复代码 bug；
- 调整 schema validator；
- 选择 prompt wording；
- 选择 benchmark-native hyperparameter space 和统一 Ridge diagnostic alpha grid；
- 选择 retrieval implementation；
- 选择 descriptor ranking rule；
- 确定 model registry；
- 确定 public dataset 和 split；
- 确定 OOD groups。

所有选择必须在 first outcome-bearing matrix run 前锁定。

### 15.2 Freeze 后允许

- 修复纯 operational failure；
- 重试完全相同 request；
- 增加日志；
- 修复不改变 scientific output 的显示问题；
- 完成预注册的剩余 conditions。

### 15.3 Freeze 后禁止

- 修改 primary endpoint；
- 修改 dataset/splits；
- 修改 model tier；
- 修改 prompt；
- 修改 KG membership；
- 修改 descriptor budget；
- 修改 candidate budget；
- 修改 selection rule；
- 修改 downstream model/grid；
- 修改 seeds；
- 根据 test/private outcome 人工修复 descriptors；
- 删除失败结果。

### 15.4 Scientific bug

如果发现会改变 scientific output 的 bug：

1. 暂停受影响分析；
2. 创建 amendment；
3. 修复并增加 regression test；
4. 所有受影响 conditions 全量 rerun；
5. 原结果保留并标记 invalidated。

## 16. Statistical Analysis

### 16.1 Primary model

Small KG MVP 只在一个 benchmark 上验证闭环，不用于宣称 scope scaling。其主分析
对每个 generation seed 计算 benchmark-native paired `Q_primary(D0 + X vs D0)`，
报告所有 seeds、失败数、effect estimate 和 bootstrap confidence interval。

完整 v2 scope study 的 confirmatory model 为：

```text
Q_primary
  ~ Model
  + KnowledgeScope
  + Model:KnowledgeScope
  + task random intercept
  + seed blocking/repeated effect
```

其中：

- Model 作为 categorical fixed effect；
- `KnowledgeScope` 为 Small、Medium、Large categorical/ordered effect；
- quantity-matched Local/Mixed/Cross-domain controls 单独估计 diversity effect；
- task 权重相同；
- seed 作为重复 block；
- 报告 model、scope、diversity、structure 和 interaction effects。

同时使用 hierarchical bootstrap 对 task 和 seed 进行 10,000 次 resampling，
生成 primary effects 的 95% confidence intervals。

### 16.2 Multiple comparisons

Primary hypotheses：

- H-K；
- H-M；
- H-MK；
- H-S。

H-K 为唯一 primary scaling hypothesis。H-M、H-MK、H-S 为 key secondary
hypotheses，并使用 Holm correction。

其余 metrics 标记为 secondary/exploratory，并报告 exact estimates 和 intervals，
不只报告 p-values。

### 16.3 Missing and failed runs

- operational failure 必须按相同 retry policy 尝试；
- 无法完成的 run 保留并报告；
- scientific failure 不能删除；
- descriptor failure 通过 null slots 进入 primary utility；
- 大规模 provider outage 可触发 protocol amendment，但不能选择性排除低分 runs。

## 17. Pre-registered Claim Criteria

### 17.1 何时认为一个 KG-derived descriptor 得到支持

必须同时满足：

1. benchmark-native `D0` baseline 在预注册 tolerance 内复现；
2. descriptor 有冻结的 hypothesis、evidence、formula、allowed inputs 和 code hash；
3. paired `D0 + X` 相对 `D0` 达到 benchmark manifest 中预注册的 minimum
   meaningful effect；
4. confidence interval 和 seed consistency 满足该 benchmark 的冻结判据；
5. 没有 critical protocol violation、target leakage 或隐藏人工修复。

未达到效应判据的 hypothesis 必须标记为 `rejected` 或 `inconclusive`，不得删除。
单 benchmark MVP 只能支持该 task 上的 descriptor 结论，不能支持普遍 KG scaling。

### 17.2 何时认为 Knowledge Scope Scaling 成立

完整 v2 study 必须同时满足：

1. `KnowledgeScope` average marginal effect 为正且 95% confidence interval 下界大于 0；
2. Large 相对 Small 达到 v2 protocol 预注册的 minimum meaningful effect；
3. 至少两个 model tiers 和至少三分之二 eligible tasks 方向一致；
4. quantity-matched controls 显示结果不能仅由更多 papers/tokens 解释；
5. 没有 critical protocol violation 或 unresolved leakage。

如果只满足部分条件，措辞只能是：

```text
suggestive or task-dependent knowledge-scope trend
```

不能声称 knowledge-scope scaling 已成立。K20-K100 结果只允许表述为 secondary
within-corpus quantity effect。

### 17.3 何时认为 Structured Knowledge Effect 成立

必须满足：

1. 在同一 frozen scope 的 token-matched 对照中：

```text
Q_primary(Evidence KG) - Q_primary(Shuffled KG) >= 0.02
```

且 95% confidence interval 下界大于 0；

2. Evidence KG 相对 Raw RAG 的差值方向为正；
3. 优势不能由 descriptor 数量、input token、downstream tuning 或
   retrieval count 差异解释。

如果 Evidence KG 不优于 Shuffled KG，只能声称“more accessible information”
或“coverage effect”，不能声称 scientific structure matters。

### 17.4 何时认为 Model Scaling 或 Model x Knowledge Interaction 成立

Model scaling 必须同时满足：

1. M3 对 M1 的 average marginal difference 在 primary endpoint 上为正；
2. 95% confidence interval 下界大于 0；
3. M3 优势在至少两个 knowledge scopes 上方向一致；
4. 模型之间 prompt、input/output budget 和 descriptor budget 匹配。

Interaction 必须满足：

1. Primary model 的 `Model:KnowledgeScope` interaction 通过 corrected threshold；
2. interaction effect 的 95% confidence interval 不跨 0；
3. interaction 达到 v2 protocol 冻结的 minimum meaningful effect；
4. interaction 不是单一 task 或单一 seed 驱动。

正 interaction 可支持 stronger model extracts disproportionately more value。

负 interaction 可支持 stronger knowledge compensates weaker models，不能被当作失败
删除。

### 17.5 Private Generalization Claim

只有 private blind test 在 frozen pipeline 下重复观察到：

- positive K effect；
- positive model effect，或明确可解释的 model-dependent pattern；
- public 方向一致的 interaction；
- Evidence KG 优于 shuffled/control；

才能支持：

```text
AI-generated scientific representations generalized to previously unseen
scientific data.
```

禁止声称：

```text
AI discovered completely new physical laws.
```

## 18. Pilot Go / Revise / Stop Criteria

### 18.1 GO

Small KG MVP 认为 pipeline ready 需要同时满足：

1. 至少 90% planned runs 完成；
2. 无 critical protocol violation；
3. 至少 80% descriptor slots 可执行，或 failure policy 可稳定处理；
4. benchmark-native `D0` baseline 在冻结 tolerance 内复现；
5. evidence bundle provenance 完整且 retrieval audit 通过；
6. primary pipeline 对重复运行稳定；
7. 没有明显 label leakage；
8. supported、rejected、inconclusive 和 execution failure 全部保留。

Pilot 不要求 KG 优于 RAG 或 LLM-only，也不要求统计显著。负结果本身不是 pipeline
failure；只有证据表明结果来自数据、retrieval、execution 或 protocol 缺陷时才 redesign。

### 18.2 REVISE BEFORE SCALE-UP

出现以下情况时不扩库，先定位原因：

- completion 在 70% 至 90%；
- executable descriptor slots 在 50% 至 80%；
- `D0` baseline 复现接近但未达到 tolerance；
- Raw RAG 与 Evidence KG 无法区分；
- shuffled control 偶尔优于 real KG；
- 不同 task 方向强烈冲突；
- primary metric seed variance 过大。

优先 debug 顺序：

```text
data leakage
-> split
-> descriptor execution
-> retrieval
-> evidence coverage
-> prompt/schema
-> benchmark task
-> downstream evaluation
```

### 18.3 STOP / REDESIGN

以下任一情况触发停止或重大 redesign：

- critical leakage；
- completed runs 低于 70%；
- executable descriptor slots 低于 50%；
- benchmark-native `D0` baseline 无法复现；
- 数据缺少计算新 descriptor 所需的 allowed raw inputs；
- 结果主要由隐藏人工修复产生；
- primary dataset 无法形成可信的 locked test 或科学合理 evaluation。

Stop 不代表项目失败，而是说明当前 task、retrieval、descriptor 或 evaluation
设计不足以测试主问题。真实、稳定的 non-positive KG outcome 必须作为 negative
scientific result 保留，不能作为删除条件。禁止在 pipeline 无效时盲目增加论文数量
或模型数量。

## 19. Private Data Firewall

### 19.1 Team separation

AI team：

- 不查看 private labels；
- 不接收 private performance 的逐样本输出；
- 不根据 private result 调整 descriptor。

Data-generation/evaluation team：

- 不根据 AI descriptor 修改 private experiment inclusion；
- 不向 AI team 暴露 labels；
- 使用 frozen evaluator。

### 19.2 Storage

Private data：

- 不进入 Git；
- 不进入 public/shared research datasets；
- 不进入 literature KG；
- 不放入普通 `research/datasets/`；
- 使用仓库外受控路径；
- 记录 file hash 和 access log，但 manifest 不包含 raw labels。

### 19.3 Freeze bundle

Blind test 前冻结：

- protocol hash；
- Git commit；
- environment/dependency lock；
- model registry；
- prompt hashes；
- KG snapshot hashes；
- retrieval config；
- hypothesis/descriptor specs；
- executable descriptor code；
- downstream model；
- hyperparameter grid；
- preprocessing；
- evaluation metrics；
- random seeds。

所有内容形成 freeze bundle hash，由项目负责人和独立 evaluator 确认。

### 19.4 One-shot rule

Pristine private evaluation 默认只执行一次。

返回 AI team 的默认结果：

- aggregate primary endpoint；
- aggregate secondary metrics；
- confidence intervals；
- failure counts；
- protocol compliance status。

不返回 raw labels 或逐样本 prediction/label pairs。

如查看结果后修改方法再运行：

- 新运行不能称为 pristine blind test；
- 必须标记为 post-blind exploratory；
- 原始 blind result 永久保留。

## 20. Negative Results

必须保留：

- descriptor generation failure；
- schema invalid；
- invalid formula；
- unsafe expression；
- non-computable；
- unit mismatch；
- missingness failure；
- zero variance；
- redundant descriptor；
- physically meaningless descriptor；
- performance-decreasing descriptor；
- unsupported hypothesis；
- retrieval failure；
- contradictory evidence；
- API/timeout failure。

论文和报告必须给出：

- 总候选数；
- 各失败类型数量和比例；
- valid/executable/selected counts；
- utility distribution；
- negative Q distribution；
- failed condition denominator。

## 21. Reporting Rules

所有主表和主图必须来自 immutable run artifacts 自动生成。

至少输出：

```text
JSON  machine-readable results
CSV   analysis tables
MD    human-readable report
PNG/PDF figures
```

禁止：

- 手工修改 figure 输入 CSV；
- 手工删除异常点而无规则；
- 只展示成功 descriptor；
- 只展示最好 seed；
- 把 exploratory result 写成 confirmatory。

## 22. Activation Gate

在以下项目全部完成前，不允许将 protocol 状态改为 `ACTIVE`：

- [x] Public dataset registry and fixed-split infrastructure verified
- [ ] Exact eligible public benchmark registered
- [ ] Dataset SHA256 and license recorded
- [ ] Target and allowed inputs frozen
- [ ] IID split manifest frozen
- [ ] OOD grouping and split manifest frozen
- [ ] Benchmark-native D0 descriptors and baseline frozen
- [ ] M1/M2/M3 identities and revisions frozen
- [ ] Canonical tokenizer frozen
- [ ] Prompt family/version frozen
- [ ] Benchmark-native model reproduction, preprocessing and tuning budget frozen
- [ ] Common Ridge diagnostic grid and preprocessing frozen
- [x] K20/K40/K60/K80/K100 manifests built
- [x] Exact 6691-paper / 8927-document structured corpus and cross-campaign document dedup frozen
- [ ] Raw-source license and DOI/title/year semantic-dedup sign-off completed
- [x] `Small-KG-zeolite-v1` snapshot and strict evidence audit frozen
- [ ] v2 Local/Domain-expanded/Cross-domain protocol and matched controls frozen
- [x] Run manifest implementation verified
- [ ] Private firewall owner and evaluator identified
- [ ] Protocol JSON lock hash generated

## 23. Amendment Log

| Version | Date | Change | Outcome seen before change? | Impact |
| --- | --- | --- | --- | --- |
| v1 | 2026-08-10 | Initial protocol freeze | No Model x KG outcome exists | Establishes rules and activation blockers |
| v1.1 | 2026-08-10 | Registers immutable `K247-photocatalysis-v1` as the first absolute-size scaling anchor | No Model x KG outcome exists | Preserves the current 247-paper corpus as a permanent experimental point |
| v1.2 | 2026-08-11 | Implements public-only dataset manifests, deterministic IID/OOD splits, label-access controls, and structural leakage audit without selecting a dataset | No Model x KG outcome exists | Adds enforcement infrastructure; protocol remains `ACTIVATION_BLOCKED` |
| v1.3 | 2026-08-11 | Freezes the 512-paper thermal corpus identity, exact K20/K40/K60/K80/K100 counts, strata, seed, and proportional deterministic selection algorithm before snapshot construction | No Model x KG outcome exists | Prevents post-outcome corpus ordering changes; coverage remains `not_measured` and protocol remains `ACTIVATION_BLOCKED` |
| v1.4 | 2026-08-25 | Records the new Local/Domain-expanded/Cross-domain scientific scope and makes a frozen Small KG from the candidate 5000-6000 zeolite papers the next pipeline milestone | No Model x KG outcome exists | Preserves v1 snapshots as quantity infrastructure, blocks new outcome-bearing runs until a v2 scope/diversity protocol and exact Small corpus manifest are frozen |
| v1.5 | 2026-09-01 | Records the frozen 6691-paper / 8927-document Small corpus and `Small-KG-zeolite-v1`, including strict provenance verification and remaining data-governance limitations | No Model x Knowledge outcome exists | Closes the Small KG construction gate but keeps benchmark, retrieval, normalization, leakage and protocol activation gates blocked |
| v1.6 | 2026-09-01 | Makes benchmark-native `D0` vs `D0 + X` the primary downstream comparison and moves common Ridge to a secondary diagnostic | No Model x Knowledge outcome exists | Aligns empirical validation with the hypothesis-discovery loop while preserving a common low-complexity cross-benchmark check |
