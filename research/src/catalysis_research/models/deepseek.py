from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class DeepSeekError(RuntimeError):
    """Raised for a failed or malformed DeepSeek API request."""


class DeepSeekClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = "https://api.deepseek.com",
        timeout_seconds: float = 120.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            raise DeepSeekError("DEEPSEEK_API_KEY is not set")
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _request(self, path: str, *, payload: dict[str, Any] | None = None) -> Any:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            method="GET" if payload is None else "POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(
                request, timeout=self.timeout_seconds
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")[:2000]
            raise DeepSeekError(f"DeepSeek HTTP {error.code}: {body}") from error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise DeepSeekError(f"DeepSeek request failed: {error}") from error

    def list_models(self) -> list[str]:
        response = self._request("/models")
        try:
            return sorted(str(item["id"]) for item in response["data"])
        except (KeyError, TypeError) as error:
            raise DeepSeekError("Malformed response from DeepSeek /models") from error

    def chat_json(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float = 0.2,
        max_tokens: int = 8000,
    ) -> dict[str, Any]:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
            "thinking": {"type": "disabled"},
            "stream": False,
        }
        response = self._request("/chat/completions", payload=payload)
        try:
            content = response["choices"][0]["message"]["content"]
            structured = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
            raise DeepSeekError("DeepSeek did not return a valid JSON object") from error
        return {
            "provider_response_id": response.get("id"),
            "provider_model": response.get("model", model),
            "usage": response.get("usage", {}),
            "structured": structured,
            "raw_content": content,
        }
