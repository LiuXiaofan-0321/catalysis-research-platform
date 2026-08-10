# Research Implementation Plan

状态日期：2026-08-10

本文档定义目标架构、模块接口、建议文件、CLI、测试和验收标准。它描述依赖关系，
不强制实施顺序。具体执行顺序由项目负责人逐步确认。

## 1. 总体原则

1. 保留现有 production backend/frontend；
2. 论文实验通过 `research/` 从命令行运行；
3. research 默认只读现有生产数据；
4. 所有重大参数进入 versioned config；
5. 所有 run 产生 machine-readable artifacts；
6. completed/failed run 均保留；
7. test labels、private labels 不进入生成和调参；
8. 不为架构美观重写已工作的导入和 UI；
9. 每个模块独立测试和验收；
10. 协议变更必须留下 amendment。

## 2. 已建立的 Research Layout

```text
research/
  configs/
  models/
  kg_snapshots/
  prompts/
  experiments/
  benchmarks/
  descriptors/
  datasets/
  runs/
  evaluation/
  statistics/
  manifests/
  scripts/
  reports/
  src/catalysis_research/
  tests/
```

当前命令：

```bash
npm run research:doctor
npm run research:test
```

## 3. 目标包结构

建议逐步增加：

```text
research/src/catalysis_research/
  cli.py
  layout.py
  config.py
  hashing.py
  logging.py
  protocol.py
  provenance/
    git_state.py
    environment.py
    run_manifest.py
    freeze_bundle.py
  corpora/
    stage1.py
    production_export.py
  kg/
    schema.py
    builder.py
    snapshot.py
    selection.py
    corruption.py
    coverage.py
    retrieval.py
  models/
    base.py
    registry.py
    retry.py
    providers/
      deepseek.py
      openai_compatible.py
  prompts/
    registry.py
    renderer.py
  hypotheses/
    schema.py
    generator.py
    validator.py
  descriptors/
    schema.py
    generator.py
    validator.py
    expression.py
    executor.py
    units.py
    selection.py
    failures.py
  datasets/
    registry.py
    schema.py
    loader.py
    split.py
    leakage.py
  baselines/
    human.py
    llm_only.py
    raw_rag.py
    entity_kg.py
    evidence_kg.py
    shuffled_kg.py
    oracle.py
  downstream/
    preprocessing.py
    ridge.py
    random_forest.py
    xgboost.py
    gaussian_process.py
    tuning.py
  evaluation/
    reasoning.py
    descriptor.py
    prediction.py
    optimization.py
    aggregation.py
  statistics/
    bootstrap.py
    mixed_effects.py
    sensitivity.py
  private_validation/
    freeze.py
    evaluator.py
    access_log.py
```

并非所有文件都必须一次建立。只有对应模块开始实施时才创建。

## 4. Module A：Protocol Registry

### 新增文件

```text
research/src/catalysis_research/protocol.py
research/configs/protocol.v1.json
research/manifests/protocol-lock.json
research/tests/test_protocol.py
```

### 接口

```python
class ExperimentProtocol:
    protocol_version: str
    primary_question: str
    primary_endpoint: dict
    secondary_endpoints: list[dict]
    model_matrix: list[str]
    knowledge_matrix: list[str]
    descriptor_budget: int
    seeds: list[int]
    freeze_rules: dict


def load_protocol(path: Path) -> ExperimentProtocol
def validate_protocol(protocol: ExperimentProtocol) -> list[str]
def lock_protocol(protocol: ExperimentProtocol) -> ProtocolLock
```

### CLI

```bash
python research/scripts/research.py protocol validate \
  --config research/configs/protocol.v1.json

python research/scripts/research.py protocol lock \
  --config research/configs/protocol.v1.json
```

### 测试

- 缺少 primary endpoint 时失败；
- descriptor budget 小于 1 时失败；
- seed 重复时失败；
- lock hash 对相同输入稳定；
- locked protocol 被修改后检测失败。

