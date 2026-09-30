"""Build and preflight a separate V3 bank from archived, source-traceable rows."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from catalysis_research.experiments.jacs_au import save_json
from catalysis_research.experiments.jacs_au_knowledge import QUERIES
from catalysis_research.experiments.jacs_au_kg_v3 import (
    build_bank, audit_bank, load_budget_config, select_evidence, render_evidence, pack_graph, unpack_graph,
)


def prepare(source, reviews, config, output):
    if output.exists(): raise ValueError('Use a new evidence directory; do not overwrite a frozen bank')
    budget = load_budget_config(config)
    bank = build_bank(json.loads(source.read_text(encoding='utf-8')),
                      json.loads(reviews.read_text(encoding='utf-8')), budget)
    audit_bank(bank)
    previews = []
    rb = budget['retrieval']
    for rd, query in enumerate(QUERIES, 1):
        bank['active_round'] = rd
        kwargs = dict(token_budget=rb['context_lexical_tokens'], item_limit=rb['max_items'],
                      candidate_limit=rb['candidates_per_round'], paper_limit=rb['max_items_per_paper'],
                      max_kg_items=rb['max_kg_items'])
        rag, rr = select_evidence(bank, 'rag_agent', query, **kwargs)
        kg, kr = select_evidence(bank, 'small_kg_rag_agent', query, **kwargs)
        flat, fr = select_evidence(bank, 'small_kg_rag_agent', query, graph_view='text', **kwargs)
        if kg[:len(rag)] != rag: raise ValueError('RAG anchor preservation failed')
        if kg != flat: raise ValueError('Graph ablation changed facts')
        if not kr['kg_selected_items']: raise ValueError('No reviewed KG fits without displacing RAG')
        if unpack_graph(pack_graph(kg)) != kg: raise ValueError('Lossy compression')
        previews.append({'query': query, 'rag': rr, 'kg': kr, 'flat': fr,
                         'actual_context': render_evidence(kg), 'anchor_identical': True, 'same_facts_across_views': True})
    bank.pop('active_round', None)
    report = {'status': 'passed', 'profile': bank['profile'], 'eligible_counts': bank['eligible_counts'],
              'paper_counts': bank['paper_counts'], 'rejected': bank['rejected'], 'previews': previews,
              'limits': ['Engineering and source applicability gate, not predictive validation.',
                         'Conditional mechanisms have unresolved source conditions; no direct target-regime proof.']}
    save_json(output/'bank.json', bank)
    save_json(output/'preflight.json', report)
    print(json.dumps({k: report[k] for k in ('status','profile','eligible_counts','paper_counts')}, ensure_ascii=False))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-bank', type=Path, required=True)
    p.add_argument('--review', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    prepare(a.source_bank, a.review, a.config, a.output)
