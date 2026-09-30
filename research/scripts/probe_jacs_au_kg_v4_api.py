"""Validate both effort payloads on a compute node, without logging credentials."""
import argparse
import ast
import json
from pathlib import Path
import time
from catalysis_research.experiments.jacs_au_kg_v4 import load_config
from catalysis_research.models.glm import GlmClient
from run_jacs_au_kg_v4 import apply_patches, patch_schema


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();c=load_config(a.config);start=time.monotonic()
    client=GlmClient(timeout_seconds=c['api_timeout_seconds'],retries=0)
    response=client.chat_json(
        model=c['model'],thinking=c['thinking'],reasoning_effort=c['reasoning_effort'],temperature=c['temperature'],
        max_tokens=c['generation']['max_tokens'],system='Return JSON only.',
        user='Return a JSON object with ok set to true. This is a connectivity probe; a short response is sufficient.')
    report={'ok':response.structured.get('ok') is True,'model':response.model,
        'reasoning_effort_requested':c['reasoning_effort'],'max_tokens_requested':c['generation']['max_tokens'],
        'client_timeout_seconds':c['api_timeout_seconds'],'finish_reason':response.raw['choices'][0].get('finish_reason'),
        'usage':response.usage,'seconds':time.monotonic()-start,
        'effort_verification':'Requested payload accepted; provider internal effort cannot be independently measured.'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not report['ok'] or report['model']!=c['model'] or report['finish_reason']!='stop':
        raise RuntimeError('Compute-node GLM effort probe failed')
    examples=[]
    for i,family in enumerate(['translation','shape','rotation'],1):
        examples.append({'slot_id':'h'+str(i),'name':'contract_probe','formula':'log(1+q_Vol)',
            'hypothesis':'Illustrative fixed hypothesis '+str(i),'rationale':'Contract probe only',
            'falsification_criteria':'Not a scientific result','novelty_status':'uncertain','evidence_ids':[],
            'physical_claims':['empirical_proxy'],'variable_mappings':{'Vol':'molecular_vdw_volume'},
            'scientific_test':{'mechanism_family':family,'proxy_assumptions':'Probe only',
                'physical_interpretation':'Native volume proxy','boundary_behavior':'Finite at zero',
                'vary_input':'Vol','descriptor_direction':'increasing','regime_input':'Vol',
                'regime_train_quantiles':[0.,1.],'entropy_direction':'increasing'}})
    patched=client.chat_json(model=c['model'],thinking=c['thinking'],reasoning_effort=c['reasoning_effort'],
        temperature=c['temperature'],max_tokens=c['generation']['max_tokens'],system='Return JSON only.',
        user=json.dumps({'task':'Return partial updates only: change h1 formula to log(1+q_Vol**2); keep h2/h3 exactly unchanged. Do not repeat or modify hypotheses or test declarations.',
            'candidates':examples,'schema':patch_schema(['h1','h2','h3'],strict=True)}))
    final=apply_patches(examples,patched.structured,['h1','h2','h3'],strict=True)
    if ast.dump(ast.parse(final[0]['formula'],mode='eval'))!=ast.dump(ast.parse('log(1+q_Vol**2)',mode='eval')) or final[1:]!=examples[1:]:raise RuntimeError('Partial-update compute probe failed')
    report['partial_update_contract']={'status':'passed','model':patched.model,'usage':patched.usage,
        'finish_reason':patched.raw['choices'][0].get('finish_reason')}
    if patched.model!=c['model'] or report['partial_update_contract']['finish_reason']!='stop':raise RuntimeError('Wrong partial probe model/finish')
    report['seconds']=time.monotonic()-start
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