### 验收

- Markdown 协议和 JSON config 一致；
- protocol hash 可进入所有 run；
- outcome-bearing run 必须引用 protocol lock。

## 5. Module B：Run Manifest and Immutable Runs

状态：`IMPLEMENTED / PIPELINE_INTEGRATION_PENDING`

### 已实现文件

```text
research/src/catalysis_research/provenance/run_manifest.py
research/manifests/schemas/run-manifest.schema.json
research/manifests/README.md
research/configs/runs/example-run-spec.json
research/tests/test_run_manifest.py
```

### Run 目录

```text
research/runs/<run_id>/
  manifest.json
  retrieved_evidence.json
  hypothesis.json
  descriptors.json
  raw_model_output.json|txt
  structured_output.json
  FINALIZED.json
```

大体量 scientific outputs 独立保存，manifest 中记录 relative path、SHA256、
byte count 和 media type。`FINALIZED.json` 锚定终态 manifest hash。

### 核心字段

```json
{
  "run_id": "",
  "status": "running|completed|failed",
  "created_at": "",
  "git_commit": "",
  "git_dirty": false,
  "model_provider": "",
  "model_name": "",
  "model_version": "",
  "temperature": 0,
  "seed": 0,
  "reasoning_budget": {},
  "prompt_version": "",
  "kg_snapshot": "",
  "kg_hash": "",
  "retrieval_mode": "",
  "retrieved_evidence": {},
  "hypothesis": {},
  "descriptors": {},
  "raw_model_output": {},
  "structured_output": {},
  "dataset": {},
  "split": {},
  "downstream_model": {},
  "hyperparameters": {},
  "metrics": {},
  "errors": [],
  "runtime": {},
  "manual_interventions": [],
  "manifest_content_hash": ""
}
```

### 接口

```python
def create_run(*, runs_root: Path, spec: dict, repository_root: Path) -> dict
def record_artifact(*, run_directory: Path, field: str, value: object) -> dict
def record_error(*, run_directory: Path, stage: str, error: BaseException) -> dict
def record_runtime_stage(*, run_directory: Path, stage: str, duration_seconds: float) -> None
def complete_run(*, run_directory: Path, metrics: dict) -> dict
def fail_run(*, run_directory: Path, stage: str, error: BaseException) -> dict
def verify_run(run_dir: Path) -> VerificationReport
```

### CLI

```bash
python research/scripts/research.py run create --config <run-spec>
python research/scripts/research.py run record --run <run-dir> --field <field> --input <file>
python research/scripts/research.py run error --run <run-dir> --stage <stage> --message <message>
python research/scripts/research.py run complete --run <run-dir> --metrics <metrics.json>
python research/scripts/research.py run fail --run <run-dir> --stage <stage> --message <message>
python research/scripts/research.py run verify --run <run-dir>
python research/scripts/research.py run show --run <run-dir>
```

### 验收状态

- [x] every required traceability field is represented；
- [x] completed and failed runs are retained；
- [x] finalized runs reject API mutation；
- [x] artifact、manifest、finalization tampering is detectable；
- [x] dirty Git worktree is rejected by default；
- [x] CLI create/verify is covered by tests；
- [ ] downstream modules must adopt this API before outcome-bearing runs。

### CLI

```bash
python research/scripts/research.py run verify \
  --run research/runs/<run_id>
```

### 测试

- run ID 唯一；
- completed run 不可覆盖；
- artifact hash 可复算；
- failed run 保留 request 和 error；
- dirty Git state 正确记录；
- manifest schema validation。

### 验收

- 任意 run 可被独立审计；
- 不依赖 shell history；
- raw output 和 postprocessed output 同时存在；
- 未记录人工 intervention 的手工修改会导致 hash verification 失败。

## 6. Module C：Corpus Registry and Production Export

### 新增文件

