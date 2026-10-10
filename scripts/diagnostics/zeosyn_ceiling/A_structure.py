"""A. Dataset structure and OSDA -> framework determinism (in-sample and leave-own-paper-out)."""
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from common import load_cache, log, save_results  # noqa: E402

c = load_cache()
meta, y, gel_raw, gel_cols = c['meta'], c['y'], c['gel_raw'], list(c['gel_cols'])
n = len(y)
col = {k: i for i, k in enumerate(gel_cols)}
keys = meta['osda_key'].tolist()
dois = meta['doi'].tolist()
paper = np.array([d if d else f'row:{i}' for i, d in enumerate(dois)], dtype=object)  # loader's grouping rule

out = {}
# ---------------- A1
classes = Counter(y)
osda_counts = Counter(k for k in keys if k)
out['n_recipes'] = n
out['n_papers_with_doi'] = len({d for d in dois if d})
out['n_rows_without_doi'] = int(sum(1 for d in dois if not d))
out['n_classes_incl_failed'] = len(classes)
out['n_failed'] = int(classes.get('Failed', 0))
out['class_top20'] = [{'class': k, 'n': v, 'share': v / n} for k, v in classes.most_common(20)]
out['n_classes_lt10'] = int(sum(1 for v in classes.values() if v < 10))
out['n_classes_lt5'] = int(sum(1 for v in classes.values() if v < 5))
out['n_distinct_osda1_keys'] = len(osda_counts)
out['n_distinct_osda1_smiles'] = len({s for s in meta['osda1_smiles'] if s})
out['share_no_osda'] = float(np.mean([k is None for k in keys]))
out['n_no_osda'] = int(sum(k is None for k in keys))
display = {}
for k in osda_counts:
    names = Counter(meta['osda1'][i] for i in range(n) if keys[i] == k and meta['osda1'][i])
    display[k] = names.most_common(1)[0][0] if names else k
rows = []
for k, cnt in osda_counts.most_common(20):
    fw = Counter(y[i] for i in range(n) if keys[i] == k)
    top, topn = fw.most_common(1)[0]
    npap = len({paper[i] for i in range(n) if keys[i] == k})
    rows.append({'osda_key': k, 'name': display[k], 'n_recipes': cnt, 'n_papers': npap,
                 'dominant_framework': top, 'dominant_share': topn / cnt, 'n_frameworks': len(fw)})
out['osda_top20'] = rows
vals = np.array(sorted(osda_counts.values()))
out['recipes_per_osda'] = {'mean': float(vals.mean()), 'median': float(np.median(vals)),
                           'p90': float(np.percentile(vals, 90)), 'max': int(vals.max()),
                           'n_osda_eq1': int((vals == 1).sum()), 'n_osda_lt5': int((vals < 5).sum()),
                           'n_osda_ge5': int((vals >= 5).sum()), 'n_osda_ge20': int((vals >= 20).sum()),
                           'share_recipes_in_osda_ge5': float(vals[vals >= 5].sum() / vals.sum()),
                           'share_recipes_in_osda_ge20': float(vals[vals >= 20].sum() / vals.sum()),
                           'share_recipes_in_top20_osda': float(sum(v for _, v in osda_counts.most_common(20)) / vals.sum())}
# no-OSDA recipes: what are they?
no = [i for i in range(n) if keys[i] is None]
out['no_osda_class_top10'] = Counter(y[i] for i in no).most_common(10)

# ---------------- A2 determinism
Si, Al, F = gel_raw[:, col['Si']], gel_raw[:, col['Al']], gel_raw[:, col['F']]
HETERO = ['P', 'Ge', 'Ti', 'B', 'Ga', 'Zn', 'Sn', 'Zr', 'V', 'Be', 'W', 'Cu']
het = np.nansum(gel_raw[:, [col[h] for h in HETERO]], axis=1)


def sial_bin(si, al):
    if np.isnan(si) or np.isnan(al):
        return 'unknown'
    if al <= 0:
        return 'Al=0' if si > 0 else 'Si=0,Al=0'
    r = si / al
    for edge, name in ((2, '<=2'), (5, '2-5'), (15, '5-15'), (50, '15-50'), (200, '50-200')):
        if r <= edge:
            return name
    return '>200'


sial = np.array([sial_bin(Si[i], Al[i]) for i in range(n)], dtype=object)
fpres = np.where(np.isnan(F), 'F?', np.where(F > 0, 'F', 'noF'))
hpres = np.where(np.isnan(het), 'H?', np.where(het > 0, 'het', 'nohet'))
out['si_al_bin_counts'] = dict(Counter(sial))
out['f_present_counts'] = dict(Counter(fpres))
out['hetero_present_counts'] = dict(Counter(hpres))
out['hetero_elements'] = HETERO


