from __future__ import annotations

import asyncio
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from pydantic import ValidationError

from .config import ExtractionConfig
from .hashing import atomic_write_json, content_hash, sha256_file, sha256_text
from .ledger import PipelineLedger
from .models import (
    EXTRACTION_SCHEMA_VERSION,
    EvidenceRecord,
    PaperArtifactV2,
    ParsedDocument,
)
from .prompts import (
    build_core_prompt,
    build_data_prompt,
    context_token_count,
    prompt_hashes,
)
from .providers import ModelProvider, ProviderResult


DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\b(?:19|20)\d{2}\b")


def _normalized(value: str) -> str:
    return "".join(character.casefold() for character in value if character.isalnum())


def _sentences(value: str) -> Iterable[str]:
    for part in re.split(r"(?<=[.!?。！？])\s+|\n+", value):
        compact = re.sub(r"\s+", " ", part).strip()
        if compact:
            yield compact


def _recover_quote(quote: str, page_text: str) -> tuple[str, str]:
    normalized_quote = _normalized(quote)
    normalized_page = _normalized(page_text)
    if normalized_quote and normalized_quote in normalized_page:
        return quote, "exact"
    quote_terms = set(re.findall(r"[A-Za-z0-9\u3400-\u9fff]+", quote.casefold()))
    best: tuple[float, str] | None = None
    for sentence in _sentences(page_text):
        terms = set(
            re.findall(r"[A-Za-z0-9\u3400-\u9fff]+", sentence.casefold())
        )
        union = quote_terms | terms
        score = len(quote_terms & terms) / max(1, len(union))
        if best is None or score > best[0]:
            best = (score, sentence)
    if best and best[0] >= 0.45:
        return best[1][:600], "locally_recovered"
    return quote, "unverified"


