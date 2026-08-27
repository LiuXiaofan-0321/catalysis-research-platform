from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any


def baseline_summary(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload if isinstance(payload, list) else payload.get("papers") or []
    if not isinstance(records, list):
        raise ValueError("Baseline manifest does not contain records")
    successful = [
        item
        for item in records
        if isinstance(item, dict)
        and item.get("status") in {"completed", "cached"}
    ]
    token_values = [
        int((item.get("usage") or {}).get("total_tokens") or 0)
        for item in successful
        if (item.get("usage") or {}).get("total_tokens") is not None
    ]
    prompt_values = [
        int((item.get("usage") or {}).get("prompt_tokens") or 0)
        for item in successful
        if (item.get("usage") or {}).get("prompt_tokens") is not None
    ]
    return {
        "schema_version": "literature_baseline_report.v1",
        "manifest": str(path.resolve()),
        "records": len(records),
        "successful": len(successful),
        "failed": sum(
            isinstance(item, dict) and item.get("status") == "failed"
            for item in records
        ),
        "average_prompt_tokens": mean(prompt_values) if prompt_values else None,
        "average_total_tokens": mean(token_values) if token_values else None,
        "projected_6000_total_tokens": (
            mean(token_values) * 6000 if token_values else None
        ),
    }
