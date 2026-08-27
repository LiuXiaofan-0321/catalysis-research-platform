from __future__ import annotations

import asyncio
import json
import traceback
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .extractor import ExtractionRunner
from .hashing import atomic_write_json, canonical_json, content_hash
from .indexing import build_index
from .inventory import build_inventory, load_inventory
from .ledger import PipelineLedger
from .manifest import (
    create_run_manifest,
    finalize_manifest,
    generate_run_id,
    load_manifest,
    register_artifact,
    update_manifest,
)
from .parsing import parse_pdf
from .providers import provider_for


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def run_directory_for(workspace: Path, run_id: str) -> Path:
    return workspace.resolve() / "runs" / run_id


def _config_payload(config: PipelineConfig) -> dict[str, Any]:
    return config.model_dump(mode="json")


def _result_stats(results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "parse": {
            "completed": sum(
                row.get("parse_status") == "completed" for row in results
            ),
            "cached": sum(row.get("parse_status") == "cached" for row in results),
            "failed": sum(row.get("parse_status") == "failed" for row in results),
        },
        "extract": {
            "completed": sum(
                row.get("extract_status") == "completed" for row in results
            ),
            "cached": sum(
                row.get("extract_status") == "cached" for row in results
            ),
            "failed": sum(
                row.get("extract_status") == "failed" for row in results
            ),
        },
    }


def _load_result_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.is_file():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict) or not value.get("paper_id"):
                raise ValueError(f"Invalid result row at {path}:{line_number}")
            rows[str(value["paper_id"])] = value
    return rows


def _load_latest_results(run_directory: Path) -> dict[str, dict[str, Any]]:
    rows = _load_result_rows(run_directory / "paper-results.jsonl")
    rows.update(_load_result_rows(run_directory / "paper-results.journal.jsonl"))
    return rows