def _evidence_containers(extraction: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for finding in (extraction.get("summary") or {}).get("main_findings") or []:
        if isinstance(finding, dict):
            yield finding
    for keyword in (extraction.get("keywords") or {}).get("extracted") or []:
        if isinstance(keyword, dict):
            yield keyword
    for key in ("entities", "experiments", "observations", "claims"):
        for item in extraction.get(key) or []:
            if isinstance(item, dict):
                yield item


def _normalize_evidence_shapes(extraction: dict[str, Any]) -> None:
    for container in _evidence_containers(extraction):
        evidence = container.get("evidence")
        if not isinstance(evidence, list):
            container["evidence"] = []
            container["needs_visual_review"] = True
            continue
        normalized: list[dict[str, Any]] = []
        coerced = False
        for entry in evidence:
            if isinstance(entry, dict):
                normalized.append(entry)
            elif isinstance(entry, str) and entry.strip():
                normalized.append(
                    {
                        "pdf_page_index": 1,
                        "section": None,
                        "source": "text",
                        "source_id": None,
                        "quote": entry.strip(),
                    }
                )
                coerced = True
            else:
                coerced = True
        container["evidence"] = normalized
        if coerced:
            container["needs_visual_review"] = True


def annotate_evidence(extraction: dict[str, Any], parsed: ParsedDocument) -> None:
    counts = {"exact": 0, "locally_recovered": 0, "unverified": 0}
    needs_review = 0
    pages = {page.page_index: page.text for page in parsed.pages}
    for container in _evidence_containers(extraction):
        validations: set[str] = set()
        evidence = container.get("evidence")
        if not isinstance(evidence, list):
            evidence = []
            container["evidence"] = evidence
        for entry in evidence:
            entry["document_id"] = parsed.document_id
            entry["document_type"] = parsed.document_type
            record = EvidenceRecord.model_validate(entry)
            page_text = pages.get(record.pdf_page_index, "")
            quote, validation = _recover_quote(record.quote, page_text)
            entry["quote"] = quote
            entry["evidence_validation"] = validation
            counts[validation] += 1
            validations.add(validation)
        review = bool(container.get("needs_visual_review")) or "unverified" in validations
        container["review_status"] = "needs_review" if review else "extracted"
        needs_review += int(review)
    quality = extraction.setdefault("quality", {})
    quality["evidence_validation_counts"] = counts
    quality["evidence_count"] = sum(counts.values())
    quality["needs_review_count"] = needs_review + len(
        extraction.get("visual_review_items") or []
    )


def _abstract_from_pages(parsed: ParsedDocument) -> dict[str, Any]:
    opening = "\n".join(page.text for page in parsed.pages[:3])
    match = re.search(
        r"(?is)\babstract\b\s*[:.-]?\s*(.+?)"
        r"(?=\n\s*(?:key\s*words?|keywords?|1\.?\s+introduction|introduction)\b)",
        opening,
    )
    if not match:
        return {
            "exists": False,
            "source_type": "none",
            "original_language": None,
            "original": None,
            "chinese_translation": None,
            "key_points": [],
            "pdf_page_indexes": [],
        }
    original = re.sub(r"\s+", " ", match.group(1)).strip()
    return {
        "exists": True,
        "source_type": "explicit_abstract",
        "original_language": "English",
        "original": original,
        "chinese_translation": None,
        "key_points": [],
        "pdf_page_indexes": [1],
    }


def _program_paper_metadata(
    parsed: ParsedDocument,
    core: dict[str, Any],
) -> dict[str, Any]:
    paper = dict(core.get("paper") or {})
    opening = "\n".join(page.text for page in parsed.pages[:2])
    title = paper.get("title")
    if not title:
        title = next(
            (
                line.strip()
                for line in opening.splitlines()
                if len(line.strip()) >= 12
            ),
            Path(parsed.source_path).stem,
        )
    doi = paper.get("doi")
    if not doi:
        match = DOI_PATTERN.search(opening)
        doi = match.group(0).rstrip(".,;)") if match else None
    year = paper.get("year")
    if year is None:
        match = YEAR_PATTERN.search(opening)
        year = int(match.group(0)) if match else None
    paper.update(
        {
            "id": f"doi:{str(doi).lower()}" if doi else parsed.paper_id,
            "title": title,
            "doi": doi,
            "year": year,
            "authors": paper.get("authors") or [],
            "journal": paper.get("journal"),
            "paper_type": paper.get("paper_type") or "unclear",
            "catalysis_system": paper.get("catalysis_system") or "unclear",
            "reaction_categories": paper.get("reaction_categories") or [],
            "source_path": parsed.source_path,
            "source_document_id": parsed.document_id,
            "source_document_type": parsed.document_type,
            "source_pdf_sha256": parsed.source_pdf_sha256,
            "page_count": parsed.page_count,
        }
    )
    return paper


def _normalize_references(extraction: dict[str, Any]) -> None:
    entity_ids = {
        str(item.get("id"))
        for item in extraction.get("entities") or []
        if isinstance(item, dict) and item.get("id")
    }
    experiment_ids = {
        str(item.get("id"))
        for item in extraction.get("experiments") or []
        if isinstance(item, dict) and item.get("id")
    }
    for experiment in extraction.get("experiments") or []:
        if not isinstance(experiment, dict):
            continue
        for key in ("sample_entity_ids", "material_entity_ids", "method_entity_ids"):
            experiment[key] = [
                value
                for value in (experiment.get(key) or [])
                if str(value) in entity_ids
            ]
    for observation in extraction.get("observations") or []:
        if not isinstance(observation, dict):
            continue
        if observation.get("experiment_id") not in experiment_ids:
            observation["experiment_id"] = None
        for key in ("sample_entity_id", "property_entity_id", "method_entity_id"):
            if observation.get(key) not in entity_ids:
                observation[key] = None


class ExtractionRunner:
    def __init__(
        self,
        *,
        config: ExtractionConfig,
        provider: ModelProvider,
        ledger: PipelineLedger,
        workspace: Path,
        collection_hint: str | None = None,
    ):
        self.config = config
        self.provider = provider
        self.ledger = ledger
        self.workspace = workspace.resolve()
        self.collection_hint = collection_hint
        self.prompt_hash = prompt_hashes()
        self.semaphore = asyncio.Semaphore(max(1, config.workers))

    async def _cached_call(
        self,
        *,
        paper_id: str,
        stage: str,
        prompt: str,
        max_tokens: int,
    ) -> tuple[ProviderResult, bool]:
        prompt_hash = sha256_text(prompt)
        input_hash = content_hash(
            {
                "paper_id": paper_id,
                "stage": stage,
                "prompt": prompt_hash,
            }
        )
        call_key = content_hash(
            {
                "provider": self.config.provider,
                "model": self.config.model,
                "temperature": self.config.temperature,
                "reasoning_effort": self.config.reasoning_effort,
                "seed": self.config.seed,
                "max_tokens": max_tokens,
                "prompt_version": self.config.prompt_version,
                "prompt_hash": prompt_hash,
                "input_hash": input_hash,
            }
        )
        cached = self.ledger.model_call(call_key)
        if cached:
            path = Path(cached["response_path"])
            if path.is_file() and sha256_file(path) == cached["response_sha256"]:
                payload = json.loads(path.read_text(encoding="utf-8"))
                return (
                    ProviderResult(
                        data=payload["data"],
                        raw=payload["raw"],
                        provider=payload["provider"],
                        model=payload["model"],
                        usage=payload.get("usage") or {},
                    ),
                    True,
                )
        async with self.semaphore:
            result = await self.provider.generate_json(
                prompt=prompt,
                stage=stage,
                max_tokens=max_tokens,
            )
        path = self.workspace / "model_calls" / call_key[:2] / f"{call_key}.json"
        atomic_write_json(
            path,
            {
                "data": result.data,
                "raw": result.raw,
                "provider": result.provider,
                "model": result.model,
                "usage": result.usage,
            },
        )
        self.ledger.record_model_call(
            call_key=call_key,
            provider=result.provider,
            model=result.model,
            prompt_hash=prompt_hash,
            input_hash=input_hash,
            response_path=str(path),
            response_sha256=sha256_file(path),
            usage=result.usage,
        )
        return result, False

    async def extract(
        self,
        parsed: ParsedDocument,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        extraction_key = content_hash(
            {
                "parsed_text": parsed.extracted_text_sha256,
                "schema_version": PaperArtifactV2.model_json_schema(),
                "provider": self.config.provider,
                "model": self.config.model,
                "temperature": self.config.temperature,
                "reasoning_effort": self.config.reasoning_effort,
                "seed": self.config.seed,
                "prompt_version": self.config.prompt_version,
                "prompt_hashes": self.prompt_hash,
                "context_budgets": [
                    self.config.max_context_tokens_core,
                    self.config.max_context_tokens_data,
                ],
                "output_budgets": [
                    self.config.max_tokens_core,
                    self.config.max_tokens_data,
                ],
            }
        )
        artifact_path = (
            self.workspace
            / "extractions"
            / parsed.source_pdf_sha256[:2]
            / parsed.source_pdf_sha256
            / f"{extraction_key}.json"
        )
        if artifact_path.is_file():
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            PaperArtifactV2.model_validate(artifact["extraction"])
            return artifact, {
                "cached": True,
                "cache_key": extraction_key,
                "artifact_path": str(artifact_path),
                "artifact_sha256": sha256_file(artifact_path),
                "usage": {},
                "cache_hits": 1,
                "model_calls": 0,
                "runtime_seconds": 0.0,
            }

        started = time.perf_counter()
        core_prompt, core_chunks = build_core_prompt(
            parsed=parsed,
            collection_hint=self.collection_hint,
            token_budget=self.config.max_context_tokens_core,
        )
        core_result, core_cached = await self._cached_call(
            paper_id=parsed.paper_id,
            stage="core",
            prompt=core_prompt,
            max_tokens=self.config.max_tokens_core,
        )
        entities = core_result.data.get("entities") or []
        data_prompt, data_chunks = build_data_prompt(
            parsed=parsed,
            entities=entities,
            token_budget=self.config.max_context_tokens_data,
        )
        data_result, data_cached = await self._cached_call(
            paper_id=parsed.paper_id,
            stage="data",
            prompt=data_prompt,
            max_tokens=self.config.max_tokens_data,
        )
        local_abstract = _abstract_from_pages(parsed)
        abstract_analysis = core_result.data.get("abstract_analysis") or {}
        local_abstract["chinese_translation"] = abstract_analysis.get(
            "chinese_translation"
        )
        local_abstract["key_points"] = abstract_analysis.get("key_points") or []
        usage = {
            "prompt_tokens": sum(
                int((result.usage or {}).get("prompt_tokens") or 0)
                for result in (core_result, data_result)
            ),
            "completion_tokens": sum(
                int((result.usage or {}).get("completion_tokens") or 0)
                for result in (core_result, data_result)
            ),
            "total_tokens": sum(
                int((result.usage or {}).get("total_tokens") or 0)
                for result in (core_result, data_result)
            ),
            "core": core_result.usage,
            "data": data_result.usage,
        }
        extraction: dict[str, Any] = {
            "schema_version": EXTRACTION_SCHEMA_VERSION,
            "paper": _program_paper_metadata(parsed, core_result.data),
            "abstract": local_abstract,
            "summary": core_result.data.get("summary") or {
                "one_sentence": "",
                "research_objective": None,
                "research_problem": None,
                "main_methods": [],
                "main_findings": [],
                "innovations": [],
                "limitations": [],
            },
            "keywords": core_result.data.get("keywords")
            or {"author_keywords": [], "extracted": []},
            "entities": entities,
            "experiments": data_result.data.get("experiments") or [],
            "observations": data_result.data.get("observations") or [],
            "claims": core_result.data.get("claims") or [],
            "visual_review_items": list(
                {
                    json.dumps(item, ensure_ascii=False, sort_keys=True): item
                    for item in (
                        (core_result.data.get("visual_review_items") or [])
                        + (data_result.data.get("visual_review_items") or [])
                    )
                    if isinstance(item, dict)
                }.values()
            ),
            "quality": core_result.data.get("quality") or {
                "overall_confidence": "medium",
                "extraction_status": "partial",
                "missing_sections": [],
                "warnings": [],
            },
            "extraction_metadata": {
                "provider": core_result.provider,
                "model": core_result.model,
                "prompt_version": self.config.prompt_version,
                "prompt_hashes": self.prompt_hash,
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "source_pdf_sha256": parsed.source_pdf_sha256,
                "extracted_text_sha256": parsed.extracted_text_sha256,
                "parser_name": parsed.parser_name,
                "parser_version": parsed.parser_version,
                "selected_chunk_ids": {
                    "core": [chunk.chunk_id for chunk in core_chunks],
                    "data": [chunk.chunk_id for chunk in data_chunks],
                },
                "selected_context_tokens": {
                    "core": context_token_count(core_chunks),
                    "data": context_token_count(data_chunks),
                },
                "temperature": self.config.temperature,
                "seed": self.config.seed,
                "usage": usage,
            },
        }
        _normalize_references(extraction)
        _normalize_evidence_shapes(extraction)
        annotate_evidence(extraction, parsed)
        try:
            validated = PaperArtifactV2.model_validate(extraction)
        except ValidationError as error:
            raise RuntimeError(f"Structured extraction validation failed: {error}") from error
        artifact = {
            "source": {
                "paper_id": parsed.paper_id,
                "document_id": parsed.document_id,
                "document_type": parsed.document_type,
                "path": parsed.source_path,
                "source_pdf_sha256": parsed.source_pdf_sha256,
                "page_count": parsed.page_count,
                "extracted_text_sha256": parsed.extracted_text_sha256,
            },
            "extraction": validated.model_dump(mode="json"),
        }
        atomic_write_json(artifact_path, artifact)
        return artifact, {
            "cached": False,
            "cache_key": extraction_key,
            "artifact_path": str(artifact_path),
            "artifact_sha256": sha256_file(artifact_path),
            "usage": usage,
            "cache_hits": int(core_cached) + int(data_cached),
            "model_calls": int(not core_cached) + int(not data_cached),
            "runtime_seconds": time.perf_counter() - started,
        }
