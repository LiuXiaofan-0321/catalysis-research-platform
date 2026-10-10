"""Own re-scoring: D0 + ONE descriptor (every distinct V2 formula) and cumulative D0 + first k descriptors per trajectory.
Uses the repo's own scorer (ev.score / z.fit_predict), the frozen prepared split and the 5 official fit seeds.
Writes JSON incrementally so partial results are usable."""
import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json, time, glob
ROOT = _REPO
sys.path[:0] = [ROOT + '/src', ROOT + '/scripts', ROOT + '/literature_pipeline/src']
import numpy as np
import run_zeosyn_v2 as rz
from catalysis_research.discovery import zeosyn_v2 as v2, zeosyn_direct as v1, zeosyn_v2_eval as ev
OUT = sys.argv[1]
RUN = ROOT + '/results/zeosyn_v2_dev_1'
split = rz.load_split(RUN)
seeds = [3, 7, 11, 17, 23]
kw = dict(seeds=seeds, n_estimators=100, n_jobs=4)
res = json.load(open(OUT)) if __import__('os').path.exists(OUT) else {}
def dump():
    json.dump(res, open(OUT, 'w'), indent=1)
t = time.time()
if 'd0' not in res:
    rows, preds = ev.score(split, split['d0'], **kw)
    res['d0'] = {'per_seed': rows, 'seconds': time.time() - t}
    np.save(OUT + '.d0preds.npy', preds)
    dump()
print('d0 done', res['d0']['per_seed'][0]['accuracy'], f'{time.time()-t:.0f}s', flush=True)
base = res['d0']['per_seed']
gens = [json.load(open(f)) for f in sorted(glob.glob(RUN + '/generation/*.json'))]
# distinct single formulas (exact string) -> evaluated with the env of the mode that produced them (kg env is a superset)
singles = {}
for g in gens:
    for f in g['final_formulas']:
        singles.setdefault(f['formula'], {'name': f['name'], 'modes': set()})['modes'].add(g['mode'])
res.setdefault('single', {})
for i, (formula, info) in enumerate(sorted(singles.items())):
    if formula in res['single']:
        continue
    env = v2.env_for_mode(split, 'kg')
    col, _ = v1.precheck(formula, env, split['train'], {})
    x = np.hstack([split['d0'], col[:, None]])
    t = time.time()
    rows, preds = ev.score(split, x, **kw)
    res['single'][formula] = {'name': info['name'], 'modes': sorted(info['modes']), 'per_seed': rows,
                              'delta': ev.paired(rows, base), 'strata': ev.stratified_deltas(split, preds, np.load(OUT + '.d0preds.npy', allow_pickle=True)),
                              'seconds': time.time() - t}
    dump()
    print(f'single {i+1}/{len(singles)} {formula[:60]!r} acc delta {res["single"][formula]["delta"]["mean"]["accuracy"]:+.4f} ({time.time()-t:.0f}s)', flush=True)
# cumulative D0 + first k (k=1,2) per trajectory; k=3 is the stored evaluation
res.setdefault('cumulative', {})
for g in gens:
    name = f"{g['mode']}-replicate-{g['replicate']}"
    for k in (1, 2, 3):
        key = f'{name}:k{k}'
        if key in res['cumulative'] or len(g['final_formulas']) < k:
            continue
        gk = {**g, 'final_formulas': g['final_formulas'][:k]}
        t = time.time()
        rows, preds = ev.score(split, v2.final_matrix(split, gk), **kw)
        res['cumulative'][key] = {'per_seed': rows, 'delta': ev.paired(rows, base), 'seconds': time.time() - t}
        dump()
        print(f'cumulative {key} acc delta {res["cumulative"][key]["delta"]["mean"]["accuracy"]:+.4f} ({time.time()-t:.0f}s)', flush=True)
print('ALL DONE', flush=True)
