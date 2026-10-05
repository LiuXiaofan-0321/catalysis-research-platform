"""Audit all thirty V5 traces and ninety slots; no new API calls or ANN fits."""
from collections import Counter
from copy import deepcopy
import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'),str(ROOT/'scripts')]
from catalysis_research.experiments.jacs_au import save_json
from catalysis_research.experiments.jacs_au_direct_interface import validate_candidate_with_proxy_adapter
from manage_jacs_au_direct import summarize


def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))


def diagnose(source):
    gs=[read(p) for p in sorted((source/'generation').glob('*.json'))]
    es=[read(p) for p in sorted((source/'evaluation').glob('*.json'))]
    rebuilt=summarize(read(source/'scheduling-tasks.json'),gs,es)
    normalized=json.loads(json.dumps(rebuilt))
    if normalized!=read(source/'summary.json'): raise ValueError('Local all-record summary differs from server')
    evals={(e['mode'],e['replicate']):e for e in es};groups={};slots=[];traces=[]
    pinned=('formula','hypothesis','rationale','falsification_criteria','proxy_assumptions','mechanism_family','physical_prediction')
    for g in gs:
        e=evals[g['mode'],g['replicate']]
        if g['scoring_performed'] or len(g['rounds'])!=3 or g['appended']!=[r['final_candidate'] for r in g['rounds'] if r['appended']]:
            raise ValueError('Frozen unscored direct-append provenance mismatch')
        record={'mode':g['mode'],'replicate':g['replicate'],'mean_gain_pct':e['mean_gain_pct'],
                'input_count':e['input_count'],'successful_additions':e['successful_additions'],
                'fallbacks':e['fallbacks'],'formulas':[c['formula'] for c in g['appended']],
                'mean_within_trace_seed_sd_pp':float(np.std([s['gain_pct'] for s in e['seeds']],ddof=1)),
                'mean_outer_development_gain_pct':float(np.mean([100*(s['d0_outer']['mae_R']-s['outer']['mae_R'])/s['d0_outer']['mae_R'] for s in e['seeds']]))}
        traces.append(record)
        for r in g['rounds']:
            first=r['events'][0]['attempts'][0]; last=r['events'][0]['attempts'][-1]
            old=first.get('response',{}).get('descriptor_candidate',{})
            new=last.get('response',{}).get('descriptor_candidate',{})
            type_problem='proxy_assumptions' in first.get('validation_error','') and isinstance(old.get('proxy_assumptions'),list)
            adapter_status='not_applicable'; adapter_error=None
            if type_problem:
                try:
                    validate_candidate_with_proxy_adapter(first['response']); adapter_status='schema_passed_after_lossless_type_adapter'
                except ValueError as error:
                    adapter_status='other_schema_failure'; adapter_error=str(error)
            changed=[k for k in pinned if k in old and old[k]!=new.get(k)] if len(r['events'][0]['attempts'])>1 else []
            row={'candidate_id':f'{g["mode"]}/replicate-{g["replicate"]}/round-{r["round"]}',
                 'mode':g['mode'],'replicate':g['replicate'],'round':r['round'],'status':r['status'],'appended':r['appended'],
                 'original_proxy_type':type(old.get('proxy_assumptions')).__name__,
                 'initial_formula':old.get('formula'),'final_formula':r.get('final_candidate',{}).get('formula') if r.get('final_candidate') else None,
                 'first_validation_error':first.get('validation_error'),
                 'proposal_failure_reason':r.get('reason'),'draft_precheck':deepcopy(r.get('draft_check')),
                 'final_precheck':deepcopy(r.get('final_check')),'repair_error':r.get('repair_error'),
                 'proxy_list_type_problem':type_problem,'lossless_adapter_schema_status':adapter_status,
                 'lossless_adapter_error':adapter_error,'recovery_changed_pinned_fields':changed,
                 'formula_preserved_in_recovery':old.get('formula')==new.get('formula'),
                 'draft_final_formula_string_equal':r.get('draft_candidate',{}).get('formula')==r.get('final_candidate',{}).get('formula') if r.get('final_candidate') else None,
                 'scientific_issues':r.get('final_check',{}).get('scientific_issues',[]),
                 'citations':r.get('final_candidate',{}).get('evidence_ids',[]) if r.get('final_candidate') else [],
                 'syntax_duplicate_prior_rounds':r.get('syntax_duplicate_prior_rounds',[]),
                 'affine_duplicate_prior_formulas':r.get('affine_duplicate_prior_formulas',[]),
                 'review_issues':deepcopy(r.get('review_issues',[]))}
            if r['appended']:
                for field in ('hypothesis','rationale','falsification_criteria','proxy_assumptions','mechanism_family','physical_prediction'):
                    if r['draft_candidate'][field]!=r['final_candidate'][field]: raise ValueError('Preserved draft scientific field changed')
            slots.append(row)
    for mode in rebuilt['groups']:
        gds=[g for g in gs if g['mode']==mode]; rs=[r for g in gds for r in g['rounds']]
        rows=[r for r in slots if r['mode']==mode];ts=[r for r in traces if r['mode']==mode]
        events=[e for r in rs for e in r['events']];attempts=[a for e in events for a in e['attempts']]
        groups[mode]={'slot_statuses':dict(Counter(r['status'] for r in rs)),
            'proxy_list_type_failures':sum(r['proxy_list_type_problem'] for r in rows),
            'schema_passed_by_lossless_proxy_adapter':sum(r['lossless_adapter_schema_status']=='schema_passed_after_lossless_type_adapter' for r in rows),
            'recovery_only_proxy_field_changed':sum(r['proxy_list_type_problem'] and r['recovery_changed_pinned_fields']==['proxy_assumptions'] for r in rows),
            'negative_final_traces':sum(t['mean_gain_pct']<0 for t in ts),
            'no_addition_traces':sum(t['successful_additions']==0 for t in ts),
            'actual_final_ann_fits':5*sum(t['successful_additions']>0 for t in ts),
            'prediction_fallbacks':sum(t['fallbacks'] for t in ts),
            'mean_outer_development_gain_pct':float(np.mean([t['mean_outer_development_gain_pct'] for t in ts])),
            'mean_within_trace_seed_sd_pp':float(np.mean([t['mean_within_trace_seed_sd_pp'] for t in ts])),
            'per_seed_mean_gains_pct':{str(s):float(np.mean([e['seeds'][i]['gain_pct'] for e in es if e['mode']==mode])) for i,s in enumerate([3,7,11,17,23])},
            'appended_with_scientific_consistency_failed':sum(r['appended'] and r.get('final_check',{}).get('scientific_consistency')=='failed' for r in rs),
            'finish_reasons':dict(Counter(a.get('finish_reason') for a in attempts)),
            'api_calls':sum(e['api_calls'] for e in events),
            'usage_totals':{k:sum(a.get('usage',{}).get(k,0) for a in attempts) for k in ('prompt_tokens','completion_tokens','total_tokens')},
            'cached_input_tokens':sum(a.get('usage',{}).get('prompt_tokens_details',{}).get('cached_tokens',0) for a in attempts),
            'used_native_inputs':dict(Counter(k for g in gds for c in g['appended'] for k in c['variable_mappings'])),
            'within_trace_affine_duplicate_slots':sum(bool(r['affine_duplicate_prior_formulas']) for r in rows)}
    ids=[a.get('response_id') for g in gs for r in g['rounds'] for e in r['events'] for a in e['attempts']]
    diagnostic={'profile':'jacs-au-direct-v5-audit-20261005','status':'completed_all_records_audited',
        'trajectories':len(gs),'evaluated_trajectories':len(es),'candidate_slots':len(slots),
        'all_seed_records':sum(len(e['seeds']) for e in es),'actual_final_ann_fits':sum(g['actual_final_ann_fits'] for g in groups.values()),
        'local_summary_identical_to_server_after_json_key_normalization':True,
        'groups':groups,'distinct_saved_response_ids':len(set(ids)), 'saved_response_ids':len(ids),
        'interface_audit_new_api_calls':0,'interface_audit_new_ann_fits':0,
        'limitations':['Lossless-adapter schema pass is not an execution/physics/ANN score.',
            'Corrected failed slots cannot be inserted into an old trajectory and called a new causal ranking.',
            'All original failures, all seeds and negative gains remain in the primary summary.',
            'Outer data is a previously viewed development diagnostic, not independent validation.']}
    return rebuilt,diagnostic,slots,traces


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists(): raise ValueError('New audit output required')
    summary,diagnostic,slots,traces=diagnose(a.source)
    a.output.mkdir(parents=True)
    for name,value in [('verified-summary',summary),('diagnostic',diagnostic),('all-90-slots',slots),('all-30-traces',traces)]:
        save_json(a.output/(name+'.json'),value)
    print(json.dumps({'status':diagnostic['status'],'actual_final_ann_fits':diagnostic['actual_final_ann_fits'],
        'list_type_failures':sum(g['proxy_list_type_failures'] for g in diagnostic['groups'].values()),
        'list_adapter_schema_passed':sum(g['schema_passed_by_lossless_proxy_adapter'] for g in diagnostic['groups'].values())}))
