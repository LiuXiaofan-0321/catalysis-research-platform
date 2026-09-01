"""Immutable scientific normalization overlays for frozen KG snapshots."""

from .builder import NormalizationError, build_normalization_overlay
from .overlay import ScientificNormalizationOverlay
from .review import summarize_unresolved
from .verifier import verify_normalization_overlay

__all__ = [
    "NormalizationError",
    "ScientificNormalizationOverlay",
    "build_normalization_overlay",
    "summarize_unresolved",
    "verify_normalization_overlay",
]
