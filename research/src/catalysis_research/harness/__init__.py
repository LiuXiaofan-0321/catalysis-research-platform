"""Auditable hypothesis-discovery harness primitives.

The harness separates model proposals from evidence review, novelty checks,
feasibility checks, validation planning, and final routing.  Every stage is
represented as structured data so a run can be replayed without an LLM.
"""

from .controller import HarnessController
from .jev import HttpJevClient, RuleBasedJev, build_jev_request, validate_jev_decision
from .roles import DEFAULT_ROLES
from .topic import JevTopicScout, RuleBasedTopicScout
from .types import HarnessRun, JevDecision, RoundInput

__all__ = [
    "DEFAULT_ROLES",
    "HarnessController",
    "HarnessRun",
    "HttpJevClient",
    "JevDecision",
    "JevTopicScout",
    "RoundInput",
    "RuleBasedJev",
    "RuleBasedTopicScout",
    "build_jev_request",
    "validate_jev_decision",
]
