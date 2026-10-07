from __future__ import annotations

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Protocol

import httpx

from .config import ExtractionConfig


@dataclass(frozen=True)
class ProviderResult:
    data: dict[str, Any]
    raw: dict[str, Any]
    provider: str
    model: str
    usage: dict[str, Any]


class ModelProvider(Protocol):
    name: str

    async def generate_json(
        self,
        *,
        prompt: str,
        stage: str,
        max_tokens: int,
    ) -> ProviderResult: ...


class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.interval = 60.0 / max(1, requests_per_minute)
        self._lock = asyncio.Lock()
        self._next = 0.0

    async def wait(self) -> None:
        async with self._lock:
            now = time.monotonic()
            delay = max(0.0, self._next - now)
            self._next = max(now, self._next) + self.interval
        if delay:
            await asyncio.sleep(delay)


def _parse_json_object(value: str) -> dict[str, Any]:
    cleaned = value.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first < 0 or last <= first:
        raise RuntimeError("Model did not return a JSON object")
    parsed = json.loads(cleaned[first : last + 1])
    if not isinstance(parsed, dict):
        raise RuntimeError("Model JSON must be an object")
    return parsed


class DeepSeekProvider:
    name = "deepseek"

    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is not set")
        self.rate_limiter = RateLimiter(config.requests_per_minute)
        self._client = httpx.AsyncClient(
            base_url=config.base_url.rstrip("/"),
            timeout=httpx.Timeout(300.0),
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def generate_json(
        self,
        *,
        prompt: str,
        stage: str,
        max_tokens: int,
    ) -> ProviderResult:
        last_error: Exception | None = None
        for attempt in range(1, 5):
            await self.rate_limiter.wait()
            try:
                response = await self._client.post(
                    "/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.config.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You extract scientific evidence and return valid JSON only."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": self.config.temperature,
                        "seed": self.config.seed,
                        "thinking": {"type": "disabled"},
                        "max_tokens": max_tokens,
                        "stream": False,
                    },
                )
                if response.status_code in {408, 409, 425, 429, 500, 502, 503, 504}:
                    retry_after = response.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else min(30.0, 2**attempt)
                    await asyncio.sleep(delay)
                    continue
                response.raise_for_status()
                raw = response.json()
                content = raw["choices"][0]["message"]["content"]
                return ProviderResult(
                    data=_parse_json_object(content),
                    raw=raw,
                    provider=self.name,
                    model=str(raw.get("model") or self.config.model),
                    usage=raw.get("usage") or {},
                )
            except (httpx.HTTPError, KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
                last_error = error
                if attempt < 4:
                    await asyncio.sleep(min(30.0, 2**attempt))
        raise last_error or RuntimeError(f"{stage} model call failed")


class ZhipuProvider:
    name = "zhipu"

    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.api_key = os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise RuntimeError("ZHIPU_API_KEY is not set")
        self.rate_limiter = RateLimiter(config.requests_per_minute)
        self._client = httpx.AsyncClient(
            base_url=config.base_url.rstrip("/"),
            timeout=httpx.Timeout(300.0),
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def generate_json(
        self,
        *,
        prompt: str,
        stage: str,
        max_tokens: int,
    ) -> ProviderResult:
        last_error: Exception | None = None
        for attempt in range(1, 5):
            await self.rate_limiter.wait()
            try:
                response = await self._client.post(
                    "/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.config.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You extract scientific evidence and return valid JSON only."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": self.config.temperature,
                        "top_p": 0.95,
                        "thinking": {
                            "type": "enabled",
                            "clear_thinking": True,
                        },
                        "reasoning_effort": self.config.reasoning_effort,
                        "max_tokens": max_tokens,
                        "stream": False,
                    },
                )
                if response.status_code in {408, 409, 425, 429, 500, 502, 503, 504}:
                    retry_after = response.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else min(30.0, 2**attempt)
                    await asyncio.sleep(delay)
                    continue
                response.raise_for_status()
                raw = response.json()
                content = raw["choices"][0]["message"]["content"]
                return ProviderResult(
                    data=_parse_json_object(content),
                    raw=raw,
                    provider=self.name,
                    model=str(raw.get("model") or self.config.model),
                    usage=raw.get("usage") or {},
                )
            except (
                httpx.HTTPError,
                KeyError,
                IndexError,
                TypeError,
                json.JSONDecodeError,
                RuntimeError,
            ) as error:
                last_error = error
                if attempt < 4:
                    await asyncio.sleep(min(30.0, 2**attempt))
        raise last_error or RuntimeError(f"{stage} model call failed")


class MockProvider:
    name = "mock"

    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.calls = 0

    async def generate_json(
        self,
        *,
        prompt: str,
        stage: str,
        max_tokens: int,
    ) -> ProviderResult:
        del max_tokens
        self.calls += 1
        page_match = re.search(r"pages=(\d+)-", prompt)
        page = int(page_match.group(1)) if page_match else 1
        context = prompt.split("Selected page-aware evidence:", 1)[-1]
        candidate = ""
        for line in context.splitlines():
            line = line.strip()
            if line and not line.startswith("<<<"):
                candidate = line
                break
        quote = " ".join(candidate.split()[:18]) or "No extractable text"
        evidence = [
            {
                "pdf_page_index": page,
                "section": None,
                "source": "text",
                "source_id": None,
                "quote": quote,
            }
        ]
        if stage == "core":
            data = {
                "paper": {
                    "title": "Mock paper",
                    "doi": None,
                    "year": None,
                    "authors": [],
                    "journal": None,
                    "paper_type": "research_article",
                    "catalysis_system": "unclear",
                    "reaction_categories": [],
                },
                "abstract_analysis": {
                    "chinese_translation": None,
                    "key_points": [],
                },
                "summary": {
                    "one_sentence": "用于验证流水线的模拟抽取结果。",
                    "research_objective": None,
                    "research_problem": None,
                    "main_methods": [],
                    "main_findings": [
                        {"statement": "模拟证据记录。", "evidence": evidence}
                    ],
                    "innovations": [],
                    "limitations": [],
                },
                "keywords": {
                    "author_keywords": [],
                    "extracted": [
                        {
                            "id": "keyword:k001",
                            "raw_term": "catalysis",
                            "normalized_term": "催化",
                            "category": "reaction",
                            "importance": "core",
                            "definition_in_context": None,
                            "source_scope": "main_text",
                            "evidence": evidence,
                            "needs_visual_review": False,
                        }
                    ],
                },
                "entities": [],
                "claims": [
                    {
                        "id": "claim:c001",
                        "claim_type": "reported_result",
                        "statement": "模拟证据记录。",
                        "evidence_basis": "unclear",
                        "evidence": evidence,
                        "needs_visual_review": False,
                    }
                ],
                "visual_review_items": [],
                "quality": {
                    "overall_confidence": "medium",
                    "extraction_status": "partial",
                    "missing_sections": [],
                    "warnings": ["mock provider"],
                },
            }
        else:
            data = {
                "experiments": [],
                "observations": [],
                "visual_review_items": [],
            }
        raw = {
            "model": "mock-model",
            "choices": [{"message": {"content": json.dumps(data, ensure_ascii=False)}}],
            "usage": {
                "prompt_tokens": max(1, len(prompt) // 4),
                "completion_tokens": max(1, len(json.dumps(data)) // 4),
            },
        }
        raw["usage"]["total_tokens"] = (
            raw["usage"]["prompt_tokens"] + raw["usage"]["completion_tokens"]
        )
        return ProviderResult(
            data=data,
            raw=raw,
            provider=self.name,
            model="mock-model",
            usage=raw["usage"],
        )


def provider_for(config: ExtractionConfig) -> ModelProvider:
    if config.provider == "mock":
        return MockProvider(config)
    if config.provider == "zhipu":
        return ZhipuProvider(config)
    return DeepSeekProvider(config)
