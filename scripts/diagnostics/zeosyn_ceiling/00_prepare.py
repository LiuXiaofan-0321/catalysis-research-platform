"""Load ZeoSyn through the repo loader, build keys/splits, impute on training rows, cache to OUT/cache.

Cache contents (cache/base.npz + cache/meta.pkl):
  d0_paper      D0 (43 cols, loader's D0 order) imputed with the imputer fit on PAPER-split training rows
  d0_osda_f{k}  D0 imputed with the imputer fit on OSDA fold k training rows (k = 0..4)
  y             label (Code1, 'Failed' when missing)
  paper_train / paper_test   row indices of the authors' DOI-group split (seed 20261007, 20% test)
  osda_fold     fold id per row (-1 = no OSDA -> always training)
  gel_raw       raw (un-imputed) GEL_INPUTS + CONDITION_INPUTS values, NaN where missing
  osda_desc30   OSDA1 scalar descriptors (19 table scalars + 11 rdkit counts), per recipe
  osda_desc_full  OSDA1 full numeric osda_descriptors.csv row (all 445 numeric cols) + 11 rdkit, per recipe
meta.pkl: doi (normalized), year, osda1 name, osda1 smiles, osda_key (InChIKey from zeosyn_osda_keys.json), y
"""
import json
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from common import CACHE, ROOT, OSDA_FOLDS, OSDA_SPLIT_SEED, PAPER_SPLIT_SEED, PAPER_TEST_FRACTION, log  # noqa: E402

from catalysis_research.benchmarks import zeosyn as z  # noqa: E402

CACHE.mkdir(parents=True, exist_ok=True)

t0 = time.time()
log('loading ZeoSyn via loader (hash check + native_frame)')
data = z.load(ROOT / 'data/zeosyn')
frame, y = data.frame, data.y
log(f'rows={len(frame)} load took {time.time() - t0:.0f}s')

# ---- keys: the V2 runner's OSDA identity (InChIKey of osda1 smiles from the frozen table)
table = json.loads((ROOT / 'data/kg_zeolite_v1/zeosyn_osda_keys.json').read_text())
keys = []
for smi in frame['osda1 smiles']:
    if not isinstance(smi, str) or not smi.strip():
        keys.append(None)
    else:
        keys.append(table[smi])  # KeyError would mean the frozen table is stale
dois = frame['doi'].map(z.normalize_doi).tolist()
years = pd.to_numeric(frame['year'], errors='coerce').to_numpy(float)
meta = pd.DataFrame({'doi': [d or '' for d in dois], 'year': years,
                     'osda1': frame['osda1'].astype(object).where(frame['osda1'].notna(), None),
                     'osda1_smiles': frame['osda1 smiles'].astype(object).where(frame['osda1 smiles'].notna(), None),
                     'osda_key': keys, 'y': y})
meta.to_pickle(CACHE / 'meta.pkl')

# ---- paper split (authors')
paper_train, paper_test, test_dois = z.doi_group_split(frame, test_fraction=PAPER_TEST_FRACTION, seed=PAPER_SPLIT_SEED)
log(f'paper split: train={len(paper_train)} test={len(paper_test)} test_dois={len(test_dois)}')

# ---- OSDA split: GroupKFold on osda_key, 5 folds, seed 1; rows without OSDA always train (fold -1)
from sklearn.model_selection import GroupKFold  # noqa: E402
has = np.array([k is not None for k in keys])
idx = np.flatnonzero(has)
gkf = GroupKFold(n_splits=OSDA_FOLDS, shuffle=True, random_state=OSDA_SPLIT_SEED)
fold = np.full(len(frame), -1, dtype=int)
for f, (_, te) in enumerate(gkf.split(idx, groups=np.array(keys, dtype=object)[idx])):
    fold[idx[te]] = f
for f in range(OSDA_FOLDS):
    log(f'osda fold {f}: test rows={int((fold == f).sum())} test OSDAs={len({keys[i] for i in np.flatnonzero(fold == f)})}')

# ---- raw gel + condition inputs (un-imputed)
gel_cols = list(z.GEL_INPUTS + z.CONDITION_INPUTS)
gel_raw = frame[gel_cols].apply(pd.to_numeric, errors='coerce').to_numpy(float)

# ---- OSDA descriptor spaces per recipe
desc30 = np.column_stack([pd.to_numeric(frame[col], errors='coerce').fillna(0).to_numpy(float)
                          for col in z.OSDA_TABLE_INPUTS.values()])
rd = z.osda_composition(frame['osda1 smiles'].tolist(), data.rdkit_table).to_numpy(float)
desc30 = np.hstack([desc30, rd])
osda_tab = pd.read_csv(ROOT / 'data/zeosyn/osda_descriptors.csv').drop(columns=['Unnamed: 0'])
num_cols = [c for c in osda_tab.columns if c != 'osda smiles']
full_lookup = {s: r for s, r in zip(osda_tab['osda smiles'], osda_tab[num_cols].apply(pd.to_numeric, errors='coerce').to_numpy(float))}
full = np.array([full_lookup.get(s, np.full(len(num_cols), np.nan)) if isinstance(s, str) else np.zeros(len(num_cols))
                 for s in frame['osda1 smiles']])
desc_full = np.hstack([np.nan_to_num(full, nan=0.0), rd])
log(f'desc30 shape={desc30.shape} desc_full shape={desc_full.shape}; osda rows missing from table: '
    f'{int(sum(isinstance(s, str) and s not in full_lookup for s in frame["osda1 smiles"]))}')

# ---- imputation: loader's IterativeImputer settings, restricted to the 43 D0 columns (fast; ceiling analysis only)
def impute_d0(frame, fit_rows):
    cols = list(z.D0)
    x = frame[cols].apply(pd.to_numeric, errors='coerce')
    imp = z._imputer().fit(x.iloc[fit_rows])
    return pd.DataFrame(imp.transform(x), columns=cols)

log('imputation restricted to the 43 D0 columns (IterativeImputer, same settings as loader)')
t = time.time()
d0_paper = z.d0_matrix(impute_d0(frame, paper_train))
log(f'paper-split imputation took {time.time() - t:.0f}s')
arrays = dict(d0_paper=d0_paper, y=y.astype(str), paper_train=paper_train, paper_test=paper_test,
              osda_fold=fold, gel_raw=gel_raw, osda_desc30=desc30, osda_desc_full=desc_full,
              test_dois=np.array(test_dois, dtype=object), gel_cols=np.array(gel_cols, dtype=object),
              d0_cols=np.array(list(z.D0), dtype=object),
              desc30_cols=np.array(list(z.OSDA_TABLE_INPUTS) + list(z.RDKIT_INPUTS), dtype=object))
np.savez_compressed(CACHE / 'base.npz', **arrays)
log('saved base.npz (paper split); now per-fold imputation for the OSDA split')
for f in range(OSDA_FOLDS):
    t = time.time()
    tr = np.flatnonzero(fold != f)
    arrays[f'd0_osda_f{f}'] = z.d0_matrix(impute_d0(frame, tr))
    log(f'fold {f} imputation took {time.time() - t:.0f}s')
    np.savez_compressed(CACHE / 'base.npz', **arrays)
log('done')
