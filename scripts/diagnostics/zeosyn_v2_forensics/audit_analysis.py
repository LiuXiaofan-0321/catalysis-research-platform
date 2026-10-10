import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import json, glob, collections, random
RUN = _REPO + '/results/zeosyn_v2_dev_1'
a = json.load(open(RUN + '/retrieval-audit.json'))
# where do the 30 audit queries come from?
qsrc = collections.defaultdict(set); allq = []
for fn in sorted(glob.glob(RUN + '/generation/*.json')):
    g = json.load(open(fn))
    for s in g['slots']:
        for q in (s.get('plan') or {}).get('queries', []):
            qsrc[q].add(g['mode']); allq.append(q)
print('distinct model-written queries in the run:', len(set(allq)), 'of', len(allq), 'total; by group:',
      {m: len({q for q in qsrc if m in qsrc[q]}) for m in ('rag', 'kg', 'kg_shuffled', 'agent')})
print('audit sample of 30: origin groups', collections.Counter(tuple(sorted(qsrc[q])) for q in a['queries']))
for mode in ('kg', 'rag'):
    st = a['modes'][mode]
    J = st['judgements']
    print(f"\n=== {mode}: items {st['items']} relevant_rate {st['relevant_rate']:.3f} target {st['target']} passed {st['passed']} empty_queries {st['empty_queries']} ===")
    per_q = collections.defaultdict(lambda: [0, 0])
    for j in J: per_q[j['query']][0] += 1; per_q[j['query']][1] += j['relevant']
    nitems = [per_q[q][0] for q in a['queries']]
    print('items per query: mean', round(sum(nitems) / 30, 2), 'distribution', collections.Counter(nitems))
    print('queries with 0 items:', [q for q in a['queries'] if per_q[q][0] == 0])
    if mode == 'kg':
        bytype = collections.defaultdict(lambda: [0, 0])
        for j in J:
            t = j['key'].split(':')[0]; bytype[t][0] += 1; bytype[t][1] += j['relevant']
        print('relevance by KG fact type:', {t: f'{v[1]}/{v[0]}' for t, v in bytype.items()})
        bykey = collections.defaultdict(lambda: [0, 0])
        for j in J: bykey[j['key']][0] += 1; bykey[j['key']][1] += j['relevant']
        print('per key (n judged, n relevant):', sorted(((k, v[0], v[1]) for k, v in bykey.items()), key=lambda x: -x[1]))
    print('per query (items, relevant):')
    for q in a['queries']: print(f'   {per_q[q][1]}/{per_q[q][0]}  {q}')
    fr = [j for j in J if any(x.get('kind') == 'format_repair' for x in j['attempts'])]
    print('judgements needing a format repair:', len(fr))
