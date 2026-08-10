# Private Data Protocol

Protocol ID：`private-thermocatalysis-blind-validation.v1`

设计冻结日期：2026-08-10

状态：`DESIGN_FROZEN / PRIVATE_DATA_NOT_OPENED`

本文只定义 private unseen thermocatalysis data 的组织、访问、冻结和盲测规则。
本次工作不读取、不定位、不扫描、不复制任何 private data 或 private labels。

## 1. Purpose

Private thermocatalysis data 的唯一主要用途是：

```text
Contamination-resistant external validation
```

它不是：

- development dataset；
- prompt tuning dataset；
- descriptor selection dataset；
- hyperparameter tuning dataset；
- error analysis dataset；
- 可反复使用的 validation set。

Private validation 要检验 frozen public-data conclusions 是否能迁移到：

- 新产生；
- 未发表；
- 从未公开；
- 不存在于互联网；
- 不可能进入 foundation model pretraining corpus；

的热催化数据。

## 2. Non-negotiable Principles

1. AI team 不能查看最终 private labels；
2. AI team 不能根据 private performance 修改方法；
3. Data team 不能根据 AI descriptors 调整实验、样本或 labels；
4. development 只使用 public/existing data；
5. private data 不进入 Git repository；
6. private data 不进入 literature KG；
7. private data 不进入 prompt；
8. private evaluation 前必须冻结完整方法；
9. blind evaluation 默认 one-shot；
10. 所有访问、hash、执行和结果发布均需审计。

## 3. Roles

### 3.1 AI Team

负责：

- public literature/KG；
- model and prompt；
- hypothesis and descriptors；
- descriptor computation code；
- public downstream ML；
- public evaluation；
- freeze bundle。

禁止：

- 查看 private target labels；
- 查看逐样本 private prediction errors；
- 访问 private raw label files；
- 根据 private aggregate result 修改 descriptor；
- 要求 Data Team 补做有利样本；
- 将 private information 加入 KG 或 prompt。

### 3.2 Data-Generation Team

负责：

- 生成 private experiments；
- 定义 measurement protocol；
- 执行预先设定的 quality control；
- 完成 sample inclusion/exclusion；
- 维护 raw data 和 labels。

禁止：

- 根据 AI descriptor set 修改实验设计；
- 根据 AI model preference 删除样本；
- 根据 preliminary AI predictions 修正 labels；
- 在看到 AI descriptor 后选择性增加有利 experiments；
- 向 AI team 泄露 labels 或结果方向。

### 3.3 Data Custodian

独立维护：

- private storage；
- access permissions；
- private dataset manifest；
- file hashes；
- access log；
- dataset lock。

Data Custodian 不参与 descriptor selection。

### 3.4 Independent Evaluator

负责：

- 验证 freeze bundle；
- 在受控环境运行 frozen pipeline；
- 计算预注册 metrics；
- 生成 aggregate report；
- 不向 AI team释放 raw labels。

Independent Evaluator 不修改模型、descriptor 或 preprocessing。

### 3.5 Project Lead / Protocol Owner

负责：

- 批准 freeze；
- 确认 public development 已结束；
- 确认 Data Team dataset lock 独立完成；
- 处理 protocol violation；
- 决定结果的 confirmatory/exploratory 状态。

## 4. Access Matrix

| Asset | AI Team | Data Team | Custodian | Evaluator |
| --- | --- | --- | --- | --- |
| Public literature/KG | Read/write research artifacts | Optional read | No requirement | Read |
| Public predictive data | Read | Optional read | No requirement | Read |
| Private feature schema | Approved schema only | Read/write | Read | Read |
| Private unlabeled inputs | No direct access by default | Read/write | Read | Controlled read |
| Private labels | No access | Read/write | Read | Controlled read |
| Freeze bundle | Create/read | Read summary | Store | Verify/read |
| Private predictions | Aggregate only | No access before final report | Store | Read/write |
| Per-sample errors | No access | No access before final report | Store | Controlled read |

任何超出该矩阵的访问必须先创建 protocol amendment。

## 5. Data Separation

### 5.1 Physical Separation

Private data 必须：

- 存储在 repository 之外；
- 使用独立权限控制目录或 storage account；
- 不位于普通 `research/datasets/`；
- 不通过 Git、Git LFS、issue attachment 或 chat attachment 传播；
- 不复制到 AI team 的开发机器；
- 不出现在 model API request。

### 5.2 Logical Separation

Private dataset loader 只能在 independent evaluation environment 中启用。

Development environment：

- 没有 private path；
- 没有 private credentials；
- 没有 private label schema implementation；
- mock/synthetic data 用于接口测试。

### 5.3 Logging

Custodian 记录：

- actor；
- timestamp；
- asset；
- action；
- purpose；
- approval；
- result；
- file hashes before/after。

访问日志不可由 AI team 修改。

## 6. What AI Team May Know Before Freeze

AI team 可以在 Data Team 独立确定后获得：