def determinism(group_key, min_count=5, label=''):
    """In-sample modal-rule accuracy and leave-own-paper-out modal-rule accuracy over recipes with an OSDA."""
    groups = defaultdict(list)
    for i in range(n):
        if keys[i]:
            groups[group_key(i)].append(i)
    cov_rows = [i for g, idx in groups.items() if len(idx) >= min_count for i in idx]
    # in-sample modal share, recipe-weighted
    ins_hits = 0
    modal_share = []
    for g, idx in groups.items():
        if len(idx) < min_count:
            continue
        cnt = Counter(y[i] for i in idx)
        top = cnt.most_common(1)[0][1]
        ins_hits += top
        modal_share.append(top / len(idx))
    # leave-own-paper-out: predict modal of other-paper recipes in same group
    lopo_hits, lopo_cov = 0, 0
    lopo_hits_all, lopo_cov_all = 0, 0
    for g, idx in groups.items():
        by_paper = defaultdict(Counter)
        for i in idx:
            by_paper[paper[i]][y[i]] += 1
        total = Counter()
        for cnt in by_paper.values():
            total.update(cnt)
        for i in idx:
            others = total.copy()
            others.subtract(by_paper[paper[i]])
            others = +others
            if not others:
                continue
            pred = sorted(others.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
            hit = int(pred == y[i])
            lopo_hits_all += hit
            lopo_cov_all += 1
            if len(idx) >= min_count:
                lopo_hits += hit
                lopo_cov += 1
    n_with_osda = sum(1 for k in keys if k)
    return {
        'label': label, 'n_groups': len(groups), 'n_groups_ge_min': int(sum(len(v) >= min_count for v in groups.values())),
        'min_count': min_count,
        'recipes_in_groups_ge_min': len(cov_rows), 'share_recipes_in_groups_ge_min': len(cov_rows) / n_with_osda,
        'in_sample_modal_accuracy_ge_min': ins_hits / max(1, len(cov_rows)),
        'in_sample_modal_share_unweighted_mean_ge_min': float(np.mean(modal_share)) if modal_share else None,
        'lopo_modal_accuracy_ge_min': lopo_hits / max(1, lopo_cov), 'lopo_covered_ge_min': lopo_cov,
        'lopo_modal_accuracy_all_covered': lopo_hits_all / max(1, lopo_cov_all), 'lopo_covered_all': lopo_cov_all,
        'lopo_coverage_all_share_of_osda_recipes': lopo_cov_all / n_with_osda,
        'lopo_accuracy_over_all_osda_recipes_uncovered_as_wrong': lopo_hits_all / n_with_osda,
    }


out['determinism'] = {
    'osda': determinism(lambda i: keys[i], 5, 'OSDA key'),
    'osda_sial': determinism(lambda i: (keys[i], sial[i]), 5, 'OSDA + Si/Al bin'),
    'osda_sial_F_het': determinism(lambda i: (keys[i], sial[i], fpres[i], hpres[i]), 5, 'OSDA + Si/Al bin + F + heteroatom'),
    'osda_min2': determinism(lambda i: keys[i], 2, 'OSDA key (groups >=2)'),
    'osda_sial_F_het_min2': determinism(lambda i: (keys[i], sial[i], fpres[i], hpres[i]), 2, 'OSDA + Si/Al bin + F + heteroatom (groups >=2)'),
}
# in-sample modal accuracy over ALL recipes (OSDA-only rule + no-OSDA modal)
hits = 0
groups = defaultdict(Counter)
for i in range(n):
    groups[keys[i]][y[i]] += 1
for g, cnt in groups.items():
    hits += cnt.most_common(1)[0][1]
out['in_sample_modal_per_osda_accuracy_all_rows_incl_no_osda_group'] = hits / n
# how many OSDAs appear in only one paper
one_paper = sum(1 for k in osda_counts if len({paper[i] for i in range(n) if keys[i] == k}) == 1)
out['n_osda_in_single_paper'] = int(one_paper)
out['share_osda_recipes_whose_osda_appears_in_single_paper'] = float(sum(
    osda_counts[k] for k in osda_counts if len({paper[i] for i in range(n) if keys[i] == k}) == 1) / sum(osda_counts.values()))
save_results('A', out)
log('A done')
print(pd.DataFrame(out['osda_top20']).to_string())
for k, v in out['determinism'].items():
    print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})
print({k: v for k, v in out.items() if not isinstance(v, (list, dict))})
