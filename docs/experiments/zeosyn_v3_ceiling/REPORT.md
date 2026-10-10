# ZeoSyn framework prediction: headroom for a literature-knowledge channel

All numbers computed on the real data with the repo loader (`src/catalysis_research/benchmarks/zeosyn.py`): native row selection (`native_frame`), label = `Code1` with missing -> `Failed`, D0 = the loader's 43 columns (`GEL_INPUTS` 27 + `CONDITION_INPUTS` 2 + `NATIVE_OSDA_D0` 14), `IterativeImputer` fit on training rows only (re-fit per fold for the OSDA split). OSDA identity = InChIKey of `osda1 smiles` from `data/kg_zeolite_v1/zeosyn_osda_keys.json` (the key the V2 runner uses). Paper identity = normalized `doi`, rows without a DOI are their own paper (loader rule). RandomForest: 60 trees, `max_features=sqrt`, full depth, 2 fit seeds (3, 7), mean reported. Scripts: `scripts/diagnostics/zeosyn_ceiling/*.py`; raw results: `docs/experiments/zeosyn_v3_ceiling/results.json`. Generated 2026-10-10 as part of the V3 diagnosis (see `docs/experiments/ZEOSYN_V3_PLAN.md`).

## A. Dataset structure

- Recipes: **21972**; papers with a DOI: **3036** (+0 rows without DOI, each its own group).
- Classes (IZA code incl. `Failed`): **226**; `Failed` = 5406 recipes (24.6%). Classes with < 10 recipes: **104**; with < 5: 65.
- Distinct OSDA1 keys (InChIKey): **746** (distinct SMILES strings: 795). Recipes without an OSDA1: **2627** (12.0%); their top classes: [['Failed', 720], ['FAU', 291], ['CHA', 165], ['MOR', 157], ['LTA', 149]].
- Recipes per OSDA: median 5, mean 25.9, p90 56, max 1866. OSDAs with 1 recipe: 152; < 5: 346; >= 5: 400; >= 20: 171. Share of OSDA recipes in OSDAs with >= 5 recipes: 96.4%; >= 20: 84.6%; top-20 OSDAs: 44.3%.
- OSDAs that occur in a single paper: 448 (14.9% of OSDA recipes). For these, no literature prior from *other* papers can exist.

### Class frequency (top 20)

| class | n | share % |
|---|---|---|
| Failed | 5406 | 24.6 |
| MFI | 2182 | 9.9 |
| CHA | 1354 | 6.2 |
| *BEA | 1125 | 5.1 |
| AFI | 901 | 4.1 |
| MTW | 561 | 2.6 |
| FAU | 539 | 2.5 |
| LTA | 506 | 2.3 |
| MOR | 466 | 2.1 |
| MWW | 459 | 2.1 |
| AEL | 331 | 1.5 |
| TON | 304 | 1.4 |
| FER | 294 | 1.3 |
| AEI | 230 | 1.0 |
| MTT | 225 | 1.0 |
| BEC | 218 | 1.0 |
| ANA | 215 | 1.0 |
| LEV | 211 | 1.0 |
| SOD | 208 | 0.9 |
| AEN | 206 | 0.9 |

### Top-20 OSDAs (by OSDA1 key)

| OSDA (most common ZeoSyn name) | recipes | papers | dominant framework | share % | # frameworks |
|---|---|---|---|---|---|
| tetraethylammonium | 1866 | 424 | *BEA | 24.9 | 43 |
| tetrapropylammonium | 1457 | 528 | MFI | 85.8 | 17 |
| tetramethylammonium | 618 | 163 | Failed | 23.5 | 40 |
| hexamethyleneimine | 546 | 114 | MWW | 44.9 | 21 |
| di-n-propylamine | 488 | 133 | AEL | 46.9 | 19 |
| N,N,N-trimethyl-1-adamantammonium | 467 | 99 | CHA | 53.7 | 9 |
| triethylamine | 428 | 127 | AFI | 53.7 | 14 |
| choline | 393 | 32 | Failed | 37.4 | 24 |
| N-methyl-sparteinium | 302 | 26 | Failed | 39.1 | 6 |
| ephedrine | 278 | 4 | AFI | 57.2 | 3 |
| ethylenediamine | 216 | 47 | Failed | 31.5 | 19 |
| 1,6-diaminohexane | 209 | 45 | TON | 25.8 | 14 |
| C[C@@H]1CCC[C@H](C)[N+]12Cc3ccccc3C2 | 200 | 4 | Failed | 58.0 | 8 |
| diethylamine | 182 | 43 | TON | 23.1 | 13 |
| 3',4'-dihydro-1'H-spiro[isoindoline-2,2'-isoquinolin]-2-ium | 174 | 2 | Failed | 63.2 | 5 |
| 1,1,3,5-tetramethylpiperidinium | 160 | 15 | AEI | 46.9 | 12 |
| tetrabutylammonium | 157 | 55 | MEL | 52.9 | 14 |
| 4,4,10,10-tetraethyl-1,14-dimethyl-4,10-diazoniatetracyclo[5.5.2.02,6.08,12]tetradec-13-ene | 154 | 4 | Failed | 59.7 | 3 |
| 7-ethyl-6-azoniaspiro[5.5]undecane | 143 | 10 | UTL | 69.2 | 6 |
| pyrrolidine | 139 | 41 | FER | 36.7 | 9 |

