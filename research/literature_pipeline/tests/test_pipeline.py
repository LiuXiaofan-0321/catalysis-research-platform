from __future__ import annotations

import asyncio
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PIPELINE_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_literature.chunking import build_chunks
from catalysis_literature.config import (
    ChunkingConfig,
    ExtractionConfig,
    IndexConfig,
    ParserConfig,
    PipelineConfig,
)
from catalysis_literature.exporter import export_stage1
from catalysis_literature.hashing import content_hash, sha256_file
from catalysis_literature.indexing import verify_index
from catalysis_literature.inventory import build_inventory, load_inventory
from catalysis_literature.ledger import PipelineLedger
from catalysis_literature.manifest import verify_manifest
from catalysis_literature.models import PageRecord
from catalysis_literature.pipeline import execute_run, run_directory_for
from catalysis_literature.retrieval import PortableRetriever


def write_text_pdf(path: Path, text: str) -> None:
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 11 Tf 54 740 Td ({escaped}) Tj ET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"\nendstream",
    ]
    payload = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, item in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{index} 0 obj\n".encode("ascii"))
        payload.extend(item)
        payload.extend(b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(payload)


class LiteraturePipelineTests(unittest.TestCase):
    def test_content_hash_is_order_stable(self) -> None:
        self.assertEqual(content_hash({"a": 1, "b": 2}), content_hash({"b": 2, "a": 1}))

    def test_inventory_deduplicates_by_pdf_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "papers"
            source.mkdir()
            payload = b"%PDF-1.4\nsame\n%%EOF"
            (source / "a.pdf").write_bytes(payload)
            (source / "b.pdf").write_bytes(payload)
            ledger = PipelineLedger(root / "ledger.sqlite")
            manifest = build_inventory(
                source=source,
                output_path=root / "inventory.jsonl",
                ledger=ledger,
            )
            records = load_inventory(root / "inventory.jsonl")
            ledger.close()

        self.assertEqual(manifest["paper_count"], 1)
        self.assertEqual(len(records[0]["duplicate_paths"]), 1)

    def test_chunking_is_deterministic_and_excludes_references(self) -> None:
        pages = [
            PageRecord(
                page_index=1,
                text=(
                    "Abstract\n\nCatalyst conversion selectivity and stability were measured. "
                    "Results\n\nThe catalyst reached 80 percent conversion at 500 K. "
                    "References\n\nA reference that should not be indexed."
                ),
            )
        ]
        config = ChunkingConfig(target_tokens=100, overlap_tokens=10, min_tokens=5)
        first = build_chunks(paper_id="sha256:test", pages=pages, config=config)
        second = build_chunks(paper_id="sha256:test", pages=pages, config=config)

        self.assertEqual(
            [item.chunk_id for item in first],
            [item.chunk_id for item in second],
        )
        self.assertNotIn("should not be indexed", " ".join(item.text for item in first))

    def test_mock_pipeline_resume_index_retrieve_and_export(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "papers"
            workspace = root / "workspace"
            source.mkdir()
            pdf = source / "paper.pdf"
            write_text_pdf(
                pdf,
                (
                    "Abstract This catalytic study reports catalyst conversion and selectivity. "
                    "Results The catalyst reached 80 percent conversion at 500 K. "
                    "Conclusion The catalyst remained stable during testing."
                ),
            )
            config = PipelineConfig(
                source=source,
                workspace=workspace,
                parser=ParserConfig(engine="pypdf", docling_fallback=False),
                chunking=ChunkingConfig(
                    target_tokens=120,
                    overlap_tokens=10,
                    min_tokens=5,
                ),
                extraction=ExtractionConfig(
                    provider="mock",
                    workers=2,
                    requests_per_minute=10000,
                ),
                index=IndexConfig(
                    backend="portable",
                    embedding_model="hash-embedding-v1",
                    vector_dimensions=64,
                ),
            )
            manifest = asyncio.run(
                execute_run(config=config, run_id="test-literature-run")
            )
            run_directory = run_directory_for(workspace, "test-literature-run")
            report = verify_manifest(run_directory)
            results = [
                json.loads(line)
                for line in (run_directory / "paper-results.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            index_directory = workspace / "indexes" / "test-literature-run-index"
            index_report = verify_index(index_directory)
            retrieval = PortableRetriever(index_directory).retrieve(
                query="catalyst conversion selectivity",
                top_k=3,
                include_unverified=True,
            )
            connection = sqlite3.connect(workspace / "ledger.sqlite")
            try:
                model_calls_before = connection.execute(
                    "SELECT COUNT(*) FROM model_calls"
                ).fetchone()[0]
            finally:
                connection.close()
            resumed = asyncio.run(
                execute_run(
                    config=config,
                    run_id="test-literature-run",
                    resume=True,
                )
            )
            connection = sqlite3.connect(workspace / "ledger.sqlite")
            try:
                model_calls_after = connection.execute(
                    "SELECT COUNT(*) FROM model_calls"
                ).fetchone()[0]
            finally:
                connection.close()
            export_directory = root / "stage1-export"
            export_manifest = export_stage1(
                run_directory=run_directory,
                output_directory=export_directory,
            )

        self.assertEqual(manifest["status"], "completed")
        self.assertTrue(report["valid"], report["failures"])
        self.assertEqual(results[0]["status"], "completed")
        self.assertTrue(index_report["valid"], index_report["failures"])
        self.assertGreaterEqual(retrieval["selected_count"], 1)
        self.assertEqual(model_calls_before, 2)
        self.assertEqual(model_calls_after, model_calls_before)
        self.assertEqual(resumed["status"], "completed")
        self.assertEqual(export_manifest["counts"]["documents"], 1)


if __name__ == "__main__":
    unittest.main()