- feature/column names；
- units；
- data types；
- allowed value ranges；
- missing-value conventions；
- target name and units；
- sample ID contract；
- evaluation interface；
- scientific domain description。

AI team 不可以获得：

- row-level target values；
- target distribution；
- correlation with candidate descriptors；
- best/worst samples；
- private subgroup performance；
- preliminary model score；
- labels disguised as rankings or categories。

如果 feature distribution 本身可能泄露 labels，默认也不提供。

## 7. Data-Team Independence Rule

Data Team 必须在看到最终 AI descriptor set 以前冻结：

- experimental protocol；
- sample generation plan；
- measurement method；
- inclusion/exclusion criteria；
- quality-control thresholds；
- replicate handling；
- target calculation；
- missing/failed experiment policy；
- final sample list。

Data Team dataset lock 至少包含：

```text
private_dataset_id
dataset_version
sample_count
sample_id_hash
feature_file_hash
label_file_hash
measurement_protocol_hash
inclusion_exclusion_hash
quality_control_hash
locked_at
approved_by
```

Dataset lock 可以由 Custodian 和 Project Lead 验证，但 label hash 和 raw label
path 不向 AI team 暴露。

如果 Data Team 在 descriptor disclosure 后新增或修改数据：

- 新数据不能并入原 pristine private set；
- 必须建立独立 `post-disclosure` dataset version；
- 只能作为 exploratory follow-up；
- 原 private set 保持不变。

## 8. Freeze Timing

Freeze 发生在：

1. public dataset 已锁定；
2. public train/validation/test 和 OOD splits 已锁定；
3. public pilot 和允许的 development 已结束；
4. final Model x Knowledge method 已选定；
5. descriptor generation 不再修改；
6. descriptor execution 通过 public/synthetic tests；
7. downstream ML 和 evaluation 已锁定；
8. private dataset inclusion/QC 已由 Data Team 独立锁定；
9. AI team 尚未查看任何 private outcome；
10. Independent Evaluator 已确认环境可执行。

Freeze 必须发生在 private evaluator 第一次加载真实 private labels 以前。

## 9. What Must Be Frozen

### 9.1 Knowledge Graph

冻结：

- exact KG snapshot ID；
- paper ID list；
- source corpus hash；
- nodes/edges hashes；
- ontology version；
- retrieval configuration；
- evidence/token budget；
- corruption mapping for controls。

### 9.2 Model

冻结：

- provider；
- model ID；
- model revision；
- endpoint；
- temperature；
- seed policy；
- max tokens；
- reasoning budget；
- retry policy；
- timeout；
- concurrency。

### 9.3 Prompt

冻结：

- prompt family；
- prompt version；
- system/user templates；
- rendered static instructions；
- prompt hashes；
- structured output schema；
- schema repair policy。

### 9.4 Descriptor Set

冻结：

- descriptor IDs；
- complete DescriptorSpecifications；
- order；
- selected count；
- failed/null slots；
- evidence/claim links；
- formula；
- units；
- assumptions；
- applicable domain。

### 9.5 Descriptor Computation Code

冻结：

- expression/implementation；
- source code hash；
- allowed input mapping；
- units conversion；
- missing-value behavior；
- clipping/domain rules；
- runtime/dependency lock；
- feature output schema；
- test vectors and expected hashes。

### 9.6 Downstream ML

冻结：

- model architecture；
- library/version；
- feature set/order；
- training procedure；
- validation selection rule；
- final fitting rule；
- random seeds；
- prediction output contract。

### 9.7 Hyperparameters

冻结：

- complete search grid；
- trial budget；
- selection metric；
- tie-breaking；
- selected values or deterministic selection procedure；
- early stopping；
- regularization；
- acquisition/optimization settings。

### 9.8 Preprocessing

冻结：

- numeric imputation；
- categorical encoding；
- scaling；
- missing indicators；
- outlier policy；
- duplicate handling；
- units conversion；
- train-only fit policy；
- column ordering。

### 9.9 Evaluation Metrics

冻结：

- primary endpoint；
- secondary endpoints；
- aggregation；
- task/sample weighting；
- confidence interval method；
- bootstrap seeds/replicates；
- failure handling；
- subgroup policy；
- optimization metrics。

### 9.10 Additional Required Freeze Items

同时冻结：

- experiment protocol hash；
- Git commit；
- clean working-tree requirement；
- environment lock；
- public dataset/split hashes；
- model registry hash；
- reporting code；
- evaluator version；
- output redaction policy。

## 10. Freeze Bundle

AI Team 创建 machine-readable freeze bundle：

```json
{
  "freeze_bundle_id": "",
  "protocol_hash": "",
  "git_commit": "",
  "git_tree": "",
  "git_dirty": false,
  "environment_hash": "",
  "kg_snapshot": {},
  "model_registry_hash": "",
  "model_config": {},
  "prompt_hashes": {},
  "descriptor_set_hash": "",
  "descriptor_code_hash": "",
  "downstream_config_hash": "",
  "hyperparameter_config_hash": "",
  "preprocessing_hash": "",
  "evaluation_config_hash": "",
  "public_dataset_hashes": {},
  "created_at": "",
  "approved_by": []
}
```

