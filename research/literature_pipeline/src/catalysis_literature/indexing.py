from __future__ import annotations

import importlib.util
import json
import math
import re
import shutil
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from .config import IndexConfig
from .hashing import (
    atomic_write_json,
    canonical_json,
    content_hash,
    sha256_file,
    stable_id,
)
from .manifest import git_state, utc_now
from .models import INDEX_SCHEMA_VERSION, ParsedDocument


WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:[+._/-][A-Za-z0-9]+)*")
HAN_PATTERN = re.compile(r"[\u3400-\u9fff]+")


def search_tokens(value: str) -> list[str]:
    normalized = value.casefold()
    result = set(WORD_PATTERN.findall(normalized))
    for chunk in HAN_PATTERN.findall(normalized):
        if len(chunk) <= 4:
            result.add(chunk)
        for size in (2, 3, 4):
            for index in range(max(0, len(chunk) - size + 1)):
                result.add(chunk[index : index + size])
    return sorted(result)


def fts_text(value: str) -> str:
    return " ".join(search_tokens(value))


class EmbeddingProvider:
    def __init__(self, config: IndexConfig):
        self.config = config
        self.actual_model = config.embedding_model
        self.actual_revision = config.embedding_revision
        self.dimensions = config.vector_dimensions
        self.backend = "hash"
        self._model: Any = None
        if config.embedding_model == "hash-embedding-v1":
            if not config.allow_hash_embedding_fallback:
                raise RuntimeError(
                    "hash-embedding-v1 is test-only; explicitly enable "
                    "allow_hash_embedding_fallback for offline tests"
                )
            self.actual_revision = "builtin"
            return
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(
                config.embedding_model,
                revision=(
                    None
                    if config.embedding_revision == "default"
                    else config.embedding_revision
                ),
            )
            dimension_reader = getattr(
                self._model,
                "get_embedding_dimension",
                None,
            ) or getattr(self._model, "get_sentence_embedding_dimension", None)
            dimensions = dimension_reader() if dimension_reader else None
            if dimensions:
                self.dimensions = int(dimensions)
            self.backend = "sentence-transformers"
        except (ImportError, ModuleNotFoundError, OSError, RuntimeError):
            if not config.allow_hash_embedding_fallback:
                raise
            self.actual_model = "hash-embedding-v1"
            self.actual_revision = "builtin"

    def _hash_embedding(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimensions, dtype=np.float32)
        for token in search_tokens(text):
            digest = bytes.fromhex(content_hash(token))
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign * (1.0 + math.log1p(len(token)))
        norm = float(np.linalg.norm(vector))
        return vector / norm if norm else vector

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float32)
        if self._model is None:
            return np.stack([self._hash_embedding(text) for text in texts])
        values = self._model.encode(
            texts,
            batch_size=self.config.embedding_batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(values, dtype=np.float32)


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(canonical_json(row))
            handle.write("\n")


def _load_results(run_directory: Path) -> list[dict[str, Any]]:
    path = run_directory / "paper-results.jsonl"
    if not path.is_file():
        raise FileNotFoundError(f"Run has no paper-results.jsonl: {run_directory}")
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _evidence_rows(extraction: dict[str, Any]) -> list[dict[str, Any]]:
    paper = extraction["paper"]
    paper_id = str(paper["id"])
    rows: list[dict[str, Any]] = []

    def add(kind: str, item: dict[str, Any], text: str) -> None:
        evidence = item.get("evidence") or []
        for evidence_index, entry in enumerate(evidence, start=1):
            quote = str(entry.get("quote") or "").strip()
            if not quote:
                continue
            record_id = stable_id(
                "evidence",
                paper_id,
                kind,
                item.get("id"),
                evidence_index,
                quote,
            )
            combined = "\n".join(part for part in (text, quote) if part)
            rows.append(
                {
                    "record_id": record_id,
                    "paper_id": paper_id,
                    "kind": kind,
                    "source_record_id": item.get("id"),
                    "text": combined,
                    "fts_text": fts_text(combined),
                    "section": entry.get("section"),
                    "page_start": entry.get("pdf_page_index"),
                    "page_end": entry.get("pdf_page_index"),
                    "review_status": item.get("review_status") or "extracted",
                    "evidence_validation": entry.get("evidence_validation")
                    or "unverified",
                    "source": entry.get("source") or "text",
                    "source_id": entry.get("source_id"),
                    "quote": quote,
                    "metadata_json": canonical_json(item),
                    "neighbor_ids_json": "[]",
                }
            )

    for finding in (extraction.get("summary") or {}).get("main_findings") or []:
        if isinstance(finding, dict):
            add("finding", finding, str(finding.get("statement") or ""))
    for keyword in (extraction.get("keywords") or {}).get("extracted") or []:
        if isinstance(keyword, dict):
            add(
                "keyword",
                keyword,
                " ".join(
                    str(value or "")
                    for value in (
                        keyword.get("raw_term"),
                        keyword.get("normalized_term"),
                        keyword.get("definition_in_context"),
                    )
                ),
            )
    for kind, field, text_field in (
        ("entity", "entities", "canonical_name"),
        ("experiment", "experiments", "objective"),
        ("observation", "observations", "metric_name"),
        ("claim", "claims", "statement"),
    ):
        for item in extraction.get(field) or []:
            if isinstance(item, dict):
                text = str(item.get(text_field) or "")
                if kind == "observation":
                    text += " " + str(item.get("raw_value") or item.get("text_value") or "")
                add(kind, item, text.strip())
    return _link_evidence_neighbors(rows)


def _link_evidence_neighbors(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_paper_and_source: dict[tuple[str, str], list[str]] = {}
    for row in rows:
        source_record_id = row.get("source_record_id")
        if source_record_id:
            by_paper_and_source.setdefault(
                (row["paper_id"], str(source_record_id)),
                [],
            ).append(row["record_id"])
    neighbors: dict[str, set[str]] = {
        row["record_id"]: set() for row in rows
    }
    for row in rows:
        metadata = json.loads(row["metadata_json"])
        references: list[str] = []
        for key in (
            "experiment_id",
            "sample_entity_id",
            "property_entity_id",
            "method_entity_id",
        ):
            if metadata.get(key):
                references.append(str(metadata[key]))
        for key in (
            "sample_entity_ids",
            "material_entity_ids",
            "method_entity_ids",
        ):
            references.extend(str(value) for value in metadata.get(key) or [])
        same_record = by_paper_and_source.get(
            (row["paper_id"], str(row.get("source_record_id") or "")),
            [],
        )
        references_ids = [
            record_id
            for reference in references
            for record_id in by_paper_and_source.get(
                (row["paper_id"], reference),
                [],
            )
        ]
        for target in [*same_record, *references_ids]:
            if target == row["record_id"]:
                continue
            neighbors[row["record_id"]].add(target)
            neighbors[target].add(row["record_id"])
    for row in rows:
        row["neighbor_ids_json"] = canonical_json(
            sorted(neighbors[row["record_id"]])
        )
    return rows


def _logical_rows(run_directory: Path) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    papers_by_id: dict[str, dict[str, Any]] = {}
    documents: list[dict[str, Any]] = []
    chunks: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for result in _load_results(run_directory):
        if result.get("status") != "completed":
            continue
        parsed_path = Path(result["parsed_artifact_path"])
        parsed = ParsedDocument.model_validate_json(
            parsed_path.read_text(encoding="utf-8")
        )
        extraction_path = result.get("extraction_artifact_path")
        extraction: dict[str, Any] | None = None
        if extraction_path:
            extraction = json.loads(
                Path(extraction_path).read_text(encoding="utf-8")
            )["extraction"]
        metadata = parsed.source_metadata
        paper_data = extraction["paper"] if extraction is not None else {}
        resolved_paper_id = str(paper_data.get("id") or parsed.paper_id)
        title = str(
            paper_data.get("title")
            or metadata.get("title")
            or Path(parsed.source_path).stem
        )
        paper = papers_by_id.get(resolved_paper_id)
        if paper is None:
            paper = {
                "paper_id": resolved_paper_id,
                "title": title,
                "doi": paper_data.get("doi") or metadata.get("doi"),
                "year": paper_data.get("year") or metadata.get("year"),
                "journal": paper_data.get("journal") or metadata.get("journal"),
                "paper_type": paper_data.get("paper_type"),
                "catalysis_system": paper_data.get("catalysis_system") or "unclear",
                "reaction_categories_json": canonical_json(
                    paper_data.get("reaction_categories") or []
                ),
                "main_source_path": None,
                "document_count": 0,
                "main_document_count": 0,
                "si_document_count": 0,
                "quality_json": canonical_json(
                    (extraction or {}).get("quality") or parsed.quality
                ),
            }
            papers_by_id[resolved_paper_id] = paper
        if parsed.document_type == "main":
            paper["title"] = title
            paper["main_source_path"] = parsed.source_path
            paper["quality_json"] = canonical_json(parsed.quality)
        paper["document_count"] += 1
        if parsed.document_type == "main":
            paper["main_document_count"] += 1
        elif parsed.document_type == "si":
            paper["si_document_count"] += 1
        documents.append(
            {
                "document_id": parsed.document_id,
                "paper_id": resolved_paper_id,
                "document_type": parsed.document_type,
                "source_path": parsed.source_path,
                "source_media_type": parsed.source_media_type,
                "source_document_sha256": parsed.source_pdf_sha256,
                "page_count": parsed.page_count,
                "extracted_characters": parsed.extracted_characters,
                "chunk_count": len(parsed.chunks),
                "quality_json": canonical_json(parsed.quality),
                "metadata_json": canonical_json(metadata),
            }
        )
        for chunk in parsed.chunks:
            text = chunk.text
            chunks.append(
                {
                    "record_id": chunk.chunk_id,
                    "paper_id": resolved_paper_id,
                    "document_id": parsed.document_id,
                    "document_type": parsed.document_type,
                    "kind": "chunk",
                    "source_record_id": chunk.chunk_id,
                    "text": text,
                    "fts_text": fts_text(text),
                    "section": chunk.section,
                    "page_start": chunk.page_start,
                    "page_end": chunk.page_end,
                    "review_status": "extracted",
                    "evidence_validation": "exact",
                    "source": "text",
                    "source_id": parsed.document_id,
                    "source_path": parsed.source_path,
                    "quote": None,
                    "metadata_json": canonical_json(
                        {
                            "token_count": chunk.token_count,
                            "source_text_sha256": chunk.source_text_sha256,
                            "document_id": parsed.document_id,
                            "document_type": parsed.document_type,
                        }
                    ),
                    "neighbor_ids_json": "[]",
                }
            )
        if extraction is not None:
            evidence.extend(_evidence_rows(extraction))
    papers = sorted(papers_by_id.values(), key=lambda row: row["paper_id"])
    documents.sort(key=lambda row: row["document_id"])
    chunks.sort(key=lambda row: row["record_id"])
    evidence.sort(key=lambda row: row["record_id"])
    return papers, documents, chunks, evidence


def _build_lancedb(
    index_directory: Path,
    *,
    papers: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    chunk_vectors: np.ndarray,
    evidence_vectors: np.ndarray,
) -> tuple[str, list[str]]:
    import lancedb

    warnings: list[str] = []
    database = lancedb.connect(index_directory / "lancedb")
    database.create_table("papers", data=papers, mode="overwrite")
    database.create_table("documents", data=documents, mode="overwrite")
    for name, rows, vectors in (
        ("chunks", chunks, chunk_vectors),
        ("evidence_records", evidence, evidence_vectors),
    ):
        data = [
            {**row, "vector": vector.tolist()}
            for row, vector in zip(rows, vectors, strict=True)
        ]
        table = database.create_table(name, data=data, mode="overwrite")
        try:
            table.create_fts_index("fts_text", replace=True)
        except Exception as error:
            warnings.append(f"{name} FTS index: {type(error).__name__}: {error}")
        if len(rows) >= 256:
            try:
                table.create_index(
                    vector_column_name="vector",
                    metric="cosine",
                    replace=True,
                )
            except Exception as error:
                warnings.append(
                    f"{name} vector index: {type(error).__name__}: {error}"
                )
    return "lancedb", warnings


def build_index(
    *,
    run_directory: Path,
    index_directory: Path,
    index_id: str,
    config: IndexConfig,
    repository_root: Path,
) -> dict[str, Any]:
    run_directory = run_directory.resolve()
    index_directory = index_directory.resolve()
    if index_directory.exists():
        raise FileExistsError(f"Index directory already exists: {index_directory}")
    temporary = index_directory.with_name(f".{index_directory.name}.tmp")
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir(parents=True)
    try:
        papers, documents, chunks, evidence = _logical_rows(run_directory)
        embedder = EmbeddingProvider(config)
        chunk_vectors = embedder.encode([row["text"] for row in chunks])
        evidence_vectors = embedder.encode([row["text"] for row in evidence])
        _write_jsonl(temporary / "papers.jsonl", papers)
        _write_jsonl(temporary / "documents.jsonl", documents)
        _write_jsonl(temporary / "chunks.jsonl", chunks)
        _write_jsonl(temporary / "evidence_records.jsonl", evidence)
        np.save(temporary / "chunk_vectors.npy", chunk_vectors)
        np.save(temporary / "evidence_vectors.npy", evidence_vectors)
        backend = "portable"
        warnings: list[str] = []
        wants_lance = config.backend in {"auto", "lancedb"}
        if wants_lance and importlib.util.find_spec("lancedb"):
            try:
                backend, warnings = _build_lancedb(
                    temporary,
                    papers=papers,
                    documents=documents,
                    chunks=chunks,
                    evidence=evidence,
                    chunk_vectors=chunk_vectors,
                    evidence_vectors=evidence_vectors,
                )
            except Exception as error:
                if config.backend == "lancedb":
                    raise
                warnings.append(
                    f"LanceDB build failed; portable index retained: "
                    f"{type(error).__name__}: {error}"
                )
        elif config.backend == "lancedb":
            raise RuntimeError("LanceDB backend requested but lancedb is not installed")
        logical_hash = content_hash(
            {
                "papers": papers,
                "documents": documents,
                "chunks": chunks,
                "evidence": evidence,
                "embedding_model": embedder.actual_model,
                "embedding_revision": embedder.actual_revision,
                "dimensions": embedder.dimensions,
            }
        )
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
        manifest = {
            "schema_version": INDEX_SCHEMA_VERSION,
            "index_id": index_id,
            "created_at": utc_now(),
            "run_id": run_directory.name,
            "backend": backend,
            "logical_content_hash": logical_hash,
            "git": git_state(repository_root),
            "embedding": {
                "requested_model": config.embedding_model,
                "requested_revision": config.embedding_revision,
                "actual_model": embedder.actual_model,
                "actual_revision": embedder.actual_revision,
                "backend": embedder.backend,
                "dimensions": embedder.dimensions,
            },
            "counts": {
                "papers": len(papers),
                "documents": len(documents),
                "main_documents": sum(
                    row["document_type"] == "main" for row in documents
                ),
                "si_documents": sum(
                    row["document_type"] == "si" for row in documents
                ),
                "chunks": len(chunks),
                "evidence_records": len(evidence),
            },
            "retrieval": {
                "top_k_dense": config.top_k_dense,
                "top_k_lexical": config.top_k_lexical,
                "top_k_final": config.top_k_final,
                "max_records_per_paper": config.max_records_per_paper,
                "context_token_budget": config.context_token_budget,
            },
            "artifacts": artifacts,
            "warnings": warnings,
            "manifest_content_hash": "",
        }
        manifest["manifest_content_hash"] = content_hash(
            {**manifest, "manifest_content_hash": ""}
        )
        atomic_write_json(temporary / "manifest.json", manifest)
        temporary.replace(index_directory)
        return manifest
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def verify_index(index_directory: Path) -> dict[str, Any]:
    failures: list[str] = []
    manifest_path = index_directory / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {"valid": False, "failures": [str(error)]}
    if manifest.get("schema_version") != INDEX_SCHEMA_VERSION:
        failures.append("Unsupported index schema")
    expected_hash = content_hash({**manifest, "manifest_content_hash": ""})
    if expected_hash != manifest.get("manifest_content_hash"):
        failures.append("Index manifest content hash mismatch")
    for name, artifact in (manifest.get("artifacts") or {}).items():
        path = index_directory / artifact["path"]
        if not path.is_file():
            failures.append(f"Missing index artifact: {name}")
        elif sha256_file(path) != artifact.get("sha256"):
            failures.append(f"Index artifact hash mismatch: {name}")
    return {
        "index_id": manifest.get("index_id"),
        "valid": not failures,
        "failures": failures,
        "logical_content_hash": manifest.get("logical_content_hash"),
        "counts": manifest.get("counts"),
    }
