"""Summarize all completed and failed trajectories without positive-only filtering."""
import argparse
import json
from pathlib import Path
import statistics


def summarize(root):
    root=Path(root); groups={}
    for mode in ['agent','rag_agent','small_kg_rag_agent']:
        records=[json.loads(p.read_text()) for p in sorted((root/'discovery').glob(mode+'-replicate-*.json'))]
        done=[r for r in records if r['status']=='completed']
        group={'found':len(records),'expected':10,'completed':len(done),
               'failed':[{'replicate':r['replicate'],'error':r.get('error')} for r in records if r['status']=='failed'],
               'unfinished':[r['replicate'] for r in records if r['status']=='running']}
        if done:
            for field in ['score_improvement_pct','test_improvement_pct','seconds']:
                vals=[r[field] for r in done]
                group[field]={'mean':statistics.mean(vals),'std':statistics.stdev(vals) if len(vals)>1 else None,
                              'min':min(vals),'max':max(vals)}
            vals=[100*(r['test']['all_raw_ann']['mae_R']-r['all_raw_plus_selected']['test']['mae_R'])/r['test']['all_raw_ann']['mae_R'] for r in done]
            group['all_raw_test_improvement_pct']={'mean':statistics.mean(vals),'min':min(vals),'max':max(vals)}
            candidates=[c for r in done for rd in r['rounds'] for c in rd['candidates']]
            group['proposals']={'total':len(candidates),'scored':sum(c['status']=='scored' for c in candidates),
                                'rejected':sum(c['status']=='rejected' for c in candidates),
                                'retained':sum(c['retained'] for c in candidates)}
            group['positive_test_trajectories']=sum(r['test_improvement_pct']>0 for r in done)
        groups[mode]=group
    result={'groups':groups,'complete':all(g['completed']==10 for g in groups.values()),
      'limitations':['All repeats share one fixed row split and fit seed; no independent-task significance claim.',
                     'Scoring improvement is adaptively selected; test and all-raw-control improvements may be negative.',
                     'All retained hypotheses require literature novelty and mechanism validation.',
                     'Unseen molecule/framework group generalization remains future work.']}
    (root/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('run_root',type=Path)
    summarize(parser.parse_args().run_root)
