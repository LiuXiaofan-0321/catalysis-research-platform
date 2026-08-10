# Current Architecture

状态日期：2026-08-10

本文档描述当前仓库已经实现的行为，不把计划中的 research 能力写成现有能力。

## 1. 系统定位

当前系统是一个面向光催化与分子筛热催化的科研辅助平台，主链路为：

```text
结构化论文 JSON
  -> 数据包去重与打包
  -> Workspace 级 SQLite 证据图
  -> 关键词启发式证据检索
  -> DeepSeek 生成候选假设
  -> 可选的实验方案扩展
  -> 用户实验记录与后续建议
```

当前系统适合作为交互式生产平台和 evidence-grounded research assistant，
但尚不是用于受控研究 `Q = f(M, K)` 的论文实验系统。

## 2. 仓库结构

```text
backend/       Express、Prisma、SQLite、DeepSeek API
frontend/      React、Vite、科研平台界面
data/          两个结构化论文语料包
scripts/       生产平台初始化脚本
research/      已建立的独立科研实验层骨架
```

`research/` 当前只包含目录契约、CLI 自检和基础测试。Run manifest、KG
snapshot、model provider、descriptor 和 evaluation 尚未实现。

## 3. 生产运行架构

### 3.1 后端

后端入口为 `backend/src/index.ts`。

启动过程：

1. 加载 `.env`；
2. 验证 `SESSION_SECRET`；
3. 配置 SQLite WAL、foreign keys 和 busy timeout；
4. 运行 Prisma 管理的业务 schema；
5. 通过原生 SQL 确保科研数据表存在；
6. 注册认证、Workspace、Profile 和 Research API；
7. 监听 HTTP 请求。

主要 API：

| API | 用途 |
| --- | --- |
| `/api/auth/*` | 注册、登录、会话 |
| `/api/workspaces/*` | 用户 Workspace |
| `/api/profile/*` | 研究者画像 |
| `/api/research/workspaces/:id/stats` | 图谱统计 |
| `/api/research/workspaces/:id/graph` | 图谱浏览 |
| `/api/research/workspaces/:id/advice` | 候选方向生成 |
| `/api/research/workspaces/:id/experiments` | 实验记录 |

### 3.2 前端

前端入口为 `frontend/src/main.tsx`，主要页面包括：

| 页面 | 当前能力 |
| --- | --- |
| Login | 登录和注册 |
| Workspace | 选择光催化或热催化 Workspace |
| Research Lab | 图谱浏览、AI 方向、实验反馈 |
| Profile | 研究兴趣、设备、约束和表达偏好 |

前端承担交互式生产工作流，不应作为论文实验的必要执行入口。

### 3.3 部署

本地部署使用 Node.js、npm 和 SQLite。Docker 部署使用：

- Node.js backend container；
- Nginx frontend container；
- SQLite volume；
- 首次启动数据导入 marker。

Docker marker `.catalysis-datasets-v1` 只能防止重复导入，不能表示严格的
dataset 或 KG snapshot 版本。

## 4. 数据层

### 4.1 当前语料

| 数据包 | 文献数 | ZIP SHA256 | corpusFingerprint |
| --- | ---: | --- | --- |
| `photocatalysis-stage1.zip` | 247 | `492fedadfaca0056ca5233620959745485d307d90888c114214df65ec82c74d9` | `1f2b4df8e7faedeffcf1366ba3f54afe595dff0764d341d051a5743d637a2721` |
| `thermal-catalysis-stage1.zip` | 512 | `f0161fb2ee27a643831fb57392d304a1f6c139175b16ffd446c3f0d8921b5af5` | `7d653a9ff110d3edd287d22f3a46cec2ef256ee1bd33abc7c257bae3e2f4a875` |

数据包内包含：

```text
dataset-manifest.json
json/*.json
```

结构化论文 schema 为 `zeolite_paper_extraction.v1`，主要对象包括：

