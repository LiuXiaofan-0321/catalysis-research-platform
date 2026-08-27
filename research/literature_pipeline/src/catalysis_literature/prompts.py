from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .chunking import token_count
from .models import ChunkRecord, ParsedDocument


PROMPTS_ROOT = Path(__file__).resolve().parents[2] / "prompts"
CORE_PROMPT_FILE = PROMPTS_ROOT / "core-v2.txt"
DATA_PROMPT_FILE = PROMPTS_ROOT / "data-v2.txt"


CORE_SECTION_WEIGHTS = {
    "abstract": 12,
    "conclusion": 11,
    "results": 10,
    "discussion": 9,
    "introduction": 5,
    "experimental": 3,
    "methods": 3,
    None: 4,
}
DATA_SECTION_WEIGHTS = {
    "experimental": 12,
    "methods": 12,
    "results": 11,
    "discussion": 8,
    "conclusion": 5,
    None: 3,
}
CORE_TERMS = {
    "catalyst",
    "zeolite",
    "photocatal",
    "conversion",
    "selectivity",
    "yield",
    "mechanism",
    "active site",
    "performance",
    "催化",
    "转化",
    "选择性",
    "机理",
}
DATA_TERMS = {
    "temperature",
    "pressure",
    "flow",
    "conversion",
    "selectivity",
    "yield",
    "activity",
    "stability",
    "table",
    "figure",
    "reaction condition",
    "温度",
    "压力",
    "转化率",
    "选择性",
    "产率",
}


def _score_chunk(
    chunk: ChunkRecord,
    *,
    section_weights: dict[str | None, int],
    terms: set[str],
) -> float:
    text = chunk.text.casefold()
    score = float(section_weights.get(chunk.section, 2))
    score += sum(2.0 for term in terms if term.casefold() in text)
    if re.search(r"\b\d+(?:\.\d+)?\s*(?:%|k|°c|bar|mpa|h|min)\b", text):
        score += 2.5
    return score


def select_chunks(
    parsed: ParsedDocument,
    *,
    stage: str,
    token_budget: int,
    entity_terms: list[str] | None = None,
) -> list[ChunkRecord]:
    if stage == "core":
        weights = CORE_SECTION_WEIGHTS
        terms = set(CORE_TERMS)
    elif stage == "data":
        weights = DATA_SECTION_WEIGHTS
        terms = set(DATA_TERMS)
        terms.update(term.casefold() for term in (entity_terms or []) if term)
    else:
        raise ValueError(f"Unsupported prompt stage: {stage}")
    ranked = sorted(
        parsed.chunks,
        key=lambda chunk: (
            -_score_chunk(chunk, section_weights=weights, terms=terms),
            chunk.page_start,
            chunk.chunk_id,
        ),
    )
    selected: list[ChunkRecord] = []
    used = 0
    for chunk in ranked:
        if selected and used + chunk.token_count > token_budget:
            continue
        selected.append(chunk)
        used += chunk.token_count
        if used >= token_budget:
            break
    return sorted(selected, key=lambda chunk: (chunk.page_start, chunk.chunk_id))


def render_context(chunks: list[ChunkRecord]) -> str:
    return "\n\n".join(
        (
            f"<<<CHUNK id={chunk.chunk_id} section={chunk.section or 'unknown'} "
            f"pages={chunk.page_start}-{chunk.page_end}>>>\n{chunk.text}"
        )
        for chunk in chunks
    )


def prompt_hashes() -> dict[str, str]:
    from .hashing import sha256_file

    return {
        "core": sha256_file(CORE_PROMPT_FILE),
        "data": sha256_file(DATA_PROMPT_FILE),
    }


