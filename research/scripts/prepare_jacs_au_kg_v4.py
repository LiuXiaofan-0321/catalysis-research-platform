"""Prepare source-safe V4 bank and test actual live retrieval before API jobs."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src')]
from catalysis_research.experiments.jacs_au import load_data, make_split, save_json
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v4 import (
    build_bank,audit_bank,load_config,training_domains,scientific_graph,select_evidence,FullIndexEvidence,
)


def prepare(source,output,config_path,data_root,index=None):
    if output.exists(): raise ValueError('New output directory required')
    config=load_config(config_path);bank=build_bank(json.loads(source.read_text(encoding='utf-8')));audit_bank(bank)
    data=load_data(data_root);split=make_split(data);env,_=formula_environment(data,split['train'])
    domains=training_domains(env,split['train']);live=FullIndexEvidence(index,bank) if index else None
    if config['require_live_index'] and not live: raise ValueError('Server full index required for preflight')
    previews=[]
    for question in ['rotational inertia linear single site zero boundary', 'probe accessible volume zero translational entropy', 'bottleneck free sphere included along path cage window']:
        evidence,trace=select_evidence(bank,[{'hypothesis':question,'formula':''}],[],config,live)
        previews.append({'question':question,'retrieval':trace,'context':evidence})
    save_json(output/'bank.json',bank)
    report={'status':'passed','profile':bank['profile'],'eligible_counts':bank['eligible_counts'],
            'live_index_enabled':live is not None,'training_domains':domains,'previews':previews,
            'graph':scientific_graph(bank),'limit':'Unknown source papers require separate review; no guessed conditions or causal mechanisms.'}
    save_json(output/'preflight.json',report)
    print(json.dumps({'status':'passed','profile':bank['profile'],'rag':len(bank['rag']),'mechanisms':len(bank['kg']),
                      'preview_record_counts':[x['retrieval']['items'] for x in previews],'live_index':live is not None}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ['source','output','config','data']:p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--index',type=Path)
    a=p.parse_args();prepare(a.source,a.output,a.config,a.data,a.index)