- paper；
- abstract；
- summary；
- extracted keywords；
- entities；
- experiments；
- observations；
- claims；
- visual review items；
- quality；
- extraction metadata。

两个数据包中所有 entity、experiment、observation 和 claim 记录均包含
evidence 数组，但 evidence 的质量状态不同。

Evidence validation 包括：

- `exact`；
- `locally_recovered`；
- `unverified`。

### 4.2 数据打包

`backend/src/scripts/packageDataset.ts`：

1. 扫描一个或多个 Stage 1 JSON 目录；
2. 按催化体系筛选；
3. 按 DOI、PDF SHA 或 title/year 去重；
4. 统计文献与结构化对象数量；
5. 生成 `dataset-manifest.json`；
6. 写入 ZIP。

当前 `corpusFingerprint` 只基于排序后的 document keys，不覆盖：

- 每个 JSON 的完整内容；
- extraction prompt；
- extraction model version；
- 打包脚本 Git commit；
- 压缩包文件 hash；
- relation distribution；
- benchmark evidence coverage。

### 4.3 数据导入

`backend/src/scripts/importDataset.ts`：

1. 接收目录或 ZIP；
2. 找到 JSON 目录；
3. 逐文件解析 Stage 1 artifact；
4. 按 Workspace 催化体系筛选；
5. 调用 `ResearchGraphService.importArtifacts`；
6. 可选 `--replace` 清空 Workspace 图谱后重新导入。

当前导入过程不读取或保存 `dataset-manifest.json`，数据库状态因此没有与
数据包 hash、manifest hash 或生成脚本版本绑定。

数据打包和数据库导入的 document identity 规则不完全相同：

- 打包优先 DOI；
- 导入优先 `paper.id`，之后才是 DOI 和 SHA。

这一差异可能导致跨阶段文献身份不一致。

## 5. 数据库 Schema

### 5.1 Prisma 管理的业务表

`backend/prisma/schema.prisma` 管理：

- `User`；
- `AuthToken`；
- `Workspace`；
- `ResearcherProfile`。

### 5.2 原生 SQL 管理的科研表

`backend/src/config/ensureResearchSchema.ts` 动态创建：

#### ResearchCorpusDocument

保存论文级信息：

- document key；
- title、DOI、year、journal；
- paper type；
- catalysis system；
- source path 和 source SHA；
- abstract、summary、quality、metadata JSON；
- Workspace 归属。

#### ResearchGraphNode

保存图节点：

- `nodeKey`；
- `nodeType`；
- label、canonical name、Chinese name；
- local ID；
- `dataJson`；
- `evidenceJson`；
- confidence；
- review status；
- source document。

#### ResearchGraphEdge

保存有方向的来源边：

- `edgeType`；
- from/to node；
- source record type 和 ID；
- evidence；
- confidence；
- review status；
- source document。

#### ResearchExperimentLog

保存用户或 AI 产生的实验计划和反馈：

- objective；
- materials；
- procedure；
- conditions；
- observations；
- outcome；
- constraints；
- source；
- status。

该记录允许原地更新，不是 immutable experiment run。

#### ResearchAdviceRun

保存一次建议生成：

- request；
- model-visible context；
- normalized response；
- provider；
- model；
- usage；
- error；
- optional experiment link。

它不是完整的论文实验 manifest。

## 6. KG Schema

### 6.1 节点类型

| 类型 | 作用域 | 说明 |
| --- | --- | --- |
| `paper` | 单篇论文 | 文献根节点 |
| `entity` | 跨论文合并 | 材料、方法、性质等 |
| `keyword` | 跨论文合并 | 结构化关键词 |
| `experiment` | 单篇论文 | 关键实验 |
| `observation` | 单篇论文 | 原子化观测 |
| `claim` | 单篇论文 | 论文级 Claim |

### 6.2 边类型

当前边主要包括：

