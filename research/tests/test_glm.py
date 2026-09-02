from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.models.glm import GlmClient, GlmError  # noqa: E402


class _Response:
    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps({
            "id": "test-response",
            "model": "glm-5.3-flash",
            "choices": [{"message": {"content": '{"ok": true}'}}],
            "usage": {"total_tokens": 3},
        }).encode("utf-8")


class GlmClientTests(unittest.TestCase):
    def test_glm53_payload_enables_thinking_with_frozen_effort(self) -> None:
        captured: dict[str, object] = {}

        def fake_urlopen(request: object, timeout: float) -> _Response:
            del timeout
            captured.update(json.loads(io.BytesIO(request.data).read().decode("utf-8")))  # type: ignore[attr-defined]
            return _Response()

        client = GlmClient(api_key="test-key", base_url="https://example.invalid")
        with patch("urllib.request.urlopen", fake_urlopen):
            response = client.chat_json(
                model="glm-5.3-flash",
                system="system",
                user="user",
                thinking="enabled",
                reasoning_effort="low",
            )
        self.assertTrue(response.structured["ok"])
        self.assertEqual(captured["thinking"], {"type": "enabled", "clear_thinking": True})
        self.assertEqual(captured["reasoning_effort"], "low")

    def test_reasoning_effort_requires_enabled_thinking(self) -> None:
        client = GlmClient(api_key="test-key", base_url="https://example.invalid")
        with self.assertRaisesRegex(GlmError, "requires thinking=enabled"):
            client.chat_json(
                model="glm-5.3-flash",
                system="system",
                user="user",
                thinking="disabled",
                reasoning_effort="low",
            )


if __name__ == "__main__":
    unittest.main()
