import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json, glob, csv, collections, statistics
F = _REPO + '/docs/experiments/zeosyn_v2_forensics'
sys.path.insert(0, F)
from families import family
RUN = _REPO + '/results/zeosyn_direct_v1_local_20261008'
evals = {}
for fn in glob.glob(RUN + '/evaluation/*-replicate-*.json'):
    e = json.load(open(fn)); evals[(e['mode'], e['replicate'])] = e
rows = []
for fn in sorted(glob.glob(RUN + '/generation/*.json')):
    g = json.load(open(fn)); e = evals[(g['mode'], g['replicate'])]
    for s in g['slots']:
        c = s.get('candidate') or {}
        repaired = any(a['kind'] == 'technical_repair' for a in s['attempts'])
        errs = [a.get('error') for a in s['attempts'] if a.get('error')]
        rows.append(dict(group=g['mode'], traj=g['replicate'], round=s['round'], name=c.get('name'), formula=c.get('formula'),
                         family=family(c.get('formula')), evidence_items=s.get('evidence_items'), evidence_ids=' '.join(map(str, c.get('evidence_ids', []))) or '-',
                         knowledge_source=c.get('knowledge_source'), novelty=c.get('novelty'),
                         status='failed' if s['status'] != 'appended' else ('repaired' if repaired else 'accepted'), repair_error='; '.join(errs),
                         traj_delta_acc_pp=round(100 * e['delta']['mean']['accuracy'], 3), traj_delta_bacc_pp=round(100 * e['delta']['mean']['balanced_accuracy'], 3),
                         traj_delta_f1_pp=round(100 * e['delta']['mean']['macro_f1'], 3)))
with open(F + '/slots_v1.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('wrote', len(rows), 'rows to slots_v1.csv; statuses', collections.Counter(r['status'] for r in rows))
print('\n=== V1 SLOTS (group traj round | family | formula | cites | traj d-acc) ===')
for r in rows:
    print(f"{r['group']:18s} r{r['traj']:<2d} R{r['round']} | {r['family']:30s} | {r['formula'][:75]:75s} | cite={r['evidence_ids'][:12]:12s} | {r['traj_delta_acc_pp']:+.2f}")
print('\n=== V1 FAMILY COUNTS BY GROUP ===')
fam = collections.defaultdict(collections.Counter)
for r in rows: fam[r['group']][r['family']] += 1
allf = sorted({f for g in fam for f in fam[g]})
print(f"{'family':32s}" + ''.join(f'{g:>20s}' for g in fam) + '   total')
for f in allf: print(f"{f:32s}" + ''.join(f'{fam[g][f]:20d}' for g in fam) + f"{sum(fam[g][f] for g in fam):8d}")
print('\n=== V1 FAMILY BY ROUND ===')
fr = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for r in rows: fr[r['round']][r['group']][r['family']] += 1
for rd in sorted(fr):
    for g in fr[rd]: print(rd, g, dict(fr[rd][g].most_common()))
print('\n=== V1 PER-TRAJECTORY DELTAS ===')
for g in fam:
    d = [100 * evals[(g, r)]['delta']['mean']['accuracy'] for r in range(1, 11)]
    print(g, ' '.join(f'{x:+.2f}' for x in d), f'| mean {statistics.mean(d):+.3f} sd {statistics.stdev(d):.3f}')
print('\n=== V1 knowledge_source / novelty by group ===')
for g in fam:
    rs = [r for r in rows if r['group'] == g]
    print(g, dict(collections.Counter(r['knowledge_source'] for r in rs)), dict(collections.Counter(r['novelty'] for r in rs)), 'citing', sum(r['evidence_ids'] != '-' for r in rs))
