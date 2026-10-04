"""Summarize all 54 faithful blocks without constructing a counterfactual rollout."""
from collections import defaultdict
import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from catalysis_research.experiments.jacs_au import save_json


def summarize(directory, manifest):
    expected={b['block_id'] for b in manifest['blocks']}
    loaded=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(directory.glob('*.json'))]
    if len(loaded)!=54 or {b['block_id'] for b in loaded}!=expected:
        raise ValueError('Exactly all 54 historical blocks required')
    if any(b['status']!='completed' for b in loaded): raise ValueError('Incomplete fits retained; do not issue complete result')
    groups=defaultdict(list); rows=[]
    source=ROOT/'reports/jacs_au_kg_v4_20260930/complete-server-results'
    blocks={b['block_id']:b for b in manifest['blocks']}
    for b in loaded:
        effort,mode,rep,rd=b['block_id'].split('/')
        groups[effort+'/'+mode].append(b)
        old=json.loads((source/blocks[b['block_id']]['source_identity']).read_text(encoding='utf-8'))
        d0=old['d0_score_mae_R']
        stage={k:{c['slot_id']:c for c in v['candidates']} for k,v in b['stages'].items()}
        for slot in ('h1','h2','h3'):
            row={'candidate_id':b['block_id']+'/'+slot,'effort':effort,'mode':mode,
                 'replicate':int(rep.split('-')[-1]),'round':int(rd.split('-')[-1]),
                 'd0_score_mae_R':d0,'fixed_prefix_score_mae_R':b['prefix_score']['mae_R']}
            for stage_name,label in [('blind_drafts','blind'),('reviewed_candidates','review'),('final_candidates','final')]:
                c=stage[stage_name][slot]
                row.update({label+'_formula':c['formula'],label+'_status':c['status'],
                            label+'_mae_R':c.get('score',{}).get('mae_R'),label+'_reason':c.get('reason')})
            row['paired_final_minus_blind_pp']=100*(row['blind_mae_R']-row['final_mae_R'])/d0 if row['blind_status']==row['final_status']=='scored' else None
            row['paired_review_minus_blind_pp']=100*(row['blind_mae_R']-row['review_mae_R'])/d0 if row['blind_status']==row['review_status']=='scored' else None
            rows.append(row)
    results={}
    for key,bs in groups.items():
        match=[r['paired_final_minus_blind_pp'] for r in rows if r['effort']+'/'+r['mode']==key and r['paired_final_minus_blind_pp'] is not None]
        transitions=defaultdict(int)
        for r in rows:
            if r['effort']+'/'+r['mode']==key: transitions[r['blind_status']+'->'+r['final_status']]+=1
        trace=defaultdict(list)
        for b in bs: trace[b['block_id'].rsplit('/',1)[0]].append(b['final_minus_blind_pp'])
        results[key]={'blocks':len(bs),'origin_trajectories':len(trace),
            'mean_local_stage_best_final_minus_blind_pp':float(np.mean([b['final_minus_blind_pp'] for b in bs])),
            'positive_blocks':sum(b['final_minus_blind_pp']>1e-10 for b in bs),
            'negative_blocks':sum(b['final_minus_blind_pp']< -1e-10 for b in bs),
            'paired_scored_slots':len(match),'paired_slot_mean_pp_conditional_on_both_scored':float(np.mean(match)) if match else None,
            'status_transitions':dict(transitions),
            'origin_trace_means_of_local_differences_pp':{k:float(np.mean(v)) for k,v in trace.items()}}
    result={'protocol':'all-fixed-stage-replay-summary-v1','status':'completed',
        'blocks':54,'candidate_slots':len(rows),'api_calls':0,'fit_calls':sum(b['fit_calls'] for b in loaded),
        'max_abs_prefix_replay_delta_R':max(abs(b['prefix_replay_delta_R']) for b in loaded),
        'max_abs_final_replay_delta_R':max(abs(b['final_replay_delta_R']) for b in loaded),
        'groups':results,'limits':['Local effects on historical prefixes, not whole new trajectories.',
            'Do not sum local gains into a hypothetical new final result or rank methods by these differences.',
            'Paired slot statistics condition on both stages being executable; all rejected slots/statuses also retained.',
            '54 blocks are nested in 18 source trajectories; no candidate-level independent-sample claim.',
            'Faithful V4 metadata rejection preserved; numeric-only diagnostic not yet run.']}
    return result,rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('blocks','manifest','output'): p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args()
    if a.output.exists(): raise ValueError('New summary directory required')
    result,rows=summarize(a.blocks,json.loads(a.manifest.read_text(encoding='utf-8')))
    a.output.mkdir(parents=True)
    save_json(a.output/'summary.json',result); save_json(a.output/'paired-slots.json',rows)
    with (a.output/'paired-slots.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({k:result[k] for k in ('status','blocks','candidate_slots','fit_calls','max_abs_final_replay_delta_R')}))
