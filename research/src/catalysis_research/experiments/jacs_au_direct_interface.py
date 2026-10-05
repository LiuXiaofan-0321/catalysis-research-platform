"""Lossless proxy-assumption interface adapter for a future, separately frozen run.

The completed 20261004 V5 release intentionally remains unchanged. This adapter
accepts a nonempty list of text assumptions without an LLM rewrite. Raw responses
must still be retained separately; this is representation repair, not a new claim.
"""
from copy import deepcopy

from .jacs_au_direct import validate_candidate


def normalize_proxy_assumptions(value):
    """Preserve every text item and all other fields; never fill missing science."""
    normalized = deepcopy(value)
    if not isinstance(normalized, dict) or not isinstance(normalized.get('descriptor_candidate'), dict):
        raise ValueError('One descriptor_candidate object required')
    c = normalized['descriptor_candidate']; assumptions = c.get('proxy_assumptions')
    audit = {'field': 'proxy_assumptions', 'edit_type': 'representation_only',
             'original_type': type(assumptions).__name__, 'llm_calls': 0,
             'formula_or_scientific_text_reworded': False}
    if isinstance(assumptions, list):
        if not assumptions or any(not isinstance(item, str) or not item.strip() for item in assumptions):
            raise ValueError('Assumption list must contain nonempty strings only; do not invent missing content')
        c['proxy_assumptions'] = '\n'.join(assumptions)
        audit.update(items_preserved=len(assumptions), rule='Exact ordered newline join; no paraphrase')
    elif not isinstance(assumptions, str) or not assumptions.strip():
        raise ValueError('Nonempty string or list of nonempty assumption strings required')
    else:
        audit.update(items_preserved=1, rule='Original string unchanged')
    return normalized, audit


def validate_candidate_with_proxy_adapter(value):
    normalized, audit = normalize_proxy_assumptions(value)
    return validate_candidate(normalized), audit
