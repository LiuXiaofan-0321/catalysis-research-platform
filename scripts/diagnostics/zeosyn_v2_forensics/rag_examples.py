import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import json
F = _REPO + '/docs/experiments/zeosyn_v2_forensics'
RUN = _REPO + '/results/zeosyn_direct_v1_local_20261008'
k = json.load(open(RUN + '/prepared/knowledge.json'))
out = []
for mode in ('rag_agent', 'small_kg_rag_agent'):
    for b in k['bundles'][mode]:
        out.append(f"########## V1 {mode} | query: {b['query']} | items {b['selected_count']} tokens {b['selected_token_count']}\n")
        for it in b['items']:
            keys = {kk: it[kk] for kk in it if kk not in ('quote', 'text')}
            out.append(f"--- item fields: {json.dumps({kk: (str(v)[:80]) for kk, v in keys.items()}, ensure_ascii=False)}\n")
            out.append((it.get('quote') or it.get('text') or '')[:3000] + '\n')
        out.append('\n=== CONTEXT STRING AS SHOWN (first 2500 chars) ===\n' + b['context'][:2500] + '\n\n')
open(F + '/v1_rag_bundles.txt', 'w').write(''.join(out))
# print a compact view: for rag_agent bundle 1 (round 1) the first 4 items with section + quote (600 chars)
for mode in ('rag_agent', 'small_kg_rag_agent'):
    b = k['bundles'][mode][1]
    print(f"===== V1 {mode} round-2 bundle | query: {b['query']} | items {b['selected_count']} =====")
    for it in b['items'][:10]:
        print(f"[{it.get('rank', '?')}] paper={it.get('paper_id')} record={it.get('record_id')} section={it.get('section') or it.get('locator') or ''} type={it.get('source_type') or it.get('knowledge_mode') or ''}")
        print('   QUOTE:', (it.get('quote') or '')[:500].replace('\n', ' '))
    print()
print('item keys example:', list(k['bundles']['rag_agent'][0]['items'][0].keys()))
print('\nCONTEXT (rag_agent round 1, first 1800 chars):\n', k['bundles']['rag_agent'][0]['context'][:1800])
