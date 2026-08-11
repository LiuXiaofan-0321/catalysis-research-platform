#!/bin/sh
set -eu

cd /opt/catalysis-research-platform
exec docker compose \
  --env-file .env.production \
  -f docker-compose.prod.yml \
  up -d --build
