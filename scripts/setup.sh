#!/usr/bin/env sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "已创建 .env。请填写 INITIAL_ADMIN_PASSWORD、SESSION_SECRET 和 DEEPSEEK_API_KEY 后重新运行。"
  exit 1
fi

npm run install:all
npm --prefix backend run db:push
npm run bootstrap
npm run import:photocatalysis
npm run import:thermal
npm run build

echo "初始化完成。分别运行 npm run dev:backend 和 npm run dev:frontend。"
