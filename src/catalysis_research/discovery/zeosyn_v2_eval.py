"""ZeoSyn V2 evaluation and statistics.

Scores are paired: every descriptor set is compared with D0 at the same fit seed on the same rows.
The statistical unit is a generation trajectory (fit seeds averaged within it). All trajectories
enter the analysis, including failed slots, zero-append and negative ones.
"""
from __future__ import annotations

import numpy as np

from ..benchmarks import zeosyn as z
from ..knowledge.kg_features import FEATURE_NAMES
from . import zeosyn_v2 as v2

METRICS = ('accuracy', 'macro_f1', 'balanced_accuracy')
RARE_OSDA_TRAINING_RECIPES = 10  # pre-specified: an OSDA with fewer training recipes is "rare" (incl. unseen)


def fit_predict(x_train, y_train, x_eval, *, seed, n_estimators, n_jobs, predictor='rf', hgb=None):
    if predictor == 'rf':
        return z.fit_predict(x_train, y_train, x_eval, seed=seed, n_jobs=n_jobs, n_estimators=n_estimators)
    if predictor == 'hgb':
        from sklearn.ensemble import HistGradientBoostingClassifier
        hgb = hgb or {}
        model = HistGradientBoostingClassifier(max_iter=hgb.get('max_iter', 100), learning_rate=hgb.get('learning_rate', 0.1),
                                               early_stopping=False, random_state=seed)
        model.fit(x_train, y_train)
        return model.predict(x_eval)
    raise ValueError(predictor)


def score(split, x, *, seeds, n_estimators, n_jobs, predictor='rf', hgb=None):
    """Per-seed metrics and predictions on the split's evaluation rows."""
    tr, ev, y = split['train'], split['eval'], split['y']
    rows, preds = [], []
    for s in seeds:
        p = fit_predict(x[tr], y[tr], x[ev], seed=s, n_estimators=n_estimators, n_jobs=n_jobs, predictor=predictor, hgb=hgb)
        rows.append({'seed': s, **z.classification_metrics(y[ev], p)})
        preds.append(p)
    return rows, np.array(preds, dtype=object)


def paired(final, base):
    by_seed = {r['seed']: r for r in base}
    per = [{'seed': r['seed'], **{k: r[k] - by_seed[r['seed']][k] for k in METRICS}} for r in final]
    return {'per_seed': per, 'mean': {k: float(np.mean([r[k] for r in per])) for k in METRICS}}


def library_matrix(split, table='kg'):
    t = split['kg_tables'][table]
    return np.hstack([split['d0'], np.column_stack([t[f] for f in FEATURE_NAMES])])


def variant_split(split, variant):
    """The same split with the kg_* inputs of the KG condition replaced by a sensitivity table."""
    out = dict(split)
    out['kg_tables'] = {**split['kg_tables'], 'kg': split['kg_variants'][variant]}
    return out


def stratum_masks(split):
    """Boolean masks over evaluation rows: KG coverage, and OSDA frequency among training recipes."""
    ev, tr = split['eval'], split['train']
    covered = np.asarray(split['kg_tables']['kg']['kg_osda_known'])[ev] > 0
    keys = split['osda_keys']
    counts = {}
    for i in tr:
        if keys[i]:
            counts[keys[i]] = counts.get(keys[i], 0) + 1
    has_osda = np.array([bool(keys[i]) for i in ev])
    rare = np.array([bool(keys[i]) and counts.get(keys[i], 0) < RARE_OSDA_TRAINING_RECIPES for i in ev])
    return {'kg_covered': covered, 'kg_not_covered': ~covered, 'osda_rare_in_training': rare,
            'osda_common_in_training': has_osda & ~rare, 'no_osda': ~has_osda}


def stratified_deltas(split, preds, base_preds):
    """Accuracy change per stratum (mean over seeds) for one descriptor set versus D0."""
    y = split['y'][split['eval']]
    out = {}
    for name, mask in stratum_masks(split).items():
        if mask.sum() == 0:
            out[name] = {'n': 0, 'accuracy_delta': None}
            continue
        d = [float((p[mask] == y[mask]).mean() - (b[mask] == y[mask]).mean()) for p, b in zip(preds, base_preds)]
        out[name] = {'n': int(mask.sum()), 'accuracy_delta': float(np.mean(d))}
    return out


