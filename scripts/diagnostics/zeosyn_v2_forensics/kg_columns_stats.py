import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json, collections
import numpy as np
ROOT = _REPO
sys.path.insert(0, ROOT + '/src')
from catalysis_research.knowledge.kg_features import FEATURE_NAMES, TRACKED_FRAMEWORKS
RUN = ROOT + '/results/zeosyn_v2_dev_1'
t = np.load(RUN + '/prepared/kg_tables.npz'); m = np.load(RUN + '/prepared/matrices.npz'); s = np.load(RUN + '/prepared/split.npz')
y = m['y']; train = s['train']; ev = s['eval']
vocab = json.load(open(ROOT + '/data/kg_zeolite_v1/framework_vocabulary.json'))
keys = json.load(open(RUN + '/prepared/osda_keys.json'))
print('vocab size', len(vocab), '| rows', len(y), 'train', len(train), 'eval', len(ev))
for variant in ('kg', 'kg_shuffled', 'temporal', 'external'):
    known = t[f'{variant}__kg_osda_known']
    print(f'\n=== {variant}: kg_osda_known fraction all {known.mean():.3f} train {known[train].mean():.3f} eval {known[ev].mean():.3f} ===')
    if variant != 'kg': continue
    print(f"{'column':34s} {'non-null(all)':>13s} {'non-null(eval)':>14s} {'n_distinct(all)':>15s} {'n_distinct(eval)':>16s} {'min':>8s} {'median|known':>12s} {'max':>8s}")
    for f in FEATURE_NAMES:
        col = t[f'{variant}__{f}']
        if f in ('kg_osda_top_framework', 'kg_osda_median_temperature_c', 'kg_osda_median_product_si_al'):
            nn = col != -1
        else:
            nn = known > 0
        med = np.median(col[nn]) if nn.any() else float('nan')
        print(f'{f:34s} {nn.mean():13.3f} {nn[ev].mean():14.3f} {len(np.unique(col)):15d} {len(np.unique(col[ev])):16d} {col.min():8.2f} {med:12.2f} {col.max():8.2f}')
# class identity check
top = t['kg__kg_osda_top_framework'].astype(int); known = t['kg__kg_osda_known'] > 0
top_label = np.array([vocab[i] if i >= 0 else None for i in top], dtype=object)
for name, rows in (('train', train), ('eval', ev)):
    k = known[rows]; eq = (top_label[rows] == y[rows]) & k
    print(f'\n{name}: covered {k.sum()} / {len(rows)} ({k.mean():.3f}); KG top framework == label on {eq.sum()} of covered ({eq.sum()/k.sum():.3f})')
    # label among tracked frameworks with share>0
    shares = {fw: t[f'kg__kg_osda_share_{fw.replace("*","")}'][rows] for fw in TRACKED_FRAMEWORKS}
    lab = y[rows]
    in_tracked = np.array([l in TRACKED_FRAMEWORKS for l in lab])
    hit = np.array([(l in TRACKED_FRAMEWORKS and shares[l][i] > 0) for i, l in enumerate(lab)])
    print(f'   label is one of the 12 tracked frameworks: {in_tracked[k].mean():.3f} of covered rows; label has share>0 in its OSDA KG profile: {hit[k].mean():.3f} of covered rows')
    # majority-label baseline among covered
    print('   label distribution among covered rows (top 8):', collections.Counter(lab[k]).most_common(8))
    print('   KG top-framework distribution among covered rows (top 8):', collections.Counter(top_label[rows][k]).most_common(8))
# D0 predictions by coverage (eval rows)
preds = np.load(RUN + '/evaluation/d0-predictions.npy', allow_pickle=True)
yv = y[ev]; k = known[ev]; tl = top_label[ev]
acc = np.array([(p == yv) for p in preds])  # seeds x rows
print(f'\nD0 accuracy on eval: all {acc.mean():.4f} | covered {acc[:, k].mean():.4f} | not covered {acc[:, ~k].mean():.4f}')
eq = (tl == yv) & k
print(f'D0 accuracy on covered rows where KG top==label: {acc[:, eq].mean():.4f} (n={eq.sum()}) | covered rows where KG top!=label: {acc[:, k & ~eq].mean():.4f} (n={(k & ~eq).sum()})')
wrong_d0_right_kg = (~acc[:, :] & eq[None, :]).mean(1).mean() * len(yv)
right_d0_wrong_kg = (acc & (k & ~eq)[None, :]).mean(1).mean() * len(yv)
print(f'per seed mean count: D0 wrong but KG top right = {wrong_d0_right_kg:.0f} rows ({100*wrong_d0_right_kg/len(yv):.2f} pp upper bound); D0 right but KG top wrong = {right_d0_wrong_kg:.0f} rows')
# concentration of covered eval rows over OSDAs
osda_rows = collections.Counter(keys[i] for i in ev if known[i])
print('\ndistinct OSDAs among covered eval rows:', len(osda_rows), '| top 10 OSDAs by eval rows (rows, train rows with same OSDA, KG top, label agreement, D0 acc):')
tr_counts = collections.Counter(keys[i] for i in train if keys[i])
disp = json.load(open(ROOT + '/data/kg_zeolite_v1/osda_display.json'))
for key, nrow in osda_rows.most_common(10):
    idx = [j for j, i in enumerate(ev) if keys[i] == key]
    agree = np.mean([tl[j] == yv[j] for j in idx]); d0a = acc[:, idx].mean()
    print(f'   {disp.get(key, key)[:40]:40s} eval rows {nrow:4d} train rows {tr_counts[key]:5d} KG top {tl[idx[0]]:6s} top==label {agree:.2f} D0 acc {d0a:.2f} n_exp {int(t["kg__kg_osda_n_experiments"][ev[idx[0]]])} n_papers {int(t["kg__kg_osda_n_papers"][ev[idx[0]]])}')
# how many covered eval OSDAs are absent from training
absent = [key for key in osda_rows if tr_counts[key] == 0]
print('covered eval OSDAs with zero training rows:', len(absent), 'rows:', sum(osda_rows[k] for k in absent))
rare = [key for key in osda_rows if tr_counts[key] < 10]
print('covered eval OSDAs with <10 training rows:', len(rare), 'rows:', sum(osda_rows[k] for k in rare))