```text
research/src/catalysis_research/corpora/stage1.py
research/src/catalysis_research/corpora/production_export.py
research/manifests/corpora/photocatalysis-stage1.json
research/manifests/corpora/thermal-catalysis-stage1.json
research/tests/corpora/test_stage1.py
```

可选 production 修改：

```text
backend/src/scripts/exportResearchCorpus.ts
backend/package.json
```

### 接口

```python
def inspect_archive(path: Path) -> CorpusManifest
def verify_archive(path: Path, manifest: CorpusManifest) -> VerificationReport
def load_stage1_records(path: Path) -> Iterator[Stage1Artifact]
def export_production_snapshot(database: Path, output: Path) -> ExportManifest
```

### CLI

```bash
python research/scripts/research.py corpus inspect \
  --input data/thermal-catalysis-stage1.zip

python research/scripts/research.py corpus verify \
  --input data/thermal-catalysis-stage1.zip \
  --manifest research/manifests/corpora/thermal-catalysis-stage1.json
```

### 测试

- archive hash；
- document count；
- duplicate identity；
- evidence coverage；
- malformed JSON；
- package/import identity consistency。

### 验收

- research 不直接修改 production DB；
- corpus manifest 覆盖 archive SHA、paper list、record hashes 和 generation metadata；
- identity rule 统一。

## 7. Module D：KG Snapshot Versioning

### 新增文件

```text
research/src/catalysis_research/kg/schema.py
research/src/catalysis_research/kg/selection.py
research/src/catalysis_research/kg/builder.py
research/src/catalysis_research/kg/snapshot.py
research/src/catalysis_research/kg/coverage.py
research/manifests/schemas/kg-snapshot.schema.json
research/configs/kg/thermal-nested-v1.json
research/tests/kg/
```

### Snapshot 目录

```text
research/kg_snapshots/<snapshot_id>/
  manifest.json
  papers.jsonl
  nodes.jsonl
  edges.jsonl
  coverage.json
  build.log
```

### Snapshot manifest

```json
{
  "snapshot_id": "",
  "schema_version": "kg_snapshot.v1",
  "corpus_hash": "",
  "selection_config_hash": "",
  "paper_ids": [],
  "paper_hash": "",
  "node_count": 0,
  "edge_count": 0,
  "relation_distribution": {},
  "topic_distribution": {},
  "year_distribution": {},
  "coverage": {},
  "generation_commit": "",
  "snapshot_hash": ""
}
```

### 接口

```python
def select_nested_papers(corpus: Corpus, config: SelectionConfig) -> NestedPaperSets
def build_snapshot(corpus: Corpus, papers: list[str], mode: str) -> KGSnapshot
def verify_nested(snapshots: list[KGSnapshot]) -> VerificationReport
def measure_coverage(snapshot: KGSnapshot, benchmark: Benchmark) -> CoverageReport
```

### CLI

```bash
python research/scripts/research.py kg build \
  --corpus thermal-stage1 \
  --config research/configs/kg/thermal-nested-v1.json

python research/scripts/research.py kg verify-nested \
  --snapshots K20 K40 K60 K80 K100

python research/scripts/research.py kg coverage \
  --snapshot K60 \
  --benchmark thermal-primary-v1
```

### 测试

- deterministic selection；
- exact nested relation；
- stable snapshot hash；
- no dangling edges；
- relation counts；
- same corpus/config rebuild；
- no target-label leakage。

### 验收

- K20/K40/K60/K80/K100 可脚本重建；
- selection 与 downstream labels 独立；
- snapshot hash 进入 run manifest；
- coverage 是测量值，不是按 test outcome 优化的值。

## 8. Module E：Knowledge Structure Controls

### 新增文件

```text
research/src/catalysis_research/kg/corruption.py
research/src/catalysis_research/kg/retrieval.py
research/configs/kg/structures/*.json
research/tests/kg/test_corruption.py
research/tests/kg/test_retrieval_budget.py
```

### Modes