def _write_results(path: Path, rows: list[dict[str, Any]]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        "".join(f"{canonical_json(row)}\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _load_frozen_inventory(
    *,
    inventory_path: Path,
    expected_source: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest_path = inventory_path.with_suffix(".manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = load_inventory(inventory_path)
    if manifest.get("source") != str(expected_source.resolve()):
        raise RuntimeError("Frozen inventory source does not match the run config")
    if manifest.get("inventory_hash") != content_hash(records):
        raise RuntimeError("Frozen inventory hash mismatch; use --refresh-inventory")
    return manifest, records


def build_preflight_report(
    *,
    config: PipelineConfig,
    limit: int | None = None,
    refresh_inventory: bool = False,
) -> dict[str, Any]:
    if limit is not None and limit < 1:
        raise ValueError("limit must be at least 1")
    workspace = config.workspace.resolve()
    preflight_directory = workspace / "preflight" / config.config_hash
    inventory_path = preflight_directory / "inventory.jsonl"
    ledger = PipelineLedger(workspace / "ledger.sqlite")
    try:
        if inventory_path.is_file() and not refresh_inventory:
            inventory, records = _load_frozen_inventory(
                inventory_path=inventory_path,
                expected_source=config.source,
            )
        else:
            inventory = build_inventory(
                source=config.source,
                output_path=inventory_path,
                ledger=ledger,
            )
            records = load_inventory(inventory_path)
    finally:
        ledger.close()
    selected = records[:limit] if limit is not None else records
    paper_count = len(selected)
    calls_per_paper = 2 if config.extraction.enabled else 0
    max_tokens_per_paper = (
        config.extraction.max_context_tokens_core
        + config.extraction.max_context_tokens_data
        + config.extraction.max_tokens_core
        + config.extraction.max_tokens_data
        if config.extraction.enabled
        else 0
    )
    warnings: list[str] = []
    if inventory.get("missing_count"):
        warnings.append("The source manifest contains missing PDF paths")
    if config.index.enabled and config.index.embedding_revision == "default":
        warnings.append("Pin an embedding model revision before a production run")
    if config.index.enabled and config.index.allow_hash_embedding_fallback:
        warnings.append("Hash embedding fallback is enabled and is unsuitable for production")
    return {
        "schema_version": "literature_preflight.v1",
        "config_hash": config.config_hash,
        "source": str(config.source.resolve()),
        "inventory": inventory,
        "selection": {
            "paper_count": paper_count,
            "limit": limit,
            "full_inventory": limit is None or paper_count == len(records),
        },
        "estimated_work": {
            "model_calls": paper_count * calls_per_paper,
            "maximum_configured_tokens": paper_count * max_tokens_per_paper,
            "cost": None,
            "cost_note": "Not estimated because provider pricing is not part of the frozen config.",
        },
        "large_run_confirmation_required": paper_count
        > config.execution.large_run_threshold,
        "ready": bool(paper_count) and not inventory.get("missing_count") and not warnings,
        "warnings": warnings,
    }


async def execute_run(
    *,
    config: PipelineConfig,
    run_id: str | None = None,
    resume: bool = False,
    limit: int | None = None,
    refresh_inventory: bool = False,
    confirm_large_run: bool = False,
) -> dict[str, Any]:
    if limit is not None and limit < 1:
        raise ValueError("limit must be at least 1")
    workspace = config.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    ledger = PipelineLedger(workspace / "ledger.sqlite")
    resolved_run_id = run_id or generate_run_id(config.config_hash)
    run_directory = run_directory_for(workspace, resolved_run_id)
    provider = None
    try:
        if run_directory.exists():
            if not resume:
                raise FileExistsError(f"Run already exists: {resolved_run_id}")
            if (run_directory / "FINALIZED.json").exists():
                return load_manifest(run_directory)
        else:
            create_run_manifest(
                run_directory=run_directory,
                run_id=resolved_run_id,
                config=_config_payload(config),
                config_hash=config.config_hash,
                repository_root=repository_root(),
            )
            atomic_write_json(run_directory / "config.json", _config_payload(config))

        ledger.register_run(
            run_id=resolved_run_id,
            status="running",
            config_hash=config.config_hash,
            manifest_path=str(run_directory / "manifest.json"),
        )
        inventory_path = run_directory / "inventory.jsonl"
        if inventory_path.is_file() and not refresh_inventory:
            inventory_manifest, records = _load_frozen_inventory(
                inventory_path=inventory_path,
                expected_source=config.source,
            )
        else:
            inventory_manifest = build_inventory(
                source=config.source,
                output_path=inventory_path,
                ledger=ledger,
            )
            records = load_inventory(inventory_path)
        register_artifact(
            run_directory,
            name="inventory",
            path=inventory_path,
            media_type="application/x-ndjson",
        )

        existing_manifest = load_manifest(run_directory)
        prior_selection = existing_manifest.get("selection") if resume else None
        if isinstance(prior_selection, dict) and prior_selection.get("paper_ids"):
            selected_ids = set(prior_selection["paper_ids"])
            records = [row for row in records if row["paper_id"] in selected_ids]
            if len(records) != len(selected_ids):
                raise RuntimeError(
                    "The refreshed inventory is missing papers from the frozen selection"
                )
        elif limit is not None:
            records = records[:limit]
        if len(records) > config.execution.large_run_threshold and not confirm_large_run:
            raise RuntimeError(
                f"Run {resolved_run_id} selects {len(records)} papers; rerun with "
                "--confirm-large-run after reviewing `litpipe preflight`."
            )

        def record_inventory(manifest: dict[str, Any]) -> None:
            manifest["inventory"] = inventory_manifest
            manifest["selection"] = {
                "paper_count": len(records),
                "limit": prior_selection.get("limit")
                if isinstance(prior_selection, dict)
                else limit,
                "paper_ids": [row["paper_id"] for row in records],
            }
            manifest["status"] = "running"

        update_manifest(run_directory, record_inventory)
        provider = provider_for(config.extraction) if config.extraction.enabled else None
        runner = (
            ExtractionRunner(
                config=config.extraction,
                provider=provider,
                ledger=ledger,
                workspace=workspace,
                collection_hint=config.collection_hint,
            )
            if provider is not None
            else None
        )

        async def process(record: dict[str, Any]) -> dict[str, Any]:
            result: dict[str, Any] = {
                "paper_id": record["paper_id"],
                "source_path": record["source_path"],
                "source_pdf_sha256": record["source_pdf_sha256"],
                "status": "failed",
                "parse_status": "failed",
                "extract_status": "disabled"
                if not config.extraction.enabled
                else "failed",
            }
            try:
                parsed, parse_info = await asyncio.to_thread(
                    parse_pdf,
                    paper=record,
                    parser_config=config.parser,
                    chunking_config=config.chunking,
                    cache_root=workspace / "cache" / "parsed",
                )
                if (
                    config.parser.fail_on_low_quality
                    and parsed.quality.get("low_quality")
                ):
                    raise RuntimeError(
                        "Parsed PDF did not pass the configured quality gate: "
                        + "; ".join(parsed.quality.get("warnings") or [])
                    )
                result.update(
                    {
                        "parse_status": "cached"
                        if parse_info["cached"]
                        else "completed",
                        "parsed_artifact_path": parse_info["artifact_path"],
                        "parsed_artifact_sha256": parse_info["artifact_sha256"],
                        "page_count": parsed.page_count,
                        "chunk_count": len(parsed.chunks),
                    }
                )
                ledger.record_stage(
                    paper_id=record["paper_id"],
                    stage="parse",
                    cache_key=parse_info["cache_key"],
                    status=result["parse_status"],
                    artifact_path=parse_info["artifact_path"],
                    artifact_sha256=parse_info["artifact_sha256"],
                    runtime_seconds=parse_info["runtime_seconds"],
                )
                if runner is None:
                    result["status"] = "completed"
                    return result
                _, extract_info = await runner.extract(parsed)
                result.update(
                    {
                        "status": "completed",
                        "extract_status": "cached"
                        if extract_info["cached"]
                        else "completed",
                        "extraction_artifact_path": extract_info["artifact_path"],
                        "extraction_artifact_sha256": extract_info["artifact_sha256"],
                        "usage": extract_info["usage"],
                        "model_calls": extract_info["model_calls"],
                        "cache_hits": extract_info["cache_hits"],
                    }
                )
                ledger.record_stage(
                    paper_id=record["paper_id"],
                    stage="extract",
                    cache_key=extract_info["cache_key"],
                    status=result["extract_status"],
                    artifact_path=extract_info["artifact_path"],
                    artifact_sha256=extract_info["artifact_sha256"],
                    runtime_seconds=extract_info["runtime_seconds"],
                )
            except Exception as error:
                result.update(
                    {
                        "status": "failed",
                        "error_type": type(error).__name__,
                        "error": str(error),
                        "traceback": traceback.format_exc(),
                    }
                )
                stage = "parse" if result["parse_status"] == "failed" else "extract"
                ledger.record_stage(
                    paper_id=record["paper_id"],
                    stage=stage,
                    cache_key="failed",
                    status="failed",
                    error={"type": type(error).__name__, "message": str(error)},
                )
            return result

        latest = _load_latest_results(run_directory)
        pending = [
            record
            for record in records
            if (latest.get(record["paper_id"]) or {}).get("status") != "completed"
        ]
        journal_path = run_directory / "paper-results.journal.jsonl"
        progress_path = run_directory / "progress.json"
        result_lock = asyncio.Lock()
        queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
        for record in pending:
            queue.put_nowait(record)
        worker_count = min(max(1, config.extraction.workers), max(1, len(pending)))
        for _ in range(worker_count):
            queue.put_nowait(None)
        processed_this_attempt = 0

        async def worker() -> None:
            nonlocal processed_this_attempt
            while True:
                record = await queue.get()
                try:
                    if record is None:
                        return
                    result = await process(record)
                    async with result_lock:
                        latest[result["paper_id"]] = result
                        with journal_path.open(
                            "a", encoding="utf-8", newline="\n"
                        ) as handle:
                            handle.write(canonical_json(result))
                            handle.write("\n")
                        processed_this_attempt += 1
                        if (
                            processed_this_attempt
                            % config.execution.result_progress_interval
                            == 0
                            or processed_this_attempt == len(pending)
                        ):
                            selected_results = [
                                latest[row["paper_id"]]
                                for row in records
                                if row["paper_id"] in latest
                            ]
                            atomic_write_json(
                                progress_path,
                                {
                                    "run_id": resolved_run_id,
                                    "selected": len(records),
                                    "processed_this_attempt": processed_this_attempt,
                                    "pending": len(records) - len(selected_results),
                                    "stats": _result_stats(selected_results),
                                },
                            )
                finally:
                    queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(worker_count)]
        await asyncio.gather(*workers)

        results = [
            latest[row["paper_id"]]
            for row in records
            if row["paper_id"] in latest
        ]
        results.sort(key=lambda row: row["source_pdf_sha256"])
        results_path = run_directory / "paper-results.jsonl"
        _write_results(results_path, results)
        register_artifact(
            run_directory,
            name="paper_results",
            path=results_path,
            media_type="application/x-ndjson",
        )
        stats = _result_stats(results)
        usage = {
            "prompt_tokens": sum(
                int((row.get("usage") or {}).get("prompt_tokens") or 0)
                for row in results
            ),
            "completion_tokens": sum(
                int((row.get("usage") or {}).get("completion_tokens") or 0)
                for row in results
            ),
            "total_tokens": sum(
                int((row.get("usage") or {}).get("total_tokens") or 0)
                for row in results
            ),
            "model_calls": sum(int(row.get("model_calls") or 0) for row in results),
            "cache_hits": sum(int(row.get("cache_hits") or 0) for row in results),
        }
        errors = [
            {
                "paper_id": row["paper_id"],
                "type": row.get("error_type"),
                "message": row.get("error"),
            }
            for row in results
            if row["status"] == "failed"
        ]

        def record_outcome(manifest: dict[str, Any]) -> None:
            manifest["stages"]["parse"] = stats["parse"]
            manifest["stages"]["extract"] = stats["extract"]
            manifest["usage"] = usage
            manifest["errors"] = errors
            manifest["status"] = "partial" if errors else "running"

        update_manifest(run_directory, record_outcome)
        completed = sum(row["status"] == "completed" for row in results)
        all_completed = bool(records) and completed == len(records)
        if config.index.enabled and all_completed:
            index_id = f"{resolved_run_id}-index"
            index_directory = workspace / "indexes" / index_id
            if not index_directory.exists():
                index_manifest = await asyncio.to_thread(
                    build_index,
                    run_directory=run_directory,
                    index_directory=index_directory,
                    index_id=index_id,
                    config=config.index,
                    repository_root=repository_root(),
                )
            else:
                index_manifest = json.loads(
                    (index_directory / "manifest.json").read_text(encoding="utf-8")
                )
            register_artifact(
                run_directory,
                name="rag_index_manifest",
                path=index_directory / "manifest.json",
                media_type="application/json",
            )
            update_manifest(
                run_directory,
                lambda manifest: manifest["stages"].__setitem__(
                    "index",
                    {
                        "completed": 1,
                        "failed": 0,
                        "index_id": index_manifest["index_id"],
                        "index_hash": index_manifest["logical_content_hash"],
                        "index_directory": str(index_directory),
                    },
                ),
            )

        final_status = "completed" if all_completed else "partial"
        ledger.register_run(
            run_id=resolved_run_id,
            status=final_status,
            config_hash=config.config_hash,
            manifest_path=str(run_directory / "manifest.json"),
        )
        if all_completed:
            return finalize_manifest(run_directory, status="completed")
        update_manifest(
            run_directory,
            lambda manifest: manifest.__setitem__("status", "partial"),
        )
        return load_manifest(run_directory)
    finally:
        close = getattr(provider, "close", None)
        if close is not None:
            await close()
        ledger.close()


def load_run_config(workspace: Path, run_id: str) -> PipelineConfig:
    path = run_directory_for(workspace, run_id) / "config.json"
    return PipelineConfig.model_validate(
        json.loads(path.read_text(encoding="utf-8"))
    )


def finalize_partial_run(*, workspace: Path, run_id: str) -> dict[str, Any]:
    run_directory = run_directory_for(workspace, run_id)
    manifest = load_manifest(run_directory)
    if (run_directory / "FINALIZED.json").is_file():
        return manifest
    if manifest.get("status") != "partial":
        raise RuntimeError("Only an incomplete partial run can be finalized explicitly")
    results = _load_latest_results(run_directory)
    completed = sum(row.get("status") == "completed" for row in results.values())
    if not completed:
        raise RuntimeError("Cannot finalize a partial run with no completed papers")
    return finalize_manifest(run_directory, status="partial")


def build_index_for_run(
    *,
    workspace: Path,
    run_id: str,
    index_id: str | None = None,
) -> dict[str, Any]:
    config = load_run_config(workspace, run_id)
    run_directory = run_directory_for(workspace, run_id)
    manifest = load_manifest(run_directory)
    finalized_partial = (
        manifest.get("status") == "partial"
        and (run_directory / "FINALIZED.json").is_file()
    )
    if manifest.get("status") != "completed" and not finalized_partial:
        raise RuntimeError(
            "Indexing requires a completed run or an explicitly finalized partial run"
        )
    resolved_index_id = index_id or f"{run_id}-index"
    index_directory = workspace.resolve() / "indexes" / resolved_index_id
    if index_directory.exists():
        return json.loads(
            (index_directory / "manifest.json").read_text(encoding="utf-8")
        )
    return build_index(
        run_directory=run_directory,
        index_directory=index_directory,
        index_id=resolved_index_id,
        config=config.index,
        repository_root=repository_root(),
    )
