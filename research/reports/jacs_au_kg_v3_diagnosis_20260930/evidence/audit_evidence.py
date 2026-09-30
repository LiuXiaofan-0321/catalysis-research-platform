"""Read-only V3 evidence/domain audit; no LLM calls or predictive fitting."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import statistics
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'research' / 'src'))
from catalysis_research.experiments.jacs_au import FEATURES, load_data, make_split
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v3 import render_evidence, token_count


def normalized(text):
    return ' '.join(re.findall(r'\w+', text.lower()))


def audit(data_root):
    source = ROOT / 'research/reports/jacs_au_kg_v3_repair_20260929'
    bank = json.loads((source / 'evidence-final/bank.json').read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('read_only_jacs_runner', ROOT / 'research/scripts/run_jacs_au.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    data = load_data(data_root)
    train = make_split(data)['train']
    env, references = formula_environment(data, train)
    out = {'protocol': 'Read-only source, saved trajectories and train-domain checks; no new API calls or fitting',
           'train_n': len(train), 'retrieval_policy': bank['retrieval_policy'], 'bank': {}, 'training_domain': {},
           'modes': {}, 'nonfinite_candidate_checks': []}
    out['bank']['eligible_counts'] = bank['eligible_counts']
    out['bank']['paper_counts'] = {c: dict(Counter(r['paper_id'] for r in bank[c])) for c in ('rag', 'kg')}
    overlap = []
    for row in bank['kg']:
        matches = [r['record_id'] for r in bank['rag'] if normalized(row['quote']) in normalized(r['quote'])]
        overlap.append({'mechanism_id': row['mechanism_id'], 'same_quote_in_rag_records': matches})
    out['bank']['kg_quote_overlap'] = overlap
    out['bank']['kg_graphs'] = [{
        'mechanism_id': r['mechanism_id'], 'paths': len(r['graph_paths']),
        'node_count': sum(len(p['nodes']) for p in r['graph_paths']),
        'edge_count': sum(len(p['edges']) for p in r['graph_paths']),
        'nodes': [n['id'] for p in r['graph_paths'] for n in p['nodes']],
    } for r in bank['kg']]
    for i, name in enumerate(FEATURES):
        values = data['x'][train, i]
        out['training_domain'][name] = {'min': float(values.min()), 'max': float(values.max()),
            'zeros': int((values == 0).sum()), 'zero_pct': float((values == 0).mean()*100),
            'nonpositive': int((values <= 0).sum()), 'positive_reference': references[name]}
    for mode in ('agent', 'rag_agent', 'small_kg_rag_agent'):
        ds = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((source / 'server-results/discovery').glob(mode+'-*.json'))]
        candidates = [c for d in ds for rd in d['rounds'] for c in rd['candidates']]
        rounds = [rd for d in ds for rd in d['rounds']]
        usages = [u for rd in rounds for u in rd['usage']]
        memberships = [frozenset((r['paper_id'], r['quote'], tuple(r['channels'])) for r in e['items'])
                       for d in ds for e in d['evidence_by_round']]
        reasoning = [u.get('completion_tokens_details', {}).get('reasoning_tokens', 0) for u in usages]
        first_items = ds[0]['evidence_by_round'][0]['items']
        out['modes'][mode] = {
            'trajectories': len(ds), 'candidate_n': len(candidates),
            'status_counts': dict(Counter(c['status'] for c in candidates)),
            'rejection_reasons': dict(Counter(c['reason'] for c in candidates if c['status']=='rejected')),
            'log_formulas': sum(bool(re.search(r'\blog(?:10)?\s*\(', c['formula'])) for c in candidates),
            'full_training_domain_declarations': sum(c['scientific_test']['regime_train_quantiles']==[0.,1.] for c in candidates),
            'positive_candidate_n': sum((c.get('marginal_improvement') or 0)>0 for c in candidates),
            'retained_n': sum(c['retained'] for c in candidates),
            'different_evidence_membership_sets': len(set(memberships)),
            'first_round_evidence_lexical_tokens': token_count(render_evidence(first_items)) if first_items else 0,
            'first_round_quote_only_lexical_tokens': token_count([r['quote'] for r in first_items]) if first_items else 0,
            'api_calls': len(usages), 'api_prompt_tokens_mean': statistics.mean(u.get('prompt_tokens',0) for u in usages),
            'reasoning_tokens_mean': statistics.mean(reasoning), 'reasoning_tokens_median': statistics.median(reasoning),
            'reasoning_tokens_per_call': reasoning,
            'finish_reasons': dict(Counter(c['finish_reason'] for rd in rounds for c in rd['completion_attempts'])),
            'trajectories_results': [{'replicate': d['replicate'], 'score_improvement_pct': d['score_improvement_pct'],
                                     'test_improvement_pct': d['test_improvement_pct']} for d in ds],
        }
        for d in ds:
            for rd in d['rounds']:
                for c in rd['candidates']:
                    if c.get('reason')!='Formula unstable inside declared physical regime':
                        continue
                    st = c['scientific_test']
                    local = {k:v[train].copy() for k,v in env.items()}
                    lo, hi = np.quantile(local[st['regime_input']], st['regime_train_quantiles'])
                    mask = (local[st['regime_input']]>=lo)&(local[st['regime_input']]<=hi)
                    values = local[st['vary_input']]
                    step = max(float(np.quantile(values,.9)-np.quantile(values,.1))*.01, 1e-8)
                    plus = {k:v.copy() for k,v in local.items()}
                    plus[st['vary_input']] = values+step
                    plus['q_'+st['vary_input']] = plus[st['vary_input']]/plus[st['vary_input']+'_ref']
                    before = runner.evaluate_formula(c['formula'], local)
                    after = runner.evaluate_formula(c['formula'], plus)
                    bad = mask & (~np.isfinite(before)|~np.isfinite(after))
                    names = {n.id for n in ast.walk(ast.parse(c['formula'])) if isinstance(n, ast.Name)}
                    zero_inputs = [f for f in FEATURES if (f in names or 'q_'+f in names) and (local[f][bad]==0).any()]
                    out['nonfinite_candidate_checks'].append({'mode':mode, 'replicate':d['replicate'], 'round':rd['round'],
                        'name':c['name'], 'formula':c['formula'], 'declared_regime':st,
                        'bad_rows':int(bad.sum()), 'regime_rows':int(mask.sum()),
                        'invalid_regime_pct':float(bad.sum()/mask.sum()*100), 'zero_inputs_in_bad_rows':zero_inputs})
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-root', default='C:/Users/18963/AppData/Local/Temp/jacs-au-4c00429/Supporting_final_2')
    parser.add_argument('--output', default=str(Path(__file__).with_name('audit_evidence.json')))
    args=parser.parse_args()
    result=audit(args.data_root)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({'output':args.output,'nonfinite_candidates_rechecked':len(result['nonfinite_candidate_checks']),
                      'mode_counts':{m:v['status_counts'] for m,v in result['modes'].items()}},ensure_ascii=False))
