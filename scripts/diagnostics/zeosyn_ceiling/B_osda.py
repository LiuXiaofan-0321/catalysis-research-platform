"""B2-B4: OSDA-group split (5 folds, seed 1): D0 baselines, oracle literature prior, combined models."""
import gc
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import CACHE, OSDA_FOLDS, SEEDS, acc, fit_proba, load_cache, log, metrics, save_results  # noqa: E402
from prior import build_pool, dist_matrix, modal, oracle_predictions, paper_ids, prior_block  # noqa: E402

c = load_cache()
meta, y = c['meta'], c['y']
d0_cols = list(c['d0_cols'])
gel_idx = [d0_cols.index(k) for k in c['gel_cols'] if k not in ('cryst_time', 'cryst_temp')]
gelcond_idx = [d0_cols.index(k) for k in c['gel_cols']]
fold = c['osda_fold']
keys = meta['osda_key'].tolist()
paper = paper_ids(meta['doi'].tolist())
desc30, desc_full = c['osda_desc30'], c['osda_desc_full']
METRICS = ('accuracy', 'balanced_accuracy', 'macro_f1')
EPS = (0.01, 0.05, 0.2, 1.0)
TOPK = 10
only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else list(range(OSDA_FOLDS))


def mean_metrics(rows):
    return {k: float(np.mean([r[k] for r in rows])) for k in METRICS}


def osda_level(rows, desc):
    """Per-OSDA descriptor vector (mean over recipes) and modal framework over `rows`."""
    by = {}
    for i in rows:
        if keys[i]:
            by.setdefault(keys[i], []).append(i)
    ks = sorted(by)
    V = np.array([desc[by[k]].mean(0) for k in ks])
    md = {k: modal(Counter(y[by[k]])) for k in ks}
    return ks, V, md


def nn_osda(tr, te, desc):
    ks_tr, V_tr, md_tr = osda_level(tr, desc)
    ks_te, V_te, _ = osda_level(te, desc)
    mu, sd = V_tr.mean(0), V_tr.std(0)
    keep = sd > 0
    Ztr, Zte = (V_tr[:, keep] - mu[keep]) / sd[keep], (V_te[:, keep] - mu[keep]) / sd[keep]
    from sklearn.neighbors import NearestNeighbors
    nn = NearestNeighbors(n_neighbors=1).fit(Ztr)
    _, ind = nn.kneighbors(Zte)
    pred_osda = {k: md_tr[ks_tr[j]] for k, j in zip(ks_te, ind[:, 0])}
    return np.array([pred_osda[keys[i]] for i in te], dtype=object), int(keep.sum())


results = {'folds': {}, 'seeds': list(SEEDS), 'n_estimators': 60, 'eps_grid': list(EPS), 'top_k_prior_classes': TOPK}
prev = {}
try:
    from common import load_results
    prev = load_results().get('B_osda', {}).get('folds', {})
except Exception:
    pass