# ---------------------------------------------------------------- statistics

def bootstrap_mean(values, *, n, seed, level=0.95):
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    m = v[rng.integers(0, len(v), size=(n, len(v)))].mean(1)
    a = (1 - level) / 2
    return {'mean': float(v.mean()), 'ci': [float(np.quantile(m, a)), float(np.quantile(m, 1 - a))], 'n': int(len(v)), 'level': level}


def bootstrap_difference(a, b, *, n, seed, level=0.95):
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    d = a[rng.integers(0, len(a), size=(n, len(a)))].mean(1) - b[rng.integers(0, len(b), size=(n, len(b)))].mean(1)
    q = (1 - level) / 2
    return {'mean': float(a.mean() - b.mean()), 'ci': [float(np.quantile(d, q)), float(np.quantile(d, 1 - q))], 'level': level,
            'n_a': int(len(a)), 'n_b': int(len(b))}


def summarize(config, generations, evaluations, *, d0, library):
    an = config['analysis']
    n, seed = an['bootstrap_resamples'], an['bootstrap_seed']
    primary = config['evaluation']['primary_metric']
    modes = [m for m in config['modes'] if any(e['mode'] == m for e in evaluations)]
    per_mode, deltas = {}, {}
    for mode in modes:
        ev = [e for e in evaluations if e['mode'] == mode]
        gens = [g for g in generations if g['mode'] == mode]
        deltas[mode] = [e['delta']['mean'][primary] for e in ev]
        slots = [s for g in gens for s in g['slots']]
        appended = [s for s in slots if s['status'] == 'appended']
        per_mode[mode] = {
            'trajectories_evaluated': len(ev), 'trajectories_expected': config['replicates_per_mode'],
            'slots': len(slots), 'appended_slots': len(appended),
            'zero_append_trajectories': sum(g['appended'] == 0 for g in gens),
            'negative_trajectories': sum(d < 0 for d in deltas[mode]),
            **{k: bootstrap_mean([e['delta']['mean'][k] for e in ev], n=n, seed=seed) for k in METRICS},
            'strata_accuracy_delta': {s: float(np.mean([e['strata'][s]['accuracy_delta'] for e in ev
                                                         if e['strata'][s]['accuracy_delta'] is not None] or [np.nan]))
                                      for s in (ev[0]['strata'] if ev else {})},
            'quality': {
                'slots_using_kg_inputs': sum(bool(s['candidate'].get('uses_kg_inputs')) for s in appended),
                'slots_citing_evidence': sum(bool(s['candidate'].get('evidence_ids')) for s in appended),
                'mean_evidence_items': float(np.mean([len((s.get('evidence') or {}).get('items', [])) for s in slots] or [0])),
                'distinct_factors': len({(s.get('plan') or {}).get('factor', '').lower() for s in slots if s.get('plan')}),
            },
        }
    contrasts = {}
    pairs = [('kg', 'agent'), ('kg', 'rag'), ('kg', 'kg_shuffled'), ('kg_shuffled', 'agent'), ('rag', 'agent'),
             ('kg_flat', 'kg')]
    for a, b in pairs:
        if a in deltas and b in deltas and deltas[a] and deltas[b]:
            contrasts[f'{a}-{b}'] = bootstrap_difference(deltas[a], deltas[b], n=n, seed=seed)
    decision = None
    if 'kg-agent' in contrasts:
        lo = contrasts['kg-agent']['ci'][0]
        decision = {'rule': an['decision_rule'], 'kg_minus_agent_ci_lower': lo, 'H2_supported': bool(lo > 0)}
    h1 = per_mode.get('agent', {}).get(primary)
    return {
        'profile': v2.PROFILE, 'primary_metric': primary, 'unit': an['unit'], 'd0': d0, 'library_only': library,
        'per_mode': per_mode, 'contrasts': contrasts,
        'hypotheses': {'H1_agent_vs_d0': h1 and {**h1, 'supported': bool(h1['ci'][0] > 0)},
                       'H2_kg_vs_agent': decision,
                       'H3_kg_vs_rag': contrasts.get('kg-rag')},
        'note': 'Deltas are absolute metric differences versus D0 at the same fit seed. Failed slots, zero-append '
                'and negative trajectories are all included.',
    }
