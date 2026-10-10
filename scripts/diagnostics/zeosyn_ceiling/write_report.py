"""Render ceiling/REPORT.md from ceiling/results.json."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import OUT, RESULTS  # noqa: E402

R = json.loads(RESULTS.read_text())
L = []
P = L.append


def pct(x, d=1):
    return 'n/a' if x is None or x != x else f'{100 * x:.{d}f}'


def table(header, rows):
    P('| ' + ' | '.join(header) + ' |')
    P('|' + '|'.join(['---'] * len(header)) + '|')
    for r in rows:
        P('| ' + ' | '.join(str(v) for v in r) + ' |')
    P('')


P('# ZeoSyn framework prediction: headroom for a literature-knowledge channel')
P('')
P('All numbers computed on the real data with the repo loader (`src/catalysis_research/benchmarks/zeosyn.py`): '
  'native row selection (`native_frame`), label = `Code1` with missing -> `Failed`, D0 = the loader\'s 43 columns '
  '(`GEL_INPUTS` 27 + `CONDITION_INPUTS` 2 + `NATIVE_OSDA_D0` 14), `IterativeImputer` fit on training rows only '
  '(re-fit per fold for the OSDA split). OSDA identity = InChIKey of `osda1 smiles` from '
  '`data/kg_zeolite_v1/zeosyn_osda_keys.json` (the key the V2 runner uses). Paper identity = normalized `doi`, rows without a '
  'DOI are their own paper (loader rule). RandomForest: 60 trees, `max_features=sqrt`, full depth, 2 fit seeds (3, 7), '
  'mean reported. Scripts and raw results: `ceiling/*.py`, `ceiling/results.json`.')
P('')

# ---------------- A
A = R.get('A')
if A:
    P('## A. Dataset structure')
    P('')
    P(f"- Recipes: **{A['n_recipes']}**; papers with a DOI: **{A['n_papers_with_doi']}** (+{A['n_rows_without_doi']} rows without DOI, each its own group).")
    P(f"- Classes (IZA code incl. `Failed`): **{A['n_classes_incl_failed']}**; `Failed` = {A['n_failed']} recipes ({pct(A['n_failed'] / A['n_recipes'])}%). "
      f"Classes with < 10 recipes: **{A['n_classes_lt10']}**; with < 5: {A['n_classes_lt5']}.")
    P(f"- Distinct OSDA1 keys (InChIKey): **{A['n_distinct_osda1_keys']}** (distinct SMILES strings: {A['n_distinct_osda1_smiles']}). "
      f"Recipes without an OSDA1: **{A['n_no_osda']}** ({pct(A['share_no_osda'])}%); their top classes: {A['no_osda_class_top10'][:5]}.")
    r = A['recipes_per_osda']
    P(f"- Recipes per OSDA: median {r['median']:.0f}, mean {r['mean']:.1f}, p90 {r['p90']:.0f}, max {r['max']}. "
      f"OSDAs with 1 recipe: {r['n_osda_eq1']}; < 5: {r['n_osda_lt5']}; >= 5: {r['n_osda_ge5']}; >= 20: {r['n_osda_ge20']}. "
      f"Share of OSDA recipes in OSDAs with >= 5 recipes: {pct(r['share_recipes_in_osda_ge5'])}%; >= 20: {pct(r['share_recipes_in_osda_ge20'])}%; top-20 OSDAs: {pct(r['share_recipes_in_top20_osda'])}%.")
    P(f"- OSDAs that occur in a single paper: {A['n_osda_in_single_paper']} ({pct(A['share_osda_recipes_whose_osda_appears_in_single_paper'])}% of OSDA recipes). "
      'For these, no literature prior from *other* papers can exist.')
    P('')
    P('### Class frequency (top 20)')
    P('')
    table(['class', 'n', 'share %'], [(c['class'], c['n'], pct(c['share'])) for c in A['class_top20']])
    P('### Top-20 OSDAs (by OSDA1 key)')
    P('')
    table(['OSDA (most common ZeoSyn name)', 'recipes', 'papers', 'dominant framework', 'share %', '# frameworks'],
          [(o['name'], o['n_recipes'], o['n_papers'], o['dominant_framework'], pct(o['dominant_share']), o['n_frameworks']) for o in A['osda_top20']])
    P('### A2. How deterministic is OSDA -> framework?')
    P('')
    P('Conditioning keys: Si/Al bin from raw gel `Si`/`Al` (`Al=0`, `<=2`, `2-5`, `5-15`, `15-50`, `50-200`, `>200`, `unknown`), '
      'F present = raw `F` > 0, heteroatom present = any of ' + ', '.join(A['hetero_elements']) + ' > 0. '
      '"In-sample" = accuracy of the modal-class rule evaluated on the recipes it was built from (groups with >= `min` recipes). '
      '"LOPO" = leave-own-paper-out: each recipe is predicted by the modal class of the *other-paper* recipes of its group '
      '(this is the honest version of an in-dataset literature oracle; coverage = recipes with at least one other-paper recipe in the group).')
    P('')
    rows = []
    for k, d in A['determinism'].items():
        rows.append((d['label'], d['min_count'], d['n_groups'], d['n_groups_ge_min'], pct(d['share_recipes_in_groups_ge_min']),
                     pct(d['in_sample_modal_accuracy_ge_min']), pct(d['lopo_modal_accuracy_ge_min']), d['lopo_covered_ge_min'],
                     pct(d['lopo_coverage_all_share_of_osda_recipes']), pct(d['lopo_modal_accuracy_all_covered']),
                     pct(d['lopo_accuracy_over_all_osda_recipes_uncovered_as_wrong'])))
    table(['grouping', 'min', '# groups', '# groups >= min', 'OSDA recipes in groups >= min %', 'in-sample modal acc % (>= min)',
           'LOPO modal acc % (>= min)', 'LOPO covered (>= min)', 'LOPO coverage % (all groups)', 'LOPO acc % on covered (all groups)',
           'LOPO acc % over all OSDA recipes (uncovered = wrong)'], rows)
    P(f"In-sample modal-per-OSDA accuracy over *all* {A['n_recipes']} rows (no-OSDA rows as one group): "
      f"**{pct(A['in_sample_modal_per_osda_accuracy_all_rows_incl_no_osda_group'])}%**.")
    P('')
    P(f"Si/Al bins: {A['si_al_bin_counts']}; F: {A['f_present_counts']}; heteroatom: {A['hetero_present_counts']}.")
    P('')

# ---------------- B1
B1 = R.get('B1')
if B1:
    P('## B1. Paper (DOI-group) split, seed 20261007, 20 % test')
    P('')
    P(f"Train {B1['train_rows']} / test {B1['test_rows']} rows. Global modal class in training: `{B1['global_modal_class_train']}`.")
    P('')
    t = B1['trivial_train_modal_per_osda']
    table(['model', 'accuracy %', 'balanced acc %', 'macro-F1 %'], [
        ('RF D0 (60 trees, mean of 2 seeds)', pct(B1['rf_d0']['mean']['accuracy']), pct(B1['rf_d0']['mean']['balanced_accuracy']), pct(B1['rf_d0']['mean']['macro_f1'])),
        ('training-modal framework per OSDA (fallback global modal)', pct(t['accuracy']), pct(t['balanced_accuracy']), pct(t['macro_f1'])),
        ('1-NN in standardized D0', pct(B1['nn1_d0_standardized']['accuracy']), pct(B1['nn1_d0_standardized']['balanced_accuracy']), pct(B1['nn1_d0_standardized']['macro_f1'])),
        ('global modal class', pct(B1['global_modal_accuracy']), '', ''),
    ])
    P(f"- Test rows whose OSDA1 was seen in training: {t['test_rows_with_osda_seen_in_train']} ({pct(t['share_test_rows_with_osda_seen_in_train'])}%); "
      f"rows with any OSDA: {pct(t['share_test_rows_with_osda'])}%.")
    P(f"- On seen-OSDA rows: trivial rule {pct(t['accuracy_on_seen_osda_rows'])}% vs RF D0 {pct(t['rf_d0_accuracy_on_seen_osda_rows_mean'])}%. "
      f"On unseen/no-OSDA rows: trivial {pct(t['accuracy_on_unseen_or_no_osda_rows'])}% vs RF D0 {pct(t['rf_d0_accuracy_on_unseen_or_no_osda_rows_mean'])}%.")
    P('')

# ---------------- B2-4
B = R.get('B_osda')
if B and B.get('folds'):
    P('## B2-B4. OSDA-group split (GroupKFold on OSDA1 key, 5 folds, shuffle seed 1; no-OSDA rows always train)')
    P('')
    F = B['folds']
    fids = sorted(F, key=int)
    P('### B2. Baselines per fold')
    P('')
    rows = []
    for f in fids:
        d = F[f]
        rows.append((f, d['test_rows'], d['test_osdas'], pct(d['rf_d0']['mean']['accuracy']), pct(d['rf_d0']['mean']['balanced_accuracy']),
                     pct(d['rf_d0']['mean']['macro_f1']), f"{d['global_modal_class']} {pct(d['global_modal_accuracy'])}",
                     pct(d['nn1_osda_desc30']['accuracy']), pct(d['nn1_osda_desc_full']['accuracy'])))
    if B.get('summary'):
        S = B['summary']
        rows.append(('mean', '', '', pct(S['rf_d0_accuracy']['mean']), pct(S['rf_d0_balanced_accuracy']['mean']), pct(S['rf_d0_macro_f1']['mean']),
                     pct(S['global_modal_accuracy']['mean']), pct(S['nn1_osda_desc30_accuracy']['mean']), pct(S['nn1_osda_desc_full_accuracy']['mean'])))
        rows.append(('recipe-weighted mean', '', '', pct(S['rf_d0_accuracy']['recipe_weighted_mean']), pct(S['rf_d0_balanced_accuracy']['recipe_weighted_mean']),
                     pct(S['rf_d0_macro_f1']['recipe_weighted_mean']), pct(S['global_modal_accuracy']['recipe_weighted_mean']),
                     pct(S['nn1_osda_desc30_accuracy']['recipe_weighted_mean']), pct(S['nn1_osda_desc_full_accuracy']['recipe_weighted_mean'])))
    table(['fold', 'test rows', 'test OSDAs', 'RF D0 acc %', 'RF D0 bal-acc %', 'RF D0 macro-F1 %', 'global modal (class, acc %)',
           '1-NN OSDA desc (30 scalar) acc %', '1-NN OSDA desc (455+11 full) acc %'], rows)
    P('1-NN OSDA descriptor space: per-OSDA vector = the 19 scalar conformer descriptors exposed by the loader (`OSDA_TABLE_INPUTS`) + 11 RDKit counts (`RDKIT_INPUTS`), '
      'or every numeric column of `osda_descriptors.csv` (incl. box/getaway/whim vectors) + 11 RDKit counts; standardized on training OSDAs, zero-variance dims dropped; '
      'prediction = modal framework of the nearest training OSDA (among its training recipes).')
    P('')
    P('### B3. Oracle literature prior (other-paper test recipes with the same OSDA)')
    P('')
    P('For a test recipe with OSDA o, the "literature" is every other test recipe with OSDA o from a different paper (own paper left out). '
      'Predictions: (a) modal framework; (b) framework of the nearest such recipe in standardized gel space (27 `GEL_INPUTS` of D0, standardized on fold-training rows); '
      '(b\') same with `cryst_time`/`cryst_temp` added; (c) majority of the 5 nearest (ties -> nearest). "Overall" = oracle where covered, RF D0 elsewhere.')
    P('')
    rows = []
    for f in fids:
        d = F[f]
        o = d['oracle']
        rows.append((f, pct(o['coverage']), o['covered_osdas'], pct(o['coverage_ge3']), pct(d['rf_d0_acc_covered']), pct(d['rf_d0_acc_uncovered']),
                     pct(o['modal']['acc_covered']), pct(o['nn1_gel']['acc_covered']), pct(o['nn1_gel_plus_conditions']['acc_covered']), pct(o['knn5_gel']['acc_covered']),
                     pct(o['true_class_in_other_paper_support_share_covered']),
                     pct(d['rf_d0']['mean']['accuracy']), pct(o['modal']['overall_oracle_where_covered_else_rf_d0']['accuracy']),
                     pct(o['nn1_gel']['overall_oracle_where_covered_else_rf_d0']['accuracy']), pct(o['knn5_gel']['overall_oracle_where_covered_else_rf_d0']['accuracy'])))
    if B.get('summary'):
        S = B['summary']
        rows.append(('mean', pct(S['oracle_coverage']['mean']), '', pct(S['oracle_coverage_ge3']['mean']), pct(S['rf_d0_acc_covered']['mean']), pct(S['rf_d0_acc_uncovered']['mean']),
                     pct(S['oracle_modal_acc_covered']['mean']), pct(S['oracle_nn1_gel_acc_covered']['mean']), pct(S['oracle_nn1_gelcond_acc_covered']['mean']),
                     pct(S['oracle_knn5_gel_acc_covered']['mean']), pct(S['true_class_in_support_covered']['mean']), pct(S['rf_d0_accuracy']['mean']),
                     pct(S['overall_modal_else_d0']['mean']), pct(S['overall_nn1_gel_else_d0']['mean']), pct(S['overall_knn5_gel_else_d0']['mean'])))
        rows.append(('recipe-weighted mean', pct(S['oracle_coverage']['recipe_weighted_mean']), '', pct(S['oracle_coverage_ge3']['recipe_weighted_mean']),
                     pct(S['rf_d0_acc_covered']['recipe_weighted_mean']), pct(S['rf_d0_acc_uncovered']['recipe_weighted_mean']),
                     pct(S['oracle_modal_acc_covered']['recipe_weighted_mean']), pct(S['oracle_nn1_gel_acc_covered']['recipe_weighted_mean']),
                     pct(S['oracle_nn1_gelcond_acc_covered']['recipe_weighted_mean']), pct(S['oracle_knn5_gel_acc_covered']['recipe_weighted_mean']),
                     pct(S['true_class_in_support_covered']['recipe_weighted_mean']), pct(S['rf_d0_accuracy']['recipe_weighted_mean']),
                     pct(S['overall_modal_else_d0']['recipe_weighted_mean']), pct(S['overall_nn1_gel_else_d0']['recipe_weighted_mean']),
                     pct(S['overall_knn5_gel_else_d0']['recipe_weighted_mean'])))
    table(['fold', 'coverage %', 'covered OSDAs', 'coverage (>=3 other-paper recipes) %', 'RF D0 acc on covered %', 'RF D0 acc on uncovered %',
           'oracle (a) modal %', 'oracle (b) 1-NN gel %', "oracle (b') 1-NN gel+cond %", 'oracle (c) 5-NN vote %', 'true class in oracle support %',
           'RF D0 overall %', 'overall (a)+D0 %', 'overall (b)+D0 %', 'overall (c)+D0 %'], rows)
    P('Long tail: restricted to recipes whose OSDA has >= 3 other-paper recipes vs. only 1-2:')
    P('')
    rows = []
    for f in fids:
        o = F[f]['oracle']
        rows.append((f, o['covered_rows'], o['covered_rows_ge3'], pct(F[f]['rf_d0_acc_covered_ge3']), pct(o['modal']['acc_covered_ge3']), pct(o['nn1_gel']['acc_covered_ge3']),
                     pct(o['knn5_gel']['acc_covered_ge3']), pct(o['modal']['acc_covered_support_1_2']), pct(o['nn1_gel']['acc_covered_support_1_2']),
                     pct(o['true_class_in_other_paper_support_share_covered_ge3']),
                     pct(o['modal']['overall_oracle_where_support_ge3_else_rf_d0']['accuracy']), pct(o['nn1_gel']['overall_oracle_where_support_ge3_else_rf_d0']['accuracy']),
                     {k: round(v) for k, v in o['support_quantiles'].items()}))
    table(['fold', 'covered rows', 'rows with support >= 3', 'RF D0 acc (support >= 3) %', 'modal acc (>= 3) %', '1-NN gel acc (>= 3) %', '5-NN acc (>= 3) %',
           'modal acc (support 1-2) %', '1-NN gel acc (support 1-2) %', 'true class in support (>= 3) %', 'overall modal(>=3)+D0 %', 'overall 1-NN(>=3)+D0 %',
           'support quantiles (p10/25/50/75/90)'], rows)
    P('### B4. Combining the oracle prior with the RF')
    P('')
    P('Prior block (13 columns): per-recipe probability of each of the 10 most frequent training classes among other-paper same-OSDA recipes, '
      'modal class id (index into fold-training classes, -1 = none), support count, Shannon entropy (bits). Training recipes: other-paper recipes of the same OSDA '
      '*within the training rows* (leave-own-paper-out); test recipes: other-paper test recipes (as in B3). Product rule: RF D0 class probabilities x (prior + eps), '
      'prior = other-paper class distribution (or 5-nearest-in-gel distribution), uniform where uncovered.')
    P('')
    rows = []
    for f in fids:
        d = F[f]
        pr = d['rf_d0_plus_prior']
        rows.append((f, pct(d['rf_d0']['mean']['accuracy']), pct(pr['mean']['accuracy']), f"{100 * pr['delta_vs_d0']['accuracy']:+.1f}",
                     pct(pr['mean']['balanced_accuracy']), pct(pr['mean']['macro_f1']),
                     pct(d['rf_d0_acc_covered']), pct(pr['acc_covered']), pct(d['rf_d0_acc_uncovered']), pct(pr['acc_uncovered']),
                     pct(d['rf_prior_block_only']['mean']['accuracy']), pct(d['prior_block']['train_rows_covered_share'])))
    if B.get('summary'):
        S = B['summary']
        rows.append(('mean', pct(S['rf_d0_accuracy']['mean']), pct(S['rf_d0_plus_prior_accuracy']['mean']),
                     f"{100 * (S['rf_d0_plus_prior_accuracy']['mean'] - S['rf_d0_accuracy']['mean']):+.1f}",
                     pct(S['rf_d0_plus_prior_balanced_accuracy']['mean']), pct(S['rf_d0_plus_prior_macro_f1']['mean']),
                     pct(S['rf_d0_acc_covered']['mean']), pct(S['rf_d0_plus_prior_acc_covered']['mean']), pct(S['rf_d0_acc_uncovered']['mean']),
                     pct(S['rf_d0_plus_prior_acc_uncovered']['mean']), pct(S['rf_prior_only_accuracy']['mean']), ''))
    table(['fold', 'RF D0 acc %', 'RF D0+prior acc %', 'delta pp', 'D0+prior bal-acc %', 'D0+prior macro-F1 %', 'D0 acc covered %', 'D0+prior acc covered %',
           'D0 acc uncovered %', 'D0+prior acc uncovered %', 'RF prior-block only acc %', 'train rows covered %'], rows)
    P('Product rule (accuracy %, overall / on covered rows), per eps:')
    P('')
    header = ['fold', 'RF D0'] + [f'dist eps={e}' for e in B['eps_grid']] + [f'5-NN eps={e}' for e in B['eps_grid']]
    rows = []
    for f in fids:
        d = F[f]
        row = [f, f"{pct(d['rf_d0']['mean']['accuracy'])} / {pct(d['rf_d0_acc_covered'])}"]
        for pname in ('distribution_prior', 'knn5_gel_prior'):
            for e in B['eps_grid']:
                q = d['product_rule'][f'{pname}_eps{e}']
                row.append(f"{pct(q['accuracy'])} / {pct(q['acc_covered'])}")
        rows.append(row)
    if B.get('summary'):
        S = B['summary']
        row = ['mean', f"{pct(S['rf_d0_accuracy']['mean'])} / {pct(S['rf_d0_acc_covered']['mean'])}"]
        for pname in ('distribution_prior', 'knn5_gel_prior'):
            for e in B['eps_grid']:
                row.append(f"{pct(S[f'product_{pname}_eps{e}_accuracy']['mean'])} / {pct(S[f'product_{pname}_eps{e}_acc_covered']['mean'])}")
        rows.append(row)
    table(header, rows)

# ---------------- C
C = R.get('C')
if C:
    P('## C. The real KG synthesis layer (`data/kg_zeolite_v1`)')
    P('')
    P(f"- Synthesis records: **{C['n_records']}** (all carry >= 1 product framework code by construction: {C['n_records_with_product_code']}; "
      f"{C['n_records_multi_product']} list more than one product). Papers: {C['n_papers']} ({C['n_papers_with_doi']} with DOI); records with a DOI: {C['n_records_with_doi']}.")
    P(f"- Records linked to a ZeoSyn OSDA (via `osda_links.json`): **{C['n_records_linked_to_zeosyn_osda']}** ({C['n_records_linked_to_more_than_one_osda']} linked to > 1 OSDA); "
      f"distinct linked OSDAs: **{C['n_distinct_zeosyn_osdas_linked']}**, of which {C['n_linked_osdas_that_are_osda1_in_benchmark']} occur as OSDA1 in the benchmark "
      f"(benchmark has {C['n_distinct_zeosyn_osda1_keys_in_benchmark']} distinct OSDA1 keys).")
    P(f"- ZeoSyn recipes whose OSDA1 is linked at all (before any paper exclusion): {pct(C['share_zeosyn_recipes_osda1_linked_any'])}% of all recipes, "
      f"{pct(C['share_zeosyn_recipes_with_osda_whose_osda1_linked_any'])}% of recipes with an OSDA.")
    P(f"- Records whose paper DOI is NOT a ZeoSyn DOI (external): **{pct(C['share_records_doi_not_in_zeosyn'])}%**; in ZeoSyn: {pct(C['share_records_doi_in_zeosyn'])}%; "
      f"no DOI: {pct(C['share_records_without_doi'])}%. Among OSDA-linked records: external {pct(C['linked_records_share_doi_not_in_zeosyn'])}%, no DOI {pct(C['linked_records_share_without_doi'])}%. "
      f"KG papers that are ZeoSyn papers: {C['n_papers_with_doi_in_zeosyn']} of {C['n_zeosyn_papers_total']} ZeoSyn DOIs.")
    r = C['records_per_linked_osda']
    P(f"- Records per linked OSDA: n={r['n_osdas']}, median {r['median']:.0f}, mean {r['mean']:.1f}; with 1 record: {r['n_eq1']}, >= 5: {r['n_ge5']}, >= 20: {r['n_ge20']}.")
    s = C['share_records_with']
    sl = C['share_linked_records_with']
    P(f"- Parsed conditions, share of records (all / OSDA-linked): product Si/Al {pct(s['product_si_al'])} / {pct(sl['product_si_al'])}%, "
      f"fluoride flag {pct(s['fluoride_flag_true'])} / {pct(sl['fluoride_flag_true'])}%, heteroatom flag {pct(s['heteroatoms_nonempty'])} / {pct(sl['heteroatoms_nonempty'])}%, "
      f"temperature {pct(s['temperature_c'])} / {pct(sl['temperature_c'])}%, time {pct(s['time_h'])} / {pct(sl['time_h'])}%. "
      f"Gel composition: 0% (no record carries it). {C['note_conditions']}.")
    P('')
    P('### Records per linked OSDA (top 20)')
    P('')
    table(['OSDA (display)', 'KG records', 'KG papers', 'KG modal framework', 'modal share %', '# frameworks', 'ZeoSyn OSDA1 recipes'],
          [(o['display'], o['kg_records'], o['kg_papers'], o['kg_modal_framework'], pct(o['kg_modal_share']), o['kg_n_frameworks'], o['zeosyn_osda1_recipes'])
           for o in C['records_per_linked_osda_top20']])
    P('### KG reach on the OSDA-split test folds')
    P('')
    P('Two information conditions. (i) `exclude_fold_test_papers`: every KG record whose DOI belongs to a paper with a recipe in the fold\'s test rows is removed '
      '(the request\'s definition; stricter than the oracle, which may use other test papers). (ii) `exclude_own_paper_only`: same information condition as the oracle '
      'in B3. "Both" = recipes covered by the KG *and* by the oracle (own-paper-excluded); accuracies are compared on exactly those rows.')
    P('')
    for v in ('exclude_fold_test_papers', 'exclude_own_paper_only'):
        P(f'**{v}**')
        P('')
        rows = []
        for f in sorted(C['folds'], key=int):
            d = C['folds'][f][v]
            rows.append((f, C['folds'][f]['test_rows'], pct(d['coverage']), d['covered_osdas'], pct(d['kg_modal_acc_covered']), pct(d['true_class_in_kg_support_share_covered']),
                         d['kg_records_per_covered_recipe_median'], d['rows_covered_by_both_kg_and_oracle'], pct(d['kg_modal_acc_on_both']), pct(d['oracle_modal_acc_on_both']),
                         pct(d['oracle_nn1_gel_acc_on_both']), pct(d['agreement_kg_vs_oracle_modal_on_both']), d['rows_kg_uncovered_but_oracle_covered'],
                         pct(d['oracle_modal_acc_on_kg_uncovered_but_oracle_covered'])))
        S = C['summary']
        rows.append(('recipe-weighted mean', '', pct(S[f'{v}__coverage']['recipe_weighted_mean']), '', pct(S[f'{v}__kg_modal_acc_covered']['recipe_weighted_mean']),
                     pct(S[f'{v}__true_class_in_kg_support_share_covered']['recipe_weighted_mean']), '', '', pct(S[f'{v}__kg_modal_acc_on_both']['recipe_weighted_mean']),
                     pct(S[f'{v}__oracle_modal_acc_on_both']['recipe_weighted_mean']), pct(S[f'{v}__oracle_nn1_gel_acc_on_both']['recipe_weighted_mean']), '', '',
                     pct(S[f'{v}__oracle_modal_acc_on_kg_uncovered_but_oracle_covered']['recipe_weighted_mean'])))
        table(['fold', 'test rows', 'KG coverage %', 'covered OSDAs', 'KG modal acc on covered %', 'true class in KG support %', 'median KG records/recipe',
               'rows covered by both', 'KG modal acc on both %', 'oracle modal acc on both %', 'oracle 1-NN gel acc on both %', 'KG = oracle modal %',
               'rows KG-uncovered but oracle-covered', 'oracle modal acc there %'], rows)
    P('### Per-OSDA agreement, 20 most frequent KG-covered OSDAs per fold (`exclude_fold_test_papers`)')
    P('')
    for f in sorted(C['folds'], key=int):
        P(f'Fold {f}:')
        P('')
        table(['OSDA', 'test recipes', 'KG records (median)', 'KG modal', 'true modal (test)', 'true modal share %', 'agree', 'KG modal acc %', 'oracle modal acc %'],
              [(o['display'], o['n_test_recipes'], o['kg_records'], o['kg_modal_framework'], o['true_modal_framework_in_test'], pct(o['true_modal_share']),
                'yes' if o['agreement'] else 'no', pct(o['kg_modal_accuracy_on_these_recipes']), pct(o['oracle_modal_acc_on_these_recipes']))
               for o in C['folds'][f]['per_osda_top20_exclude_fold_test_papers']])

# ---------------- D
D = R.get('D')
if D:
    P('## D. Headroom under the paper split for hand-made gel ratios')
    P('')
    P('20 ratios built from the imputed D0 gel columns (zero denominator -> ' + str(D['cap_for_zero_denominator']) + ' when numerator > 0, else 0): ' + ', '.join(f'`{r}`' for r in D['ratio_names']) + '.')
    P('')
    table(['model', 'accuracy %', 'balanced acc %', 'macro-F1 %'], [
        ('RF D0', pct(D['rf_d0']['mean']['accuracy'], 2), pct(D['rf_d0']['mean']['balanced_accuracy'], 2), pct(D['rf_d0']['mean']['macro_f1'], 2)),
        ('RF D0 + 20 ratios', pct(D['rf_d0_plus_ratios']['mean']['accuracy'], 2), pct(D['rf_d0_plus_ratios']['mean']['balanced_accuracy'], 2), pct(D['rf_d0_plus_ratios']['mean']['macro_f1'], 2)),
        ('delta (pp)', f"{100 * D['delta_mean']['accuracy']:+.2f}", f"{100 * D['delta_mean']['balanced_accuracy']:+.2f}", f"{100 * D['delta_mean']['macro_f1']:+.2f}"),
    ])
    P(f"Per-seed accuracy deltas (pp): {[round(100 * x, 2) for x in D['delta_per_seed_accuracy']]}.")
    P('')

if R.get('notes'):
    P('## Notes and surprises')
    P('')
    for n in R['notes']:
        P(f'- {n}')
    P('')

(OUT / 'REPORT.md').write_text('\n'.join(L) + '\n')
print('wrote', OUT / 'REPORT.md', len(L), 'lines')