Freeze bundle 必须：

- 自身生成 SHA256；
- 由 AI Team、Project Lead 和 Independent Evaluator 签字/批准；
- 在 private execution 前通过 verification command；
- 不允许原地覆盖；
- 任何变化产生新 bundle ID。

## 11. Blind Evaluation Workflow

```text
Data Team locks private dataset
  -> Custodian records private hashes
  -> AI Team locks method freeze bundle
  -> Independent Evaluator verifies both locks
  -> Evaluator loads private inputs and labels
  -> Frozen descriptor code computes features
  -> Frozen downstream pipeline predicts
  -> Frozen evaluator computes metrics
  -> Aggregate report is signed and released
```

AI Team 不参与 evaluator 的逐样本运行。

## 12. Result Release

第一次结果释放给 AI Team 时，默认只包含：

- protocol compliance；
- number of eligible/evaluated/failed samples；
- aggregate primary endpoint；
- aggregate secondary metrics；
- confidence intervals；
- aggregate failure counts；
- pre-registered subgroup summaries when allowed。

默认不释放：

- raw labels；
- per-sample predictions；
- residuals；
- sample rankings；
- best/worst examples；
-可用于反推 labels 的小样本 subgroup。

更详细结果只有在 pristine blind conclusion 完成并永久冻结后，按单独批准流程
释放。

## 13. One-shot and Rerun Policy

### 13.1 Allowed Operational Rerun

仅在以下情况下允许保持 pristine status：

- evaluator infrastructure failure；
- file read failure；
- dependency installation failure；
- process interruption；
- 已证明没有成功读取或计算 outcome。

必须使用完全相同 freeze bundle，并记录 failure log。

### 13.2 Scientific Rerun

如果第一次 private metrics 已计算或被任何成员查看，则之后：

- 修改 descriptor；
- 修改 preprocessing；
- 修改 hyperparameters；
- 修改 model；
- 修改 metric；
- 修改 sample inclusion；

都会使新运行成为 `post-blind exploratory`。

原始 blind result 不得替换。

## 14. Private Dataset Failure Handling

预先区分：

- invalid sample；
- missing required input；
- descriptor domain violation；
- computation failure；
- model prediction failure；
- label unavailable；
- protocol exclusion。

失败处理规则必须在 freeze bundle 中定义。

禁止在看到 failure 对 overall score 的影响后改变 exclusion rule。

## 15. Protocol Breach

以下属于 breach：

- AI Team 获得 private labels；
- label 或 outcome 出现在 chat、issue、Git、prompt；
- Data Team 根据 descriptor 修改样本；
- freeze bundle 不完整仍执行；
- evaluator 使用未冻结代码；
- private result 被用于调参；
- access log 缺失或被修改。

发现 breach 后：

1. 立即停止 evaluation；
2. 保存日志和证据；
3. 撤销不必要访问；
4. 标记受影响 dataset/run；
5. Project Lead 决定是否仍可作为 exploratory；
6. 论文中披露；
7. 不得悄悄重新定义 private set。

## 16. Reporting Language

如果 frozen pipeline 在 private data 上复现 public trends，可以表述：

```text
AI-generated scientific representations generalized to previously unseen
scientific data under a pre-specified blind evaluation protocol.
```

不应表述：

```text
AI discovered completely new physical laws.
```

如果 private result 不支持 public trend，也必须完整报告，并讨论：

- public benchmark overfitting；
- knowledge coverage mismatch；
- descriptor domain failure；
- dataset shift；
- model contamination assumptions；
- statistical uncertainty。

## 17. Activation Checklist

在 private data 被 evaluator 加载前必须全部满足：

- [ ] Data Team protocol independently locked
- [ ] Private sample inclusion/exclusion locked
- [ ] Private feature and label hashes recorded by Custodian
- [ ] AI Team has not viewed final private labels
- [ ] Public method development completed
- [ ] KG snapshot frozen
- [ ] Model and revision frozen
- [ ] Prompt and schema frozen
- [ ] Descriptor set frozen
- [ ] Descriptor computation code frozen
- [ ] Downstream ML frozen
- [ ] Hyperparameters frozen
- [ ] Preprocessing frozen
- [ ] Evaluation metrics frozen
- [ ] Git commit and environment frozen
- [ ] Freeze bundle hash generated
- [ ] Independent Evaluator verified bundle
- [ ] Aggregate-only release policy approved
- [ ] Access log enabled

## 18. Current Declaration

截至 2026-08-10：

- 本协议只完成设计冻结；
- 未打开 private data；
- 未读取 private labels；
- 未创建 private dataset path；
- 未执行 private evaluation；
- 未根据 private information 修改任何 descriptor 或实验规则。

## 19. Amendment Log

| Version | Date | Change | Private outcome seen? | Impact |
| --- | --- | --- | --- | --- |
| v1 | 2026-08-10 | Initial private data firewall and blind evaluation protocol | No | Establishes roles, freeze contents and one-shot rules |
