"""Freeze ZeoSyn evidence bundles before any generation.

Held-out ZeoSyn publications are removed from both the RAG index and the Small
KG through the existing fail-closed retrieval contract. The expected exclusion
counts are computed by streaming the index files and then re-verified when the
retriever loads; any mismatch, or any held-out paper in a bundle, stops the run.
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from ..datasets.zeosyn import normalize_doi


def _rows(path):
    with Path(path).open('r', encoding='utf-8') as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def paper_doi(paper_id):
    text = str(paper_id)
    return normalize_doi(text) if text.casefold().startswith('doi:') else None


def match_index_papers(rag_index, dois):
    """Exact index paper IDs whose DOI is in ``dois`` (case-insensitive)."""
    wanted = {normalize_doi(d) for d in dois if normalize_doi(d)}
    return sorted({str(r['paper_id']) for r in _rows(Path(rag_index) / 'papers.jsonl')
                   if paper_doi(r['paper_id']) in wanted})


def exclusion_counts(rag_index, excluded):
    rag_index = Path(rag_index)
    excluded = frozenset(excluded)
    papers = {str(r['paper_id']) for r in _rows(rag_index / 'papers.jsonl')}
    documents = list(_rows(rag_index / 'documents.jsonl'))
    chunk_total = chunk_excluded = evidence_excluded = 0
    for r in _rows(rag_index / 'chunks.jsonl'):
        chunk_total += 1
        chunk_excluded += str(r['paper_id']) in excluded
    for r in _rows(rag_index / 'evidence_records.jsonl'):
        evidence_excluded += str(r['paper_id']) in excluded
    excluded_documents = sum(str(r['paper_id']) in excluded for r in documents)
    return {
        'expected_excluded_documents': excluded_documents,
        'expected_excluded_records': chunk_excluded + evidence_excluded,
        'expected_retained_papers': len(papers - excluded),
        'expected_retained_documents': len(documents) - excluded_documents,
        'expected_retained_chunks': chunk_total - chunk_excluded,
    }


def retrieval_config(base_config, *, matched_ids, counts, test_dois, matrix_sha256):
    c = deepcopy(base_config)
    base_excluded = list(c['rag']['excluded_paper_ids'])
    excluded = sorted(set(base_excluded) | set(matched_ids))
    c['retrieval_id'] = c['retrieval_id'] + '-zeosyn-heldout'
    c['rag'].update({'excluded_paper_ids': excluded, **counts})
    c['benchmark_exclusion'] = {
        'benchmark': 'ZeoSyn', 'policy': 'held-out test publications removed from RAG and Small KG',
        'held_out_dois': len(test_dois), 'held_out_dois_in_index': len(matched_ids),
        'base_excluded_paper_ids': base_excluded, 'matrix_sha256': matrix_sha256,
    }
    return c


def leaked_items(bundle, held_out_dois):
    held = {normalize_doi(d) for d in held_out_dois}
    return [item['paper_id'] for item in bundle.get('items', []) if paper_doi(item.get('paper_id')) in held]


def freeze_bundles(retriever, *, queries, budget, held_out_dois, modes=('rag_agent', 'small_kg_rag_agent')):
    bundles, leaks = {}, []
    for mode in modes:
        bundles[mode] = []
        for q in queries:
            b = retriever.retrieve(query=q, experiment_mode=mode, budget=budget)
            leaks += [(mode, q, p) for p in leaked_items(b, held_out_dois)]
            bundles[mode].append(b)
    if leaks:
        raise RuntimeError(f'Held-out ZeoSyn publication in evidence: {leaks[:5]}')
    return bundles
