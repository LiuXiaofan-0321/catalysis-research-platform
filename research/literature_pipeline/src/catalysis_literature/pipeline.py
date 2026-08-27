from __future__ import annotations

import asyncio
import json
import traceback
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .extractor import ExtractionRunner
from .hashing import atomic_write_json, canonical_json
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


async def execute_run(
    *,
    config: PipelineConfig,
    run_id: str | None = None,
    resume: bool = False,
) -> dict[str, Any]:
    workspace = config.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    ledger = PipelineLedger(workspace / "ledger.sqlite")
    resolved_run_id = run_id or generate_run_id(config.config_hash)
    run_directory = run_directory_for(workspace, resolved_run_id)
    if run_directory.exists():
        if not resume:
            raise FileExistsError(f"Run already exists: {resolved_run_id}")
        if (run_directory / "FINALIZED.json").exists():
            manifest = load_manifest(run_directory)
            ledger.close()
            return manifest
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
    inventory_manifest = build_inventory(
        source=config.source,
        output_path=inventory_path,
        ledger=ledger,
    )
    register_artifact(
        run_directory,
        name="inventory",
        path=inventory_path,
        media_type="application/x-ndjson",
    )
    update_manifest(
        run_directory,
        lambda manifest: manifest.__setitem__("inventory", inventory_manifest),
    )
    records = load_inventory(inventory_path)
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
    parse_semaphore = asyncio.Semaphore(max(1, config.extraction.workers))

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
            async with parse_semaphore:
                parsed, parse_info = await asyncio.to_thread(
                    parse_pdf,
                    paper=record,
                    parser_config=config.parser,
                    chunking_config=config.chunking,
                    cache_root=workspace / "cache" / "parsed",
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
            artifact, extract_info = await runner.extract(parsed)
            del artifact
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
                error={
                    "type": type(error).__name__,
                    "message": str(error),
                },
            )
        return result

    results = await asyncio.gather(*(process(record) for record in records))
    close = getattr(provider, "close", None)
    if close is not None:
        await close()
    results.sort(key=lambda row: row["source_pdf_sha256"])
    results_path = run_directory / "paper-results.jsonl"
    results_path.write_text(
        "".join(f"{canonical_json(row)}\n" for row in results),
        encoding="utf-8",
        newline="\n",
    )
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

    update_manifest(run_directory, record_outcome)
    completed = sum(row["status"] == "completed" for row in results)
    if config.index.enabled and completed:
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
    final_status = "completed" if completed else "failed"
    ledger.register_run(
        run_id=resolved_run_id,
        status=final_status,
        config_hash=config.config_hash,
        manifest_path=str(run_directory / "manifest.json"),
    )
    manifest = finalize_manifest(run_directory, status=final_status)
    ledger.close()
    return manifest


def load_run_config(workspace: Path, run_id: str) -> PipelineConfig:
    path = run_directory_for(workspace, run_id) / "config.json"
    return PipelineConfig.model_validate(
        json.loads(path.read_text(encoding="utf-8"))
    )


def build_index_for_run(
    *,
    workspace: Path,
    run_id: str,
    index_id: str | None = None,
) -> dict[str, Any]:
    config = load_run_config(workspace, run_id)
    resolved_index_id = index_id or f"{run_id}-index"
    index_directory = workspace.resolve() / "indexes" / resolved_index_id
    if index_directory.exists():
        return json.loads(
            (index_directory / "manifest.json").read_text(encoding="utf-8")
        )
    return build_index(
        run_directory=run_directory_for(workspace, run_id),
        index_directory=index_directory,
        index_id=resolved_index_id,
        config=config.index,
        repository_root=repository_root(),
    )