def build_core_prompt(
    *,
    parsed: ParsedDocument,
    collection_hint: str | None,
    token_budget: int,
) -> tuple[str, list[ChunkRecord]]:
    chunks = select_chunks(parsed, stage="core", token_budget=token_budget)
    template = CORE_PROMPT_FILE.read_text(encoding="utf-8")
    schema = {
        "paper": {
            "title": "string|null",
            "doi": "string|null",
            "year": "integer|null",
            "authors": ["string"],
            "journal": "string|null",
            "paper_type": "string",
            "catalysis_system": "thermal_catalysis|photocatalysis|both|unclear",
            "reaction_categories": ["string"],
        },
        "abstract_analysis": {
            "chinese_translation": "string|null",
            "key_points": ["string"],
        },
        "summary": {
            "one_sentence": "string",
            "research_objective": "string|null",
            "research_problem": "string|null",
            "main_methods": ["string"],
            "main_findings": [
                {
                    "statement": "string",
                    "evidence": [
                        {
                            "pdf_page_index": 1,
                            "section": "string|null",
                            "source": "text",
                            "source_id": "string|null",
                            "quote": "short exact quote",
                        }
                    ],
                }
            ],
            "innovations": ["string"],
            "limitations": ["string"],
        },
        "keywords": {
            "author_keywords": [],
            "extracted": [
                {
                    "id": "keyword:k001",
                    "raw_term": "string",
                    "normalized_term": "string",
                    "category": "string",
                    "importance": "core|supporting",
                    "definition_in_context": "string|null",
                    "source_scope": "string|null",
                    "evidence": [],
                    "needs_visual_review": False,
                }
            ],
        },
        "entities": [],
        "claims": [],
        "visual_review_items": [],
        "quality": {
            "overall_confidence": "high|medium|low",
            "extraction_status": "completed|partial|failed",
            "missing_sections": [],
            "warnings": [],
        },
    }
    return (
        template.format(
            source_path=parsed.source_path,
            source_sha256=parsed.source_pdf_sha256,
            page_count=parsed.page_count,
            collection_hint=collection_hint or "none",
            schema=json.dumps(schema, ensure_ascii=False, indent=2),
            context=render_context(chunks),
        ),
        chunks,
    )


def build_data_prompt(
    *,
    parsed: ParsedDocument,
    entities: list[dict[str, Any]],
    token_budget: int,
) -> tuple[str, list[ChunkRecord]]:
    entity_terms = [
        str(item.get("canonical_name") or item.get("zh_name") or "")
        for item in entities
        if isinstance(item, dict)
    ]
    chunks = select_chunks(
        parsed,
        stage="data",
        token_budget=token_budget,
        entity_terms=entity_terms,
    )
    template = DATA_PROMPT_FILE.read_text(encoding="utf-8")
    schema = {
        "experiments": [
            {
                "id": "experiment:x001",
                "experiment_type": "string",
                "objective": "string|null",
                "sample_entity_ids": [],
                "material_entity_ids": [],
                "method_entity_ids": [],
                "conditions": [],
                "evidence": [],
                "needs_visual_review": False,
            }
        ],
        "observations": [
            {
                "id": "observation:o001",
                "experiment_id": "experiment:x001|null",
                "sample_entity_id": "entity:e001|null",
                "property_entity_id": "entity:e002|null",
                "method_entity_id": "entity:e003|null",
                "metric_name": "string",
                "numeric_value": "number|null",
                "text_value": "string|null",
                "unit": "string|null",
                "raw_value": "string|null",
                "uncertainty": "number|string|null",
                "comparison_operator": "string",
                "conditions": [],
                "evidence": [],
                "needs_visual_review": False,
            }
        ],
        "visual_review_items": [],
    }
    catalog = [
        {
            "id": item.get("id"),
            "type": item.get("type"),
            "canonical_name": item.get("canonical_name"),
            "zh_name": item.get("zh_name"),
        }
        for item in entities
        if isinstance(item, dict)
    ]
    return (
        template.format(
            source_path=parsed.source_path,
            source_sha256=parsed.source_pdf_sha256,
            page_count=parsed.page_count,
            entity_catalog=json.dumps(catalog, ensure_ascii=False, indent=2),
            schema=json.dumps(schema, ensure_ascii=False, indent=2),
            context=render_context(chunks),
        ),
        chunks,
    )


def context_token_count(chunks: list[ChunkRecord]) -> int:
    return token_count(render_context(chunks))
