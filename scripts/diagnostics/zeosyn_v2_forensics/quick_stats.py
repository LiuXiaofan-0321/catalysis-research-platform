import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, csv, json, glob, collections, statistics, re
import numpy as np
F = _REPO + '/docs/experiments/zeosyn_v2_forensics'
ROOT = _REPO; RUN = ROOT + '/results/zeosyn_v2_dev_1'
rows = list(csv.DictReader(open(F + '/slots_v2.csv')))
# per-trajectory aggregates
traj = collections.defaultdict(list)
for r in rows: traj[(r['group'], int(r['traj']))].append(r)
def corr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() == 0 or b.std() == 0: return float('nan')
    return float(np.corrcoef(a, b)[0, 1])
print('=== trajectory-level correlations with accuracy delta (all 40 trajectories) ===')
d = [float(v[0]['traj_delta_acc_pp']) for v in traj.values()]
nadd = [len(v) for v in traj.values()]
ncite = [sum(len(r['evidence_ids'].split()) if r['evidence_ids'] != '-' else 0 for r in v) for v in traj.values()]
nitems = [sum(int(r['evidence_items']) for r in v) for v in traj.values()]
nrep = [sum(r['status'] == 'repaired' for r in v) for v in traj.values()]
nq = [sum(int(r['n_queries']) for r in v) for v in traj.values()]
reason = [sum(int(r['reasoning_tokens']) for r in v) for v in traj.values()]
print(f'descriptors added: all = {set(nadd)} -> correlation undefined (constant)')
print(f'corr(delta, evidence items shown) = {corr(d, nitems):+.3f}; corr(delta, evidence ids cited) = {corr(d, ncite):+.3f}; corr(delta, queries written) = {corr(d, nq):+.3f}; corr(delta, repaired slots) = {corr(d, nrep):+.3f}; corr(delta, reasoning tokens) = {corr(d, reason):+.3f}')
for g in ('kg', 'kg_shuffled', 'rag'):
    dd = [float(traj[(g, i)][0]['traj_delta_acc_pp']) for i in range(1, 11)]
    cc = [sum(len(r['evidence_ids'].split()) if r['evidence_ids'] != '-' else 0 for r in traj[(g, i)]) for i in range(1, 11)]
    print(f'   {g}: corr(delta, cited ids) = {corr(dd, cc):+.3f}  cited per traj {cc}')
# family presence vs delta
print('\n=== mean trajectory delta by family presence (pp; n trajectories containing the family) ===')
fams = sorted({r['family'] for r in rows})
for f in fams:
    with_ = [float(v[0]['traj_delta_acc_pp']) for v in traj.values() if any(r['family'] == f for r in v)]
    without = [float(v[0]['traj_delta_acc_pp']) for v in traj.values() if not any(r['family'] == f for r in v)]
    print(f'{f:32s} with: n={len(with_):2d} mean {statistics.mean(with_):+.3f} | without: n={len(without):2d} mean {statistics.mean(without) if without else float("nan"):+.3f}')
