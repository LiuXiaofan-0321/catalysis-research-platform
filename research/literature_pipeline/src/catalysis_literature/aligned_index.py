from __future__ import annotations

import json
import re
import shutil
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from .chunking import TOKEN_PATTERN, token_count
from .config import IndexConfig
from .hashing import (
    atomic_write_json,
    canonical_json,
    content_hash,
    sha256_file,
    sha256_text,
    stable_id,
)
from .indexing import EmbeddingProvider, fts_text, verify_index
from .models import INDEX_SCHEMA_VERSION


HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*$")
SPACE_RE = re.compile(r"\s+")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as target:
        for row in rows:
            target.write(canonical_json(row) + "\n")


def _normalized(value: str) -> str:
    return SPACE_RE.sub(" ", value).strip().casefold()


def _decode_source_markdown(path: Path) -> tuple[str, str, int]:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), "strict_utf8", 0
    except UnicodeDecodeError:
        decoded = raw.decode("utf-8", errors="replace")
        return decoded, "utf8_with_replacement", decoded.count("\ufffd")


def _paragraphs(markdown: str) -> list[dict[str, str | None]]:
    section: str | None = None
    rows: list[dict[str, str | None]] = []
    for block in re.split(r"\n\s*\n", markdown):
        text = SPACE_RE.sub(" ", block).strip()
        if not text:
            continue
        heading = HEADING_RE.fullmatch(text[:500])
        if heading:
            section = SPACE_RE.sub(" ", heading.group(1)).strip()
            continue
        if text.startswith("<div") and "<img " in text:
            continue
        rows.append({"section": section, "text": text})
    return rows


def _evidence(extraction: dict[str, Any]) -> Iterable[dict[str, Any]]:
    stack: list[Any] = [extraction]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            evidence = value.get("evidence")
            if isinstance(evidence, list):
                for item in evidence:
                    if isinstance(item, dict) and item.get("quote"):
                        yield item
            for key, child in value.items():
                if key != "evidence":
                    stack.append(child)
        elif isinstance(value, list):
            stack.extend(value)


def _split_text(text: str, target_tokens: int, overlap_tokens: int) -> list[str]:
    matches = list(TOKEN_PATTERN.finditer(text))
    if len(matches) <= target_tokens:
        return [text]
    step = target_tokens - overlap_tokens
    chunks = []
    for start in range(0, len(matches), step):
        window = matches[start : start + target_tokens]
        if not window:
            break
        chunks.append(text[window[0].start() : window[-1].end()].strip())
        if start + target_tokens >= len(matches):
            break
    return chunks


def _verify_corpus(corpus: Path) -> dict[str, Any]:
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    for name, artifact in manifest.get("artifacts", {}).items():
        path = corpus / name
        if not path.is_file() or sha256_file(path) != artifact.get("sha256"):
            raise ValueError(f"Frozen corpus artifact verification failed: {name}")
    return manifest


