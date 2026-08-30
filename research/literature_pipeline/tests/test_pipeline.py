from __future__ import annotations

import asyncio
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import httpx


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PIPELINE_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))
sys.path.insert(0, str(PIPELINE_ROOT / "scripts"))

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
from catalysis_literature.indexing import merge_indexes, verify_index
from catalysis_literature.inventory import build_inventory, load_inventory
from catalysis_literature.ledger import PipelineLedger
from catalysis_literature.manifest import git_state, verify_manifest
from catalysis_literature.models import PageRecord
from catalysis_literature.pipeline import (
    build_preflight_report,
    execute_run,
    run_directory_for,
)
from catalysis_literature.parsing import parse_pdf as real_parse_pdf
from catalysis_literature.providers import ZhipuProvider, provider_for
from catalysis_literature.retrieval import PortableRetriever
from build_acs_md_manifest import build_records
from build_full_corpus_manifests import discover_records


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
    @patch.dict("os.environ", {"ZHIPU_API_KEY": "test-key"})
    def test_zhipu_provider_uses_official_json_contract(self) -> None:
        provider = provider_for(
            ExtractionConfig(
                provider="zhipu",
                model="glm-5.3-flash",
                base_url="https://open.bigmodel.cn/api/paas/v4",
                temperature=1.0,
                reasoning_effort="low",
                requests_per_minute=10000,
            )
        )
        captured: dict[str, object] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured["url"] = str(request.url)
            captured["authorization"] = request.headers.get("Authorization")
            captured["payload"] = json.loads(request.content)
            return httpx.Response(
                200,
                json={
                    "model": "glm-5.3-flash",
                    "choices": [{"message": {"content": '{"ok": true}'}}],
                    "usage": {"total_tokens": 12},
                },
            )

        async def exercise_provider() -> object:
            self.assertIsInstance(provider, ZhipuProvider)
            await provider._client.aclose()
            provider._client = httpx.AsyncClient(
                base_url="https://open.bigmodel.cn/api/paas/v4",
                transport=httpx.MockTransport(handler),
            )
            try:
                return await provider.generate_json(
                    prompt="Return one JSON object.",
                    stage="core",
                    max_tokens=1800,
                )
            finally:
                await provider.close()

        result = asyncio.run(exercise_provider())
        payload = captured["payload"]
        self.assertEqual(
            captured["url"],
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        )
        self.assertEqual(captured["authorization"], "Bearer test-key")
        self.assertEqual(payload["model"], "glm-5.3-flash")
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertEqual(payload["thinking"]["type"], "enabled")
        self.assertEqual(payload["reasoning_effort"], "low")
        self.assertEqual(result.data, {"ok": True})

    @patch("catalysis_literature.manifest.subprocess.run")
    def test_git_state_uses_old_git_compatible_branch_lookup(self, run_mock) -> None:
        outputs = {
            ("status", "--porcelain"): " M tracked.txt\n",
            ("rev-parse", "--abbrev-ref", "HEAD"): "master\n",
            ("rev-parse", "HEAD"): "commit-id\n",
            ("rev-parse", "HEAD^{tree}"): "tree-id\n",
        }

        def fake_run(command: list[str], **_: object) -> SimpleNamespace:
            return SimpleNamespace(stdout=outputs[tuple(command[1:])])

        run_mock.side_effect = fake_run
        self.assertEqual(
            git_state(Path("repository")),
            {
                "commit": "commit-id",
                "tree": "tree-id",
                "branch": "master",
                "dirty": True,
            },
        )
        commands = [tuple(call.args[0][1:]) for call in run_mock.call_args_list]
        self.assertIn(("rev-parse", "--abbrev-ref", "HEAD"), commands)
        self.assertNotIn(("branch", "--show-current"), commands)

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
        self.assertEqual(manifest["document_count"], 1)
        self.assertEqual(len(records[0]["duplicate_paths"]), 1)

    def test_markdown_main_and_si_share_one_rag_paper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            main = root / "main.md"
            si = root / "si.md"
            main.write_text(
                "# Abstract\n\nZSM-5 catalyzes methanol conversion.\n\n"
                "# Results\n\nThe main article reports high hydrocarbon selectivity.",
                encoding="utf-8",
            )
            si.write_text(
                "# Experimental\n\nThe catalyst was tested at 400 C and atmospheric pressure.\n\n"
                "# Supporting Information\n\nDetailed synthesis conditions are reported here.",
                encoding="utf-8",
            )
            manifest = root / "source.jsonl"
            records = [
                {
                    "path": str(main),
                    "paper_id": "doi:10.0000/test",
                    "document_id": "doc:main",
                    "document_type": "main",
                    "doi": "10.0000/test",
                },
                {
                    "path": str(si),
                    "paper_id": "doi:10.0000/test",
                    "document_id": "doc:si",
                    "document_type": "si",
                    "doi": "10.0000/test",
                },
            ]
            manifest.write_text(
                "".join(json.dumps(row) + "\n" for row in records),
                encoding="utf-8",
            )
            workspace = root / "workspace"
            config = PipelineConfig(
                source=manifest,
                workspace=workspace,
                parser=ParserConfig(
                    engine="auto",
                    docling_fallback=False,
                    min_document_characters=20,
                    fail_on_low_quality=True,
                ),
                chunking=ChunkingConfig(
                    target_tokens=100,
                    overlap_tokens=10,
                    min_tokens=5,
                ),
                extraction=ExtractionConfig(enabled=False),
                index=IndexConfig(
                    backend="portable",
                    embedding_model="hash-embedding-v1",
                    vector_dimensions=64,
                    allow_hash_embedding_fallback=True,
                ),
            )
            run = asyncio.run(execute_run(config=config, run_id="markdown-rag"))
            index_directory = workspace / "indexes" / "markdown-rag-index"
            index_manifest = json.loads(
                (index_directory / "manifest.json").read_text(encoding="utf-8")
            )
            document_rows = [
                json.loads(line)
                for line in (index_directory / "documents.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            chunk_rows = [
                json.loads(line)
                for line in (index_directory / "chunks.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            retrieval = PortableRetriever(index_directory).retrieve(
                query="400 C atmospheric pressure",
                top_k=2,
                include_unverified=True,
            )

        self.assertEqual(run["status"], "completed")
        self.assertEqual(index_manifest["counts"]["papers"], 1)
        self.assertEqual(index_manifest["counts"]["documents"], 2)
        self.assertEqual(index_manifest["counts"]["main_documents"], 1)
        self.assertEqual(index_manifest["counts"]["si_documents"], 1)
        self.assertEqual({row["document_type"] for row in document_rows}, {"main", "si"})
        self.assertEqual({row["paper_id"] for row in chunk_rows}, {"doi:10.0000/test"})
        self.assertTrue(
            any(row["document_type"] == "si" for row in retrieval["retrieved_evidence"])
        )

    def test_acs_manifest_selection_is_stable_and_includes_si(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch = Path(temporary) / "batch_001"
            for article_name, si_count in (("10.1021_z-last", 0), ("10.1021_a-first", 2)):
                inner = batch / article_name / article_name
                (inner / "main-output").mkdir(parents=True)
                (inner / "main-output" / f"{article_name}.md").write_text(
                    "# Abstract\n\nCatalysis paper.",
                    encoding="utf-8",
                )
                (inner / f"{article_name}.pdf").write_bytes(b"%PDF-1.4\n%%EOF")
                for index in range(si_count):
                    si_dir = inner / "si-output" / f"si-{index + 1}"
                    si_dir.mkdir(parents=True)
                    (si_dir / f"si-{index + 1}.md").write_text(
                        "# Experimental\n\nSupporting details.",
                        encoding="utf-8",
                    )
            records, summary = build_records(batch, limit=1)

        self.assertEqual(summary["paper_count"], 1)
        self.assertEqual(summary["paper_ids"], ["doi:10.1021/a-first"])
        self.assertEqual(summary["main_document_count"], 1)
        self.assertEqual(summary["si_document_count"], 2)
        self.assertEqual(summary["papers_with_original_pdf"], 1)
        self.assertEqual({record["document_type"] for record in records}, {"main", "si"})

    def test_full_corpus_discovery_excludes_subsets_and_prefers_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            article_name = "10.1021_test.001"
            article = root / "ACS" / "file" / "batch_001" / article_name / article_name
            (article / "main-output").mkdir(parents=True)
            main = article / "main-output" / f"{article_name}.md"
            main.write_text("# Main\n\nZeolite catalysis article.", encoding="utf-8")
            (article / f"{article_name}.pdf").write_bytes(b"%PDF-1.4\n%%EOF")
            si = article / "si-output" / f"{article_name}_supporting"
            si.mkdir(parents=True)
            (si / "supporting.md").write_text("# SI\n\nDetails.", encoding="utf-8")
            duplicate = (
                root
                / "ACS"
                / "file"
                / "batch_001_spectra"
                / article_name
                / article_name
            )
            duplicate.mkdir(parents=True)
            (duplicate / f"{article_name}.pdf").write_bytes(b"duplicate")

            records, summary = discover_records(root)

        self.assertEqual(summary["paper_count"], 1)
        self.assertEqual(summary["document_count"], 2)
        self.assertIn("batch_001_spectra", summary["excluded_directories"])
        main_rows = [row for row in records if row["document_type"] == "main"]
        self.assertEqual(main_rows[0]["path"], str(main.resolve()))

    def test_merge_indexes_reuses_vectors_from_disjoint_shards(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            indexes: list[Path] = []
            for number, marker in ((1, "mordenite"), (2, "chabazite")):
                source = root / f"source-{number}.md"
                source.write_text(
                    f"# Results\n\n{marker} zeolite catalytic performance " * 8,
                    encoding="utf-8",
                )
                config = PipelineConfig(
                    source=source,
                    workspace=workspace,
                    parser=ParserConfig(
                        min_document_characters=20,
                        docling_fallback=False,
                    ),
                    chunking=ChunkingConfig(
                        target_tokens=100,
                        overlap_tokens=10,
                        min_tokens=5,
                    ),
                    extraction=ExtractionConfig(enabled=False),
                    index=IndexConfig(
                        backend="portable",
                        embedding_model="hash-embedding-v1",
                        vector_dimensions=64,
                        allow_hash_embedding_fallback=True,
                    ),
                )
                run_id = f"shard-{number}"
                asyncio.run(execute_run(config=config, run_id=run_id))
                self.assertTrue(
                    (workspace / "runs" / run_id / "ledger.sqlite").is_file()
                )
                indexes.append(workspace / "indexes" / f"{run_id}-index")

            self.assertFalse((workspace / "ledger.sqlite").exists())

            output = workspace / "indexes" / "merged"
            manifest = merge_indexes(
                index_directories=indexes,
                index_directory=output,
                index_id="merged",
                repository_root=PIPELINE_ROOT.parents[1],
            )
            retrieved = PortableRetriever(output).retrieve(
                query="chabazite",
                top_k=2,
                include_unverified=True,
            )
            verification = verify_index(output)

        self.assertEqual(manifest["counts"]["papers"], 2)
        self.assertEqual(manifest["counts"]["documents"], 2)
        self.assertTrue(verification["valid"])
        self.assertEqual(retrieved["selected_count"], 2)

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

    def test_chunking_splits_a_single_long_markdown_paragraph(self) -> None:
        pages = [
            PageRecord(
                page_index=1,
                text="# Results\n\n" + " ".join(f"value-{index}" for index in range(350)),
            )
        ]
        config = ChunkingConfig(target_tokens=100, overlap_tokens=10, min_tokens=5)
        chunks = build_chunks(paper_id="doc:long", pages=pages, config=config)

        self.assertGreater(len(chunks), 1)
        self.assertLessEqual(max(item.token_count for item in chunks), 100)

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
                    allow_hash_embedding_fallback=True,
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
            connection = sqlite3.connect(run_directory / "ledger.sqlite")
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
            connection = sqlite3.connect(run_directory / "ledger.sqlite")
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

    def test_partial_run_is_not_finalized_and_resume_retries_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "papers"
            workspace = root / "workspace"
            source.mkdir()
            write_text_pdf(
                source / "good.pdf",
                "Abstract catalyst conversion. Results selectivity reached 80 percent.",
            )
            write_text_pdf(
                source / "bad.pdf",
                "Abstract catalyst stability. Results activity remained stable.",
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
                index=IndexConfig(enabled=False),
            )

            def fail_one_pdf(**kwargs: object):
                paper = kwargs["paper"]
                if Path(str(paper["source_path"])).name == "bad.pdf":
                    raise RuntimeError("intentional parse failure")
                return real_parse_pdf(**kwargs)

            with patch(
                "catalysis_literature.pipeline.parse_pdf",
                side_effect=fail_one_pdf,
            ):
                partial = asyncio.run(
                    execute_run(config=config, run_id="partial-resume-run")
                )
            run_directory = run_directory_for(workspace, "partial-resume-run")
            partial_finalized_exists = (run_directory / "FINALIZED.json").exists()
            first_journal = [
                json.loads(line)
                for line in (run_directory / "paper-results.journal.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            resumed = asyncio.run(
                execute_run(
                    config=config,
                    run_id="partial-resume-run",
                    resume=True,
                )
            )
            final_results = [
                json.loads(line)
                for line in (run_directory / "paper-results.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            final_journal = [
                json.loads(line)
                for line in (run_directory / "paper-results.journal.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            completed_finalized_exists = (run_directory / "FINALIZED.json").exists()

        self.assertEqual(partial["status"], "partial")
        self.assertFalse(partial_finalized_exists)
        self.assertEqual(len(first_journal), 2)
        self.assertEqual(
            sum(row["status"] == "completed" for row in first_journal),
            1,
        )
        self.assertEqual(resumed["status"], "completed")
        self.assertEqual(len(final_results), 2)
        self.assertTrue(all(row["status"] == "completed" for row in final_results))
        self.assertEqual(len(final_journal), 3)
        self.assertTrue(completed_finalized_exists)

    def test_preflight_estimates_two_model_calls_per_paper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "papers"
            source.mkdir()
            write_text_pdf(source / "one.pdf", "Abstract one catalytic paper.")
            write_text_pdf(source / "two.pdf", "Abstract a different catalytic paper.")
            config = PipelineConfig(
                source=source,
                workspace=root / "workspace",
                extraction=ExtractionConfig(provider="mock"),
                index=IndexConfig(
                    enabled=False,
                    embedding_revision="test-revision",
                    allow_hash_embedding_fallback=False,
                ),
            )
            report = build_preflight_report(config=config)

        self.assertEqual(report["selection"]["paper_count"], 2)
        self.assertEqual(report["estimated_work"]["model_calls"], 4)
        self.assertTrue(report["ready"])


if __name__ == "__main__":
    unittest.main()
