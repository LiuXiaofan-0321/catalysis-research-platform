# Catalysis Research Platform

面向光催化与分子筛热催化研究的证据知识图谱、多智能体方向分析与实验反馈平台。

## 核心能力

- 光催化语料：247篇结构化论文；
- 热催化语料：512篇结构化论文；
- 论文、关键词、实体、关键实验、原子化观测和 Claims 的单向证据图；
- DeepSeek 驱动的候选研究方向、证据边界和最小判别实验；
- 实验记录、观察、阶段性结论和后续建议回流；
- 独立的研究者画像，保存研究兴趣、设备技术、当前目标和实验约束；
- 账号隔离、Workspace 隔离和可复现的数据导入。

平台严格区分：

1. 论文直接证据；
2. 跨论文归纳；
3. AI 候选假设；
4. 用户实验记录。

不会把相关性自动写成因果关系，也不会将待验证假设伪装为论文结论。

## 目录

```text
backend/       Express + Prisma + SQLite + DeepSeek
frontend/      React + Vite
data/          可导入的光催化、热催化结构化数据包
research/      独立、命令行可复现的论文实验层
scripts/       Windows/Linux 初始化脚本
docker-compose.yml
```

`research/` 与生产平台解耦，用于 Model × Knowledge scaling、KG
版本化、描述符发现、下游建模、评估和统计分析。基础结构检查：

```bash
npm run research:doctor
npm run research:test
```

当前已冻结光催化知识点：

```text
research/kg_snapshots/K247-photocatalysis-v1
```

验证冻结内容：

```bash
npm run research:verify:k247
```

统一 Run Manifest：

```bash
python research/scripts/research.py run --help
```

## 研究方法文档

- `CURRENT_ARCHITECTURE.md`：当前代码、数据流和真实能力；
- `NMI_GAP_ANALYSIS.md`：按照 P0/P1/P2 排列的方法学缺口；
- `RESEARCH_IMPLEMENTATION_PLAN.md`：模块接口、CLI、测试和验收；
- `EXPERIMENT_PROTOCOL.md`：冻结的实验变量、endpoint、公平性规则和成功判据。
- `PRIVATE_DATA_PROTOCOL.md`：private unseen data 的权限、防火墙、冻结和盲测规则。

## 环境要求

- Node.js 20.19–22.x，推荐 Node.js 22；
- npm 10+；
- DeepSeek API Key；
- Windows、Linux 或 Docker。

## 本地部署

复制环境模板：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

至少填写：

```dotenv
SESSION_SECRET=<长度足够的随机字符串>
COOKIE_SECURE=false
DEEPSEEK_API_KEY=<你的密钥>
INITIAL_ADMIN_PASSWORD=<首次管理员密码，至少8位>
```

一键初始化：

```bash
npm run setup
```

Windows 也可以运行：

```powershell
.\scripts\setup.ps1
```

首次导入预计耗时：

- 光催化约1–2分钟；
- 热催化约6–8分钟；
- 具体取决于磁盘和 CPU。

启动：

```bash
npm run dev:backend
npm run dev:frontend
```

访问：

```text
http://localhost:5173
```

## Docker 部署

准备 `.env` 后运行：

```bash
docker compose up -d --build
```

首次启动会：

1. 创建 SQLite 表；
2. 创建管理员和研究者画像；
3. 创建光催化、热催化 Workspace；
4. 导入两个结构化语料包；
5. 写入数据卷标记，后续重启不会重复导入。

查看日志：

```bash
docker compose logs -f backend
```

## 常用命令

```bash
npm run build
npm run import:photocatalysis
npm run import:thermal
npm --prefix backend run check
```

重新覆盖导入：

```bash
npm --prefix backend run import:dataset -- \
  --input ../data/thermal-catalysis-stage1.zip \
  --system thermal_catalysis \
  --username admin \
  --replace
```

## AI 配置

默认科研模型：

```dotenv
AI_RESEARCH_PROVIDER=deepseek
AI_RESEARCH_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

API 密钥只能放在本地 `.env` 或服务器密钥管理系统中，不得提交到 Git。

如果平台通过 HTTPS 对外服务，请设置：

```dotenv
COOKIE_SECURE=true
FRONTEND_ORIGIN=https://你的域名
```

## 数据安全

仓库不包含：

- API 密钥；
- 论文 PDF；
- 原平台数据库；
- 用户密码和会话；
- 用户实验记录；
- 私人研究者画像；
- 开发日志和临时输出。

生产部署前应进一步配置 HTTPS、反向代理、数据库备份和访问审计。
