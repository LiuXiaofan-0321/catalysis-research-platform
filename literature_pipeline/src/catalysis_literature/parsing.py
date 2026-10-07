from __future__ import annotations

import importlib.metadata
import json
import re
import time
from pathlib import Path
from typing import Any

from .chunking import build_chunks
from .config import ChunkingConfig, ParserConfig
from .hashing import atomic_write_json, content_hash, sha256_file, sha256_text
from .models import PageRecord, ParsedDocument


def _module_version(distribution: str, fallback: str = "unknown") -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return fallback


def _extract_with_pymupdf(path: Path) -> tuple[list[PageRecord], str, str]:
    import fitz

    document = fitz.open(path)
    pages: list[PageRecord] = []
    try:
        for page_index, page in enumerate(document, start=1):
            raw_blocks = page.get_text("blocks", sort=True)
            blocks: list[dict[str, Any]] = []
            text_parts: list[str] = []
            for block in raw_blocks:
                value = str(block[4] or "").replace("\x00", "").strip()
                if not value:
                    continue
                blocks.append(
                    {
                        "bbox": [float(part) for part in block[:4]],
                        "text": value,
                        "block_type": int(block[6]) if len(block) > 6 else 0,
                    }
                )
                text_parts.append(value)
            pages.append(
                PageRecord(
                    page_index=page_index,
                    text="\n\n".join(text_parts),
                    blocks=blocks,
                )
            )
    finally:
        document.close()
    return pages, "pymupdf", _module_version("PyMuPDF")


def _extract_with_pypdf(path: Path) -> tuple[list[PageRecord], str, str]:
    from pypdf import PdfReader

    reader = PdfReader(str(path), strict=False)
    pages: list[PageRecord] = []
    for page_index, page in enumerate(reader.pages, start=1):
        try:
            text = (page.extract_text() or "").replace("\x00", "").strip()
        except Exception as error:
            text = f"[TEXT EXTRACTION ERROR: {type(error).__name__}]"
        pages.append(PageRecord(page_index=page_index, text=text, blocks=[]))
    return pages, "pypdf", _module_version("pypdf")


