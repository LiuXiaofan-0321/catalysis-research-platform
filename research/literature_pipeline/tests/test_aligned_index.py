from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "literature_pipeline" / "src"))

from catalysis_literature.aligned_index import build_evidence_aligned_index  # noqa: E402
from catalysis_literature.config import IndexConfig  # noqa: E402
from catalysis_literature.indexing import verify_index  # noqa: E402
from catalysis_literature.retrieval import PortableRetriever  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _artifact(document_id: str, title: str, quote: str | None) -> dict[str, object]:
    evidence = [] if quote is None else [{
        "document_id": document_id,
        "document_type": "main",
        "pdf_page_index": 3,
        "quote": quote,
        "evidence_validation": "exact",
    }]
    return {
        "extraction": {
            "paper": {
                "id": "paper:test",
                "title": title,
                "doi": "10.0000/test",
                "year": 2026,
                "journal": "Test",
                "paper_type": "research_article",
            },
            "summary": {"main_findings": [{"statement": "Active", "evidence": evidence}]},
            "keywords": {"extracted": []},
            "entities": [],
            "experiments": [],
            "observations": [],
            "claims": [],
        }
    }


def test_builds_identity_aligned_grounded_paragraph_index() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        corpus = root / "corpus"
        corpus.mkdir()
        quote = "Methanol conversion reached 80 percent at 673 K over H-ZSM-5."
        main = root / "main.md"
        main.write_text(
            "# Test paper\n\n## Results\n\n"
            + quote
            + " The catalyst remained stable.\n\nAn unrelated paragraph.\n",
            encoding="utf-8",
        )
        si = root / "si.md"
        si.write_text("# Supporting information\n\nNo anchored result here.\n", encoding="utf-8")
        documents = [
            {
                "document_id": "document:main",
                "paper_id": "paper:test",
                "document_type": "main",
                "source_path": str(main),
                "source_document_sha256": _sha(main),
                "artifact_entry": "json/main.json",
            },
            {
                "document_id": "document:si",
                "paper_id": "paper:test",
                "document_type": "si",
                "source_path": str(si),
                "source_document_sha256": _sha(si),
                "artifact_entry": "json/si.json",
            },
        ]
        _write_jsonl(corpus / "documents.jsonl", documents)
        _write_jsonl(corpus / "papers.jsonl", [{
            "paper_id": "paper:test",
            "document_ids": ["document:main", "document:si"],
            "main_document_ids": ["document:main"],
            "si_document_ids": ["document:si"],
        }])
        (corpus / "quality-summary.json").write_text("{}\n", encoding="utf-8")
        (corpus / "review-sample.jsonl").write_text("", encoding="utf-8")
        (corpus / "review-sample.md").write_text("# Review\n", encoding="utf-8")
        with zipfile.ZipFile(corpus / "structured-documents.zip", "w") as archive:
            archive.writestr("json/main.json", json.dumps(_artifact("document:main", "Test paper", quote)))
            archive.writestr("json/si.json", json.dumps(_artifact("document:si", "SI", None)))
        artifacts = {}
        for name in (
            "documents.jsonl",
            "papers.jsonl",
            "quality-summary.json",
            "review-sample.jsonl",
            "review-sample.md",
            "structured-documents.zip",
        ):
            path = corpus / name
            artifacts[name] = {"sha256": _sha(path), "bytes": path.stat().st_size}
        (corpus / "manifest.json").write_text(json.dumps({
            "corpus_id": "aligned-test-v1",
            "frozen_at": "2026-09-02T00:00:00+00:00",
            "document_content_hash": "documents-test",
            "paper_content_hash": "papers-test",
            "artifacts": artifacts,
        }), encoding="utf-8")

        index = root / "index"
        manifest = build_evidence_aligned_index(
            corpus_directory=corpus,
            output_directory=index,
            index_id="aligned-test-index-v1",
            index_config=IndexConfig(
                backend="portable",
                embedding_model="hash-embedding-v1",
                embedding_revision="builtin",
                vector_dimensions=64,
                allow_hash_embedding_fallback=True,
                top_k_final=5,
            ),
            code_commit="test",
        )
        assert manifest["counts"]["papers"] == 1
        assert manifest["counts"]["documents"] == 2
        assert manifest["counts"]["anchored_documents"] == 1
        assert manifest["counts"]["chunks"] == 1
        assert manifest["counts"]["source_hash_mismatches"] == 0
        assert verify_index(index)["valid"] is True

        trace = PortableRetriever(index).retrieve(query="methanol conversion 673 K")
        assert trace["retrieved_evidence"][0]["paper_id"] == "paper:test"
        assert trace["retrieved_evidence"][0]["document_id"] == "document:main"
        assert trace["retrieved_evidence"][0]["page"] == 3
        assert quote in trace["retrieved_evidence"][0]["quote"]