```text
none
raw_rag
entity_kg
experiment_kg
evidence_kg
shuffled_kg
oracle_evidence
```

### 接口

```python
def corrupt_snapshot(snapshot: KGSnapshot, config: CorruptionConfig) -> KGSnapshot
def retrieve(query: RetrievalQuery, source: KnowledgeSource) -> RetrievalResult
def match_token_budget(results: list[RetrievalResult], budget: int) -> list[RetrievalResult]
```

### 控制要求

Shuffled KG 保持：

- paper、node 和 text 数量；
- evidence text；
- approximate token count；
- node type distribution。

只随机预注册的关系：

- claim-evidence linkage；
- paper association；
- experiment-observation association；
- selected relation types。

### 验收

- corruption seed 和 mapping 被保存；
- real/shuffled token 差异在 protocol tolerance 内；
- shuffled KG 不引入 dangling references；
- oracle evidence 只用于 benchmark analysis。

## 9. Module F：Scientific Model Provider

### 新增文件

```text
research/src/catalysis_research/models/base.py
research/src/catalysis_research/models/registry.py
research/src/catalysis_research/models/retry.py
research/src/catalysis_research/models/providers/deepseek.py
research/src/catalysis_research/models/providers/openai_compatible.py
research/configs/models/model-registry.v1.json
research/tests/models/
```

### 接口

```python
class ScientificModelProvider(Protocol):
    def generate_structured(
        self,
        request: ScientificModelRequest,
        schema: dict,
    ) -> ScientificModelResponse: ...


class ScientificModelRequest:
    provider: str
    model: str
    model_revision: str | None
    messages: list[dict]
    temperature: float
    max_output_tokens: int
    reasoning_budget: dict | None
    seed: int | None
    timeout_seconds: int
    metadata: dict
```

### Response

```python
class ScientificModelResponse:
    raw: object
    text: str
    parsed: object | None
    usage: dict
    provider_request_id: str | None
    finish_reason: str | None
    attempts: list[dict]
```

### CLI

```bash
python research/scripts/research.py model validate-registry
python research/scripts/research.py model smoke-test --model M1
```

### 测试

- mocked provider；
- structured output failure；
- unsupported seed；
- retry classification；
- timeout；
- raw output retention；
- request hash stability。

### 验收

- M1/M2/M3 可以由配置切换；
- core experiment 不 import provider-specific client；
- retry 不因内容质量触发；
- model identity 和 revision 被记录。

## 10. Module G：Prompt Registry

### 新增文件

```text
research/src/catalysis_research/prompts/registry.py
research/src/catalysis_research/prompts/renderer.py
research/prompts/descriptor/v1/system.txt
research/prompts/descriptor/v1/user.txt
research/prompts/hypothesis/v1/system.txt
research/prompts/hypothesis/v1/user.txt
research/tests/prompts/
```

### 接口

```python
def load_prompt(family: str, version: str) -> PromptTemplate
def render_prompt(template: PromptTemplate, context: dict) -> RenderedPrompt
def prompt_hash(template: PromptTemplate) -> str
```

### 验收

- prompt 不再散落在业务代码；
- prompt hash 进入 manifest；
- M/K condition 使用同一 family/version；
- benchmark test outcome 不用于修改 locked prompt。

## 11. Module H：Hypothesis Schema

### 新增文件

```text
research/src/catalysis_research/hypotheses/schema.py
research/src/catalysis_research/hypotheses/generator.py
research/src/catalysis_research/hypotheses/validator.py
research/manifests/schemas/hypothesis.schema.json
research/tests/hypotheses/
```

### 核心字段

```json
{
  "hypothesis_id": "",
  "statement": "",
  "mechanistic_rationale": "",
  "epistemic_status": "ai_hypothesis",
  "supporting_evidence_ids": [],
  "contradicting_evidence_ids": [],
  "assumptions": [],
  "falsification_condition": "",
  "applicable_domain": {},
  "confidence": 0.0
}
```

