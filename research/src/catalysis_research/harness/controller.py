from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable

from .jev import JEV_DECISION_SCHEMA_VERSION, JevJudge, _strip_locked_test, build_jev_request, validate_jev_decision
from .roles import DEFAULT_ROLES, HarnessRole
from .types import HarnessRun, RoundInput


HARNESS_SCHEMA_VERSION = "scientific_harness_run.v1"


class HarnessController:
    """Run auditable role checks and Jev routing for hypothesis rounds."""

    def __init__(self, *, judge: JevJudge, roles: Iterable[HarnessRole] = DEFAULT_ROLES):
        self.judge = judge
        self.roles = tuple(roles)
        if not self.roles:
            raise ValueError("at least one harness role is required")

    def run(self, *, run_id: str, rounds: Iterable[RoundInput], run_context: dict[str, Any] | None = None) -> HarnessRun:
        previous: list[dict[str, Any]] = []
        output_rounds: list[dict[str, Any]] = []
        for round_input in rounds:
            round_result = self.run_round(round_input, previous, run_context or {})
            output_rounds.append(round_result)
            for candidate, record in zip(round_input.candidates, round_result["records"]):
                previous.append({
                    **candidate,
                    "harness_decision": record["jev"],
                    "role_outputs": record["role_outputs"],
                })
        return HarnessRun(
            schema_version=HARNESS_SCHEMA_VERSION,
            run_id=run_id,
            rounds=output_rounds,
            warnings=[
                "Jev decisions route work; they do not replace programmatic execution or locked evaluation.",
                "A compute recommendation is not scientific confirmation.",
            ],
        )

    def run_round(self, round_input: RoundInput, prior_candidates: list[dict[str, Any]], run_context: dict[str, Any]) -> dict[str, Any]:
        records: list[dict[str, Any]] = []
        decisions: Counter[str] = Counter()
        stage_context = {**run_context, **round_input.context}
        for candidate in round_input.candidates:
            role_outputs = {
                role.role_id: role.evaluate(_strip_locked_test(candidate), {**stage_context, "prior_candidates": prior_candidates})
                for role in self.roles
            }
            request = build_jev_request(
                candidate=candidate,
                role_outputs=role_outputs,
                prior_candidates=prior_candidates,
                round_id=round_input.round_id,
                run_context=stage_context,
            )
            decision = validate_jev_decision(self.judge.judge(request), request=request)
            decisions[decision.recommendation] += 1
            record = {
                "candidate_id": candidate["candidate_id"],
                "candidate": candidate,
                "role_outputs": role_outputs,
                "jev": {
                    "schema_version": JEV_DECISION_SCHEMA_VERSION,
                    **decision.to_dict(),
                },
            }
            record["request_sha256"] = hashlib.sha256(
                json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            record["role_output_sha256"] = {
                role_id: hashlib.sha256(
                    json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest()
                for role_id, output in role_outputs.items()
            }
            record["decision_sha256"] = hashlib.sha256(
                json.dumps(decision.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            records.append(record)
        gains = [
            float((item["role_outputs"].get("validation_planner") or {}).get("marginal_gain"))
            for item in records
            if isinstance((item["role_outputs"].get("validation_planner") or {}).get("marginal_gain"), (int, float))
        ]
        positive_gains = [gain for gain in gains if gain > 0]
        return {
            "round_id": round_input.round_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "candidate_count": len(records),
            "decision_counts": dict(sorted(decisions.items())),
            "mean_validation_gain": sum(gains) / len(gains) if gains else None,
            "progress": {
                "positive_validation_gain_rate": len(positive_gains) / len(gains) if gains else None,
                "candidates_eligible_for_compute": decisions.get("compute_validate", 0),
                "candidates_requiring_more_evidence": decisions.get("retrieve_more", 0),
                "candidates_revised": decisions.get("revise", 0),
                "candidates_deferred": decisions.get("defer", 0),
                "candidates_abandoned": decisions.get("abandon", 0),
            },
            "records": records,
        }
