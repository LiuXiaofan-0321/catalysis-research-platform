$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path -LiteralPath '.env')) {
  Copy-Item -LiteralPath '.env.example' -Destination '.env'
  Write-Host '已创建 .env。请填写 INITIAL_ADMIN_PASSWORD、SESSION_SECRET 和 DEEPSEEK_API_KEY 后重新运行。'
  exit 1
}

npm run install:all
npm --prefix backend run db:push
npm run bootstrap
npm run import:photocatalysis
npm run import:thermal
npm run build

Write-Host '初始化完成。分别运行 npm run dev:backend 和 npm run dev:frontend。'
