"""Audit completed JACS trajectories and export descriptive scientific figures.

No model calls, retraining, selection changes, or significance claims.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import statistics

import numpy as np

MODES = ['agent', 'rag_agent', 'small_kg_rag_agent']
LABELS = ['Agent', 'RAG', 'KG+RAG']


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def describe(values):
    return dict(mean=statistics.mean(values), std=statistics.stdev(values),
                min=min(values), max=max(values))


def elapsed_seconds(value):
    days, rest = value.split('-') if '-' in value else ('0', value)
    h, m, s = map(int, rest.split(':'))
    return int(days)*86400+h*3600+m*60+s


def analyze(root, jobs=None, data=None):
    root=Path(root)
    raw=read(root/'summary.json')
    baseline=read(root/'baseline/baseline.json')
    assert raw['complete'] and baseline['status']=='completed'
    groups={}; records=[]; controls=None; checks=0
    for mode in MODES:
        rs=[read(p) for p in sorted((root/'discovery').glob(mode+'-replicate-*.json'))]
        assert len(rs)==10 and {r['replicate'] for r in rs}==set(range(1,11))
        for r in rs:
            assert r['status']=='completed' and r['mode']==mode and len(r['rounds'])==3
            current=r['d0_score_mae_R']
            retained=[]
            for j,rd in enumerate(r['rounds'],1):
                assert rd['round']==j and len(rd['candidates'])==3
                assert abs(rd['before_mae_R']-current)<1e-8
                scored=[c for c in rd['candidates'] if c['status']=='scored']
                assert all(c['status'] in {'scored','rejected'} for c in rd['candidates'])
                expected=min([current]+[c['score']['mae_R'] for c in scored])
                assert abs(rd['after_mae_R']-expected)<1e-8
                winners=[c for c in rd['candidates'] if c['retained']]
                assert len(winners)==int(expected<current-1e-10)
                if winners:
                    assert abs(winners[0]['score']['mae_R']-expected)<1e-8
                    assert rd['retained_formula']==winners[0]['formula']
                    retained.append(winners[0]['formula'])
                else:
                    assert rd['retained_formula'] is None
                current=rd['after_mae_R']; checks+=1
            assert retained==[c['formula'] for c in r['retained']]
            assert abs(r['score_improvement_pct']-100*(r['d0_score_mae_R']-current)/r['d0_score_mae_R'])<1e-8
            assert abs(r['test_improvement_pct']-100*(r['test']['d0']['mae_R']-r['test']['selected']['mae_R'])/r['test']['d0']['mae_R'])<1e-8
            reference={k:r['test'][k] for k in ['d0','all_raw_ann','native14_hgb','all_raw_hgb']}
            if controls is None: controls=reference
            assert reference==controls
        candidates=[c for r in rs for rd in r['rounds'] for c in rd['candidates']]
        selected=[c for c in candidates if c['retained']]
        bundle=read(root/'evidence'/(mode+'.json'))
        kg_ids={f'E{i+1:02d}' for i,item in enumerate(bundle['items']) if 'kg' in item['retrieval_channels']}
        best=max(rs,key=lambda r:r['score_improvement_pct'])
        group={
            'n':len(rs), 'score_gain_pct':describe([r['score_improvement_pct'] for r in rs]),
            'test_gain_pct':describe([r['test_improvement_pct'] for r in rs]),
            'selected_test_mae_R':describe([r['test']['selected']['mae_R'] for r in rs]),
            'all_raw_plus_selected_test_mae_R':describe([r['all_raw_plus_selected']['test']['mae_R'] for r in rs]),
            'all_raw_ann_test_gain_pct':describe([100*(r['test']['all_raw_ann']['mae_R']-r['all_raw_plus_selected']['test']['mae_R'])/r['test']['all_raw_ann']['mae_R'] for r in rs]),
            'positive_test':sum(r['test_improvement_pct']>0 for r in rs),
            'positive_all_raw_test':sum(r['all_raw_plus_selected']['test']['mae_R']<r['test']['all_raw_ann']['mae_R'] for r in rs),
            'selected_beats_all_raw_hgb':sum(r['test']['selected']['mae_R']<r['test']['all_raw_hgb']['mae_R'] for r in rs),
            'all_raw_selected_beats_all_raw_hgb':sum(r['all_raw_plus_selected']['test']['mae_R']<r['test']['all_raw_hgb']['mae_R'] for r in rs),
            'round_mean_score_gain_pct':[statistics.mean(100*(r['d0_score_mae_R']-r['rounds'][j]['after_mae_R'])/r['d0_score_mae_R'] for r in rs) for j in range(3)],
            'round_retained':[sum(r['rounds'][j]['retained_formula'] is not None for r in rs) for j in range(3)],
            'proposals':len(candidates), 'scored':sum(c['status']=='scored' for c in candidates),
            'retained':len(selected), 'rejection_reasons':dict(Counter(c['reason'] for c in candidates if c['status']=='rejected')),
            'retained_self_reported_novelty':dict(Counter(c['novelty_status'] for c in selected)),
            'distinct_syntactic_formulas':len({ast.dump(ast.parse(c['formula'],mode='eval'),include_attributes=False) for c in candidates}),
            'evidence_items':len(bundle['items']), 'evidence_tokens':bundle['selected_token_count'],
            'kg_evidence_items':len(kg_ids),
            'proposals_citing_kg':sum(bool(set(c.get('evidence_ids',[]))&kg_ids) for c in candidates),
            'retained_citing_kg':sum(bool(set(c.get('evidence_ids',[]))&kg_ids) for c in selected),
            'representative_by_score':{'replicate':best['replicate'], 'score_gain_pct':best['score_improvement_pct'],
                 'test_gain_pct':best['test_improvement_pct'], 'retained':best['retained']},
        }
        for key, original in [('score_gain_pct','score_improvement_pct'),('test_gain_pct','test_improvement_pct')]:
            assert abs(group[key]['mean']-raw['groups'][mode][original]['mean'])<1e-8
        groups[mode]=group; records.extend(rs)
    validation={'complete_trajectories':30,'checked_rounds':checks,'native_control_metrics_recomputed':False}
    if data:
        p=Path(data)/'s_ads/training_model'
        x=np.load(p/'X_15.npy',allow_pickle=False)
        y=np.load(p/'y_15.npy',allow_pickle=False)
        split=read(root/'baseline/split.json')
        for name, key in [('native14_ann','d0'),('all_raw_ann','all_raw_ann'),('native14_hgb','native14_hgb'),('all_raw_hgb','all_raw_hgb')]:
            pred=np.load(root/'baseline'/(name+'.npy'),allow_pickle=False)
            for part in ['score','test']:
                idx=np.array(split[part],dtype=int)
                mae=float(np.mean(np.abs((1-pred[idx])*x[idx,14]+y[idx,1])))
                expected=baseline['controls'][name]['score']['mae_R'] if part=='score' else controls[key]['mae_R']
                assert abs(mae-expected)<1e-8
        validation['native_control_metrics_recomputed']=True
    execution={}
    if jobs:
        lines=Path(jobs).read_text(encoding='utf-8').strip().splitlines()
        rows=[dict(zip(lines[0].split('|'),line.split('|'))) for line in lines[1:]]
        by_id={r['JobID']:r for r in rows}
        durations=[]
        for r in records:
            task=(r['replicate']-1)*3+MODES.index(r['mode'])
            sec=elapsed_seconds(by_id[f'3827004_{task}']['Elapsed'])
            if r.get('recovery'):sec+=elapsed_seconds(by_id['3827582']['Elapsed'])
            durations.append(sec)
        starts=[by_id[f'3827004_{i}']['Start'] for i in range(30)]
        execution={'first_array_start':min(starts),'discovery_finished':by_id['3827582']['End'],
                   'summary_finished':by_id['3827005']['End'], 'sum_trajectory_allocated_seconds_including_failed_attempt':sum(durations),
                   'per_trajectory_allocated_seconds':describe(durations),
                   'note':'Slurm allocated duration includes imports/recovery; raw RAG replicate 2 seconds counts only resumed stage.'}
    result={'validation':validation,'controls_test':controls,'baseline_score':baseline['controls'],
            'groups':groups,'execution':execution,
            'limitations':['One fixed row split and one fit seed; error bars describe LLM variation, not independent scientific tasks.',
                'All formulas require scientific meaning, units and literature novelty review.',
                'No intermediates were evaluated on test; round curves are scoring results only.',
                'RAG and KG+RAG share a maximum budget, but consumed different token counts.']}
    (root/'analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def figures(result,directory):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    colors=['#386CB0','#E59D2C','#2A927E']
    fig,axs=plt.subplots(1,2,figsize=(10.8,4.2),layout='constrained')
    for ax,field,title in zip(axs,['score_gain_pct','test_gain_pct'],['Adaptive scoring gain','Held-out test gain']):
        vals=[result['groups'][m][field] for m in MODES]
        ax.bar(LABELS,[v['mean'] for v in vals],yerr=[v['std'] for v in vals],capsize=4,color=colors,alpha=.9)
        ax.axhline(0,color='#555555',lw=.8);ax.set_ylabel('MAE reduction versus D0 (%)');ax.set_title(title)
        ax.set_ylim(-.5,10)
        for i,v in enumerate(vals):ax.text(i,v['mean']+v['std']+.25,f"{v['mean']:.2f}%",ha='center')
    fig.suptitle('JACS Au pilot: 10 LLM trajectories per condition; error bars = SD')
    fig.savefig(directory/'jacs_au_gains.png',dpi=220);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(11,4.4),layout='constrained')
    for m,label,color in zip(MODES,LABELS,colors):
        axs[0].plot([0,1,2,3],[0]+result['groups'][m]['round_mean_score_gain_pct'],marker='o',label=label,color=color)
    axs[0].set(xlabel='Completed proposal rounds',ylabel='Mean scoring MAE reduction (%)',title='Round progression (scoring only)')
    axs[0].set_xticks([0,1,2,3]);axs[0].legend(frameon=False)
    names=['D0 ANN','All-input ANN','D0 HGB','All-input HGB']+LABELS
    vals=[result['controls_test'][k]['mae_R'] for k in ['d0','all_raw_ann','native14_hgb','all_raw_hgb']]+[result['groups'][m]['selected_test_mae_R']['mean'] for m in MODES]
    axs[1].barh(names,vals,color=['#ACB5BC']*4+colors)
    axs[1].invert_yaxis();axs[1].set(xlabel='Held-out test MAE (R), lower is better',title='Predictor and input controls',xlim=(0,.7))
    for i,v in enumerate(vals):axs[1].text(v+.008,i,f'{v:.4f}',va='center')
    fig.savefig(directory/'jacs_au_rounds_controls.png',dpi=220);plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('root',type=Path);parser.add_argument('--jobs',type=Path)
    parser.add_argument('--data',type=Path);parser.add_argument('--figures',type=Path)
    args=parser.parse_args();result=analyze(args.root,args.jobs,args.data)
    if args.figures:figures(result,args.figures)
    print(json.dumps({'validation':result['validation'],'execution':result['execution'],
                     'groups':{m:{k:v for k,v in g.items() if k in ['retained','positive_all_raw_test','proposals_citing_kg','retained_citing_kg']} for m,g in result['groups'].items()}},ensure_ascii=False,indent=2))