### 验收

- evidence IDs 可解析；
- paper fact 与 AI inference 字段分离；
- 没有 falsification condition 的 hypothesis 不进入 descriptor generation。

## 12. Module I：DescriptorSpecification

### 新增文件

```text
research/src/catalysis_research/descriptors/schema.py
research/src/catalysis_research/descriptors/generator.py
research/src/catalysis_research/descriptors/validator.py
research/src/catalysis_research/descriptors/failures.py
research/manifests/schemas/descriptor-specification.schema.json
research/tests/descriptors/test_schema.py
research/tests/descriptors/test_evidence_links.py
```

### Schema

```json
{
  "descriptor_id": "",
  "name": "",
  "scientific_hypothesis": "",
  "mechanistic_rationale": "",
  "physical_meaning": "",
  "mathematical_definition": "",
  "formula": "",
  "required_inputs": [],
  "units": "",
  "expected_relationship": "",
  "applicable_domain": {},
  "supporting_evidence_ids": [],
  "supporting_claim_ids": [],
  "assumptions": [],
  "potential_confounders": [],
  "falsification_condition": "",
  "computation_method": {},
  "novelty_rationale": "",
  "confidence": 0.0
}
```

### CLI

```bash
python research/scripts/research.py descriptor generate --config <run-config>
python research/scripts/research.py descriptor validate --input descriptors.json
```

### 验收

- 固定 candidate 和 selected descriptor budget；
- validation failure 不允许人工删除后假装不存在；
- evidence/claim linkage 可追溯；
- descriptor ID 和 spec hash 稳定。

## 13. Module J：Executable Feature Pipeline

### 新增文件

```text
research/src/catalysis_research/descriptors/expression.py
research/src/catalysis_research/descriptors/executor.py
research/src/catalysis_research/descriptors/units.py
research/src/catalysis_research/descriptors/selection.py
research/tests/descriptors/test_executor.py
research/tests/descriptors/test_units.py
research/tests/descriptors/test_safety.py
```

### 设计

第一阶段优先采用受限表达式 DSL，而不是执行任意模型生成 Python。

允许：

- arithmetic；
- log/exp/sqrt；
- min/max/ratio；
- conditional clipping；
- explicitly registered scientific functions。

禁止：

- filesystem；
- network；
- imports；
- process execution；
- reflection；
- arbitrary code。

### 接口

```python
def compile_descriptor(spec: DescriptorSpecification) -> ExecutableDescriptor
def execute_descriptor(
    descriptor: ExecutableDescriptor,
    dataset: DatasetView,
) -> FeatureResult
def validate_feature(result: FeatureResult, policy: FeaturePolicy) -> FeatureReport
```

### 失败 taxonomy

```text
schema_invalid
unsupported_input
invalid_formula
unsafe_expression
unit_mismatch
execution_error
missingness_exceeded
non_finite
zero_variance
redundant
physically_invalid
unsupported_hypothesis
```

### 验收

- 相同 input/spec 得到相同 feature hash；
- 禁止任意代码执行；
- invalid slots 进入固定 failure policy；
- 人工修复必须创建新 descriptor version。

## 14. Module K：Public Dataset Registry and Splits

### 新增文件

```text
research/src/catalysis_research/datasets/registry.py
research/src/catalysis_research/datasets/schema.py
research/src/catalysis_research/datasets/loader.py
research/src/catalysis_research/datasets/split.py
research/src/catalysis_research/datasets/leakage.py
research/configs/datasets/public-registry.v1.json
research/manifests/schemas/dataset-manifest.schema.json
research/tests/datasets/
```

### Dataset registry 必填字段

```json
{
  "dataset_id": "",
  "version": "",
  "domain": "thermal_catalysis",
  "source": "",
  "license": "",
  "file_hashes": {},
  "target": {},
  "allowed_inputs": [],
  "forbidden_inputs": [],
  "group_columns": [],
  "split_manifest": "",
  "label_access_policy": ""
}
```

