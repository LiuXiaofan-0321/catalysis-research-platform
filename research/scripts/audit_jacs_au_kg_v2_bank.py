"""Gate a queued pilot on source exclusions, connected paths and usable contexts.

This is a technical evidence audit, not a verdict that the source mechanisms
apply to the benchmark or that KG improves predictive performance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from catalysis_research.experiments.jacs_au import DOI, save_json
from catalysis_research.experiments.jacs_au_sources import assert_clean
from catalysis_research.experiments.jacs_au_knowledge import (
    PROFILE, load_budget_config, relevance, adaptive_query, select_evidence,
)


def audit(bank, config_path, document_papers=None):
    budget = load_budget_config(config_path)
    if bank.get('profile') != PROFILE or bank.get('status') != 'ready':
        raise ValueError('Evidence bank is not ready for KG-v2')
    if bank.get('budget_config') != budget:
        raise ValueError('Evidence bank budget differs from the queued pilot')
    excluded = set(bank['source_audit']['excluded_paper_ids'])
    unsupported_edges = set(); unknown_scope = 0
    for channel in ['rag', 'kg']:
        if not bank.get(channel): raise ValueError('Empty evidence channel: '+channel)
        for row in bank[channel]:
            if row['channel'] != channel: raise ValueError('Wrong evidence channel')
            assert_clean(row, excluded, bank['source_audit'].get('excluded_document_ids', []))
            if document_papers is not None and document_papers.get(row['document_id']) != row['paper_id']:
                raise ValueError('Quote source document and attributed paper differ')
            if not relevance(row['quote'])[0]: raise ValueError('Irrelevant evidence passage')
            if row['locator']['kind'] == 'pdf_page' and (
                    type(row['locator'].get('page')) is not int or row['locator']['page'] < 1):
                raise ValueError('Invalid source page')
            unknown_scope += 'conditions_not_explicit_in_excerpt' in row['scope_tags']
            if channel == 'kg' and not row['graph_paths']:
                raise ValueError('KG entry has no relation path')
            for path in row['graph_paths']:
                if len(path['nodes']) != len(path['edges']) + 1:
                    raise ValueError('Incomplete connected path')
                for i, edge in enumerate(path['edges']):
                    expected = {path['nodes'][i]['id'], path['nodes'][i+1]['id']}
                    if {edge['source'], edge['target']} != expected:
                        raise ValueError('Disconnected or invented relation path')
                    if edge.get('source_paper_id') in excluded:
                        raise ValueError('Excluded paper in graph relation')
                    if not edge['support']: unsupported_edges.add(edge['id'])
    rb = budget['retrieval']; previews = []
    for mode in ['agent', 'rag_agent', 'small_kg_rag_agent']:
        for round_no in range(1, 4):
            bank['active_round'] = round_no
            items, report = select_evidence(bank, mode, adaptive_query(round_no, [], []),
                token_budget=rb['context_lexical_tokens'], item_limit=rb['max_items'],
                candidate_limit=rb['candidates_per_round'], paper_limit=rb['max_items_per_paper'],
                kg_priority_items=rb['kg_priority_items'])
            if mode != 'agent' and not items: raise ValueError('No evidence fits '+mode)
            if mode == 'small_kg_rag_agent' and not report['kg_selected_items']:
                raise ValueError('No connected KG evidence fits the configured budget')
            if report['lexical_tokens'] > rb['context_lexical_tokens']:
                raise ValueError('Context budget exceeded')
            previews.append({'mode': mode, 'round': round_no, 'retrieval': report, 'items': items})
    return {'status': 'passed', 'profile': PROFILE, 'budget_config': budget,
            'eligible_counts': bank['eligible_counts'], 'paper_counts': bank['paper_counts'],
            'source_audit': bank['source_audit'], 'neutral_query_previews': previews,
            'rows_with_unspecified_scope': unknown_scope,
            'edges_without_direct_support_quote': len(unsupported_edges),
            'interpretation': 'Source and path integrity gate. Scope unknowns and unquoted edges require scientific review; no causal or performance validation is claimed.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--base', type=Path, required=True)
    args = p.parse_args()
    try:
        probe = json.loads((args.run/'api-probe-result.json').read_text())
        if probe.get('ok') is not True or probe.get('finish_reason') != 'stop':
            raise ValueError('Compute-node GLM probe failed')
        document_papers={d['document_id']:d['paper_id']
            for line in (args.base/'workspace-full/indexes/full-rag-v1-index/documents.jsonl').read_text().splitlines()
            if line.strip() for d in [json.loads(line)]}
        result = audit(json.loads((args.run/'evidence/bank.json').read_text()), args.config, document_papers)
        result['compute_api_probe'] = probe
    except Exception as error:
        save_json(args.run/'evidence/preflight.json', {'status': 'failed', 'error': str(error)})
        raise
    save_json(args.run/'evidence/preflight.json', result)
    print(json.dumps({'status': result['status'], 'eligible_counts': result['eligible_counts'],
                      'paper_counts': result['paper_counts']}, ensure_ascii=False))


if __name__ == '__main__': main()
