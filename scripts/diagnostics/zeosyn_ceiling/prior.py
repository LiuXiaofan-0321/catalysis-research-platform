"""Literature-prior helpers: per-OSDA pools of recipes, leave-own-paper-out counts, gel-space neighbours."""
from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np


def paper_ids(dois):
    """Loader's grouping rule: DOI, or a per-row group when the DOI is missing."""
    return np.array([d if d else f'row:{i}' for i, d in enumerate(dois)], dtype=object)


def build_pool(rows, keys, paper):
    """osda_key -> array of row indices (rows with an OSDA only)."""
    pool = defaultdict(list)
    for i in rows:
        if keys[i]:
            pool[keys[i]].append(i)
    return {k: np.array(v) for k, v in pool.items()}


def other_paper_rows(pool, key, own_paper, paper, allowed_mask=None):
    rows = pool.get(key)
    if rows is None or key is None:
        return np.array([], dtype=int)
    m = paper[rows] != own_paper
    if allowed_mask is not None:
        m &= allowed_mask[rows]
    return rows[m]


def modal(counter):
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def entropy_bits(counter):
    t = sum(counter.values())
    return -sum(c / t * math.log2(c / t) for c in counter.values()) if t else 0.0


def oracle_predictions(query_rows, pool, keys, paper, y, xgel, k_vote=5, allowed_mask=None):
    """For each query row: modal / 1-NN gel / k-NN-vote predictions from other-paper same-OSDA rows.

    xgel: standardized gel-composition matrix (all rows). Returns dict of arrays aligned to query_rows
    (None where not covered) plus support counts.
    """
    n = len(query_rows)
    pm, p1, pk = np.full(n, None, dtype=object), np.full(n, None, dtype=object), np.full(n, None, dtype=object)
    support = np.zeros(n, dtype=int)
    dist = [None] * n
    for j, i in enumerate(query_rows):
        others = other_paper_rows(pool, keys[i], paper[i], paper, allowed_mask)
        support[j] = len(others)
        if len(others) == 0:
            continue
        cnt = Counter(y[others])
        dist[j] = cnt
        pm[j] = modal(cnt)
        d = np.linalg.norm(xgel[others] - xgel[i], axis=1)
        order = np.argsort(d, kind='stable')
        p1[j] = y[others[order[0]]]
        kk = others[order[:k_vote]]
        ck = Counter(y[kk])
        best = max(ck.values())
        # ties -> the nearest among the tied classes
        pk[j] = next(y[r] for r in kk if ck[y[r]] == best)
    return {'modal': pm, 'nn1': p1, 'knn': pk, 'support': support, 'dist': dist}


def prior_block(query_rows, pool, keys, paper, y, top_classes, class_index, allowed_mask=None):
    """Per-recipe literature-prior feature block: top-K class probabilities, modal class id, support, entropy."""
    K = len(top_classes)
    tc = {c: j for j, c in enumerate(top_classes)}
    out = np.zeros((len(query_rows), K + 3))
    out[:, K] = -1.0
    for j, i in enumerate(query_rows):
        others = other_paper_rows(pool, keys[i], paper[i], paper, allowed_mask)
        if len(others) == 0:
            continue
        cnt = Counter(y[others])
        t = sum(cnt.values())
        for c, v in cnt.items():
            if c in tc:
                out[j, tc[c]] = v / t
        out[j, K] = class_index.get(modal(cnt), -1)
        out[j, K + 1] = t
        out[j, K + 2] = entropy_bits(cnt)
    return out


def dist_matrix(dists, classes):
    """Counter per row -> probability matrix over `classes` (uniform where no evidence)."""
    ci = {c: j for j, c in enumerate(classes)}
    P = np.full((len(dists), len(classes)), 1.0 / len(classes))
    for j, cnt in enumerate(dists):
        if not cnt:
            continue
        row = np.zeros(len(classes))
        t = 0
        for c, v in cnt.items():
            if c in ci:
                row[ci[c]] += v
            t += v
        if row.sum() > 0:
            P[j] = row / t  # classes unseen in training are dropped from the prior
    return P