### A2. How deterministic is OSDA -> framework?

Conditioning keys: Si/Al bin from raw gel `Si`/`Al` (`Al=0`, `<=2`, `2-5`, `5-15`, `15-50`, `50-200`, `>200`, `unknown`), F present = raw `F` > 0, heteroatom present = any of P, Ge, Ti, B, Ga, Zn, Sn, Zr, V, Be, W, Cu > 0. "In-sample" = accuracy of the modal-class rule evaluated on the recipes it was built from (groups with >= `min` recipes). "LOPO" = leave-own-paper-out: each recipe is predicted by the modal class of the *other-paper* recipes of its group (this is the honest version of an in-dataset literature oracle; coverage = recipes with at least one other-paper recipe in the group).

| grouping | min | # groups | # groups >= min | OSDA recipes in groups >= min % | in-sample modal acc % (>= min) | LOPO modal acc % (>= min) | LOPO covered (>= min) | LOPO coverage % (all groups) | LOPO acc % on covered (all groups) | LOPO acc % over all OSDA recipes (uncovered = wrong) |
|---|---|---|---|---|---|---|---|---|---|---|
| OSDA key | 5 | 746 | 400 | 96.4 | 50.1 | 39.4 | 16350 | 85.1 | 39.5 | 33.6 |
| OSDA key (groups >=2) | 2 | 746 | 594 | 99.2 | 50.9 | 39.5 | 16466 | 85.1 | 39.5 | 33.6 |
| OSDA + Si/Al bin | 5 | 1686 | 620 | 90.1 | 58.6 | 45.7 | 14392 | 76.5 | 45.8 | 35.0 |
| OSDA + Si/Al bin + F + heteroatom | 5 | 2212 | 746 | 86.8 | 62.2 | 49.1 | 12937 | 69.7 | 49.1 | 34.2 |
| OSDA + Si/Al bin + F + heteroatom (groups >=2) | 2 | 2212 | 1394 | 95.8 | 63.7 | 49.1 | 13484 | 69.7 | 49.1 | 34.2 |

In-sample modal-per-OSDA accuracy over *all* 21972 rows (no-OSDA rows as one group): **48.4%**.

Si/Al bins: {'15-50': 3881, '2-5': 1090, '5-15': 2477, '50-200': 1423, '<=2': 4981, '>200': 727, 'Al=0': 6564, 'Si=0,Al=0': 829}; F: {'F': 5060, 'noF': 16912}; heteroatom: {'het': 8617, 'nohet': 13355}.

## B1. Paper (DOI-group) split, seed 20261007, 20 % test

Train 17567 / test 4405 rows. Global modal class in training: `Failed`.

| model | accuracy % | balanced acc % | macro-F1 % |
|---|---|---|---|
| RF D0 (60 trees, mean of 2 seeds) | 43.6 | 35.5 | 31.0 |
| training-modal framework per OSDA (fallback global modal) | 28.6 | 16.7 | 13.5 |
| 1-NN in standardized D0 | 36.2 | 32.5 | 26.1 |
| global modal class | 20.0 |  |  |

- Test rows whose OSDA1 was seen in training: 2960 (67.2%); rows with any OSDA: 79.9%.
- On seen-OSDA rows: trivial rule 35.0% vs RF D0 50.1%. On unseen/no-OSDA rows: trivial 15.7% vs RF D0 30.3%.

## B2-B4. OSDA-group split (GroupKFold on OSDA1 key, 5 folds, shuffle seed 1; no-OSDA rows always train)

### B2. Baselines per fold

| fold | test rows | test OSDAs | RF D0 acc % | RF D0 bal-acc % | RF D0 macro-F1 % | global modal (class, acc %) | 1-NN OSDA desc (30 scalar) acc % | 1-NN OSDA desc (455+11 full) acc % |
|---|---|---|---|---|---|---|---|---|
| 0 | 2564 | 150 | 31.6 | 10.4 | 10.9 | Failed 28.0 | 14.0 | 21.0 |
| 1 | 4956 | 149 | 23.8 | 8.8 | 8.9 | Failed 22.7 | 7.2 | 10.4 |
| 2 | 3179 | 149 | 29.9 | 12.0 | 11.5 | Failed 24.9 | 18.4 | 15.9 |
| 3 | 3976 | 149 | 33.1 | 11.3 | 11.8 | Failed 26.8 | 20.9 | 20.8 |
| 4 | 4670 | 149 | 26.5 | 10.7 | 9.3 | Failed 21.1 | 10.1 | 9.3 |
| mean |  |  | 29.0 | 10.7 | 10.5 | 24.7 | 14.1 | 15.5 |
| recipe-weighted mean |  |  | 28.4 | 10.5 | 10.3 | 24.2 | 13.4 | 14.6 |