### CLI

```bash
python research/scripts/research.py dataset register --config <dataset-config>
python research/scripts/research.py dataset split --dataset <id> --strategy iid
python research/scripts/research.py dataset split --dataset <id> --strategy ood
python research/scripts/research.py dataset leakage-audit --dataset <id>
```

### 验收

- exact public dataset 在 descriptor generation 前冻结；
- split membership 和 hash 可复算；
- train-only preprocessing；
- test labels 不可由 generation pipeline 读取；
- OOD grouping 有 domain rationale。

## 15. Module L：Baselines and Downstream ML

### 新增文件

```text
research/src/catalysis_research/baselines/
research/src/catalysis_research/downstream/
research/configs/downstream/primary-ridge-v1.json
research/configs/downstream/secondary-models-v1.json
research/tests/downstream/
```

### Baseline conditions

```text
human
llm_only
raw_rag
entity_kg
evidence_kg
strong_model_evidence_kg
shuffled_kg
oracle_evidence
```

### Primary ML

Ridge regression，使用固定：

- preprocessing；
- hyperparameter grid；
- validation policy；
- descriptor count；
- seeds；
- evaluation metrics。

### Secondary ML

- Random Forest；
- XGBoost；
- Gaussian Process Regression。

是否启用由 dataset size 和 protocol 决定，在结果前冻结。

### 接口

```python
def build_pipeline(config: DownstreamConfig) -> ModelPipeline
def tune_on_validation(pipeline: ModelPipeline, data: SplitData) -> TunedPipeline
def evaluate_locked(pipeline: TunedPipeline, test: TestView) -> PredictionMetrics
```

### 验收

- condition 共享同一 pipeline；
- test 一次性评估；
- tuning trial 数一致；
- feature count 一致；
- baseline 和 AI descriptors 使用同一 metric implementation。

## 16. Module M：Evaluation and Statistics

### 新增文件

```text
research/src/catalysis_research/evaluation/
research/src/catalysis_research/statistics/
research/configs/evaluation/primary-v1.json
research/tests/evaluation/
research/tests/statistics/
```

### Metrics

Prediction：

- RMSE；
- MAE；
- R2；
- Spearman；
- Pearson；
- calibration when applicable。

Descriptor：

- schema validity；
- executability；
- missingness；
- variance；
- redundancy；
- utility delta；
- novelty。

Optimization：

- top-k enrichment；
- hit rate；
- best-found value；
- normalized regret；
- samples to target。

### 接口

```python
def compute_primary_endpoint(metrics: PredictionMetrics, baseline: PredictionMetrics) -> float
def aggregate_runs(runs: list[RunManifest]) -> AggregatedResult
def fit_scaling_model(data: AnalysisTable) -> ScalingModelResult
def bootstrap_effects(data: AnalysisTable, replicates: int) -> BootstrapResult
```

### CLI

```bash
python research/scripts/research.py evaluate run --run <run-id>
python research/scripts/research.py evaluate aggregate --experiment <id>
python research/scripts/research.py statistics scaling --experiment <id>
```

### 验收

- primary endpoint 只存在一个 canonical implementation；
- confidence interval 可复现；
- model、knowledge 和 interaction effects 全部报告；
- negative and failed runs 进入 denominator。

## 17. Module N：Experiment Orchestration

### 新增文件

```text
research/src/catalysis_research/experiments/matrix.py
research/src/catalysis_research/experiments/runner.py
research/src/catalysis_research/experiments/resume.py
research/configs/experiments/pilot-v1.json
research/configs/experiments/full-scaling-v1.json
research/tests/experiments/
```

### 接口

```python
def expand_matrix(config: ExperimentConfig) -> list[RunConfig]
def execute_run(config: RunConfig) -> RunManifest
def resume_incomplete(experiment_id: str) -> ResumeReport
def summarize_experiment(experiment_id: str) -> ExperimentSummary
```

