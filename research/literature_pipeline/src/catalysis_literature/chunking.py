from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .config import ChunkingConfig
from .hashing import sha256_text, stable_id
from .models import ChunkRecord, PageRecord


TOKEN_PATTERN = re.compile(
    r"[A-Za-z0-9]+(?:[+._/-][A-Za-z0-9]+)*|[\u3400-\u9fff]|[^\s]",
    re.UNICODE,
)
HEADING_PATTERN = re.compile(
    r"^(?:\d+(?:\.\d+)*\s+)?"
    r"(abstract|introduction|background|experimental|materials?\s+and\s+methods?|"
    r"methods?|results?(?:\s+and\s+discussion)?|discussion|conclusions?|"
    r"references?|acknowledg(?:e)?ments?|supporting\s+information)\s*[:.]?$",
    re.IGNORECASE,
)
REFERENCE_HEADINGS = {"reference", "references", "bibliography"}
MARKDOWN_HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*$")


def tokens(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text)


def token_count(text: str) -> int:
    return max(1, len(tokens(text)))


def normalized_section(value: str | None) -> str | None:
    if not value:
        return None
    normalized = re.sub(r"\s+", " ", value).strip().lower()
    normalized = re.sub(r"^\d+(?:\.\d+)*\s+", "", normalized)
    aliases = {
        "material and methods": "methods",
        "materials and methods": "methods",
        "experimental section": "experimental",
        "result": "results",
        "results and discussion": "results",
        "conclusions": "conclusion",
    }
    return aliases.get(normalized, normalized)


@dataclass(frozen=True)
class TextUnit:
    page_index: int
    section: str | None
    text: str


def iter_units(
    pages: list[PageRecord],
    *,
    exclude_references: bool,
) -> Iterable[TextUnit]:
    section: str | None = None
    in_references = False
    for page in pages:
        page_text = re.sub(
            (
                r"(?i)(?<=[.!?。！？])\s+"
                r"(?=(?:abstract|introduction|background|experimental|"
                r"materials?\s+and\s+methods?|methods?|results?|discussion|"
                r"conclusions?|references?|supporting\s+information)\s*(?:\n|$))"
            ),
            "\n\n",
            page.text,
        )
        paragraphs = [
            re.sub(r"\s+", " ", part).strip()
            for part in re.split(r"\n\s*\n|\r\n\s*\r\n", page_text)
            if part.strip()
        ]
        if len(paragraphs) <= 1:
            paragraphs = [
                re.sub(r"\s+", " ", line).strip()
                for line in page_text.splitlines()
                if line.strip()
            ]
        for paragraph in paragraphs:
            markdown_heading = MARKDOWN_HEADING_PATTERN.fullmatch(paragraph[:240])
            if markdown_heading:
                section = normalized_section(markdown_heading.group(1))
                in_references = section in REFERENCE_HEADINGS
                continue
            heading = HEADING_PATTERN.fullmatch(paragraph[:160])
            if heading:
                section = normalized_section(heading.group(1))
                in_references = section in REFERENCE_HEADINGS
                continue
            if exclude_references and in_references:
                continue
            if paragraph:
                yield TextUnit(page.page_index, section, paragraph)


def _tail_for_overlap(text: str, overlap_tokens: int) -> str:
    if overlap_tokens <= 0:
        return ""
    parts = tokens(text)
    if len(parts) <= overlap_tokens:
        return text
    tail = parts[-overlap_tokens:]
    return " ".join(tail)


def _split_long_unit(unit: TextUnit, maximum_tokens: int) -> Iterable[TextUnit]:
    matches = list(TOKEN_PATTERN.finditer(unit.text))
    if len(matches) <= maximum_tokens:
        yield unit
        return
    for start in range(0, len(matches), maximum_tokens):
        window = matches[start : start + maximum_tokens]
        yield TextUnit(
            page_index=unit.page_index,
            section=unit.section,
            text=unit.text[window[0].start() : window[-1].end()].strip(),
        )


def build_chunks(
    *,
    paper_id: str,
    pages: list[PageRecord],
    config: ChunkingConfig,
) -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    buffer: list[TextUnit] = []
    buffer_tokens = 0

    def flush() -> None:
        nonlocal buffer, buffer_tokens
        if not buffer:
            return
        text = "\n\n".join(unit.text for unit in buffer).strip()
        count = token_count(text)
        if count < config.min_tokens and chunks:
            previous = chunks[-1]
            merged_text = f"{previous.text}\n\n{text}"
            merged_hash = sha256_text(merged_text)
            chunks[-1] = previous.model_copy(
                update={
                    "chunk_id": stable_id(
                        "chunk",
                        paper_id,
                        len(chunks),
                        previous.page_start,
                        buffer[-1].page_index,
                        merged_hash,
                    ),
                    "page_end": buffer[-1].page_index,
                    "text": merged_text,
                    "token_count": token_count(merged_text),
                    "source_text_sha256": merged_hash,
                }
            )
        else:
            chunk_index = len(chunks) + 1
            chunks.append(
                ChunkRecord(
                    chunk_id=stable_id(
                        "chunk",
                        paper_id,
                        chunk_index,
                        buffer[0].page_index,
                        buffer[-1].page_index,
                        sha256_text(text),
                    ),
                    paper_id=paper_id,
                    kind="section",
                    section=buffer[0].section,
                    page_start=buffer[0].page_index,
                    page_end=buffer[-1].page_index,
                    text=text,
                    token_count=count,
                    source_text_sha256=sha256_text(text),
                )
            )
        overlap = _tail_for_overlap(text, config.overlap_tokens)
        buffer = (
            [TextUnit(buffer[-1].page_index, buffer[-1].section, overlap)]
            if overlap
            else []
        )
        buffer_tokens = token_count(overlap) if overlap else 0

    units = iter_units(
        pages,
        exclude_references=config.exclude_references,
    )
    maximum_unit_tokens = max(1, config.target_tokens - config.overlap_tokens)
    for original_unit in units:
        for unit in _split_long_unit(original_unit, maximum_unit_tokens):
            count = token_count(unit.text)
            section_changed = bool(
                buffer
                and unit.section
                and buffer[0].section
                and unit.section != buffer[0].section
            )
            if buffer and (
                section_changed or buffer_tokens + count > config.target_tokens
            ):
                flush()
            buffer.append(unit)
            buffer_tokens += count
    flush()
    return chunks
