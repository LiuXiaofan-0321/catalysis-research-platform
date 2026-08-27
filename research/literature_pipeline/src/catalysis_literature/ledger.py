from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class PipelineLedger:
    def __init__(self, path: Path):
        self.path = path.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._initialize()

    def _connection(self) -> sqlite3.Connection:
        connection = getattr(self._local, "connection", None)
        if connection is None:
            connection = sqlite3.connect(self.path, timeout=30, isolation_level=None)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA busy_timeout=30000")
            self._local.connection = connection
        return connection

    def close(self) -> None:
        connection = getattr(self._local, "connection", None)
        if connection is not None:
            connection.close()
            self._local.connection = None

    def __enter__(self) -> "PipelineLedger":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self._connection()
        connection.execute("BEGIN IMMEDIATE")
        try:
            yield connection
        except BaseException:
            connection.execute("ROLLBACK")
            raise
        else:
            connection.execute("COMMIT")

    def _initialize(self) -> None:
        connection = self._connection()
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS papers (
                paper_id TEXT PRIMARY KEY,
                source_path TEXT NOT NULL,
                source_sha256 TEXT NOT NULL UNIQUE,
                size_bytes INTEGER NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS stages (
                paper_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                cache_key TEXT NOT NULL,
                status TEXT NOT NULL,
                artifact_path TEXT,
                artifact_sha256 TEXT,
                error_json TEXT,
                runtime_seconds REAL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (paper_id, stage),
                FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
            );
            CREATE TABLE IF NOT EXISTS model_calls (
                call_key TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_hash TEXT NOT NULL,
                input_hash TEXT NOT NULL,
                response_path TEXT NOT NULL,
                response_sha256 TEXT NOT NULL,
                usage_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                config_hash TEXT NOT NULL,
                manifest_path TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )

    def register_paper(
        self,
        *,
        paper_id: str,
        source_path: str,
        source_sha256: str,
        size_bytes: int,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        timestamp = utc_now()
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO papers (
                    paper_id, source_path, source_sha256, size_bytes,
                    metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(paper_id) DO UPDATE SET
                    source_path=excluded.source_path,
                    size_bytes=excluded.size_bytes,
                    metadata_json=excluded.metadata_json,
                    updated_at=excluded.updated_at
                """,
                (
                    paper_id,
                    source_path,
                    source_sha256,
                    size_bytes,
                    json.dumps(metadata or {}, ensure_ascii=False, sort_keys=True),
                    timestamp,
                    timestamp,
                ),
            )

    def papers(self) -> list[dict[str, Any]]:
        rows = self._connection().execute(
            "SELECT * FROM papers ORDER BY source_sha256"
        ).fetchall()
        return [
            {
                **dict(row),
                "metadata": json.loads(row["metadata_json"]),
            }
            for row in rows
        ]

    def stage(self, paper_id: str, stage: str) -> dict[str, Any] | None:
        row = self._connection().execute(
            "SELECT * FROM stages WHERE paper_id=? AND stage=?",
            (paper_id, stage),
        ).fetchone()
        return dict(row) if row else None

    def record_stage(
        self,
        *,
        paper_id: str,
        stage: str,
        cache_key: str,
        status: str,
        artifact_path: str | None = None,
        artifact_sha256: str | None = None,
        error: dict[str, Any] | None = None,
        runtime_seconds: float | None = None,
    ) -> None:
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO stages (
                    paper_id, stage, cache_key, status, artifact_path,
                    artifact_sha256, error_json, runtime_seconds, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(paper_id, stage) DO UPDATE SET
                    cache_key=excluded.cache_key,
                    status=excluded.status,
                    artifact_path=excluded.artifact_path,
                    artifact_sha256=excluded.artifact_sha256,
                    error_json=excluded.error_json,
                    runtime_seconds=excluded.runtime_seconds,
                    updated_at=excluded.updated_at
                """,
                (
                    paper_id,
                    stage,
                    cache_key,
                    status,
                    artifact_path,
                    artifact_sha256,
                    json.dumps(error, ensure_ascii=False, sort_keys=True)
                    if error
                    else None,
                    runtime_seconds,
                    utc_now(),
                ),
            )

    def model_call(self, call_key: str) -> dict[str, Any] | None:
        row = self._connection().execute(
            "SELECT * FROM model_calls WHERE call_key=?",
            (call_key,),
        ).fetchone()
        return dict(row) if row else None

    def record_model_call(
        self,
        *,
        call_key: str,
        provider: str,
        model: str,
        prompt_hash: str,
        input_hash: str,
        response_path: str,
        response_sha256: str,
        usage: dict[str, Any],
    ) -> None:
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO model_calls (
                    call_key, provider, model, prompt_hash, input_hash,
                    response_path, response_sha256, usage_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    call_key,
                    provider,
                    model,
                    prompt_hash,
                    input_hash,
                    response_path,
                    response_sha256,
                    json.dumps(usage, ensure_ascii=False, sort_keys=True),
                    utc_now(),
                ),
            )

    def register_run(
        self,
        *,
        run_id: str,
        status: str,
        config_hash: str,
        manifest_path: str,
    ) -> None:
        timestamp = utc_now()
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO runs (
                    run_id, status, config_hash, manifest_path, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_id) DO UPDATE SET
                    status=excluded.status,
                    updated_at=excluded.updated_at
                """,
                (run_id, status, config_hash, manifest_path, timestamp, timestamp),
            )
