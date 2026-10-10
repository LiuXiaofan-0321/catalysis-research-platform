"""B1 (paper split baselines) and D (gel-ratio headroom under the paper split)."""
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import CACHE, SEEDS, acc, fit_proba, load_cache, log, metrics, save_results  # noqa: E402
from prior import build_pool, modal, paper_ids  # noqa: E402

c = load_cache()
meta, y = c['meta'], c['y']
X = c['d0_paper']
d0_cols = list(c['d0_cols'])
tr, te = c['paper_train'], c['paper_test']
keys = meta['osda_key'].tolist()
paper = paper_ids(meta['doi'].tolist())
log(f'paper split train={len(tr)} test={len(te)}')

out = {'train_rows': int(len(tr)), 'test_rows': int(len(te)), 'seeds': list(SEEDS), 'n_estimators': 60}
# ---- RF D0
per_seed, preds_d0 = [], {}
for s in SEEDS:
    log(f'RF D0 seed {s}')
    classes, P = fit_proba(X[tr], y[tr], X[te], s)
    pred = classes[P.argmax(1)]
    preds_d0[s] = pred
    per_seed.append({'seed': s, **metrics(y[te], pred)})
    np.savez_compressed(CACHE / f'paper_s{s}_d0.npz', classes=classes, proba=P.astype(np.float32), pred=pred)
out['rf_d0'] = {'per_seed': per_seed, 'mean': {k: float(np.mean([r[k] for r in per_seed])) for k in ('accuracy', 'balanced_accuracy', 'macro_f1')}}

# ---- trivial rule: modal framework of this OSDA in the TRAINING set, fallback global modal class
train_modal = {}
pool = build_pool(tr, keys, paper)
for k, rows in pool.items():
    train_modal[k] = modal(Counter(y[rows]))
gmodal = modal(Counter(y[tr]))
pred = np.array([train_modal.get(keys[i], gmodal) if keys[i] else gmodal for i in te], dtype=object)
seen = np.array([keys[i] in train_modal for i in te])
has_osda = np.array([keys[i] is not None for i in te])
out['global_modal_class_train'] = gmodal
out['trivial_train_modal_per_osda'] = {
    **metrics(y[te], pred), 'test_rows_with_osda_seen_in_train': int(seen.sum()),
    'share_test_rows_with_osda_seen_in_train': float(seen.mean()),
    'share_test_rows_with_osda': float(has_osda.mean()),
    'accuracy_on_seen_osda_rows': acc(y[te][seen], pred[seen]),
    'accuracy_on_unseen_or_no_osda_rows': acc(y[te][~seen], pred[~seen]),
    'rf_d0_accuracy_on_seen_osda_rows_mean': float(np.mean([acc(y[te][seen], preds_d0[s][seen]) for s in SEEDS])),
    'rf_d0_accuracy_on_unseen_or_no_osda_rows_mean': float(np.mean([acc(y[te][~seen], preds_d0[s][~seen]) for s in SEEDS])),
}
out['global_modal_accuracy'] = acc(y[te], np.full(len(te), gmodal, dtype=object))

# ---- 1-NN in standardized D0 space
mu, sd = X[tr].mean(0), X[tr].std(0)
sd[sd == 0] = 1
Z = (X - mu) / sd
from sklearn.neighbors import KNeighborsClassifier  # noqa: E402
knn = KNeighborsClassifier(n_neighbors=1).fit(Z[tr], y[tr])
pred = knn.predict(Z[te])
out['nn1_d0_standardized'] = metrics(y[te], pred)
# ---- also: leave-own-paper-out modal-per-OSDA within the test set (oracle, paper split), for reference
save_results('B1', out)
log('B1 done', {k: v for k, v in out['rf_d0']['mean'].items()}, 'trivial', out['trivial_train_modal_per_osda']['accuracy'], '1nn', out['nn1_d0_standardized']['accuracy'])

# ======================= D: gel ratios under the paper split
ci = {k: i for i, k in enumerate(d0_cols)}
g = lambda name: X[:, ci[name]]  # noqa: E731
CAP = 1e3


def ratio(a, b):
    return np.where(b > 0, a / np.where(b > 0, b, 1), np.where(a > 0, CAP, 0.0))


Si, Al, P = g('Si'), g('Al'), g('P')
alkali = g('Na') + g('K') + g('Li') + g('Rb') + g('Cs')
alk_earth = g('Mg') + g('Ca') + g('Sr') + g('Ba')
hetero = g('Ge') + g('B') + g('Ti') + g('Ga') + g('Zn') + g('Sn') + g('Zr') + g('V') + g('Be') + g('W') + g('Cu')
T = Si + Al + P + hetero
ratios = {
    'Si/Al': ratio(Si, Al), 'Al/(Si+Al)': ratio(Al, Si + Al), 'Si/(Al+P)': ratio(Si, Al + P), 'P/Al': ratio(P, Al),
    'H2O/Si': ratio(g('H2O'), Si), 'H2O/T': ratio(g('H2O'), T), 'OH/Si': ratio(g('OH'), Si), 'OH/T': ratio(g('OH'), T),
    'F/Si': ratio(g('F'), Si), 'F/(F+OH)': ratio(g('F'), g('F') + g('OH')), 'sda1/Si': ratio(g('sda1'), Si),
    'sda1/T': ratio(g('sda1'), T), 'OH/sda1': ratio(g('OH'), g('sda1')), 'Na/Si': ratio(g('Na'), Si),
    'K/Si': ratio(g('K'), Si), 'alkali/Si': ratio(alkali, Si), 'Na/(Na+K)': ratio(g('Na'), g('Na') + g('K')),
    'alkaline_earth/Si': ratio(alk_earth, Si), 'hetero/Si': ratio(hetero, Si), '(Si+Al)/T': ratio(Si + Al, T),
}
R = np.column_stack(list(ratios.values()))
XR = np.hstack([X, R])
per_seed_r = []
for s in SEEDS:
    log(f'RF D0+ratios seed {s}')
    classes, Pr = fit_proba(XR[tr], y[tr], XR[te], s)
    pred = classes[Pr.argmax(1)]
    per_seed_r.append({'seed': s, **metrics(y[te], pred)})
d = {'ratio_names': list(ratios), 'cap_for_zero_denominator': CAP,
     'rf_d0_plus_ratios': {'per_seed': per_seed_r, 'mean': {k: float(np.mean([r[k] for r in per_seed_r])) for k in ('accuracy', 'balanced_accuracy', 'macro_f1')}},
     'rf_d0': out['rf_d0'],
     'delta_mean': {k: float(np.mean([r[k] for r in per_seed_r]) - np.mean([r[k] for r in per_seed])) for k in ('accuracy', 'balanced_accuracy', 'macro_f1')},
     'delta_per_seed_accuracy': [r2['accuracy'] - r1['accuracy'] for r1, r2 in zip(per_seed, per_seed_r)]}
save_results('D', d)
log('D done', d['delta_mean'])
