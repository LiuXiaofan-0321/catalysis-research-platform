# Alibaba Cloud ECS deployment

Production uses `docker-compose.prod.yml` and a bind-mounted SQLite database.
The database is stored at `/opt/catalysis-research-platform/storage/dev.db` on
the host so container replacement and application upgrades do not replace the
research corpus or user data.

The first server preparation can be run with:

```bash
sh /tmp/prepare-production-host.sh <public-ip-or-domain>
```

The preparation script only installs the uploaded database when
`storage/dev.db` does not already exist. Application upgrades therefore do not
replace production user data.

Production also sets `SYNC_SCHEMA_ON_START=false`. The application creates its
supplementary research tables with `CREATE TABLE IF NOT EXISTS`, while Prisma
schema synchronization is kept out of routine container restarts so it cannot
drop imported corpus or graph tables.

## Start or upgrade

```bash
cd /opt/catalysis-research-platform
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
```

The same command is available as `scripts/start-production.sh` for remote
deployments where nested shell quoting is undesirable.

## Check

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml ps
curl http://127.0.0.1/api/health
```

## Back up the database

Stop writes briefly before copying the SQLite database:

```bash
cd /opt/catalysis-research-platform
docker compose --env-file .env.production -f docker-compose.prod.yml stop backend
cp storage/dev.db "storage/dev.db.$(date +%Y%m%d-%H%M%S).bak"
docker compose --env-file .env.production -f docker-compose.prod.yml start backend
```

Do not use `--replace` for routine paper additions. Import a new processed
dataset without that flag so document keys are upserted incrementally.