### CLI

```bash
python research/scripts/research.py experiment plan \
  --config research/configs/experiments/pilot-v1.json

python research/scripts/research.py experiment run \
  --config research/configs/experiments/pilot-v1.json

python research/scripts/research.py experiment resume --experiment <id>
python research/scripts/research.py experiment report --experiment <id>
```

### 验收

- matrix 展开结果先生成并冻结；
- concurrency 不改变结果身份；
- resume 不重复 completed run；
- API failure 和 scientific failure 分开；
- report 同时生成 JSON、CSV 和 Markdown。

## 18. Module O：Private Blind Validation

### 新增文件

```text
research/src/catalysis_research/private_validation/freeze.py
research/src/catalysis_research/private_validation/evaluator.py
research/src/catalysis_research/private_validation/access_log.py
research/manifests/schemas/freeze-bundle.schema.json
research/configs/private-validation/policy.v1.json
research/tests/private_validation/
```

Private dataset 不进入 Git repository。

### Freeze bundle

```json
{
  "protocol_hash": "",
  "git_commit": "",
  "model_registry_hash": "",
  "prompt_hashes": {},
  "kg_snapshot_hashes": {},
  "descriptor_spec_hashes": {},
  "descriptor_code_hashes": {},
  "downstream_config_hash": "",
  "preprocessing_hash": "",
  "evaluation_hash": "",
  "created_at": "",
  "approved_by": []
}
```

### CLI

```bash
python research/scripts/research.py private freeze --config <freeze-config>
python research/scripts/research.py private verify-freeze --bundle <bundle>
python research/scripts/research.py private evaluate \
  --bundle <bundle> \
  --private-input <external-path>
```

### 验收

- evaluator 可由独立团队执行；
- AI team 无需获得 raw labels；
- 输出默认只有 aggregate metrics；
- 每次访问和 rerun 均有记录；
- freeze 后任何改变产生新 bundle，不能覆盖旧 bundle。

## 19. 依赖关系

```text
Protocol
  -> Run Manifest

Corpus Registry
  -> KG Snapshots
  -> Knowledge Controls

Model Provider
  -> Prompt Registry
  -> Hypothesis
  -> DescriptorSpecification
  -> Executable Features

Public Dataset + Splits
  -> Executable Features
  -> Downstream ML
  -> Evaluation

Run Manifest + KG + Model + Descriptor + Dataset + Evaluation
  -> Pilot
  -> Full Scaling

Stable Full Pipeline
  -> Private Freeze Bundle
  -> Blind Validation
```

Private firewall policy可以提前设计，但 private evaluation 必须在方法完全冻结后执行。

## 20. 建议验收 Gates

### Gate 0：Protocol Freeze

- 四份方法学文档通过检查；
- primary endpoint 和 scaling 判据冻结；
- unresolved blocking decisions 有明确 owner 和 deadline。

### Gate 1：Reproducible Inputs

- corpus registry；
- dataset registry；
- split hashes；
- KG snapshot hashes。

### Gate 2：Reproducible Generation

- model registry；
- prompt registry；
- run manifest；
- hypothesis/descriptor schema。

### Gate 3：Executable Science

- descriptor execution；
- failure ledger；
- fixed baseline pipeline；
- leakage tests。

### Gate 4：Pilot

- 3 x 3 matrix；
- pre-registered go/no-go；
- real pilot report；
- no hidden manual repair。

### Gate 5：Full Study

- 3 x 5 matrix；
- structure ablation；
- OOD/data efficiency；
- statistical analysis；
- optimization benchmark。

### Gate 6：Private Blind Test

- freeze bundle；
- independent evaluator；
- one-shot result；
- contamination-resistant report。

## 21. 每个模块完成时必须报告

1. 修改文件；
2. schema/interface；
3. CLI；
4. tests；
5. verification output；
6. known limitations；
7. protocol impact；
8. 是否需要 rerun 已有实验。
