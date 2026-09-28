from __future__ import annotations

import hashlib
import json
import math
import os
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any, Protocol


TOPIC_SCOUT_SCHEMA_VERSION = "jev_topic_scout.v1"


@dataclass(frozen=True)
class TopicSignal:
    topic_id: str
    label: str
    recency_score: float
    momentum_score: float
    source_ids: list[str]
    window_start: str
    window_end: str
    as_of: str


class TopicScout(Protocol):
    def scout(self, records: list[dict[str, Any]], *, cutoff: str, corpus_hash: str) -> dict[str, Any]:
        ...


def _parse_day(value: Any) -> date | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except (TypeError, ValueError):
        try:
            return date.fromisoformat(str(value)[:10])
        except (TypeError, ValueError):
            return None


class RuleBasedTopicScout:
    """Offline, reproducible hotness baseline with a frozen cutoff."""

    def __init__(self, *, window_days: int = 365, half_life_days: float = 365.0):
        if window_days < 1 or half_life_days <= 0:
            raise ValueError("window_days and half_life_days must be positive")
        self.window_days = window_days
        self.half_life_days = half_life_days

    def scout(self, records: list[dict[str, Any]], *, cutoff: str, corpus_hash: str) -> dict[str, Any]:
        cutoff_day = _parse_day(cutoff)
        if cutoff_day is None:
            raise ValueError("cutoff must be an ISO date or datetime")
        window_start = cutoff_day - timedelta(days=self.window_days)
        prior_start = window_start - timedelta(days=self.window_days)
        grouped: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            published = _parse_day(record.get("published_at") or record.get("year"))
            topic_id = str(record.get("topic_id") or "").strip()
            if not published or not topic_id or published > cutoff_day or published < prior_start:
                continue
            grouped.setdefault(topic_id, []).append({**record, "_published": published})
        signals: list[TopicSignal] = []
        for topic_id, items in grouped.items():
            recent = [item for item in items if item["_published"] >= window_start]
            prior = [item for item in items if item["_published"] < window_start]
            age = min((cutoff_day - item["_published"]).days for item in recent) if recent else self.window_days
            recency = math.exp(-age / self.half_life_days) if recent else 0.0
            momentum = min(1.0, len(recent) / max(1, len(prior))) if recent else 0.0
            source_ids = sorted({str(item.get("source_id")) for item in items if item.get("source_id")})
            label = str(next((item.get("label") for item in items if item.get("label")), topic_id))
            signals.append(TopicSignal(
                topic_id=topic_id,
                label=label,
                recency_score=round(recency, 6),
                momentum_score=round(momentum, 6),
                source_ids=source_ids,
                window_start=window_start.isoformat(),
                window_end=cutoff_day.isoformat(),
                as_of=cutoff_day.isoformat(),
            ))
        signals.sort(key=lambda item: (item.momentum_score + item.recency_score, item.topic_id), reverse=True)
        return {
            "schema_version": TOPIC_SCOUT_SCHEMA_VERSION,
            "scout": "rule_based_recency_momentum_v1",
            "cutoff": cutoff_day.isoformat(),
            "corpus_hash": corpus_hash,
            "signals": [asdict(signal) for signal in signals],
            "search_queries": [signal.label for signal in signals[:10]],
            "hotness_is_retrieval_priority_only": True,
        }


class JevTopicScout:
    """Jev-compatible topic scout; validates provenance and cutoff locally."""

    def __init__(self, *, endpoint: str | None = None, api_key: str | None = None, timeout_seconds: float = 120.0):
        self.endpoint = endpoint or os.environ.get("JEV_TOPIC_ENDPOINT")
        self.api_key = api_key or os.environ.get("JEV_API_KEY", "")
        self.timeout_seconds = timeout_seconds
        if not self.endpoint or not self.api_key:
            raise ValueError("JEV_TOPIC_ENDPOINT and JEV_API_KEY are required")

    def scout(self, records: list[dict[str, Any]], *, cutoff: str, corpus_hash: str) -> dict[str, Any]:
        cutoff_day = _parse_day(cutoff)
        if cutoff_day is None:
            raise ValueError("cutoff must be an ISO date or datetime")
        known_source_ids = {str(item.get("source_id")) for item in records if item.get("source_id")}
        payload = {
            "schema_version": TOPIC_SCOUT_SCHEMA_VERSION,
            "cutoff": cutoff_day.isoformat(),
            "corpus_hash": corpus_hash,
            "records": records,
            "instruction": "Return topic signals and retrieval queries. Hotness is not evidence support.",
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            method="POST",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise RuntimeError(f"Jev topic request failed: {error}") from error
        result = raw.get("result", raw) if isinstance(raw, dict) else raw
        if not isinstance(result, dict) or result.get("schema_version") != TOPIC_SCOUT_SCHEMA_VERSION:
            raise RuntimeError("Jev topic response has an unexpected schema_version")
        signals = result.get("signals", [])
        if not isinstance(signals, list):
            raise RuntimeError("Jev topic response signals must be a list")
        for signal in signals:
            if not isinstance(signal, dict) or not signal.get("topic_id"):
                raise RuntimeError("Jev topic response contains an invalid signal")
            if any(source_id not in known_source_ids for source_id in signal.get("source_ids", [])):
                raise RuntimeError("Jev topic response cited an unknown source_id")
            if _parse_day(signal.get("as_of")) and _parse_day(signal["as_of"]) > cutoff_day:
                raise RuntimeError("Jev topic response used a future as_of date")
            for score_name in ("recency_score", "momentum_score"):
                score = signal.get(score_name)
                if not isinstance(score, (int, float)) or not 0.0 <= float(score) <= 1.0:
                    raise RuntimeError(f"Jev topic response has invalid {score_name}")
        queries = result.get("search_queries", [])
        if not isinstance(queries, list) or not all(isinstance(query, str) and query.strip() for query in queries):
            raise RuntimeError("Jev topic response search_queries must be non-empty strings")
        result["corpus_hash"] = corpus_hash
        result["cutoff"] = cutoff_day.isoformat()
        result["hotness_is_retrieval_priority_only"] = True
        return result
