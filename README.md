# Catalysis Research

研究问题：**外部科学知识（RAG 原文检索，或知识图谱 KG + RAG）能否帮助大模型提出可计算、并能被公开数据验证的科学描述符？知识范围从本领域扩展到邻近领域、跨领域（Small → Medium → Large KG）时，这种能力是否随之提高？**

做法：选取有公开数据、原生描述符（D0）和原生模型的 benchmark，让 Agent / RAG / KG+RAG 三组 LLM 在相同预算下提出新描述符，再用原论文的模型比较 D0 与 D0+新描述符。详见 [docs/RESEARCH_QUESTION.md](docs/RESEARCH_QUESTION.md)。

**当前进展与下一步：[docs/STATUS.md](docs/STATUS.md)**

## 目录

```text
src/catalysis_research/
  knowledge/     冻结的知识库：KG 快照校验、科学归一化 overlay、同预算 RAG / KG+RAG 检索
  llm/           GLM 客户端
  benchmarks/    benchmark 数据适配（当前：ZeoSyn）
  discovery/     公式 DSL、生成循环（V1 直接加入；V2 自主检索 + KG 信息通道）、评估与统计
literature_pipeline/   文献 PDF 结构化抽取与 RAG 索引构建（建 Medium/Large KG 时使用）
scripts/       run_zeosyn.py（V1）、run_zeosyn_v2.py（V2 全部阶段）、knowledge.py（overlay、检索、检索审计）
jobs/zeosyn/   集群一键提交 launch.sh、结果回收 collect.sh、Slurm 作业脚本
configs/       实验、检索与归一化配置
data/zeosyn/   ZeoSyn 原始文件（MIT 许可证，逐字节保存）
data/kg_zeolite_v1/  从 Small KG 构建的合成知识层（合成实验、OSDA 链接、RAG 合成白名单）
results/       正式运行结果（由 collect.sh 写入）
tests/         单元测试
docs/          研究问题、进展、历史、实验协议、基础设施说明
```

## 运行

**V2（当前）在台式机上运行**，步骤见 [docs/experiments/ZEOSYN_V2_RUNBOOK.md](docs/experiments/ZEOSYN_V2_RUNBOOK.md)。

V1 在华东师大集群（login02）上的运行规则见 [AGENTS.md](AGENTS.md)：

```bash
bash jobs/zeosyn/launch.sh --dry-run    # 只做检查
bash jobs/zeosyn/launch.sh              # 提交完整作业链
bash jobs/zeosyn/launch.sh --status RUN_DIR
bash jobs/zeosyn/collect.sh RUN_DIR && git push
```

本地开发：

```bash
python -m venv .venv && .venv/bin/pip install -e ".[test]"
.venv/bin/python -m pytest
.venv/bin/python scripts/run_zeosyn.py reproduce --data-root data/zeosyn --output /tmp/repro.json
```

RAG 索引（`full-rag-v1-index`）、Small KG（`Small-KG-zeolite-v1`）和归一化 overlay 只存放在服务器上，身份与 hash 见 [docs/infra/KNOWLEDGE_BASE.md](docs/infra/KNOWLEDGE_BASE.md)。

## 相关仓库与存档

- 网页平台（文献浏览、研究建议、实验记录）：[catalysis-web](https://github.com/LiuXiaofan-0321/catalysis-web)
- 2026-10-07 重组之前的完整内容（JACS Au、AdsZeo 等旧研究线及其全部结果）：tag `archive/full-2026-10-07`，概要见 [docs/HISTORY.md](docs/HISTORY.md)