for f in only:
    log(f'===== fold {f}')
    per_fold_imp = f'd0_osda_f{f}' in c
    X = c[f'd0_osda_f{f}'] if per_fold_imp else c['d0_paper']
    tr, te = np.flatnonzero(fold != f), np.flatnonzero(fold == f)
    ytr, yte = y[tr], y[te]
    R = {'train_rows': int(len(tr)), 'test_rows': int(len(te)), 'test_osdas': len({keys[i] for i in te}),
         'imputation': 'fit on this fold\'s training rows' if per_fold_imp else 'fit on paper-split training rows (fallback)',
         'test_classes_unseen_in_train_rows': int(sum(v not in set(ytr) for v in yte))}
    # ---------- RF D0
    per, P_d0, cls = [], {}, None
    for s in SEEDS:
        log(f'fold {f} RF D0 seed {s}')
        cls, P = fit_proba(X[tr], ytr, X[te], s)
        P_d0[s] = P
        pred = cls[P.argmax(1)]
        per.append({'seed': s, **metrics(yte, pred)})
        np.savez_compressed(CACHE / f'osda_f{f}_s{s}_d0.npz', classes=cls, proba=P.astype(np.float32))
    R['rf_d0'] = {'per_seed': per, 'mean': mean_metrics(per)}
    pred_d0 = {s: cls[P_d0[s].argmax(1)] for s in SEEDS}
    # ---------- global modal, 1-NN OSDA descriptor space
    gm = modal(Counter(ytr))
    R['global_modal_class'] = gm
    R['global_modal_accuracy'] = acc(yte, np.full(len(te), gm, dtype=object))
    p30, k30 = nn_osda(tr, te, desc30)
    pfull, kfull = nn_osda(tr, te, desc_full)
    R['nn1_osda_desc30'] = {**metrics(yte, p30), 'dims_used': k30}
    R['nn1_osda_desc_full'] = {**metrics(yte, pfull), 'dims_used': kfull}
    # ---------- oracle literature prior on test rows (other-paper same-OSDA test recipes)
    mu, sd = X[tr].mean(0), X[tr].std(0)
    sd[sd == 0] = 1
    Z = (X - mu) / sd
    pool_te = build_pool(te, keys, paper)
    orc = oracle_predictions(te, pool_te, keys, paper, y, Z[:, gel_idx])
    orc2 = oracle_predictions(te, pool_te, keys, paper, y, Z[:, gelcond_idx])
    cov = orc['support'] > 0
    cov3 = orc['support'] >= 3
    R['oracle'] = {'coverage': float(cov.mean()), 'covered_rows': int(cov.sum()), 'covered_osdas': len({keys[i] for i in te[cov]}),
                   'coverage_ge3': float(cov3.mean()), 'covered_rows_ge3': int(cov3.sum()),
                   'test_rows_with_osda': int(len(te))}
    for name, arr in (('modal', orc['modal']), ('nn1_gel', orc['nn1']), ('knn5_gel', orc['knn']),
                      ('nn1_gel_plus_conditions', orc2['nn1']), ('knn5_gel_plus_conditions', orc2['knn'])):
        R['oracle'][name] = {'acc_covered': acc(yte[cov], arr[cov]), 'acc_covered_ge3': acc(yte[cov3], arr[cov3]),
                             'acc_covered_support_1_2': acc(yte[cov & ~cov3], arr[cov & ~cov3])}
        comb = {}
        for s in SEEDS:
            p = pred_d0[s].copy()
            p[cov] = arr[cov]
            comb[s] = p
        R['oracle'][name]['overall_oracle_where_covered_else_rf_d0'] = mean_metrics([metrics(yte, comb[s]) for s in SEEDS])
        comb3 = {}
        for s in SEEDS:
            p = pred_d0[s].copy()
            p[cov3] = arr[cov3]
            comb3[s] = p
        R['oracle'][name]['overall_oracle_where_support_ge3_else_rf_d0'] = mean_metrics([metrics(yte, comb3[s]) for s in SEEDS])
    R['rf_d0_acc_covered'] = float(np.mean([acc(yte[cov], pred_d0[s][cov]) for s in SEEDS]))
    R['rf_d0_acc_uncovered'] = float(np.mean([acc(yte[~cov], pred_d0[s][~cov]) for s in SEEDS]))
    R['rf_d0_acc_covered_ge3'] = float(np.mean([acc(yte[cov3], pred_d0[s][cov3]) for s in SEEDS]))
    # oracle support distribution
    sup = orc['support']
    R['oracle']['support_quantiles'] = {q: float(np.percentile(sup[cov], q)) for q in (10, 25, 50, 75, 90)}
    # ---------- B4: RF on D0 + prior block
    train_classes = sorted(set(ytr))
    class_index = {cc: j for j, cc in enumerate(train_classes)}
    top = [k for k, _ in Counter(ytr).most_common(TOPK)]
    pool_tr = build_pool(tr, keys, paper)
    B_tr = prior_block(tr, pool_tr, keys, paper, y, top, class_index)
    B_te = prior_block(te, pool_te, keys, paper, y, top, class_index)
    R['prior_block'] = {'top_classes': top, 'train_rows_covered_share': float((B_tr[:, TOPK + 1] > 0).mean()),
                        'test_rows_covered_share': float((B_te[:, TOPK + 1] > 0).mean())}
    Xtr2, Xte2 = np.hstack([X[tr], B_tr]), np.hstack([X[te], B_te])
    per2, pred_pr = [], {}
    for s in SEEDS:
        log(f'fold {f} RF D0+prior seed {s}')
        cls2, P2 = fit_proba(Xtr2, ytr, Xte2, s)
        pred_pr[s] = cls2[P2.argmax(1)]
        per2.append({'seed': s, **metrics(yte, pred_pr[s])})
        del P2
        gc.collect()
    R['rf_d0_plus_prior'] = {'per_seed': per2, 'mean': mean_metrics(per2),
                             'acc_covered': float(np.mean([acc(yte[cov], pred_pr[s][cov]) for s in SEEDS])),
                             'acc_uncovered': float(np.mean([acc(yte[~cov], pred_pr[s][~cov]) for s in SEEDS])),
                             'delta_vs_d0': {k: float(np.mean([r[k] for r in per2]) - np.mean([r[k] for r in per])) for k in METRICS}}
    # prior-only variants for reference: block without D0 (RF on prior block only)
    per3 = []
    for s in SEEDS[:1]:
        cls3, P3 = fit_proba(B_tr, ytr, B_te, s)
        per3.append({'seed': s, **metrics(yte, cls3[P3.argmax(1)])})
        del P3
        gc.collect()
    R['rf_prior_block_only'] = {'per_seed': per3, 'mean': mean_metrics(per3)}
    # ---------- product rule: RF proba x (prior + eps)
    Pm = dist_matrix(orc['dist'], cls)            # modal/distribution prior (other-paper same-OSDA)
    knn_dist = []
    for j, i in enumerate(te):
        if orc['support'][j] == 0:
            knn_dist.append(None)
            continue
        others = pool_te[keys[i]]
        others = others[paper[others] != paper[i]]
        d = np.linalg.norm(Z[others][:, gel_idx] - Z[i, gel_idx], axis=1)
        knn_dist.append(Counter(y[others[np.argsort(d, kind='stable')[:5]]]))
    Pk = dist_matrix(knn_dist, cls)
    R['product_rule'] = {}
    for pname, Pp in (('distribution_prior', Pm), ('knn5_gel_prior', Pk)):
        for eps in EPS:
            rows = []
            for s in SEEDS:
                Q = P_d0[s] * (Pp + eps)
                pred = cls[Q.argmax(1)]
                m = metrics(yte, pred)
                m['acc_covered'] = acc(yte[cov], pred[cov])
                m['acc_uncovered'] = acc(yte[~cov], pred[~cov])
                rows.append(m)
            R['product_rule'][f'{pname}_eps{eps}'] = {**mean_metrics(rows),
                                                      'acc_covered': float(np.mean([r['acc_covered'] for r in rows])),
                                                      'acc_uncovered': float(np.mean([r['acc_uncovered'] for r in rows]))}
    # covered-but-wrong analysis: is the true class even in the prior support?
    in_support = np.array([(orc['dist'][j] is not None and yte[j] in orc['dist'][j]) for j in range(len(te))])
    R['oracle']['true_class_in_other_paper_support_share_covered'] = float(in_support[cov].mean())
    R['oracle']['true_class_in_other_paper_support_share_covered_ge3'] = float(in_support[cov3].mean())
    results['folds'][str(f)] = R
    # merge with previous folds (allows running folds separately)
    merged = {**prev, **results['folds']}
    results['folds'] = merged
    save_results('B_osda', results)
    log(f'fold {f}: D0 acc={R["rf_d0"]["mean"]["accuracy"]:.4f} global={R["global_modal_accuracy"]:.4f} '
        f'nn30={R["nn1_osda_desc30"]["accuracy"]:.4f} cov={R["oracle"]["coverage"]:.3f} '
        f'oracle modal={R["oracle"]["modal"]["acc_covered"]:.4f} nn1gel={R["oracle"]["nn1_gel"]["acc_covered"]:.4f} '
        f'knn5={R["oracle"]["knn5_gel"]["acc_covered"]:.4f} '
        f'overall(modal)={R["oracle"]["modal"]["overall_oracle_where_covered_else_rf_d0"]["accuracy"]:.4f} '
        f'D0+prior={R["rf_d0_plus_prior"]["mean"]["accuracy"]:.4f}')
    del X, Z, P_d0
    gc.collect()

