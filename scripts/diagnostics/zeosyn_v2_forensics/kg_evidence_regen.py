"""Regenerate the KG evidence text each kg / kg_shuffled slot saw, verify by the stored context_sha256 and
propose_prompt_sha256, dump everything verbatim, and cross-check the retrieval audit keys."""
import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json, glob, hashlib, collections
ROOT = _REPO
sys.path[:0] = [ROOT + '/src', ROOT + '/scripts', ROOT + '/literature_pipeline/src']
import run_zeosyn_v2 as rz
from catalysis_research.discovery import zeosyn_v2 as v2, zeosyn_direct as v1
F = _REPO + '/docs/experiments/zeosyn_v2_forensics'
RUN = ROOT + '/results/zeosyn_v2_dev_1'
split = rz.load_split(RUN)
cfg = v2.load_config(RUN + '/prepared/config.json')
kg = rz.load_kg_artifacts()
engines = {'kg': rz.kg_engine(split, kg, shuffled=False, seed=None),
           'kg_shuffled': rz.kg_engine(split, kg, shuffled=True, seed=cfg['kg']['shuffle_seed'])}
prov = {m: v2.KgEvidence(engines[m], token_budget=cfg['evidence_token_budget']) for m in engines}
labels_top = v1.frequent_labels({'y': split['y'], 'train': split['train']})
print('engine kg: records after exclusion', len(engines['kg'].records), '| osdas with facts', len(engines['kg'].by_osda),
      '| frameworks', len(engines['kg'].by_framework), '| conditions', {k: len(v) for k, v in engines['kg'].by_condition.items()})
ctx_ok = prompt_ok = n = 0
dump = []
for fn in sorted(glob.glob(RUN + '/generation/kg*-replicate-*.json')):
    g = json.load(open(fn)); history = []
    for s in g['slots']:
        plan = s['plan']
        evd = prov[g['mode']](plan['queries']) if plan['queries'] else {'items': [], 'context': '', 'tokens': 0, 'linking': None}
        h = hashlib.sha256((evd.get('context') or '').encode()).hexdigest()
        prompt = v2.propose_prompt(config=cfg, mode=g['mode'], round_no=s['round'], history=history,
                                   frequent_labels=labels_top, plan=plan, evidence=evd)
        ph = hashlib.sha256(prompt.encode()).hexdigest()
        n += 1; ctx_ok += h == s['evidence']['context_sha256']; prompt_ok += ph == s['propose_prompt_sha256']
        dump.append({'group': g['mode'], 'traj': g['replicate'], 'round': s['round'], 'factor': plan['factor'],
                     'queries': plan['queries'], 'linking': evd.get('linking'), 'context': evd.get('context', ''),
                     'context_sha_match': h == s['evidence']['context_sha256'], 'prompt_sha_match': ph == s['propose_prompt_sha256'],
                     'formula': s['candidate']['formula'], 'evidence_ids': s['candidate']['evidence_ids'],
                     'knowledge_source': s['candidate']['knowledge_source'], 'mechanism': s['candidate']['mechanism']})
        if g['mode'] == 'kg' and g['replicate'] == 1 and s['round'] == 1:
            open(F + '/prompt_kg_r1_round1_propose.txt', 'w').write(prompt)
            pp = v2.plan_prompt(config=cfg, mode='kg', round_no=1, history=[], frequent_labels=labels_top)
            open(F + '/prompt_kg_r1_round1_plan.txt', 'w').write(pp)
            print('plan prompt sha match:', hashlib.sha256(pp.encode()).hexdigest() == s['attempts'][0]['prompt_sha256'])
        history.append(s['candidate'])
print(f'slots checked {n}: context sha256 matches {ctx_ok}/{n}; propose prompt sha256 matches {prompt_ok}/{n}')
json.dump(dump, open(F + '/kg_evidence_v2.json', 'w'), indent=1, ensure_ascii=False)
with open(F + '/kg_evidence_v2.txt', 'w') as fh:
    for d in dump:
        fh.write(f"##### {d['group']} r{d['traj']} round {d['round']} | ctx_match={d['context_sha_match']} prompt_match={d['prompt_sha_match']}\n")
        fh.write(f"factor: {d['factor']}\nqueries: {d['queries']}\nlinking: {d['linking']}\n--- EVIDENCE AS SHOWN ---\n{d['context'] or '(nothing matched the queries)'}\n--- formula: {d['formula']} | cites {d['evidence_ids']} | source {d['knowledge_source']}\n\n")
print('empty-evidence slots:', sum(not d['context'] for d in dump), 'of', len(dump))
# statistics about what the KG said
print('\n=== EVIDENCE CONTEXT EXAMPLES (verbatim) ===')
shown = 0
for d in dump:
    if d['context'] and shown < 7 and d['evidence_ids']:
        print(f"[{d['group']} r{d['traj']} R{d['round']}] queries={d['queries']}\n{d['context']}\n-> formula {d['formula']} cites {d['evidence_ids']} ({d['knowledge_source']})\n")
        shown += 1
# audit cross-check
audit = json.load(open(RUN + '/retrieval-audit.json'))
mism = 0; per = []
for q in audit['queries']:
    keys = [i['key'] for i in prov['kg']([q])['items']]
    jk = [j['key'] for j in audit['modes']['kg']['judgements'] if j['query'] == q]
    per.append((q, keys, jk)); mism += set(keys) != set(jk)
print('\naudit kg queries whose regenerated item keys differ from the audit:', mism, 'of', len(audit['queries']))
print('\n=== WHAT THE KG RETURNED FOR THE 30 AUDIT QUERIES (keys) ===')
for q, keys, jk in per: print(f"{q[:80]:80s} -> {keys}")
