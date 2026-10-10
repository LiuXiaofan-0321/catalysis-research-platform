"""C. Reach of the real KG synthesis layer (data/kg_zeolite_v1) under the OSDA split, vs the oracle prior."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import OSDA_FOLDS, ROOT, acc, load_cache, load_results, log, save_results  # noqa: E402
from prior import build_pool, modal, oracle_predictions, paper_ids  # noqa: E402

from catalysis_research.knowledge import kg_synthesis as ks  # noqa: E402

KG = ROOT / 'data/kg_zeolite_v1'
records = ks.read_jsonl_gz(KG / 'synthesis_records.jsonl.gz')
links = {g: tuple(v) for g, v in json.loads((KG / 'osda_links.json').read_text()).items()}
display = json.loads((KG / 'osda_display.json').read_text())
vocab = json.loads((KG / 'framework_vocabulary.json').read_text())

c = load_cache()
meta, y = c['meta'], c['y']
keys = meta['osda_key'].tolist()
dois = meta['doi'].tolist()
paper = paper_ids(dois)
fold = c['osda_fold']
zeosyn_dois = {d for d in dois if d}
zeosyn_keys = {k for k in keys if k}
n = len(y)

out = {}
# ---------------- C1 counts
out['n_records'] = len(records)
out['n_records_with_product_code'] = int(sum(1 for r in records if r['products']))
out['n_records_multi_product'] = int(sum(1 for r in records if len(r['products']) > 1))
rec_keys = [sorted({links[m][0] for m in r['reagents'] if m in links}) for r in records]
linked = [bool(k) for k in rec_keys]
out['n_records_linked_to_zeosyn_osda'] = int(sum(linked))
out['n_records_linked_to_more_than_one_osda'] = int(sum(len(k) > 1 for k in rec_keys))
all_linked_keys = {k for ks_ in rec_keys for k in ks_}
out['n_distinct_zeosyn_osdas_linked'] = len(all_linked_keys)
out['n_distinct_zeosyn_osda1_keys_in_benchmark'] = len(zeosyn_keys)
out['n_linked_osdas_that_are_osda1_in_benchmark'] = len(all_linked_keys & zeosyn_keys)
out['n_records_with_doi'] = int(sum(1 for r in records if r['doi']))
out['n_papers'] = len({r['paper_id'] for r in records})
out['n_papers_with_doi'] = len({r['doi'] for r in records if r['doi']})
ext = [bool(r['doi']) and r['doi'] not in zeosyn_dois for r in records]
nodoi = [not r['doi'] for r in records]
out['share_records_doi_not_in_zeosyn'] = float(np.mean(ext))
out['share_records_without_doi'] = float(np.mean(nodoi))
out['share_records_doi_in_zeosyn'] = float(np.mean([bool(r['doi']) and r['doi'] in zeosyn_dois for r in records]))
lk = [i for i, l in enumerate(linked) if l]
out['linked_records_share_doi_not_in_zeosyn'] = float(np.mean([ext[i] for i in lk]))
out['linked_records_share_without_doi'] = float(np.mean([nodoi[i] for i in lk]))
out['n_papers_with_doi_in_zeosyn'] = len({r['doi'] for r in records if r['doi'] and r['doi'] in zeosyn_dois})
out['n_zeosyn_papers_total'] = len(zeosyn_dois)
# conditions
out['share_records_with'] = {
    'product_si_al': float(np.mean([r['product_si_al'] is not None for r in records])),
    'fluoride_flag_true': float(np.mean([r['fluoride'] for r in records])),
    'heteroatoms_nonempty': float(np.mean([bool(r['heteroatoms']) for r in records])),
    'temperature_c': float(np.mean([r['temperature_c'] is not None for r in records])),
    'time_h': float(np.mean([r['time_h'] is not None for r in records])),
    'any_of_si_al_temp_time': float(np.mean([(r['product_si_al'] is not None or r['temperature_c'] is not None or r['time_h'] is not None) for r in records])),
    'gel_composition': 0.0,
}
out['share_linked_records_with'] = {
    'product_si_al': float(np.mean([records[i]['product_si_al'] is not None for i in lk])),
    'fluoride_flag_true': float(np.mean([records[i]['fluoride'] for i in lk])),
    'heteroatoms_nonempty': float(np.mean([bool(records[i]['heteroatoms']) for i in lk])),
    'temperature_c': float(np.mean([records[i]['temperature_c'] is not None for i in lk])),
    'time_h': float(np.mean([records[i]['time_h'] is not None for i in lk])),
}
out['note_conditions'] = ('records carry no gel composition at all; fluoride/heteroatom are regex flags on free text, '
                          'product_si_al is a product-side attribute, temperature/time parsed from conditions')
# records per linked OSDA
per_osda = Counter(k for ks_ in rec_keys for k in ks_)
zs_count = Counter(k for k in keys if k)
rows = []
for k, v in per_osda.most_common(20):
    recs = [records[i] for i, ks_ in enumerate(rec_keys) if k in ks_]
    prods = Counter(p for r in recs for p in r['products'])
    rows.append({'osda_key': k, 'display': display.get(k, k), 'kg_records': v, 'kg_papers': len({r['paper_id'] for r in recs}),
                 'kg_modal_framework': modal(prods), 'kg_modal_share': prods[modal(prods)] / sum(prods.values()),
                 'kg_n_frameworks': len(prods), 'zeosyn_osda1_recipes': zs_count.get(k, 0)})
out['records_per_linked_osda_top20'] = rows
vals = np.array(list(per_osda.values()))
out['records_per_linked_osda'] = {'n_osdas': len(vals), 'median': float(np.median(vals)), 'mean': float(vals.mean()),
                                  'n_eq1': int((vals == 1).sum()), 'n_ge5': int((vals >= 5).sum()), 'n_ge20': int((vals >= 20).sum())}
# share of ZeoSyn recipes whose OSDA1 is linked at all (ignoring exclusions)
out['share_zeosyn_recipes_osda1_linked_any'] = float(np.mean([k in per_osda for k in keys]))
out['share_zeosyn_recipes_with_osda_whose_osda1_linked_any'] = float(np.mean([k in per_osda for k in keys if k]))


def kg_counts(excluded_dois, own_doi_exclusion=True):
    """osda_key -> list of (doi, products) for records not from excluded papers."""
    by = defaultdict(list)
    for r, ks_ in zip(records, rec_keys):
        if r['doi'] and r['doi'] in excluded_dois:
            continue
        for k in ks_:
            by[k].append((r['doi'], r['products']))
    return by


def kg_modal_for(by, key, own_doi):
    cnt = Counter()
    nrec = 0
    for doi, prods in by.get(key, []):
        if own_doi and doi == own_doi:
            continue
        nrec += 1
        cnt.update(prods)
    return (modal(cnt) if cnt else None), nrec, cnt


# ---------------- C1 per fold + C2 comparison
folds = {}
X_gel_cache = {}
d0_cols = list(c['d0_cols'])
gel_idx = [d0_cols.index(k) for k in c['gel_cols'] if k not in ('cryst_time', 'cryst_temp')]
for f in range(OSDA_FOLDS):
    te = np.flatnonzero(fold == f)
    tr = np.flatnonzero(fold != f)
    yte = y[te]
    test_dois = {dois[i] for i in te if dois[i]}
    variants = {}
    for vname, excl in (('exclude_fold_test_papers', test_dois), ('exclude_own_paper_only', set())):
        by = kg_counts(excl)
        pred, nrec, in_support = np.full(len(te), None, dtype=object), np.zeros(len(te), int), np.zeros(len(te), bool)
        for j, i in enumerate(te):
            p, nr, cnt = kg_modal_for(by, keys[i], dois[i])
            pred[j], nrec[j] = p, nr
            in_support[j] = yte[j] in cnt
        cov = nrec > 0
        V = {'coverage': float(cov.mean()), 'covered_rows': int(cov.sum()), 'covered_osdas': len({keys[i] for i in te[cov]}),
             'kg_modal_acc_covered': acc(yte[cov], pred[cov]),
             'true_class_in_kg_support_share_covered': float(in_support[cov].mean()) if cov.any() else None,
             'kg_records_per_covered_recipe_median': float(np.median(nrec[cov])) if cov.any() else None,
             'pred': pred, 'cov': cov, 'nrec': nrec}
        variants[vname] = V
    # oracle on the same rows (other-paper test recipes), two information conditions
    X = c[f'd0_osda_f{f}'] if f'd0_osda_f{f}' in c else c['d0_paper']
    mu, sd = X[tr].mean(0), X[tr].std(0)
    sd[sd == 0] = 1
    Z = ((X - mu) / sd)[:, gel_idx]
    pool_te = build_pool(te, keys, paper)
    orc_own = oracle_predictions(te, pool_te, keys, paper, y, Z)  # exclude own paper only
    orc_cov = orc_own['support'] > 0
    R = {'test_rows': int(len(te)), 'test_osdas': len({keys[i] for i in te})}
    for vname, V in variants.items():
        cov = V['cov']
        both = cov & orc_cov
        R[vname] = {k: v for k, v in V.items() if k not in ('pred', 'cov', 'nrec')}
        R[vname]['rows_covered_by_both_kg_and_oracle'] = int(both.sum())
        R[vname]['kg_modal_acc_on_both'] = acc(yte[both], V['pred'][both])
        R[vname]['oracle_modal_acc_on_both'] = acc(yte[both], orc_own['modal'][both])
        R[vname]['oracle_nn1_gel_acc_on_both'] = acc(yte[both], orc_own['nn1'][both])
        R[vname]['agreement_kg_vs_oracle_modal_on_both'] = float(np.mean(V['pred'][both] == orc_own['modal'][both])) if both.any() else None
        R[vname]['oracle_modal_acc_on_kg_uncovered_but_oracle_covered'] = acc(yte[~cov & orc_cov], orc_own['modal'][~cov & orc_cov])
        R[vname]['rows_kg_uncovered_but_oracle_covered'] = int((~cov & orc_cov).sum())
        R[vname]['rows_kg_covered_but_oracle_uncovered'] = int((cov & ~orc_cov).sum())
    R['oracle_own_paper_excluded_coverage'] = float(orc_cov.mean())
    R['oracle_own_paper_excluded_modal_acc_covered'] = acc(yte[orc_cov], orc_own['modal'][orc_cov])
    # per-OSDA table for the 20 most frequent covered OSDAs (fold-test-paper exclusion variant)
    V = variants['exclude_fold_test_papers']
    by_k = defaultdict(list)
    for j, i in enumerate(te):
        if V['cov'][j]:
            by_k[keys[i]].append(j)
    table = []
    for k, js in sorted(by_k.items(), key=lambda kv: -len(kv[1]))[:20]:
        truth = Counter(yte[js])
        kgpred = Counter(V['pred'][js]).most_common(1)[0][0]
        table.append({'osda_key': k, 'display': display.get(k, k), 'n_test_recipes': len(js),
                      'kg_records': int(np.median(V['nrec'][js])), 'kg_modal_framework': kgpred,
                      'true_modal_framework_in_test': modal(truth), 'true_modal_share': truth[modal(truth)] / len(js),
                      'agreement': kgpred == modal(truth), 'kg_modal_accuracy_on_these_recipes': acc(yte[js], V['pred'][js]),
                      'oracle_modal_acc_on_these_recipes': acc(yte[js], orc_own['modal'][js])})
    R['per_osda_top20_exclude_fold_test_papers'] = table
    folds[str(f)] = R
    log(f'fold {f}: KG cov(excl fold papers)={R["exclude_fold_test_papers"]["coverage"]:.3f} '
        f'acc={R["exclude_fold_test_papers"]["kg_modal_acc_covered"]:.3f}; KG cov(own only)={R["exclude_own_paper_only"]["coverage"]:.3f} '
        f'acc={R["exclude_own_paper_only"]["kg_modal_acc_covered"]:.3f}; oracle modal on both={R["exclude_fold_test_papers"]["oracle_modal_acc_on_both"]:.3f}')
    del X, Z
out['folds'] = folds
# fold means (recipe-weighted)
w = np.array([folds[str(f)]['test_rows'] for f in range(OSDA_FOLDS)], float)
summary = {}
for vname in ('exclude_fold_test_papers', 'exclude_own_paper_only'):
    for key in ('coverage', 'kg_modal_acc_covered', 'kg_modal_acc_on_both', 'oracle_modal_acc_on_both', 'oracle_nn1_gel_acc_on_both',
                'true_class_in_kg_support_share_covered', 'oracle_modal_acc_on_kg_uncovered_but_oracle_covered'):
        vals = [folds[str(f)][vname][key] for f in range(OSDA_FOLDS)]
        vals = [v if v is not None and v == v else np.nan for v in vals]
        summary[f'{vname}__{key}'] = {'mean': float(np.nanmean(vals)), 'recipe_weighted_mean': float(np.nansum(np.array(vals) * w) / w[~np.isnan(vals)].sum())}
    summary[f'{vname}__covered_osdas'] = [folds[str(f)][vname]['covered_osdas'] for f in range(OSDA_FOLDS)]
out['summary'] = summary
save_results('C', out)
log('C done')
print(json.dumps({k: v for k, v in out.items() if k not in ('folds', 'records_per_linked_osda_top20')}, indent=1, default=str)[:3000])
