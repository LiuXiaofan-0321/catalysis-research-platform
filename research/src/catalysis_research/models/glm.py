"""Small, OpenAI-compatible client for the existing GLM endpoint.

The client deliberately reads credentials only from the process environment. It
is used by exploratory research runs and never writes credentials to artifacts.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class GlmError(RuntimeError):
    """Raised when a GLM request or structured response is invalid."""


@dataclass(frozen=True)
class GlmResponse:
    structured: dict[str, Any]
    raw: dict[str, Any]
    provider: str
    model: str
    usage: dict[str, Any]


def _parse_json_object(content: str) -> dict[str, Any]:
    cleaned = content.strip()
    cleaned = re.sub(
        r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE
    )
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first < 0 or last <= first:
        raise GlmError("GLM did not return a JSON object")
    try:
        value = json.loads(cleaned[first : last + 1])
    except json.JSONDecodeError as error:
        raise GlmError("GLM returned malformed JSON") from error
    if not isinstance(value, dict):
        raise GlmError("GLM JSON must be an object")
    return value


class GlmClient:
    """Synchronous JSON client for Zhipu's OpenAI-compatible chat API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 300.0,
        retries: int = 3,
        retry_sleep_seconds: float = 2.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("ZHIPU_API_KEY", "")
        if not self.api_key:
            raise GlmError("ZHIPU_API_KEY is not set")
        self.base_url = (
            base_url
            or os.environ.get("ZHIPU_PROXY_BASE_URL")
            or os.environ.get(
                "ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4"
            )
        ).rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.retries = max(0, retries)
        self.retry_sleep_seconds = max(0.0, retry_sleep_seconds)

    def chat_json(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float = 0.2,
        max_tokens: int = 4000,
        thinking: str = "disabled",
        reasoning_effort: str | None = None,
    ) -> GlmResponse:
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if thinking not in {"enabled", "disabled"}:
            raise GlmError("thinking must be enabled or disabled")
        if reasoning_effort not in {None, "low", "high", "max"}:
            raise GlmError("reasoning_effort must be low, high, or max")
        if thinking == "enabled":
            payload["thinking"] = {"type": "enabled", "clear_thinking": True}
            if reasoning_effort is not None:
                payload["reasoning_effort"] = reasoning_effort
        else:
            if reasoning_effort is not None:
                raise GlmError("reasoning_effort requires thinking=enabled")
            payload["thinking"] = {"type": "disabled"}

        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout_seconds
                ) as response:
                    raw = json.loads(response.read().decode("utf-8"))
                content = raw["choices"][0]["message"]["content"]
                if not isinstance(content, str):
                    raise GlmError("GLM response content is not text")
                return GlmResponse(
                    structured=_parse_json_object(content),
                    raw=raw,
                    provider="zhipu",
                    model=str(raw.get("model") or model),
                    usage=raw.get("usage") or {},
                )
            except urllib.error.HTTPError as error:
                body = error.read().decode("utf-8", errors="replace")[:2000]
                last_error = GlmError(f"GLM HTTP {error.code}: {body}")
                retryable = error.code in {408, 409, 425, 429, 500, 502, 503, 504}
                if not retryable or attempt >= self.retries:
                    raise last_error from error
                retry_after = error.headers.get("Retry-After")
                delay = (
                    float(retry_after)
                    if retry_after
                    else self.retry_sleep_seconds * (2**attempt)
                )
                time.sleep(min(30.0, max(0.0, delay)))
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError, TypeError) as error:
                last_error = GlmError(f"GLM request failed: {error}")
                if attempt >= self.retries:
                    raise last_error from error
                time.sleep(min(30.0, self.retry_sleep_seconds * (2**attempt)))
        raise last_error or GlmError("GLM request failed")
