from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Sequence

from .benchmark import baseline_summary
from .config import PipelineConfig, load_config
from .exporter import export_stage1
from .indexing import merge_indexes, verify_index
from .inventory import build_inventory
from .ledger import PipelineLedger
from .manifest import verify_manifest
from .pipeline import (
    build_preflight_report,
    build_index_for_run,
    execute_run,
    finalize_partial_run,
    load_run_config,
    run_directory_for,
)
from .retrieval import PortableRetriever


DEFAULT_WORKSPACE = Path("research/literature_pipeline/workspace")


def _json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="litpipe",
        description="Scalable catalysis literature extraction and KG-aware RAG.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor")

    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--source", type=Path, required=True)
    inventory.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--config", type=Path, required=True)
    preflight.add_argument("--limit", type=int)
    preflight.add_argument("--refresh-inventory", action="store_true")

    run = subparsers.add_parser("run")
    run.add_argument("--config", type=Path, required=True)
    run.add_argument("--run-id")
    run.add_argument("--limit", type=int)
    run.add_argument("--refresh-inventory", action="store_true")
    run.add_argument("--confirm-large-run", action="store_true")

    resume = subparsers.add_parser("resume")
    resume.add_argument("--run-id", required=True)
    resume.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    resume.add_argument("--refresh-inventory", action="store_true")
    resume.add_argument("--confirm-large-run", action="store_true")

    finalize_partial = subparsers.add_parser("finalize-partial")
    finalize_partial.add_argument("--run-id", required=True)
    finalize_partial.add_argument(
        "--workspace", type=Path, default=DEFAULT_WORKSPACE
    )

    index = subparsers.add_parser("build-index")
    index.add_argument("--run-id", required=True)
    index.add_argument("--index-id")
    index.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)

    merge = subparsers.add_parser("merge-indexes")
    merge.add_argument("--index", type=Path, action="append", required=True)
    merge.add_argument("--output", type=Path, required=True)
    merge.add_argument("--index-id", required=True)

    retrieve = subparsers.add_parser("retrieve")
    retrieve.add_argument("--index", type=Path, required=True)
    retrieve.add_argument("--query", required=True)
    retrieve.add_argument("--top-k", type=int)
    retrieve.add_argument("--context-token-budget", type=int)
    retrieve.add_argument("--include-unverified", action="store_true")

    export = subparsers.add_parser("export-stage1")
    export.add_argument("--run-id", required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--run-id")
    verify.add_argument("--index", type=Path)
    verify.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)

    benchmark = subparsers.add_parser("benchmark")
    benchmark.add_argument("--baseline", type=Path, required=True)
    return parser


def doctor() -> dict[str, object]:
    modules = {
        name: bool(importlib.util.find_spec(name))
        for name in (
            "pydantic",
            "yaml",
            "httpx",
            "numpy",
            "fitz",
            "pypdf",
            "docling",
            "lancedb",
            "sentence_transformers",
        )
    }
    required = ("pydantic", "yaml", "httpx", "numpy")
    return {
        "schema_version": "literature_pipeline_doctor.v1",
        "python": sys.version,
        "modules": modules,
        "required_ready": all(modules[name] for name in required),
        "deepseek_configured": bool(os.getenv("DEEPSEEK_API_KEY")),
        "notes": [
            "PyMuPDF is the preferred parser; pypdf is the fallback.",
            "Docling, LanceDB, and sentence-transformers are optional extras.",
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            output = doctor()
        elif args.command == "inventory":
            ledger = PipelineLedger(args.workspace / "ledger.sqlite")
            try:
                output = build_inventory(
                    source=args.source,
                    output_path=args.workspace / "inventory.jsonl",
                    ledger=ledger,
                )
            finally:
                ledger.close()
        elif args.command == "preflight":
            output = build_preflight_report(
                config=load_config(args.config),
                limit=args.limit,
                refresh_inventory=args.refresh_inventory,
            )
        elif args.command == "run":
            output = asyncio.run(
                execute_run(
                    config=load_config(args.config),
                    run_id=args.run_id,
                    limit=args.limit,
                    refresh_inventory=args.refresh_inventory,
                    confirm_large_run=args.confirm_large_run,
                )
            )
        elif args.command == "resume":
            config = load_run_config(args.workspace, args.run_id)
            output = asyncio.run(
                execute_run(
                    config=config,
                    run_id=args.run_id,
                    resume=True,
                    refresh_inventory=args.refresh_inventory,
                    confirm_large_run=args.confirm_large_run,
                )
            )
        elif args.command == "finalize-partial":
            output = finalize_partial_run(
                workspace=args.workspace,
                run_id=args.run_id,
            )
        elif args.command == "build-index":
            output = build_index_for_run(
                workspace=args.workspace,
                run_id=args.run_id,
                index_id=args.index_id,
            )
        elif args.command == "retrieve":
            output = PortableRetriever(args.index).retrieve(
                query=args.query,
                top_k=args.top_k,
                context_token_budget=args.context_token_budget,
                include_unverified=args.include_unverified,
            )
        elif args.command == "merge-indexes":
            output = merge_indexes(
                index_directories=args.index,
                index_directory=args.output,
                index_id=args.index_id,
                repository_root=Path(__file__).resolve().parents[4],
            )
        elif args.command == "export-stage1":
            output = export_stage1(
                run_directory=run_directory_for(args.workspace, args.run_id),
                output_directory=args.output,
            )
        elif args.command == "verify":
            if bool(args.run_id) == bool(args.index):
                raise ValueError("Choose exactly one of --run-id or --index")
            output = (
                verify_manifest(
                    run_directory_for(args.workspace, args.run_id)
                )
                if args.run_id
                else verify_index(args.index)
            )
            _json(output)
            return 0 if output["valid"] else 1
        else:
            output = baseline_summary(args.baseline)
    except Exception as error:
        _json(
            {
                "ok": False,
                "error_type": type(error).__name__,
                "error": str(error),
            }
        )
        return 1
    _json(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
