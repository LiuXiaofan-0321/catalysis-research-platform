#!/bin/sh
set -eu

npx prisma db push --skip-generate
npm run bootstrap

MARKER="/app/storage/.catalysis-datasets-v1"
if [ "${IMPORT_DATASETS_ON_START:-true}" = "true" ] && [ ! -f "$MARKER" ]; then
  npm run import:dataset -- --input /app/data/photocatalysis-stage1.zip --system photocatalysis --username "${INITIAL_ADMIN_USERNAME:-admin}" --replace
  npm run import:dataset -- --input /app/data/thermal-catalysis-stage1.zip --system thermal_catalysis --username "${INITIAL_ADMIN_USERNAME:-admin}" --replace
  touch "$MARKER"
fi

exec node dist/index.js
