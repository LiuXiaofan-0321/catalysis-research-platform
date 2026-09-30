"""Summarize both effort conditions without using desired ranking as a filter."""
import argparse
from collections import Counter
import json
from pathlib import Path
import statistics


def describe(v):
    return {'n':len(v),'mean':statistics.mean(v) if v else None,'std':statistics.stdev(v) if len(v)>1 else None,
            'min':min(v) if v else None,'max':max(v) if v else None}


def summarize(root,expected=3):
    groups={};failures=[]
    for effort in ['low','high']:
        groups[effort]={}
        for mode in ['agent','rag_agent','small_kg_rag_agent']:
            records=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((root/effort/'discovery').glob(mode+'-replicate-*.json'))]
            rows=[r for r in records if r['status']=='completed']
            for r in records:
                if r['knowledge_profile']!='jacs-au-kg-v4' or r['reasoning_effort']!=effort or r.get('execution_revision')!='explicit-normalization-20260930c':raise ValueError('Wrong profile/effort/execution contract')
                if r['status']!='completed':failures.append({'effort':effort,'mode':mode,'replicate':r['replicate'],'error':r.get('error'),'status':r['status']})
            for r in rows:
                if len(r['rounds'])!=3:raise ValueError('Incomplete completed trajectory')
                current=r['d0_score_mae_R']
                for rd in r['rounds']:
                    if len(rd['candidates'])!=3:raise ValueError('Wrong scoring slots')
                    best=min([current]+[c['score']['mae_R'] for c in rd['candidates'] if c['status']=='scored'])
                    if abs(rd['before_mae_R']-current)>1e-8 or abs(rd['after_mae_R']-best)>1e-8:raise ValueError('Wrong winner selection')
                    if sum(c['retained'] for c in rd['candidates'])!=int(best<current-1e-10):raise ValueError('Wrong retention count')
                    current=best
            cs=[c for r in rows for rd in r['rounds'] for c in rd['candidates']]
            stages=[s for r in rows for rd in r['rounds'] for s in rd['generation_events']]
            groups[effort][mode]={'completed':len(rows),'expected':expected,'score_gain_pct':describe([r['score_improvement_pct'] for r in rows]),
                'test_gain_pct_development_diagnostic':describe([r['test_improvement_pct'] for r in rows]),
                'initial_draft_passed':sum(c['status']=='passed' for r in rows for rd in r['rounds'] for c in rd['blind_checks']),
                'post_review_passed':sum(c['status']=='passed' for r in rows for rd in r['rounds'] for c in rd['reviewed_checks']),
                'final_scored':sum(c['status']=='scored' for c in cs),'proposals':len(cs),'retained':sum(c['retained'] for c in cs),
                'repair_batches':sum(s['stage']=='pre_fit_repair' for s in stages),'rejection_reasons':dict(Counter(c['reason'] for c in cs if c['status']=='rejected')),
                'retained_scientific_checks':dict(Counter(c['scientific_check']['target_association'] for c in cs if c['retained'])),
                'api_tokens':{k:sum(r['api_usage_totals'][k] for r in rows) for k in ('prompt_tokens','completion_tokens','reasoning_tokens','total_tokens')},
                'api_calls':sum(r['api_calls'] for r in rows),'trajectory_seconds':describe([r['seconds'] for r in rows]),
                'tree_transfer_test_gain_pct':{k:describe([r['tree_transfer'][k]['test_improvement_pct'] for r in rows]) for k in ('native14_hgb','all_raw_hgb')}}
    complete=all(g['completed']==expected for gs in groups.values() for g in gs.values()) and not failures
    result={'profile':'jacs-au-kg-v4','complete':complete,'groups':groups,'unfinished_or_failed':failures,
            'rankings':{e:sorted(gs,key=lambda m:-(gs[m]['score_gain_pct']['mean'] or 0)) for e,gs in groups.items()},
            'interpretation':'Development low/high comparison; same split/fit seed. Ranking is observed, not forced; no independent mechanism/generalization claim.'}
    (root/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'complete':complete,'completed':{e:{m:g['completed'] for m,g in gs.items()} for e,gs in groups.items()}}))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--expected',type=int,default=3)
    a=p.parse_args();summarize(a.root,a.expected)
