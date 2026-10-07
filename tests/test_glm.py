from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT / "src"))

from catalysis_research.llm.glm import GlmClient, GlmError, GlmOutputTruncated, GlmMalformedJson  # noqa: E402


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
    def test_ambiguous_objects_preserve_raw_response_without_selecting_one(self):
        class Malformed(_Response):
            def read(self):
                return json.dumps({'model':'glm-5.3-flash','choices':[{'finish_reason':'stop',
                    'message':{'content':'{"candidate_patches":[]} {"other":1}'}}],
                    'usage':{'total_tokens':19}}).encode()
        with patch('urllib.request.urlopen',return_value=Malformed()):
            with self.assertRaises(GlmMalformedJson) as caught:
                GlmClient(api_key='test-key',retries=0).chat_json(model='glm-5.3-flash',system='s',user='u')
        self.assertEqual(caught.exception.content,'{"candidate_patches":[]} {"other":1}')
        self.assertEqual(caught.exception.usage['total_tokens'],19)

    def test_length_finish_reason_is_reported_before_parsing_partial_json(self) -> None:
        class Truncated(_Response):
            headers = {'x-request-id':'truncated-request'}
            def read(self) -> bytes:
                return json.dumps({'choices': [{'finish_reason': 'length',
                    'message': {'content': '{"descriptor_candidates": ['}}],
                    'usage': {'completion_tokens': 16000}}).encode()
        with patch('urllib.request.urlopen', return_value=Truncated()):
            with self.assertRaises(GlmOutputTruncated) as caught:
                GlmClient(api_key='test-key', retries=0).chat_json(model='glm-5.3-flash', system='s', user='u')
        self.assertEqual(caught.exception.usage['completion_tokens'], 16000)
        self.assertEqual(caught.exception.raw['choices'][0]['message']['content'], '{"descriptor_candidates": [')
        self.assertEqual(caught.exception.raw['_response_request_ids']['x-request-id'], 'truncated-request')

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