# top-3 and bottom-3 trajectories
allt = sorted(traj.items(), key=lambda kv: -float(kv[1][0]['traj_delta_acc_pp']))
print('\nbest 5 trajectories:'); [print('  ', k, v[0]['traj_delta_acc_pp'], [r['formula'][:45] for r in v]) for k, v in allt[:5]]
print('worst 5 trajectories:'); [print('  ', k, v[0]['traj_delta_acc_pp'], [r['formula'][:45] for r in v]) for k, v in allt[-5:]]
# F / OH exclusivity, label majority
m = np.load(RUN + '/prepared/matrices.npz'); s = np.load(RUN + '/prepared/split.npz')
env = {k[5:]: m[k] for k in m.files if k.startswith('env__')}
tr, ev = s['train'], s['eval']
Fv, OH = env['F'][tr], env['OH'][tr]
print(f'\n=== F / OH on training rows: F>0 {np.mean(Fv>0):.3f}, OH>0 {np.mean(OH>0):.3f}, both>0 {np.mean((Fv>0)&(OH>0)):.4f}, neither {np.mean((Fv==0)&(OH==0)):.3f} ===')
print('Si==0 on train rows (AlPO-type):', f'{np.mean(env["Si"][tr]==0):.3f}', '| Al==0:', f'{np.mean(env["Al"][tr]==0):.3f}', '| sda1==0:', f'{np.mean(env["sda1"][tr]==0):.3f}', '| H2O==0:', f'{np.mean(env["H2O"][tr]==0):.3f}')
y = m['y']; c = collections.Counter(y[ev]); n = len(ev)
print('eval label distribution top 6 (share):', [(k, round(v / n, 3)) for k, v in c.most_common(6)], '| majority share', round(c.most_common(1)[0][1] / n, 4), '| classes in eval', len(c), '| classes in train', len(set(y[tr])))
d0 = json.load(open(RUN + '/evaluation/d0.json'))['per_seed']
print('D0 per-seed accuracy sd (pp):', round(100 * np.std([p['accuracy'] for p in d0], ddof=1), 3))
# V1 vs V2 family sets
v1 = list(csv.DictReader(open(F + '/slots_v1.csv')))
def famset(rs): return collections.Counter(r['family'] for r in rs)
core = {'ALKALINITY_OH_per_T', 'DILUTION_H2O_per_T', 'SI_AL_P_composition'}
print('\n=== V1 vs V2: share of slots in the three dominant V2 families (OH/T, H2O/T, Si/Al-P) ===')
for name, rs in (('V1 agent', [r for r in v1 if r['group'] == 'agent']), ('V1 rag_agent', [r for r in v1 if r['group'] == 'rag_agent']), ('V1 small_kg_rag_agent', [r for r in v1 if r['group'] == 'small_kg_rag_agent']),
                 ('V2 agent', [r for r in rows if r['group'] == 'agent']), ('V2 rag', [r for r in rows if r['group'] == 'rag']), ('V2 kg', [r for r in rows if r['group'] == 'kg']), ('V2 kg_shuffled', [r for r in rows if r['group'] == 'kg_shuffled'])):
    fs = famset(rs); print(f'{name:24s} {sum(fs[f] for f in core):2d}/30 core | families present: {sorted(fs)}')
v1f = set(r['family'] for r in v1); v2f = set(r['family'] for r in rows)
print('families only in V1:', sorted(v1f - v2f), '| only in V2:', sorted(v2f - v1f), '| shared:', sorted(v1f & v2f))
# does the KG model's plan text acknowledge KG scope?
print('\n=== plan "why"/queries: does the KG-group model say the KG cannot answer? ===')
pat = re.compile(r"(does not (contain|include|have)|cannot answer|not (available|in) the (KG|knowledge graph)|no (KG|knowledge[- ]graph) (query|evidence)|KG (lacks|does not)|gel ratios)", re.I)
for g in ('kg', 'kg_shuffled'):
    n_hit = 0; ex = None
    for fn in sorted(glob.glob(RUN + f'/generation/{g}-replicate-*.json')):
        for sl in json.load(open(fn))['slots']:
            w = (sl.get('plan') or {}).get('why', '')
            if pat.search(w): n_hit += 1; ex = ex or (fn.split('/')[-1], sl['round'], pat.search(w).group(0), w[max(0, pat.search(w).start() - 150):pat.search(w).end() + 150])
    print(g, 'plan texts mentioning KG scope limits:', n_hit, '/ 30; example:', ex)
# precheck nonfinite fractions
nf = [a['precheck']['train_nonfinite_fraction'] for fn in glob.glob(RUN + '/generation/*.json') for sl in json.load(open(fn))['slots'] for a in sl['attempts'] if 'precheck' in a]
print('\ntrain_nonfinite_fraction over accepted formulas: max', max(nf), 'n>0:', sum(x > 0 for x in nf))
