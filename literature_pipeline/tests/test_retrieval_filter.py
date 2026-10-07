from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from catalysis_literature.config import IndexConfig  # noqa: E402
from catalysis_literature.hashing import content_hash, sha256_file  # noqa: E402
from catalysis_literature.indexing import EmbeddingProvider  # noqa: E402
from catalysis_literature.models import INDEX_SCHEMA_VERSION  # noqa: E402
from catalysis_literature.retrieval import PortableRetriever  # noqa: E402


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _prepare_index(root: Path) -> Path:
    index = root / "index"
    index.mkdir()
    papers = [
        {"paper_id": "paper:allowed", "document_count": 1},
        {"paper_id": "doi:10.1126/science.ads7290", "document_count": 1},
    ]
    documents = [
        {
            "document_id": "document:allowed",
            "paper_id": "paper:allowed",
            "document_type": "main",
        },
        {
            "document_id": "document:excluded",
            "paper_id": "doi:10.1126/science.ads7290",
            "document_type": "si",
        },
    ]
    chunks = [
        {
            "record_id": "chunk:allowed",
            "paper_id": "paper:allowed",
            "document_id": "document:allowed",
            "document_type": "main",
            "kind": "chunk",
            "source_record_id": "chunk:allowed",
            "source_path": "/source/allowed.md",
            "section": "Catalytic performance",
            "text": "MTO conversion over MFI zeolite.",
            "fts_text": "mto conversion over mfi zeolite",
            "page_start": 1,
            "page_end": 1,
            "review_status": "extracted",
            "evidence_validation": "exact",
            "neighbor_ids_json": "[]",
        },
        {
            "record_id": "chunk:excluded",
            "paper_id": "doi:10.1126/science.ads7290",
            "document_id": "document:excluded",
            "document_type": "si",
            "kind": "chunk",
            "source_record_id": "chunk:excluded",
            "source_path": "/source/excluded.pdf",
            "section": None,
            "text": "exclusive-search-marker",
            "fts_text": "exclusive-search-marker",
            "page_start": 1,
            "page_end": 1,
            "review_status": "extracted",
            "evidence_validation": "exact",
            "neighbor_ids_json": "[]",
        },
    ]
    _write_jsonl(index / "papers.jsonl", papers)
    _write_jsonl(index / "documents.jsonl", documents)
    _write_jsonl(index / "chunks.jsonl", chunks)
    _write_jsonl(index / "evidence_records.jsonl", [])
    config = IndexConfig(
        embedding_model="hash-embedding-v1",
        vector_dimensions=32,
        allow_hash_embedding_fallback=True,
    )
    embedder = EmbeddingProvider(config)
    np.save(index / "chunk_vectors.npy", embedder.encode([row["text"] for row in chunks]))
    np.save(index / "evidence_vectors.npy", np.empty((0, 32), dtype=np.float32))
    artifacts = {
        name: {
            "path": name,
            "sha256": sha256_file(index / name),
            "bytes": (index / name).stat().st_size,
        }
        for name in (
            "papers.jsonl",
            "documents.jsonl",
            "chunks.jsonl",
            "evidence_records.jsonl",
            "chunk_vectors.npy",
            "evidence_vectors.npy",
        )
    }
    manifest = {
        "schema_version": INDEX_SCHEMA_VERSION,
        "index_id": "filter-test-index",
        "logical_content_hash": "filter-test-logical-hash",
        "embedding": {
            "requested_model": "hash-embedding-v1",
            "requested_revision": "builtin",
            "actual_model": "hash-embedding-v1",
            "actual_revision": "builtin",
            "backend": "hash",
            "dimensions": 32,
        },
        "retrieval": {
            "top_k_dense": 10,
            "top_k_lexical": 10,
            "top_k_final": 5,
            "max_records_per_paper": 2,
            "context_token_budget": 1000,
        },
        "counts": {"papers": 2, "documents": 2, "chunks": 2, "evidence_records": 0},
        "artifacts": artifacts,
        "manifest_content_hash": "",
    }
    manifest["manifest_content_hash"] = content_hash(
        {**manifest, "manifest_content_hash": ""}
    )
    (index / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return index


class RetrievalFilterTests(unittest.TestCase):
    def test_exclusion_is_applied_before_ranking_without_mutating_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            index = _prepare_index(Path(temporary))
            before = {
                path.name: sha256_file(path)
                for path in index.iterdir()
                if path.is_file()
            }
            retriever = PortableRetriever(
                index,
                excluded_paper_ids=["doi:10.1126/science.ads7290"],
                expected_excluded_documents=1,
                expected_excluded_records=1,
                expected_retained_papers=1,
                expected_retained_documents=1,
                expected_retained_chunks=1,
            )
            rows = retriever.retrieve_candidates(
                query="exclusive-search-marker",
                limit=5,
            )
            after = {
                path.name: sha256_file(path)
                for path in index.iterdir()
                if path.is_file()
            }

        self.assertFalse(
            any(row["paper_id"] == "doi:10.1126/science.ads7290" for row in rows)
        )
        self.assertEqual(retriever.filter_summary["retained_papers"], 1)
        self.assertEqual(retriever.filter_summary["retained_documents"], 1)
        self.assertEqual(retriever.filter_summary["retained_chunks"], 1)
        self.assertEqual(retriever.filter_summary["retained_evidence_records"], 0)
        self.assertEqual(retriever.filter_summary["excluded_records"], 1)
        self.assertEqual(before, after)

        trace = retriever.retrieve(query="MTO conversion", top_k=1)
        evidence = trace["retrieved_evidence"][0]
        self.assertIsNone(evidence["page"])
        self.assertEqual(
            evidence["provenance_locator"],
            {
                "kind": "markdown_section",
                "section": "Catalytic performance",
            },
        )
        self.assertIn(
            "locator=markdown_section:Catalytic performance",
            trace["context"],
        )

    def test_exclusion_count_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            index = _prepare_index(Path(temporary))
            with self.assertRaisesRegex(RuntimeError, "record count mismatch"):
                PortableRetriever(
                    index,
                    excluded_paper_ids=["doi:10.1126/science.ads7290"],
                    expected_excluded_documents=1,
                    expected_excluded_records=19,
                )

    def test_retained_count_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            index = _prepare_index(Path(temporary))
            with self.assertRaisesRegex(RuntimeError, "Retained chunks count mismatch"):
                PortableRetriever(
                    index,
                    excluded_paper_ids=["doi:10.1126/science.ads7290"],
                    expected_excluded_documents=1,
                    expected_excluded_records=1,
                    expected_retained_papers=1,
                    expected_retained_documents=1,
                    expected_retained_chunks=2,
                )


if __name__ == "__main__":
    unittest.main()
