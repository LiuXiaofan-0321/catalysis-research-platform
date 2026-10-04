"""One high connectivity request on a compute node; no scientific candidate."""
import argparse
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from catalysis_research.experiments.jacs_au import save_json
from catalysis_research.experiments.jacs_au_direct import load_config
from catalysis_research.models.glm import GlmClient


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists(): raise ValueError('Preserve existing connectivity record')
    c=load_config(a.config); start=time.monotonic()
    client=GlmClient(timeout_seconds=c['api_timeout_seconds'],retries=0)
    try:
        r=client.chat_json(model=c['model'],thinking=c['thinking'],reasoning_effort=c['reasoning_effort'],
            temperature=c['temperature'],max_tokens=c['generation']['max_tokens'],
            system='Return ONE JSON object.',user='Connectivity probe only. Return {"ok":true}; no scientific hypotheses or descriptors. A short answer is sufficient.')
        choice=r.raw['choices'][0]
        passed=r.structured.get('ok') is True and r.model==c['model'] and choice.get('finish_reason')=='stop'
        report={'status':'passed' if passed else 'failed','model':r.model,'reasoning_effort_requested':c['reasoning_effort'],
            'max_tokens_requested':c['generation']['max_tokens'],'client_timeout_seconds':c['api_timeout_seconds'],
            'response_id':r.raw.get('id'),'request_ids':r.raw.get('_response_request_ids',{}),
            'finish_reason':choice.get('finish_reason'),'usage':r.usage,'raw_content':choice['message']['content'],
            'api_calls':1,'scientific_candidates':0,'seconds':time.monotonic()-start,
            'effort_verification':'Payload accepted; internal provider reasoning effort is not independently observable'}
    except Exception as error:
        message=str(error).replace(client.api_key,'[redacted]')
        report={'status':'failed','reason':message,'api_calls':1,'scientific_candidates':0,'seconds':time.monotonic()-start}
        save_json(a.output,report); raise RuntimeError('Compute-node API probe failed; inspect sanitized report') from None
    save_json(a.output,report)
    if not passed: raise RuntimeError('Unexpected compute-node API response')
    print('Compute-node high API probe passed',flush=True)


if __name__=='__main__': main()
