"""Summarize a partial or completed KG-v2 pilot, preserving negative results."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import statistics


MODES = ['agent', 'rag_agent', 'small_kg_rag_agent']


def describe(values):
    return {'n': len(values), 'mean': statistics.mean(values) if values else None,
            'std': statistics.stdev(values) if len(values) > 1 else None,
            'min': min(values) if values else None, 'max': max(values) if values else None}


def analyze(root, expected):
    records = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((root/'discovery').glob('*.json'))]
    profiles={r.get('knowledge_profile') for r in records}
    if not profiles <= {'jacs-au-kg-v2','jacs-au-kg-v3'} or len(profiles)>1:
        raise ValueError('Do not combine different knowledge protocols')
    profile=next(iter(profiles),'jacs-au-kg-v2')
    views={r.get('graph_view','paths') for r in records if r['mode']=='small_kg_rag_agent'}
    if len(views)>1:raise ValueError('Summarize graph and text ablations in separate run directories')
    groups = {}; errors = []
    for mode in MODES:
        all_rows = [r for r in records if r['mode'] == mode]
        rows = [r for r in all_rows if r['status'] == 'completed']
        for r in rows:
            if r.get('knowledge_profile') != profile: raise ValueError('Wrong experiment profile')
            if len(r['rounds']) != 3: raise ValueError('Incomplete completed trajectory')
            current = r['d0_score_mae_R']
            for rd in r['rounds']:
                if len(rd['candidates']) != 3: raise ValueError('Wrong proposal count')
                scored = [c for c in rd['candidates'] if c['status'] == 'scored']
                best = min([current]+[c['score']['mae_R'] for c in scored])
                if abs(rd['before_mae_R']-current)>1e-8 or abs(rd['after_mae_R']-best)>1e-8:
                    raise ValueError('Selection does not reproduce scoring winner')
                winners = [c for c in rd['candidates'] if c['retained']]
                if len(winners) != int(best < current-1e-10): raise ValueError('Invalid retained count')
                current = best
        candidates = [c for r in rows for rd in r['rounds'] for c in rd['candidates']]
        kg_cited = 0; retained_kg_cited = 0
        for r in rows:
            kg_ids = {e['id'] for rd in r['evidence_by_round'] for e in rd['items'] if 'kg' in e['channels']}
            for rd in r['rounds']:
                for candidate in rd['candidates']:
                    cites_kg = bool(set(candidate.get('evidence_ids', [])) & kg_ids)
                    kg_cited += cites_kg; retained_kg_cited += candidate['retained'] and cites_kg
        retrieval = [rd['retrieval'] for r in rows for rd in r['evidence_by_round']]
        group = {
            'completed': len(rows), 'expected': expected,
            'score_gain_pct': describe([r['score_improvement_pct'] for r in rows]),
            'test_gain_pct_development_diagnostic': describe([r['test_improvement_pct'] for r in rows]),
            'positive_test_count': sum(r['test_improvement_pct']>0 for r in rows),
            'proposals': len(candidates), 'scored': sum(c['status']=='scored' for c in candidates),
            'retained': sum(c['retained'] for c in candidates),
            'rejection_reasons': dict(Counter(c['reason'] for c in candidates if c['status']=='rejected')),
            'candidates_citing_kg': kg_cited,
            'retained_citing_kg': retained_kg_cited,
            'evidence_lexical_tokens': describe([rd['lexical_tokens'] for rd in retrieval]),
            'graph_paths_per_round': describe([rd['graph_paths'] for rd in retrieval]),
            'tree_transfer_test_gain_pct': {
                key: describe([r['tree_transfer'][key]['test_improvement_pct'] for r in rows])
                for key in ['native14_hgb','all_raw_hgb']},
        }
        group['scientific_checks'] = dict(Counter(c.get('scientific_check',{}).get('target_association','not_evaluated') for c in candidates))
        group['retained_scientific_checks'] = dict(Counter(c.get('scientific_check',{}).get('target_association','not_evaluated') for c in candidates if c['retained']))
        groups[mode] = group
        errors.extend({'mode':mode,'replicate':r['replicate'],'status':r['status'],'error':r.get('error')}
                      for r in all_rows if r['status']!='completed')
    return {'profile':profile,'graph_view':next(iter(views),'paths'),'complete':all(g['completed']==expected for g in groups.values()),
            'expected_replicates_per_mode':expected,'groups':groups,'unfinished_or_failed':errors,
            'interpretation':'Pilot on an already inspected test split. Primary search evidence is scoring improvement; test is diagnostic. Not an independent demonstration of KG superiority.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('--expected',type=int,default=3)
    args=parser.parse_args()
    result=analyze(args.root,args.expected)
    (args.root/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'complete':result['complete'],'counts':{m:g['completed'] for m,g in result['groups'].items()}},ensure_ascii=False))