- `PAPER_MENTIONS_ENTITY`；
- `PAPER_HAS_KEYWORD`；
- `PAPER_REPORTS_EXPERIMENT`；
- `EXPERIMENT_USES_SAMPLE`；
- `EXPERIMENT_USES_MATERIAL`；
- `EXPERIMENT_USES_METHOD`；
- `EXPERIMENT_PRODUCES_OBSERVATION`；
- `PAPER_REPORTS_OBSERVATION`；
- `OBSERVATION_OF_SAMPLE`；
- `OBSERVATION_MEASURES_PROPERTY`；
- `OBSERVATION_MEASURED_BY`；
- `PAPER_ASSERTS_CLAIM`。

当前没有显式实现：

- Claim 到 Observation 的结构化边；
- Claim 到 Experiment 的结构化边；
- 跨论文支持、冲突或重复关系；
- 机制路径；
- 因果边；
- descriptor 节点；
- hypothesis 节点；
- provenance graph。

## 7. Evidence Provenance

每个抽取记录可保留：

- PDF page index；
- section；
- source type；
- source ID；
- raw quote；
- normalized quote；
- evidence validation；
- visual review 标记；
- review status。

导入后：

- 节点保存 `evidenceJson`；
- 边也保存对应 evidence；
- paper-scoped 节点保存 `sourceDocumentId`；
- Advice 中的 supporting evidence 保存 graph node ID。

当前局限：

1. 跨论文合并的 entity/keyword 节点会在 upsert 时覆盖节点级
   `dataJson/evidenceJson`，完整多来源主要依赖边保留；
2. Advice 对 evidence alias 进行校验，但模型返回的 `paperId` 和 quote
   没有再次与数据库原文严格比对；
3. 没有独立 evidence ID registry；
4. 没有 task-level relevant evidence annotation；
5. 没有检索召回率和 coverage 评估。

## 8. Retrieval

`ResearchGraphService.buildEvidenceContext` 的当前流程：

1. 合并用户目标、问题、实验记录和体系关键词；
2. 提取英文 token 和中文 2 至 4 字 n-gram；
3. 在 `label` 和 `dataJson` 上执行 SQL `LIKE`；
4. 按 token 命中长度平方和与 confidence 排序；
5. 返回 claim、observation、experiment、entity、keyword；
6. 最多将 18 个节点压缩为 `E01` 至 `E18` 交给模型。

当前没有：

- vector retrieval；
- BM25/FTS index；
- graph traversal retrieval；
- learned reranker；
- fixed retrieval manifest；
- token-matched control；
- retrieval benchmark；
- oracle evidence 模式。

## 9. Agent 和模型调用链

### 9.1 Advice

`ResearchAssistantService.advise`：

1. 校验 Workspace 和用户；
2. 读取 researcher profile；
3. 调用 KG retrieval；
4. 压缩 evidence；
5. 创建 `ResearchAdviceRun`；
6. 调用一次 DeepSeek；
7. 规范化模型 JSON；
8. 保存建议。

虽然 prompt 使用了 Orchestrator 和 multi-agent 表述，当前实际是一次模型调用，
没有独立的 Retriever Agent、Mechanism Agent、Critic Agent 或 Evidence
Reviewer Agent。

### 9.2 Experiment Planning

`ResearchAssistantService.planExperiment`：

1. 读取已完成 Advice；
2. 选择一个候选方向；
3. 再调用一次 DeepSeek Planning Agent；
4. 更新原 Advice 的 experiment plan。

第二次调用没有独立保存完整配置、prompt hash、raw response 和 usage provenance。

### 9.3 Model Client

`backend/src/services/deepseekClient.ts` 当前固定：

- provider：DeepSeek；
- endpoint：DeepSeek chat completions；
- temperature：`0.25`；
- retry：2 次；
- JSON object response；
- timeout 和 max tokens 来自环境变量。

