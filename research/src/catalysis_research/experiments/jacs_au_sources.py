"""Independent benchmark identity and result-contamination guards.

The explicit DOI/PMCID/PMID identities are not inferred from an exclusion list
produced by retrieval. Guards also inspect nested graph evidence.
"""
from __future__ import annotations

import html
import json
import re
import unicodedata

DOI = '10.1021/jacsau.4c00429'
BENCHMARK_IDS = frozenset({f'doi:{DOI}', 'pmc:pmc11672123', 'pmid:39735916'})
# Known main/SI documents of the same benchmark, independently audited locally.
BENCHMARK_DOCUMENTS = frozenset({'document:ad183880ced31c026e20c474',
                                 'document:1887d169511f36a3f2d23905'})


def normalize(text):
    text = unicodedata.normalize('NFKC', html.unescape(str(text))).casefold()
    text = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m[1], 16)), text)
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values(): yield from strings(item)
    elif isinstance(value, (tuple, list)):
        for item in value: yield from strings(item)


def contamination_reason(value):
    """Inspect retrieved scientific content, not task metadata containing its DOI."""
    for text in strings(value):
        lower = text.casefold()
        normal = normalize(text)
        if DOI in lower or 'pmc11672123' in lower or re.search(r'\b39735916\b', lower):
            return 'benchmark_identity'
        if any(doc in lower for doc in BENCHMARK_DOCUMENTS):
            return 'benchmark_document'
        if 'elucidating thermodynamically driven structure property relations' in normal:
            return 'benchmark_title'
        # Specific result excerpts, not a generic ban on SHAP or pore physics.
        if any(signature in normal for signature in (
            'lsd f exhibits the strongest variation in shapley values',
            'lsd p can contribute between 0 07 and 0 07',
            'the u shaped trend within figure 12m',
            'framework descriptor shapley values demonstrated much greater variability',
        )):
            return 'benchmark_result_excerpt'
    return None


def assert_clean(value, excluded=(), excluded_documents=()):
    reason = contamination_reason(value)
    if reason:
        raise ValueError('Benchmark evidence leakage: ' + reason)
    excluded = {str(x).casefold() for x in excluded}
    documents = {str(x).casefold() for x in excluded_documents}
    def walk(obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if key in {'paper_id', 'source_paper_id'} and str(val).casefold() in excluded:
                    raise ValueError('Excluded source identity in nested evidence')
                if key in {'document_id', 'source_document_id'} and str(val).casefold() in documents:
                    raise ValueError('Excluded document identity in nested evidence')
                walk(val)
        elif isinstance(obj, list):
            for val in obj: walk(val)
    walk(value)


def exclusion_closure(papers, documents):
    excluded = set(BENCHMARK_IDS)
    docs = set(BENCHMARK_DOCUMENTS)
    # Preserve the unrelated pre-existing exclusion as an explicit policy.
    excluded.add('doi:10.1126/science.ads7290')
    for row in papers:
        if contamination_reason(row): excluded.add(str(row['paper_id']))
    changed = True
    while changed:
        before = (len(excluded), len(docs))
        for row in documents:
            if (str(row.get('paper_id')) in excluded or str(row.get('document_id')) in docs
                    or contamination_reason(row)):
                docs.add(str(row['document_id']))
                if row.get('paper_id'): excluded.add(str(row['paper_id']))
        changed = before != (len(excluded), len(docs))
    return excluded, docs
