"""Shared helpers for the ZeoSyn knowledge-channel ceiling analysis (diagnostic only, not part of any protocol)."""
from __future__ import annotations

import gc
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import os

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(os.environ.get('ZEOSYN_CEILING_OUT', ROOT / 'docs/experiments/zeosyn_v3_ceiling'))
CACHE = OUT / 'cache'
RESULTS = OUT / 'results.json'

N_EST = 60
N_JOBS = 4
SEEDS = (3, 7)          # two fit seeds, as requested (authors use 3,7,11,17,23)
PAPER_SPLIT_SEED = 20261007
PAPER_TEST_FRACTION = 0.2
OSDA_FOLDS = 5
OSDA_SPLIT_SEED = 1


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def load_results():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text())
    return {}


def save_results(section, value):
    res = load_results()
    res[section] = value
    tmp = RESULTS.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(res, indent=2, ensure_ascii=False, sort_keys=True, default=_default) + '\n')
    tmp.replace(RESULTS)


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(str(type(o)))


def load_cache():
    """Everything the analyses need, from 00_prepare.py."""
    z = np.load(CACHE / 'base.npz', allow_pickle=True)
    meta = pd.read_pickle(CACHE / 'meta.pkl')
    # rows without an OSDA must have key None (pickle round-trip turned None into NaN)
    meta['osda_key'] = pd.Series([None if (k is None or (isinstance(k, float) and np.isnan(k))) else k
                                  for k in meta['osda_key']], index=meta.index, dtype=object)
    out = {k: z[k] for k in z.files}
    out['meta'] = meta
    return out


def rf(seed, n_estimators=N_EST):
    from sklearn.ensemble import RandomForestClassifier
    return RandomForestClassifier(n_estimators=n_estimators, max_depth=None, max_features='sqrt',
                                  random_state=seed, n_jobs=N_JOBS)


def fit_proba(x_train, y_train, x_test, seed, n_estimators=N_EST):
    """Returns (classes, proba on x_test). Model is freed before returning."""
    m = rf(seed, n_estimators)
    m.fit(x_train, y_train)
    classes = m.classes_.copy()
    p = m.predict_proba(x_test)
    del m
    gc.collect()
    return classes, p


def metrics(y_true, y_pred):
    from catalysis_research.benchmarks.zeosyn import classification_metrics
    return classification_metrics(np.asarray(y_true), np.asarray(y_pred))


def acc(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    return float((y_true == y_pred).mean()) if len(y_true) else float('nan')