`.env.example` 中的 `AI_RESEARCH_PROVIDER` 没有真正参与 provider 选择。

当前缺少：

- provider interface；
- seed；
- reasoning budget；
- concurrency；
- prompt version；
- schema validator；
- raw response retention；
- model revision；
- request hash；
- deterministic retry policy。

## 10. Hypothesis 输出

当前候选方向结构包括：

- title；
- hypothesis；
- rationale；
- novelty；
- molecular sieve role；
- active phase role；
- interface strategy；
- proposed pathway；
- selectivity target；
- evidence boundary；
- supporting evidence；
- feasibility；
- confidence；
- risks；
- next experiment。

优点：

- 假设必须可证伪；
- 要求最小判别实验；
- 包含 controls、measurements、decision rules 和 stopping criteria；
- 明确提醒区分文献事实与 AI 假设。

局限：

- 没有 stable hypothesis ID；
- 没有严格枚举的 epistemic status；
- evidence boundary 是自然语言；
- 没有独立 Hypothesis schema；
- 没有 DescriptorSpecification；
- 没有 executable feature；
- 没有 novelty 或 correctness evaluator。

## 11. 数据和运行版本管理

当前已有：

- Stage 1 extraction schema version；
- extraction model；
- extraction prompt version；
- extraction time；
- source PDF SHA；
- extracted text SHA；
- token usage；
- dataset corpus fingerprint；
- Git repository。

当前缺少：

- dataset registry；
- imported manifest registry；
- KG snapshot ID 和 hash；
- prompt file hash；
- experiment config hash；
- complete run manifest；
- immutable run directory；
- model revision；
- environment lock；
- dependency lock for research；
- split hash；
- descriptor code hash；
- freeze bundle。

## 12. 当前可复用模块

建议保留和复用：

1. Stage 1 structured artifact schema；
2. 数据包打包和基础去重逻辑；
3. PDF SHA、text SHA 和 extraction metadata；
4. evidence quote 和 validation 字段；
5. paper/experiment/observation/claim 的基础映射；
6. Workspace 生产隔离；
7. SQLite 图谱作为小规模研究数据源；
8. graph import 中稳定 hash ID 的思想；
9. Advice 中 evidence alias 白名单；
10. 生产平台前端和实验反馈工作流。

## 13. 不适合直接用于论文复现的模块

以下模块可以继续服务生产平台，但不能直接作为论文实验执行层：

1. 前端触发的 Advice 工作流；
2. mutable `ResearchAdviceRun`；
3. mutable `ResearchExperimentLog`；
4. hard-coded DeepSeek client；
5. hard-coded prompt；
6. heuristic retrieval；
7. Workspace 当前数据库状态；
8. Docker import marker；
9. 只有结构计数的 `checkGraph.ts`；
10. 人工查看结果后继续修改的交互闭环。

## 14. Test Coverage

生产 backend 和 frontend 当前没有单元测试、集成测试或端到端测试。

新建 research 层当前有 3 个基础测试，仅验证：

- research 目录契约；
- 缺失目录会失败；
- `doctor` 输出机器可读 JSON。

尚未测试：

- dataset import correctness；
- evidence provenance；
- KG node/edge mapping；
- retrieval determinism；
- model structured output；
- experiment reproducibility；
- descriptor execution；
- leakage protection。

## 15. 实现 NMI 研究目标仍缺失的能力

必须新增：

- frozen experiment protocol；
- complete run provenance；
- rebuildable KG snapshots；
- model provider abstraction；
- fixed prompt families；
- descriptor schema、generation、execution 和 failure ledger；
- public predictive datasets；
- fixed IID/OOD splits；
- fair downstream ML；
- baseline and ablation conditions；
- Model x Knowledge matrix；
- statistical inference；
- optimization benchmark；
- private data firewall and blind evaluator。

这些能力应主要位于 `research/`，通过只读 adapter 使用现有结构化语料，避免
破坏生产平台。
