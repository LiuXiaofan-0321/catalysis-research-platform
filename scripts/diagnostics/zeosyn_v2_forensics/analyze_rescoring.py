import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json, csv, collections, statistics
F = _REPO + '/docs/experiments/zeosyn_v2_forensics'
sys.path.insert(0, F)
from families import family
R = json.load(open(F + '/single_descriptor_scores.json'))
d0 = R['d0']['per_seed']
print('own D0 per-seed acc:', [round(p['accuracy'], 6) for p in d0])
S = R.get('single', {})
print(f'\n=== SINGLE-DESCRIPTOR RE-SCORING: D0 + one column, 5 seeds, paired vs own D0 ({len(S)} distinct formulas) ===')
items = sorted(S.items(), key=lambda kv: -kv[1]['delta']['mean']['accuracy'])
print('> +0.5 pp accuracy:', [(f, round(100 * v['delta']['mean']['accuracy'], 2)) for f, v in items if v['delta']['mean']['accuracy'] > 0.005])
print('> +0.3 pp accuracy:', [(f[:50], round(100 * v['delta']['mean']['accuracy'], 2)) for f, v in items if v['delta']['mean']['accuracy'] > 0.003])
vals = [100 * v['delta']['mean']['accuracy'] for v in S.values()]
if vals: print(f'distribution of single-descriptor Δacc (pp): mean {statistics.mean(vals):+.3f} sd {statistics.pstdev(vals):.3f} min {min(vals):+.3f} max {max(vals):+.3f}; n>0: {sum(v>0 for v in vals)}/{len(vals)}')
print('\nrank | Δacc | Δbacc | ΔF1 | seeds Δacc | groups | family | formula')
for i, (f, v) in enumerate(items, 1):
    m = v['delta']['mean']; ps = ' '.join(f"{100*p['accuracy']:+.2f}" for p in v['delta']['per_seed'])
    print(f"{i:3d} | {100*m['accuracy']:+.3f} | {100*m['balanced_accuracy']:+.3f} | {100*m['macro_f1']:+.3f} | {ps} | {','.join(v['modes']):22s} | {family(f):28s} | {f[:70]}")
fam = collections.defaultdict(list)
for f, v in S.items(): fam[family(f)].append(100 * v['delta']['mean']['accuracy'])
print('\n=== single-descriptor Δacc by family (pp) ===')
for k, vs in sorted(fam.items(), key=lambda kv: -statistics.mean(kv[1])):
    print(f'{k:32s} n={len(vs):2d} mean {statistics.mean(vs):+.3f} min {min(vs):+.3f} max {max(vs):+.3f}')
# strata of the best singles
print('\n=== strata Δacc of top 5 singles (pp) ===')
for f, v in items[:5]:
    print(f[:50], {k: round(100 * s['accuracy_delta'], 2) for k, s in v['strata'].items()})
# cumulative
C = R.get('cumulative', {})
print(f'\n=== CUMULATIVE D0 + first k descriptors ({len(C)} entries) ===')
by = collections.defaultdict(dict)
for key, v in C.items():
    name, k = key.rsplit(':k', 1); by[name][int(k)] = 100 * v['delta']['mean']['accuracy']
rows = []
for name, ks in sorted(by.items()):
    if all(k in ks for k in (1, 2, 3)):
        rows.append((name, ks[1], ks[2], ks[3]))
if rows:
    print('traj | k=1 | k=2 | k=3 (pp)')
    for r in rows: print(f'{r[0]:26s} {r[1]:+.3f} {r[2]:+.3f} {r[3]:+.3f}')
    g = collections.defaultdict(list)
    for r in rows: g[r[0].split('-')[0]].append(r)
    print('\ngroup | mean k=1 | mean k=2 | mean k=3 | n(k2<k1) | n(k3<k2) | n(k3<k1)')
    for grp, rs in g.items():
        print(f"{grp:12s} {statistics.mean(r[1] for r in rs):+.3f} {statistics.mean(r[2] for r in rs):+.3f} {statistics.mean(r[3] for r in rs):+.3f} | {sum(r[2]<r[1] for r in rs)}/{len(rs)} | {sum(r[3]<r[2] for r in rs)}/{len(rs)} | {sum(r[3]<r[1] for r in rs)}/{len(rs)}")
    print('all: mean k=1 %+.3f, k=2 %+.3f, k=3 %+.3f' % tuple(statistics.mean(r[i] for r in rows) for i in (1, 2, 3)))
    # does k=3 (own rescoring) equal the stored evaluation?
    stored = {}
    import glob
    for fn in glob.glob(_REPO + '/results/zeosyn_v2_dev_1/evaluation/*-replicate-*.json'):
        e = json.load(open(fn)); stored[f"{e['mode']}-replicate-{e['replicate']}"] = 100 * e['delta']['mean']['accuracy']
    diffs = [abs(r[3] - stored[r[0]]) for r in rows if r[0] in stored]
    print('max |own k=3 - stored trajectory delta| (pp):', round(max(diffs), 6) if diffs else None)
    # additivity: sum of single deltas vs k=3
    singles_by_traj = {}
    for fn in glob.glob(_REPO + '/results/zeosyn_v2_dev_1/generation/*.json'):
        gg = json.load(open(fn)); nm = f"{gg['mode']}-replicate-{gg['replicate']}"
        if all(f['formula'] in S for f in gg['final_formulas']):
            singles_by_traj[nm] = sum(100 * S[f['formula']]['delta']['mean']['accuracy'] for f in gg['final_formulas'])
    pairs = [(singles_by_traj[r[0]], r[3]) for r in rows if r[0] in singles_by_traj]
    if pairs:
        import numpy as np
        a, b = np.array(pairs).T
        print(f'sum of single Δacc vs actual k=3 Δacc: corr {np.corrcoef(a, b)[0,1]:+.3f}; mean sum {a.mean():+.3f} vs mean k3 {b.mean():+.3f}')