def build_evidence_aligned_index(
    *,
    corpus_directory: Path,
    output_directory: Path,
    index_id: str,
    index_config: IndexConfig,
    target_tokens: int = 500,
    overlap_tokens: int = 60,
    code_commit: str | None = None,
) -> dict[str, Any]:
    if target_tokens < 100 or not 0 <= overlap_tokens < target_tokens:
        raise ValueError("Invalid chunking token settings")
    corpus = corpus_directory.resolve()
    output = output_directory.resolve()
    if output.exists():
        raise FileExistsError(f"Index directory already exists: {output}")
    corpus_manifest = _verify_corpus(corpus)
    documents = _load_jsonl(corpus / "documents.jsonl")
    papers_inventory = _load_jsonl(corpus / "papers.jsonl")
    document_ids = [str(row["document_id"]) for row in documents]
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("Frozen corpus contains duplicate document IDs")

    paper_metadata: dict[str, dict[str, Any]] = {}
    document_rows: list[dict[str, Any]] = []
    chunk_rows: list[dict[str, Any]] = []
    matched_evidence = 0
    total_evidence = 0
    source_hash_mismatches = 0
    source_decode_fallback_documents = 0
    source_decode_replacement_characters = 0
    page_conflicts = 0
    anchored_document_ids: set[str] = set()
    zip_path = corpus / "structured-documents.zip"
    with zipfile.ZipFile(zip_path) as archive:
        for document in documents:
            document_id = str(document["document_id"])
            paper_id = str(document["paper_id"])
            source_path = Path(str(document["source_path"]))
            if not source_path.is_file():
                raise FileNotFoundError(f"Missing frozen source document: {source_path}")
            actual_source_hash = sha256_file(source_path)
            if actual_source_hash != document["source_document_sha256"]:
                source_hash_mismatches += 1
                raise ValueError(f"Source document hash mismatch: {document_id}")
            artifact = json.loads(archive.read(document["artifact_entry"]))
            extraction = artifact.get("extraction") or {}
            paper = extraction.get("paper") or {}
            if document["document_type"] == "main":
                paper_metadata[paper_id] = {
                    "paper_id": paper_id,
                    "title": paper.get("title"),
                    "doi": paper.get("doi"),
                    "year": paper.get("year"),
                    "journal": paper.get("journal"),
                    "paper_type": paper.get("paper_type"),
                }
            source_markdown, decode_status, replacement_count = _decode_source_markdown(
                source_path
            )
            if replacement_count:
                source_decode_fallback_documents += 1
                source_decode_replacement_characters += replacement_count
            paragraphs = _paragraphs(source_markdown)
            normalized_paragraphs = [_normalized(str(row["text"])) for row in paragraphs]
            anchors: dict[int, dict[int, list[dict[str, Any]]]] = defaultdict(
                lambda: defaultdict(list)
            )
            document_evidence = list(_evidence(extraction))
            total_evidence += len(document_evidence)
            for evidence in document_evidence:
                quote = _normalized(str(evidence.get("quote") or ""))
                page = evidence.get("pdf_page_index")
                if len(quote) < 20 or not isinstance(page, int) or page < 1:
                    continue
                matches = [
                    index
                    for index, paragraph in enumerate(normalized_paragraphs)
                    if quote in paragraph
                ]
                if len(matches) != 1:
                    continue
                anchors[matches[0]][page].append(evidence)
                matched_evidence += 1
            document_chunk_count = 0
            for paragraph_index in sorted(anchors):
                pages = anchors[paragraph_index]
                if len(pages) > 1:
                    page_conflicts += 1
                    continue
                page, evidence_items = next(iter(pages.items()))
                paragraph = paragraphs[paragraph_index]
                for part_index, text in enumerate(
                    _split_text(str(paragraph["text"]), target_tokens, overlap_tokens),
                    start=1,
                ):
                    text_hash = sha256_text(text)
                    record_id = stable_id(
                        "aligned-chunk",
                        document_id,
                        page,
                        paragraph_index,
                        part_index,
                        text_hash,
                    )
                    chunk_rows.append(
                        {
                            "record_id": record_id,
                            "paper_id": paper_id,
                            "document_id": document_id,
                            "document_type": document["document_type"],
                            "kind": "chunk",
                            "source_record_id": record_id,
                            "text": text,
                            "fts_text": fts_text(text),
                            "section": paragraph["section"],
                            "page_start": page,
                            "page_end": page,
                            "review_status": "extracted",
                            "evidence_validation": "exact",
                            "source": "evidence_aligned_raw_paragraph",
                            "source_id": document_id,
                            "source_path": str(source_path),
                            "quote": None,
                            "metadata_json": canonical_json(
                                {
                                    "anchor_quote_hashes": sorted(
                                        {
                                            sha256_text(str(item["quote"]))
                                            for item in evidence_items
                                        }
                                    ),
                                    "source_text_sha256": text_hash,
                                    "token_count": token_count(text),
                                }
                            ),
                            "neighbor_ids_json": "[]",
                        }
                    )
                    document_chunk_count += 1
            if document_chunk_count:
                anchored_document_ids.add(document_id)
            document_rows.append(
                {
                    **document,
                    "source_document_sha256_verified": actual_source_hash,
                    "source_decode_status": decode_status,
                    "source_decode_replacement_count": replacement_count,
                    "aligned_chunk_count": document_chunk_count,
                    "evidence_record_count": len(document_evidence),
                }
            )

    expected_paper_ids = {str(row["paper_id"]) for row in papers_inventory}
    if set(paper_metadata) != expected_paper_ids:
        raise ValueError("Main-document paper metadata does not match frozen papers")
    paper_rows = [paper_metadata[paper_id] for paper_id in sorted(paper_metadata)]
    document_rows.sort(key=lambda row: row["document_id"])
    chunk_rows.sort(key=lambda row: row["record_id"])
    embedder = EmbeddingProvider(index_config)
    chunk_vectors = embedder.encode([row["text"] for row in chunk_rows])
    evidence_vectors = np.empty((0, embedder.dimensions), dtype=np.float32)

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        _write_jsonl(temporary / "papers.jsonl", paper_rows)
        _write_jsonl(temporary / "documents.jsonl", document_rows)
        _write_jsonl(temporary / "chunks.jsonl", chunk_rows)
        _write_jsonl(temporary / "evidence_records.jsonl", [])
        np.save(temporary / "chunk_vectors.npy", chunk_vectors)
        np.save(temporary / "evidence_vectors.npy", evidence_vectors)
        artifacts = {}
        for name in (
            "papers.jsonl",
            "documents.jsonl",
            "chunks.jsonl",
            "evidence_records.jsonl",
            "chunk_vectors.npy",
            "evidence_vectors.npy",
        ):
            path = temporary / name
            artifacts[name] = {
                "path": name,
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        logical_hash = content_hash(
            {
                "source_corpus_id": corpus_manifest["corpus_id"],
                "document_content_hash": corpus_manifest["document_content_hash"],
                "paper_content_hash": corpus_manifest["paper_content_hash"],
                "artifacts": artifacts,
                "embedding_model": embedder.actual_model,
                "embedding_revision": embedder.actual_revision,
                "dimensions": embedder.dimensions,
            }
        )
        manifest = {
            "schema_version": INDEX_SCHEMA_VERSION,
            "index_id": index_id,
            "created_at": corpus_manifest["frozen_at"],
            "run_id": "frozen-corpus-evidence-alignment",
            "backend": "portable",
            "logical_content_hash": logical_hash,
            "git": {"commit": code_commit},
            "source_corpus": {
                "corpus_id": corpus_manifest["corpus_id"],
                "manifest_sha256": sha256_file(corpus / "manifest.json"),
                "document_content_hash": corpus_manifest["document_content_hash"],
                "paper_content_hash": corpus_manifest["paper_content_hash"],
            },
            "embedding": {
                "requested_model": index_config.embedding_model,
                "requested_revision": index_config.embedding_revision,
                "actual_model": embedder.actual_model,
                "actual_revision": embedder.actual_revision,
                "backend": embedder.backend,
                "dimensions": embedder.dimensions,
            },
            "counts": {
                "papers": len(paper_rows),
                "documents": len(document_rows),
                "main_documents": sum(row["document_type"] == "main" for row in document_rows),
                "si_documents": sum(row["document_type"] == "si" for row in document_rows),
                "anchored_documents": len(anchored_document_ids),
                "chunks": len(chunk_rows),
                "evidence_records": 0,
                "source_evidence_records": total_evidence,
                "matched_evidence_records": matched_evidence,
                "page_conflicts": page_conflicts,
                "source_hash_mismatches": source_hash_mismatches,
                "source_decode_fallback_documents": source_decode_fallback_documents,
                "source_decode_replacement_characters": source_decode_replacement_characters,
            },
            "retrieval": {
                "top_k_dense": index_config.top_k_dense,
                "top_k_lexical": index_config.top_k_lexical,
                "top_k_final": index_config.top_k_final,
                "max_records_per_paper": index_config.max_records_per_paper,
                "context_token_budget": index_config.context_token_budget,
            },
            "alignment": {
                "method": "unique normalized evidence quote substring in raw Markdown paragraph",
                "target_tokens": target_tokens,
                "overlap_tokens": overlap_tokens,
                "unanchored_paragraph_policy": "excluded",
                "page_conflict_policy": "excluded",
            },
            "artifacts": artifacts,
            "warnings": [
                "This is an evidence-aligned raw-paragraph index, not a lossless full-text index.",
                "Paragraph inclusion depends on frozen structured-extraction evidence anchors.",
                "Malformed UTF-8 source bytes are decoded with replacement and counted per document.",
            ],
            "manifest_content_hash": "",
        }
        manifest["manifest_content_hash"] = content_hash(
            {**manifest, "manifest_content_hash": ""}
        )
        atomic_write_json(temporary / "manifest.json", manifest)
        temporary.replace(output)
        report = verify_index(output)
        if not report["valid"]:
            raise RuntimeError("Built index failed verification: " + "; ".join(report["failures"]))
        return manifest
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