# ---------- means over folds (recipe-weighted and plain)
folds = results['folds']
if len(folds) == OSDA_FOLDS:
    def fmean(path):
        vals = []
        for f in folds.values():
            v = f
            for p in path:
                v = v[p]
            vals.append(v)
        w = np.array([f['test_rows'] for f in folds.values()], float)
        return {'mean': float(np.mean(vals)), 'recipe_weighted_mean': float(np.average(vals, weights=w))}
    summary = {}
    for name, path in {
        'rf_d0_accuracy': ('rf_d0', 'mean', 'accuracy'), 'rf_d0_balanced_accuracy': ('rf_d0', 'mean', 'balanced_accuracy'),
        'rf_d0_macro_f1': ('rf_d0', 'mean', 'macro_f1'), 'global_modal_accuracy': ('global_modal_accuracy',),
        'nn1_osda_desc30_accuracy': ('nn1_osda_desc30', 'accuracy'), 'nn1_osda_desc_full_accuracy': ('nn1_osda_desc_full', 'accuracy'),
        'oracle_coverage': ('oracle', 'coverage'), 'oracle_coverage_ge3': ('oracle', 'coverage_ge3'),
        'oracle_modal_acc_covered': ('oracle', 'modal', 'acc_covered'), 'oracle_nn1_gel_acc_covered': ('oracle', 'nn1_gel', 'acc_covered'),
        'oracle_knn5_gel_acc_covered': ('oracle', 'knn5_gel', 'acc_covered'),
        'oracle_nn1_gelcond_acc_covered': ('oracle', 'nn1_gel_plus_conditions', 'acc_covered'),
        'oracle_modal_acc_covered_ge3': ('oracle', 'modal', 'acc_covered_ge3'),
        'oracle_nn1_gel_acc_covered_ge3': ('oracle', 'nn1_gel', 'acc_covered_ge3'),
        'oracle_knn5_gel_acc_covered_ge3': ('oracle', 'knn5_gel', 'acc_covered_ge3'),
        'overall_modal_else_d0': ('oracle', 'modal', 'overall_oracle_where_covered_else_rf_d0', 'accuracy'),
        'overall_nn1_gel_else_d0': ('oracle', 'nn1_gel', 'overall_oracle_where_covered_else_rf_d0', 'accuracy'),
        'overall_knn5_gel_else_d0': ('oracle', 'knn5_gel', 'overall_oracle_where_covered_else_rf_d0', 'accuracy'),
        'overall_nn1_gelcond_else_d0': ('oracle', 'nn1_gel_plus_conditions', 'overall_oracle_where_covered_else_rf_d0', 'accuracy'),
        'rf_d0_acc_covered': ('rf_d0_acc_covered',), 'rf_d0_acc_uncovered': ('rf_d0_acc_uncovered',),
        'rf_d0_plus_prior_accuracy': ('rf_d0_plus_prior', 'mean', 'accuracy'),
        'rf_d0_plus_prior_balanced_accuracy': ('rf_d0_plus_prior', 'mean', 'balanced_accuracy'),
        'rf_d0_plus_prior_macro_f1': ('rf_d0_plus_prior', 'mean', 'macro_f1'),
        'rf_d0_plus_prior_acc_covered': ('rf_d0_plus_prior', 'acc_covered'),
        'rf_d0_plus_prior_acc_uncovered': ('rf_d0_plus_prior', 'acc_uncovered'),
        'rf_prior_only_accuracy': ('rf_prior_block_only', 'mean', 'accuracy'),
        'true_class_in_support_covered': ('oracle', 'true_class_in_other_paper_support_share_covered'),
    }.items():
        summary[name] = fmean(path)
    for pname in ('distribution_prior', 'knn5_gel_prior'):
        for eps in EPS:
            summary[f'product_{pname}_eps{eps}_accuracy'] = fmean(('product_rule', f'{pname}_eps{eps}', 'accuracy'))
            summary[f'product_{pname}_eps{eps}_acc_covered'] = fmean(('product_rule', f'{pname}_eps{eps}', 'acc_covered'))
    results['summary'] = summary
    save_results('B_osda', results)
    log('summary', {k: round(v['mean'], 4) for k, v in summary.items()})
log('B_osda done')
