"""Frozen literature corpus inventories for research experiments."""

from .stage1 import (
    CorpusError,
    freeze_stage1_corpus,
    verify_stage1_corpus,
)

__all__ = [
    "CorpusError",
    "freeze_stage1_corpus",
    "verify_stage1_corpus",
]