1-NN OSDA descriptor space: per-OSDA vector = the 19 scalar conformer descriptors exposed by the loader (`OSDA_TABLE_INPUTS`) + 11 RDKit counts (`RDKIT_INPUTS`), or every numeric column of `osda_descriptors.csv` (incl. box/getaway/whim vectors) + 11 RDKit counts; standardized on training OSDAs, zero-variance dims dropped; prediction = modal framework of the nearest training OSDA (among its training recipes).

### B3. Oracle literature prior (other-paper test recipes with the same OSDA)

For a test recipe with OSDA o, the "literature" is every other test recipe with OSDA o from a different paper (own paper left out). Predictions: (a) modal framework; (b) framework of the nearest such recipe in standardized gel space (27 `GEL_INPUTS` of D0, standardized on fold-training rows); (b') same with `cryst_time`/`cryst_temp` added; (c) majority of the 5 nearest (ties -> nearest). "Overall" = oracle where covered, RF D0 elsewhere.

| fold | coverage % | covered OSDAs | coverage (>=3 other-paper recipes) % | RF D0 acc on covered % | RF D0 acc on uncovered % | oracle (a) modal % | oracle (b) 1-NN gel % | oracle (b') 1-NN gel+cond % | oracle (c) 5-NN vote % | true class in oracle support % | RF D0 overall % | overall (a)+D0 % | overall (b)+D0 % | overall (c)+D0 % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 73.6 | 47 | 69.8 | 28.7 | 39.6 | 32.7 | 39.8 | 41.2 | 38.1 | 81.5 | 31.6 | 34.5 | 39.8 | 38.5 |
| 1 | 86.5 | 58 | 82.6 | 20.9 | 42.6 | 36.7 | 47.4 | 47.0 | 45.7 | 89.7 | 23.8 | 37.5 | 46.8 | 45.3 |
| 2 | 84.8 | 58 | 80.0 | 28.0 | 40.6 | 37.9 | 36.8 | 39.6 | 38.8 | 78.5 | 29.9 | 38.3 | 37.4 | 39.1 |
| 3 | 85.9 | 74 | 82.9 | 32.5 | 37.3 | 36.2 | 47.9 | 48.9 | 46.0 | 86.2 | 33.1 | 36.4 | 46.4 | 44.8 |
| 4 | 89.5 | 61 | 83.1 | 25.5 | 34.6 | 49.1 | 53.8 | 54.2 | 54.4 | 83.7 | 26.5 | 47.6 | 51.8 | 52.3 |
| mean | 84.1 |  | 79.7 | 27.1 | 38.9 | 38.5 | 45.2 | 46.2 | 44.6 | 83.9 | 29.0 | 38.8 | 44.4 | 44.0 |
| recipe-weighted mean | 85.1 |  | 80.6 | 26.6 | 38.9 | 39.2 | 46.3 | 47.1 | 45.7 | 84.6 | 28.4 | 39.4 | 45.5 | 45.0 |

Long tail: restricted to recipes whose OSDA has >= 3 other-paper recipes vs. only 1-2:

| fold | covered rows | rows with support >= 3 | RF D0 acc (support >= 3) % | modal acc (>= 3) % | 1-NN gel acc (>= 3) % | 5-NN acc (>= 3) % | modal acc (support 1-2) % | 1-NN gel acc (support 1-2) % | true class in support (>= 3) % | overall modal(>=3)+D0 % | overall 1-NN(>=3)+D0 % | support quantiles (p10/25/50/75/90) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1888 | 1789 | 29.0 | 31.6 | 39.1 | 37.3 | 51.5 | 52.5 | 82.9 | 33.4 | 38.7 | {'10': 6, '25': 25, '50': 66, '75': 136, '90': 182} |
| 1 | 4288 | 4092 | 20.0 | 36.6 | 47.8 | 46.1 | 38.3 | 38.3 | 92.1 | 37.5 | 46.8 | {'10': 10, '25': 63, '50': 530, '75': 1850, '90': 1862} |
| 2 | 2697 | 2543 | 27.0 | 39.0 | 37.9 | 40.1 | 18.2 | 18.2 | 82.1 | 39.6 | 38.7 | {'10': 7, '25': 23, '50': 79, '75': 208, '90': 418} |
| 3 | 3414 | 3297 | 31.7 | 35.6 | 47.7 | 45.7 | 53.8 | 53.8 | 87.3 | 36.4 | 46.5 | {'10': 9, '25': 35, '50': 95, '75': 157, '90': 425} |
| 4 | 4179 | 3879 | 23.3 | 51.9 | 57.1 | 57.6 | 12.7 | 12.3 | 88.9 | 50.3 | 54.5 | {'10': 6, '25': 39, '50': 155, '75': 1443, '90': 1455} |

### B4. Combining the oracle prior with the RF

Prior block (13 columns): per-recipe probability of each of the 10 most frequent training classes among other-paper same-OSDA recipes, modal class id (index into fold-training classes, -1 = none), support count, Shannon entropy (bits). Training recipes: other-paper recipes of the same OSDA *within the training rows* (leave-own-paper-out); test recipes: other-paper test recipes (as in B3). Product rule: RF D0 class probabilities x (prior + eps), prior = other-paper class distribution (or 5-nearest-in-gel distribution), uniform where uncovered.

| fold | RF D0 acc % | RF D0+prior acc % | delta pp | D0+prior bal-acc % | D0+prior macro-F1 % | D0 acc covered % | D0+prior acc covered % | D0 acc uncovered % | D0+prior acc uncovered % | RF prior-block only acc % | train rows covered % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 31.6 | 32.9 | +1.3 | 9.8 | 10.7 | 28.7 | 30.5 | 39.6 | 39.7 | 25.8 | 75.1 |
| 1 | 23.8 | 22.3 | -1.5 | 6.8 | 7.0 | 20.9 | 19.0 | 42.6 | 43.8 | 15.8 | 71.6 |
| 2 | 29.9 | 32.7 | +2.7 | 8.9 | 8.9 | 28.0 | 31.0 | 40.6 | 42.1 | 26.4 | 73.3 |
| 3 | 33.1 | 34.3 | +1.1 | 10.0 | 10.6 | 32.5 | 33.9 | 37.3 | 36.4 | 25.5 | 72.5 |
| 4 | 26.5 | 25.0 | -1.5 | 6.8 | 6.9 | 25.5 | 24.4 | 34.6 | 29.6 | 37.1 | 71.0 |
| mean | 29.0 | 29.4 | +0.4 | 8.5 | 8.8 | 27.1 | 27.8 | 38.9 | 38.3 | 26.1 |  |

Product rule (accuracy %, overall / on covered rows), per eps:

| fold | RF D0 | dist eps=0.01 | dist eps=0.05 | dist eps=0.2 | dist eps=1.0 | 5-NN eps=0.01 | 5-NN eps=0.05 | 5-NN eps=0.2 | 5-NN eps=1.0 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 31.6 / 28.7 | 37.4 / 36.6 | 37.2 / 36.3 | 35.8 / 34.4 | 32.9 / 30.4 | 38.3 / 37.8 | 38.4 / 37.9 | 37.3 / 36.4 | 33.7 / 31.6 |
| 1 | 23.8 / 20.9 | 31.1 / 29.3 | 30.5 / 28.6 | 27.8 / 25.5 | 25.5 / 22.9 | 38.9 / 38.3 | 37.6 / 36.8 | 30.4 / 28.5 | 25.8 / 23.2 |
| 2 | 29.9 / 28.0 | 39.6 / 39.4 | 38.8 / 38.5 | 36.5 / 35.7 | 31.5 / 29.9 | 39.3 / 39.1 | 39.9 / 39.8 | 38.7 / 38.4 | 32.7 / 31.3 |
| 3 | 33.1 / 32.5 | 38.3 / 38.4 | 37.6 / 37.6 | 35.9 / 35.6 | 33.9 / 33.4 | 42.9 / 43.8 | 43.0 / 43.9 | 40.5 / 41.0 | 35.6 / 35.3 |
| 4 | 26.5 / 25.5 | 54.2 / 56.5 | 53.5 / 55.7 | 47.5 / 49.0 | 35.3 / 35.4 | 54.5 / 56.8 | 54.6 / 56.9 | 48.8 / 50.4 | 36.3 / 36.5 |
| mean | 29.0 / 27.1 | 40.1 / 40.0 | 39.5 / 39.4 | 36.7 / 36.1 | 31.8 / 30.4 | 42.8 / 43.2 | 42.7 / 43.1 | 39.1 / 39.0 | 32.8 / 31.6 |

## C. The real KG synthesis layer (`data/kg_zeolite_v1`)

- Synthesis records: **4656** (all carry >= 1 product framework code by construction: 4656; 368 list more than one product). Papers: 3074 (2904 with DOI); records with a DOI: 4444.
- Records linked to a ZeoSyn OSDA (via `osda_links.json`): **1234** (128 linked to > 1 OSDA); distinct linked OSDAs: **161**, of which 147 occur as OSDA1 in the benchmark (benchmark has 746 distinct OSDA1 keys).
- ZeoSyn recipes whose OSDA1 is linked at all (before any paper exclusion): 56.4% of all recipes, 64.1% of recipes with an OSDA.
- Records whose paper DOI is NOT a ZeoSyn DOI (external): **68.9%**; in ZeoSyn: 26.6%; no DOI: 4.6%. Among OSDA-linked records: external 53.3%, no DOI 3.2%. KG papers that are ZeoSyn papers: 762 of 3036 ZeoSyn DOIs.
- Records per linked OSDA: n=161, median 2, mean 8.6; with 1 record: 56, >= 5: 35, >= 20: 8.
- Parsed conditions, share of records (all / OSDA-linked): product Si/Al 19.4 / 13.9%, fluoride flag 8.2 / 13.6%, heteroatom flag 11.9 / 13.7%, temperature 61.7 / 78.0%, time 55.6 / 58.5%. Gel composition: 0% (no record carries it). records carry no gel composition at all; fluoride/heteroatom are regex flags on free text, product_si_al is a product-side attribute, temperature/time parsed from conditions.

### Records per linked OSDA (top 20)

| OSDA (display) | KG records | KG papers | KG modal framework | modal share % | # frameworks | ZeoSyn OSDA1 recipes |
|---|---|---|---|---|---|---|
| tetrapropylammonium | 437 | 322 | MFI | 95.1 | 16 | 1457 |
| tetraethylammonium | 167 | 137 | *BEA | 50.0 | 25 | 1866 |
| N,N,N-trimethyl-L-adamantammonium | 82 | 60 | CHA | 81.8 | 8 | 467 |
| hexadecyltrimethylammonium | 68 | 52 | MFI | 40.0 | 13 | 27 |
| tetramethylammonium | 50 | 41 | LTA | 26.4 | 17 | 618 |
| Hexamethyleneimine | 32 | 26 | MWW | 71.9 | 5 | 546 |
| tetrabutylammonium | 26 | 22 | MEL | 37.9 | 6 | 157 |
| triethylamine | 24 | 19 | AFI | 50.0 | 5 | 428 |
| di-n-propylamine | 18 | 14 | AEL | 42.3 | 10 | 488 |
| morpholine | 17 | 13 | CHA | 68.4 | 4 | 106 |
| 18-crown-6 | 16 | 13 | EMT | 33.3 | 4 | 125 |
| N,N-dimethyl-3,5- dimethylpiperidinium | 15 | 8 | AEI | 58.8 | 3 | 160 |
| ethylenediamine | 15 | 12 | MFI | 53.3 | 6 | 216 |
| 1-ethyl-3-methylimidazolate | 14 | 7 | AEL | 33.3 | 8 | 8 |
| [(CH3O)3SiC3H6N(CH3)2C16H37]Cl | 13 | 10 | MFI | 46.2 | 5 | 0 |
| triethanolamine | 12 | 11 | LTA | 30.8 | 6 | 48 |
| 3-butyl-1-methylimidazolium | 12 | 9 | AEL | 30.0 | 7 | 86 |
| hexamethonium | 11 | 8 | EUO | 30.8 | 7 | 40 |
| urea | 11 | 8 | MFI | 72.7 | 3 | 0 |
| diethylamine | 11 | 8 | RHO | 46.2 | 4 | 182 |

### KG reach on the OSDA-split test folds

Two information conditions. (i) `exclude_fold_test_papers`: every KG record whose DOI belongs to a paper with a recipe in the fold's test rows is removed (the request's definition; stricter than the oracle, which may use other test papers). (ii) `exclude_own_paper_only`: same information condition as the oracle in B3. "Both" = recipes covered by the KG *and* by the oracle (own-paper-excluded); accuracies are compared on exactly those rows.

**exclude_fold_test_papers**

| fold | test rows | KG coverage % | covered OSDAs | KG modal acc on covered % | true class in KG support % | median KG records/recipe | rows covered by both | KG modal acc on both % | oracle modal acc on both % | oracle 1-NN gel acc on both % | KG = oracle modal % | rows KG-uncovered but oracle-covered | oracle modal acc there % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2564 | 27.2 | 11 | 5.9 | 25.3 | 2.0 | 680 | 5.9 | 30.3 | 38.4 | 2.4 | 1208 | 34.0 |
| 1 | 4956 | 66.3 | 13 | 30.7 | 49.4 | 88.0 | 3261 | 31.0 | 33.8 | 47.1 | 91.9 | 1027 | 46.0 |
| 2 | 3179 | 46.6 | 18 | 18.3 | 24.1 | 5.0 | 1465 | 18.4 | 41.7 | 36.9 | 13.1 | 1232 | 33.3 |
| 3 | 3976 | 31.9 | 17 | 27.5 | 54.1 | 7.0 | 1249 | 27.9 | 38.8 | 50.0 | 48.3 | 2165 | 34.7 |
| 4 | 4670 | 60.8 | 22 | 54.3 | 66.4 | 324.0 | 2834 | 54.3 | 60.1 | 61.2 | 60.9 | 1345 | 25.9 |
| recipe-weighted mean |  | 49.5 |  | 30.4 | 47.1 |  |  | 30.6 | 42.0 | 48.3 |  |  | 35.1 |

**exclude_own_paper_only**

| fold | test rows | KG coverage % | covered OSDAs | KG modal acc on covered % | true class in KG support % | median KG records/recipe | rows covered by both | KG modal acc on both % | oracle modal acc on both % | oracle 1-NN gel acc on both % | KG = oracle modal % | rows KG-uncovered but oracle-covered | oracle modal acc there % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2564 | 42.1 | 19 | 21.7 | 32.6 | 2.0 | 1063 | 21.9 | 27.7 | 35.0 | 26.8 | 825 | 39.2 |
| 1 | 4956 | 72.8 | 23 | 34.3 | 62.0 | 165.0 | 3581 | 34.6 | 36.5 | 48.3 | 94.1 | 707 | 37.8 |
| 2 | 3179 | 59.6 | 28 | 23.6 | 40.4 | 10.0 | 1870 | 23.8 | 37.9 | 35.8 | 40.5 | 827 | 37.8 |
| 3 | 3976 | 53.8 | 29 | 29.3 | 46.7 | 3.0 | 2119 | 29.5 | 39.7 | 49.7 | 42.8 | 1295 | 30.4 |
| 4 | 4670 | 68.8 | 29 | 52.5 | 66.2 | 50.0 | 3208 | 52.6 | 56.9 | 60.1 | 63.9 | 971 | 23.3 |
| recipe-weighted mean |  | 61.7 |  | 34.2 | 52.4 |  |  | 34.4 | 41.1 | 47.6 |  |  | 33.0 |

### Per-OSDA agreement, 20 most frequent KG-covered OSDAs per fold (`exclude_fold_test_papers`)

Fold 0:

| OSDA | test recipes | KG records (median) | KG modal | true modal (test) | true modal share % | agree | KG modal acc % | oracle modal acc % |
|---|---|---|---|---|---|---|---|---|
| 1,6-diaminohexane | 209 | 2 | -CLO | TON | 25.8 | no | 6.2 | 11.5 |
| tetrabutylammonium | 157 | 17 | FAU | MEL | 52.9 | no | 0.0 | 52.9 |
| pyrrolidine | 139 | 2 | SOD | FER | 36.7 | no | 4.3 | 21.6 |
| isopropyl amine | 102 | 2 | CHA | MTT | 39.2 | no | 0.0 | 39.2 |
| tetra(n-butyl) phosphonium | 22 | 1 | MFI | Failed | 45.5 | no | 31.8 | 45.5 |
| dibenzyldimethylammonium | 19 | 1 | *BEA | EUO | 42.1 | no | 26.3 | 21.1 |
| octyltrimethylammonium | 16 | 3 | MTT | MWW | 68.8 | no | 0.0 | 0.0 |
| N-methylpyrrolidine | 14 | 1 | IMF | FER | 57.1 | no | 0.0 | 0.0 |
| methyltropinium | 12 | 1 | DDR | DDR | 75.0 | yes | 75.0 | 75.0 |
| 1-ethyl-1,2,6-trimethylpiperidin-1-ium | 6 | 1 | SFF | STF | 100.0 | no | 0.0 | 100.0 |
| 134TMI+ | 1 | 6 | ITW | ITW | 100.0 | yes | 100.0 | 0.0 |

Fold 1:

| OSDA | test recipes | KG records (median) | KG modal | true modal (test) | true modal share % | agree | KG modal acc % | oracle modal acc % |
|---|---|---|---|---|---|---|---|---|
| tetraethylammonium | 1866 | 88 | *BEA | *BEA | 24.9 | yes | 24.9 | 24.9 |
| Hexamethyleneimine | 546 | 21 | MWW | MWW | 44.9 | yes | 44.9 | 44.9 |
| di-n-propylamine | 488 | 6 | AEL | AEL | 46.9 | yes | 46.9 | 46.9 |
| 1-(phenylmethyl)-1-azoniabicyclo[2.2.2]octane | 71 | 1 | IFR | IFR | 64.8 | yes | 64.8 | 64.8 |
| tetraethylenepentamine | 69 | 2 | FER | CHA | 56.5 | no | 0.0 | 56.5 |
| cyclohexylamine | 67 | 2 | MWW | CHA | 37.3 | no | 0.0 | 37.3 |
| 1-methyl-3-ethylimidazolium  | 65 | 4 | TON | Failed | 23.1 | no | 1.5 | 7.7 |
| N,N-dimethylpiperidinium | 52 | 1 | JBW | LEV | 44.2 | no | 0.0 | 44.2 |
| C22-6-6 | 25 | 2 | MFI | MFI | 100.0 | yes | 100.0 | 100.0 |
| 3BDMI | 24 | 3 | *UOE | Failed | 91.7 | no | 0.0 | 0.0 |
| copper 1,4,8,11-tetraazacyclotetradecane | 9 | 1 | RHO | Failed | 44.4 | no | 0.0 | 0.0 |
| N,N,N',N'-tetramethylbutane-1,4-diamine | 3 | 3 | ESV | Failed | 66.7 | no | 0.0 | 0.0 |
| 2-methyl imidazole | 1 | 3 | MOR | CHA | 100.0 | no | 0.0 | 0.0 |

Fold 2:

| OSDA | test recipes | KG records (median) | KG modal | true modal (test) | true modal share % | agree | KG modal acc % | oracle modal acc % |
|---|---|---|---|---|---|---|---|---|
| triethylamine | 428 | 2 | CHA | AFI | 53.7 | no | 24.8 | 53.7 |
| choline | 393 | 5 | FAU | Failed | 37.4 | no | 0.3 | 37.4 |
| ethylenediamine | 216 | 9 | MFI | Failed | 31.5 | no | 11.1 | 31.5 |
| 1-adamantaneamine | 97 | 5 | DDR | DDR | 61.9 | yes | 61.9 | 61.9 |
| triethylenediamine | 66 | 2 | *BEA | Failed | 42.4 | no | 4.5 | 42.4 |
| ethylamine | 66 | 2 | ANA | Failed | 25.8 | no | 0.0 | 10.6 |
| N,N-diisopropylethylamine | 62 | 2 | AEI | AEI | 85.5 | yes | 85.5 | 85.5 |
| dimethyldipropylammonium | 47 | 1 | RRO | Failed | 34.0 | no | 4.3 | 2.1 |
| hexamethonium | 40 | 9 | EUO | EUO | 27.5 | yes | 27.5 | 2.5 |
| N,N-diethyl-cis-2,6-dimethyylpieridinium | 20 | 2 | FER | Failed | 60.0 | no | 0.0 | 10.0 |
| 1,2,3-triethylimidazolium | 12 | 1 | *STO | MFI | 66.7 | no | 0.0 | 0.0 |
| ethanolamine | 12 | 1 | MFI | APD | 66.7 | no | 0.0 | 16.7 |
| N,N,N-dimethylethylcyclohexylammonium | 11 | 2 | CHA | CHA | 81.8 | yes | 81.8 | 81.8 |
| tris(2-aminoethyl)amine | 7 | 1 | MOR | RWY | 42.9 | no | 0.0 | 42.9 |
| 1,4-dibromobutane | 2 | 1 | TUN | TUN | 100.0 | yes | 100.0 | 0.0 |
| ethylmethylpyrrolidinium | 2 | 1 | CHA | Failed | 100.0 | no | 0.0 | 0.0 |
| hexadecyl-dimethyl-(3-trimethoxysilylpropyl)azanium | 1 | 4 | MFI | *BEA | 100.0 | no | 0.0 | 0.0 |
| ethylene glycol | 1 | 3 | CHA | SOD | 100.0 | no | 0.0 | 0.0 |

Fold 3:

| OSDA | test recipes | KG records (median) | KG modal | true modal (test) | true modal share % | agree | KG modal acc % | oracle modal acc % |
|---|---|---|---|---|---|---|---|---|
| N,N,N-trimethyl-L-adamantammonium | 467 | 54 | CHA | CHA | 53.7 | yes | 53.7 | 53.7 |
| diethylamine | 182 | 6 | RHO | TON | 23.1 | no | 11.0 | 2.7 |
| 18-crown-6 | 125 | 12 | EMT | EMT | 37.6 | yes | 37.6 | 37.6 |
| piperidine | 116 | 4 | MFI | MWW | 47.4 | no | 1.7 | 47.4 |
| 1,5-bis(methylpyrrolidinium)pentane | 109 | 2 | IWW | IMF | 49.5 | no | 10.1 | 49.5 |
| propylamine | 79 | 3 | CHA | MFI | 53.2 | no | 0.0 | 53.2 |
| diquinuclidinium | 49 | 1 | *BEA | Failed | 46.9 | no | 10.2 | 46.9 |
| triethanolamine | 48 | 7 | LTA | EMT | 31.2 | no | 10.4 | 4.2 |
| spiro-pip6,5 | 27 | 1 | IWW | MTW | 25.9 | no | 0.0 | 0.0 |
| benzene-1,2-diol | 20 | 3 | MFI | SOD | 45.0 | no | 0.0 | 0.0 |
| CCc1n(C)cc(C)[n+]1C | 19 | 7 | STW | Failed | 47.4 | no | 31.6 | 26.3 |
| 1,8-diazabicyclo[5.4.0]undec-7-ene | 12 | 1 | UTL | IWR | 100.0 | no | 0.0 | 0.0 |
| N-methylpiperidine | 6 | 1 | LEV | RTH | 50.0 | no | 16.7 | 0.0 |
| 1,1-dimethyl-2,6-dimethylpiperidin-1-ium | 4 | 3 | LEV | AEI | 75.0 | no | 0.0 | 0.0 |
| 1-hexyl-2,3-dimethylimidazolium | 2 | 1 | MWW | AEL | 50.0 | no | 0.0 | 0.0 |
| cis-trans-3,5-dimethylpiperidinium | 2 | 1 | AEI | AEI | 50.0 | yes | 50.0 | 0.0 |
| N-butyl-N-methylhexamethyleneiminium | 2 | 1 | MWW | *BEA | 100.0 | no | 0.0 | 0.0 |

Fold 4:

| OSDA | test recipes | KG records (median) | KG modal | true modal (test) | true modal share % | agree | KG modal acc % | oracle modal acc % |
|---|---|---|---|---|---|---|---|---|
| tetrapropylammonium | 1457 | 324 | MFI | MFI | 85.8 | yes | 85.8 | 85.8 |
| tetramethylammonium | 618 | 25 | LTA | Failed | 23.5 | no | 14.9 | 23.5 |
| N,N-dimethyl-3,5- dimethylpiperidinium | 160 | 10 | FAU | AEI | 46.9 | no | 7.5 | 46.9 |
| morpholine | 106 | 3 | CHA | CHA | 77.4 | yes | 77.4 | 77.4 |
| 3-butyl-1-methylimidazolium | 86 | 3 | MFI | LTA | 48.8 | no | 0.0 | 48.8 |
| n-butylamine | 82 | 6 | MFI | MFI | 48.8 | yes | 48.8 | 48.8 |
| benzyltrimethylammonium | 64 | 1 | MOR | Failed | 31.2 | no | 0.0 | 18.8 |
| pyridine | 44 | 3 | CHA | AST | 31.8 | no | 20.5 | 0.0 |
| trimethylamine | 39 | 1 | CHA | AFI | 53.8 | no | 2.6 | 2.6 |
| diethylenetriamine | 30 | 2 | CHA | TON | 30.0 | no | 13.3 | 0.0 |
| diquat-7 | 29 | 1 | MTT | MTT | 48.3 | yes | 48.3 | 48.3 |
| tetraethylphosphonium | 28 | 2 | AEI | AEI | 71.4 | yes | 71.4 | 14.3 |
| hexadecyltrimethylammonium | 27 | 59 | MFI | MOR | 37.0 | no | 3.7 | 0.0 |
| 4,4'-bipyridine | 22 | 1 | FAU | NSI | 86.4 | no | 0.0 | 86.4 |
| Bis-1,6-(tripropylammonium)hexamethylene | 21 | 1 | MFI | MFI | 57.1 | yes | 57.1 | 57.1 |
| 1-ethyl-3-methylimidazolate | 8 | 9 | AEL | Failed | 50.0 | no | 37.5 | 37.5 |
| hexamethylenetetramine | 5 | 4 | MFI | AWW | 40.0 | no | 0.0 | 20.0 |
| tetrahydrofuran | 5 | 1 | FAU | FER | 80.0 | no | 0.0 | 80.0 |
| 1-butanol | 3 | 1 | LTL | MFI | 66.7 | no | 0.0 | 0.0 |
| polyethyleneimine | 2 | 3 | CHA | Failed | 100.0 | no | 0.0 | 0.0 |

## D. Headroom under the paper split for hand-made gel ratios

20 ratios built from the imputed D0 gel columns (zero denominator -> 1000.0 when numerator > 0, else 0): `Si/Al`, `Al/(Si+Al)`, `Si/(Al+P)`, `P/Al`, `H2O/Si`, `H2O/T`, `OH/Si`, `OH/T`, `F/Si`, `F/(F+OH)`, `sda1/Si`, `sda1/T`, `OH/sda1`, `Na/Si`, `K/Si`, `alkali/Si`, `Na/(Na+K)`, `alkaline_earth/Si`, `hetero/Si`, `(Si+Al)/T`.

| model | accuracy % | balanced acc % | macro-F1 % |
|---|---|---|---|
| RF D0 | 43.63 | 35.48 | 31.01 |
| RF D0 + 20 ratios | 44.15 | 35.46 | 31.28 |
| delta (pp) | +0.52 | -0.03 | +0.27 |

Per-seed accuracy deltas (pp): [0.84, 0.2].