def _extract_with_markdown(path: Path) -> tuple[list[PageRecord], str, str]:
    text = path.read_text(encoding="utf-8", errors="replace").replace("\x00", "")
    text = re.sub(r"!\[([^\]]*)\]\([^\n)]+\)", r"\1", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return [PageRecord(page_index=1, text=text.strip(), blocks=[])], "markdown", "1"


def _quality(pages: list[PageRecord], config: ParserConfig) -> dict[str, Any]:
    text = "\n".join(page.text for page in pages)
    characters = len(text)
    empty_pages = sum(not page.text.strip() for page in pages)
    replacement_ratio = text.count("\ufffd") / max(characters, 1)
    empty_page_ratio = empty_pages / max(len(pages), 1)
    low_quality = (
        characters < config.min_document_characters
        or empty_page_ratio > config.max_empty_page_ratio
        or replacement_ratio > config.max_replacement_ratio
    )
    return {
        "low_quality": low_quality,
        "characters": characters,
        "empty_pages": empty_pages,
        "empty_page_ratio": empty_page_ratio,
        "replacement_ratio": replacement_ratio,
        "warnings": [],
    }


def _extract_with_docling(path: Path, expected_pages: int) -> tuple[list[PageRecord], str, str]:
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(path)
    markdown = result.document.export_to_markdown()
    pages = [
        PageRecord(
            page_index=index,
            text=markdown if index == 1 else "",
            blocks=[],
        )
        for index in range(1, max(expected_pages, 1) + 1)
    ]
    return pages, "docling", _module_version("docling")


def parse_cache_key(
    *,
    source_pdf_sha256: str,
    paper_id: str,
    document_id: str,
    document_type: str,
    parser: ParserConfig,
    chunking: ChunkingConfig,
) -> str:
    return content_hash(
        {
            "source_pdf_sha256": source_pdf_sha256,
            "paper_id": paper_id,
            "document_id": document_id,
            "document_type": document_type,
            "parser": parser.model_dump(mode="json"),
            "chunking": chunking.model_dump(mode="json"),
            "pipeline_parser_version": "literature-parser.v2",
        }
    )


def parse_pdf(
    *,
    paper: dict[str, Any],
    parser_config: ParserConfig,
    chunking_config: ChunkingConfig,
    cache_root: Path,
) -> tuple[ParsedDocument, dict[str, Any]]:
    source_path = Path(str(paper["source_path"])).resolve()
    source_sha256 = str(
        paper.get("source_document_sha256")
        or paper.get("source_pdf_sha256")
        or sha256_file(source_path)
    )
    cache_key = parse_cache_key(
        source_pdf_sha256=source_sha256,
        paper_id=str(paper["paper_id"]),
        document_id=str(paper.get("document_id") or paper["paper_id"]),
        document_type=str(paper.get("document_type") or "paper"),
        parser=parser_config,
        chunking=chunking_config,
    )
    artifact_path = cache_root / source_sha256[:2] / source_sha256 / f"{cache_key}.json"
    if artifact_path.is_file():
        parsed = ParsedDocument.model_validate_json(
            artifact_path.read_text(encoding="utf-8")
        )
        return parsed, {
            "cached": True,
            "cache_key": cache_key,
            "artifact_path": str(artifact_path),
            "artifact_sha256": sha256_file(artifact_path),
            "runtime_seconds": 0.0,
        }

    started = time.perf_counter()
    if source_path.suffix.lower() == ".md":
        if parser_config.engine not in {"auto", "markdown"}:
            raise ValueError(
                f"Parser engine {parser_config.engine} cannot read Markdown"
            )
        pages, parser_name, parser_version = _extract_with_markdown(source_path)
    elif parser_config.engine == "markdown":
        raise ValueError("Markdown parser requires a .md source")
    elif parser_config.engine in {"auto", "pymupdf"}:
        try:
            pages, parser_name, parser_version = _extract_with_pymupdf(source_path)
        except Exception:
            if parser_config.engine == "pymupdf":
                raise
            pages, parser_name, parser_version = _extract_with_pypdf(source_path)
    else:
        pages, parser_name, parser_version = _extract_with_pypdf(source_path)
    if not pages:
        raise RuntimeError(f"PDF has no pages: {source_path}")
    quality = _quality(pages, parser_config)
    if (
        source_path.suffix.lower() == ".pdf"
        and quality["low_quality"]
        and parser_config.docling_fallback
    ):
        try:
            docling_pages, docling_name, docling_version = _extract_with_docling(
                source_path,
                len(pages),
            )
            docling_quality = _quality(docling_pages, parser_config)
            if docling_quality["characters"] > quality["characters"]:
                pages = docling_pages
                parser_name = docling_name
                parser_version = docling_version
                quality = docling_quality
                quality["warnings"].append("Docling fallback was used")
        except (ImportError, ModuleNotFoundError):
            quality["warnings"].append(
                "Low-quality PDF detected but Docling is not installed"
            )
        except Exception as error:
            quality["warnings"].append(
                f"Docling fallback failed: {type(error).__name__}: {error}"
            )
    full_text = "\n\n".join(
        f"<<<PDF_PAGE_{page.page_index:03d}>>>\n{page.text}" for page in pages
    )
    chunks = build_chunks(
        paper_id=str(paper.get("document_id") or paper["paper_id"]),
        pages=pages,
        config=chunking_config,
    )
    parsed = ParsedDocument(
        paper_id=str(paper["paper_id"]),
        document_id=str(paper.get("document_id") or paper["paper_id"]),
        document_type=str(paper.get("document_type") or "paper"),
        source_path=str(source_path),
        source_media_type=str(
            paper.get("source_media_type")
            or ("text/markdown" if source_path.suffix.lower() == ".md" else "application/pdf")
        ),
        source_metadata=dict(paper.get("source_metadata") or {}),
        source_pdf_sha256=source_sha256,
        parser_name=parser_name,
        parser_version=parser_version,
        parser_config_hash=content_hash(
            {
                "parser": parser_config.model_dump(mode="json"),
                "chunking": chunking_config.model_dump(mode="json"),
            }
        ),
        page_count=len(pages),
        extracted_characters=sum(len(page.text) for page in pages),
        extracted_text_sha256=sha256_text(full_text),
        quality=quality,
        pages=pages,
        chunks=chunks,
    )
    atomic_write_json(artifact_path, parsed.model_dump(mode="json"))
    return parsed, {
        "cached": False,
        "cache_key": cache_key,
        "artifact_path": str(artifact_path),
        "artifact_sha256": sha256_file(artifact_path),
        "runtime_seconds": time.perf_counter() - started,
    }


def load_parsed_document(path: Path) -> ParsedDocument:
    return ParsedDocument.model_validate(
        json.loads(path.read_text(encoding="utf-8"))
    )
