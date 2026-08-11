#!/bin/sh
set -eu

PUBLIC_HOST="${1:?usage: prepare-production-host.sh <public-host>}"
APP_DIR="/opt/catalysis-research-platform"
APP_ARCHIVE="/tmp/catalysis-app-deploy.tar.gz"
DB_ARCHIVE="/tmp/catalysis-db-deploy.tar.gz"
SOURCE_ENV="/tmp/.env"

install -d -m 755 "$APP_DIR"
install -d -m 700 "$APP_DIR/storage"
tar -xzf "$APP_ARCHIVE" -C "$APP_DIR"

if [ ! -f "$APP_DIR/storage/dev.db" ]; then
  tar -xzf "$DB_ARCHIVE" -C "$APP_DIR/storage"
  mv "$APP_DIR/storage/deploy.db" "$APP_DIR/storage/dev.db"
fi

grep -Ev \
  '^(PORT|FRONTEND_ORIGIN|DATABASE_URL|SESSION_SECRET|COOKIE_SECURE|HTTP_PORT|SYNC_SCHEMA_ON_START|BOOTSTRAP_ON_START|IMPORT_DATASETS_ON_START)=' \
  "$SOURCE_ENV" > "$APP_DIR/.env.production"

SESSION_SECRET="$(openssl rand -hex 32)"
cat >> "$APP_DIR/.env.production" <<EOF

PORT=3001
FRONTEND_ORIGIN=http://${PUBLIC_HOST}
DATABASE_URL=file:/app/storage/dev.db
SESSION_SECRET=${SESSION_SECRET}
COOKIE_SECURE=false
HTTP_PORT=80
SYNC_SCHEMA_ON_START=false
BOOTSTRAP_ON_START=false
IMPORT_DATASETS_ON_START=false
EOF

sed -i 's/\r$//' "$APP_DIR/.env.production"
chmod 600 "$APP_DIR/.env.production" "$APP_DIR/storage/dev.db"
sed -i 's/\r$//' "$APP_DIR/backend/docker-entrypoint.sh"

cd "$APP_DIR"
docker compose --env-file .env.production -f docker-compose.prod.yml config --quiet
echo "production_host_prepared"
