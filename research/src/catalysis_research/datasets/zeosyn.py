"""ZeoSyn adapter (Pan et al., ACS Cent. Sci. 2024, DOI 10.1021/acscentsci.3c01615).

The native frame reproduces the authors' ``classifier.ipynb`` row selection,
OSDA descriptor merge, imputation and 43-column D0. The experiment frame keeps
the same rows and D0 but uses a DOI-grouped split, fits the imputer on training
rows only, and exposes a fixed set of label-free raw inputs for new descriptors.
Product labels, product-side framework descriptors, seeds and characterization
results are never exposed as inputs.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

SOURCE_DOI = '10.1021/acscentsci.3c01615'
SOURCE_REPOSITORY = 'https://github.com/eltonpan/zeosyn_dataset'
DATA_FILES = ('ZEOSYN.xlsx', 'osda_descriptors.csv')
EXPECTED_SHA256 = {
    'ZEOSYN.xlsx': '95f9b8f5d1464fc3d577d93f9551e40cc984b5b475a49ddc8177f598c3c1987c',
    'osda_descriptors.csv': 'd6677fd3cf6f120405bbd14867aed6b1b9b8f5e788532a948fe1042f1b1f77ba',
}

# utils.osda_cols in the source repository.
NATIVE_OSDA_COLS = (
    'asphericity', 'axes', 'bertz_ct', 'binding', 'eccentricity', 'formal_charge',
    'free_sasa', 'getaway', 'gyration_radius', 'inertial_shape_factor', 'mol_weight',
    'npr1', 'npr2', 'num_bonds', 'num_rot_bonds', 'pmi1', 'pmi2', 'pmi3',
    'spherocity_index', 'volume', 'whim',
)

# utils.cols_to_drop in the source repository.
NATIVE_DROP = (
    'doi', 'normed', 'seed', 'aging_time', 'aging_temp', 'rotation', 'Seed_type',
    'react_vol', 'pH', 'osda1', 'osda2', 'osda3', 'product1', 'product2', 'product3',
    'precursors', 'brands', 'Si/Al', 'yield', 'percent cryst', 'crystal size',
    'micropore volume', 'micropore diameter', 'bet area', 'external surface area',
    'Notes', 'title', 'abstract_keywords', 'recipe_keywords', 'osda1 synonyms',
    'osda2 synonyms', 'osda3 synonyms', 'osda1 iupac', 'osda2 iupac', 'osda3 iupac',
    'osda1 smiles', 'osda2 smiles', 'osda3 smiles', 'osda1 formula', 'osda2 formula',
    'osda3 formula', 'Code1', 'Code2', 'Code3', 'year',
)

GEL_INPUTS = (
    'Si', 'Al', 'P', 'Na', 'K', 'Li', 'Sr', 'Rb', 'Cs', 'Ba', 'Ca', 'F', 'Ge', 'Ti',
    'B', 'Mg', 'Ga', 'Zn', 'Be', 'W', 'Cu', 'Sn', 'Zr', 'V', 'H2O', 'sda1', 'OH',
)
CONDITION_INPUTS = ('cryst_time', 'cryst_temp')
NATIVE_OSDA_D0 = (
    'osda1_asphericity_mean_0', 'osda1_axes_mean_0', 'osda1_axes_mean_1',
    'osda1_formal_charge', 'osda1_free_sasa_mean_0', 'osda1_mol_weight',
    'osda1_npr1_mean_0', 'osda1_npr2_mean_0', 'osda1_num_rot_bonds_mean_0',
    'osda1_pmi1_mean_0', 'osda1_pmi2_mean_0', 'osda1_pmi3_mean_0',
    'osda1_spherocity_index_mean_0', 'osda1_volume_mean_0',
)
D0 = GEL_INPUTS + CONDITION_INPUTS + NATIVE_OSDA_D0

# Scalar OSDA conformer descriptors from the authors' table, exposed under
# short names. Vector descriptors (box, getaway, whim) are not exposed.
OSDA_TABLE_INPUTS = {
    'osda_asphericity': 'osda1_asphericity_mean_0',
    'osda_axis1': 'osda1_axes_mean_0',
    'osda_axis2': 'osda1_axes_mean_1',
    'osda_bertz_ct': 'osda1_bertz_ct_mean_0',
    'osda_eccentricity': 'osda1_eccentricity_mean_0',
    'osda_charge': 'osda1_formal_charge',
    'osda_sasa': 'osda1_free_sasa_mean_0',
    'osda_gyration_radius': 'osda1_gyration_radius_mean_0',
    'osda_inertial_shape_factor': 'osda1_inertial_shape_factor_mean_0',
    'osda_mol_weight': 'osda1_mol_weight',
    'osda_npr1': 'osda1_npr1_mean_0',
    'osda_npr2': 'osda1_npr2_mean_0',
    'osda_num_bonds': 'osda1_num_bonds_mean_0',
    'osda_rot_bonds': 'osda1_num_rot_bonds_mean_0',
    'osda_pmi1': 'osda1_pmi1_mean_0',
    'osda_pmi2': 'osda1_pmi2_mean_0',
    'osda_pmi3': 'osda1_pmi3_mean_0',
    'osda_sphericity': 'osda1_spherocity_index_mean_0',
    'osda_volume': 'osda1_volume_mean_0',
}

# Composition counts of OSDA1 computed with RDKit from the recorded SMILES.
RDKIT_INPUTS = (
    'osda_nC', 'osda_nN', 'osda_nN_quaternary', 'osda_nO', 'osda_nP', 'osda_nHeavy',
    'osda_nRings', 'osda_nAromaticRings', 'osda_fraction_sp3', 'osda_logP', 'osda_tpsa',
)
COUNT_INPUTS = ('n_osda',)

INPUT_UNITS = {
    **{k: 'mole fraction of the normalized gel (all gel species sum to 1)' for k in GEL_INPUTS},
    'sda1': 'mole fraction of OSDA1 in the normalized gel',
    'cryst_time': 'hours', 'cryst_temp': 'degrees Celsius',
    'osda_charge': 'formal charge (e)', 'osda_mol_weight': 'g/mol',
    'osda_volume': 'angstrom^3', 'osda_sasa': 'angstrom^2',
    'osda_axis1': 'angstrom', 'osda_axis2': 'angstrom', 'osda_gyration_radius': 'angstrom',
    'osda_pmi1': 'amu*angstrom^2', 'osda_pmi2': 'amu*angstrom^2', 'osda_pmi3': 'amu*angstrom^2',
    'osda_logP': 'Crippen logP', 'osda_tpsa': 'angstrom^2',
    'n_osda': 'number of distinct OSDAs recorded (0-3)',
}


def raw_input_names():
    return (*GEL_INPUTS, *CONDITION_INPUTS, *OSDA_TABLE_INPUTS, *RDKIT_INPUTS, *COUNT_INPUTS)


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def normalize_doi(value):
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().casefold()
    for prefix in ('https://doi.org/', 'http://doi.org/', 'http://dx.doi.org/', 'https://dx.doi.org/', 'doi:'):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text or None


def load_tables(root):
    root = Path(root)
    df = pd.read_excel(root / 'ZEOSYN.xlsx')
    osda = pd.read_csv(root / 'osda_descriptors.csv').drop(columns=['Unnamed: 0'])
    return df, osda


def native_frame(df, osda):
    """Rows and merged OSDA columns exactly as in the authors' notebook."""
    avail = set(osda['osda smiles'])
    used = set(df['osda1 smiles'].dropna()) | set(df['osda2 smiles'].dropna()) | set(df['osda3 smiles'].dropna())
    feat = used & avail
    with_feats = df[df['osda1 smiles'].isin(feat) | df['osda2 smiles'].isin(feat) | df['osda3 smiles'].isin(feat)]
    # The notebook tests osda2 twice and never osda3; kept for fidelity.
    free = df[df['osda1 smiles'].isna() & df['osda2 smiles'].isna() & df['osda2 smiles'].isna() & ~df['Si'].isna()]
    frame = pd.concat([with_feats, free])
    parts = [osda.loc[:, osda.columns.str.contains(c)] for c in NATIVE_OSDA_COLS]
    parts.append(osda.loc[:, osda.columns.str.contains('osda smiles')])
    selected = pd.concat(parts, axis=1)
    for k in ('osda1', 'osda2', 'osda3'):
        frame = frame.merge(selected.add_prefix(k + '_'), left_on=k + ' smiles',
                            right_on=k + '_osda smiles', how='outer')
        frame = frame[~frame['Unnamed: 0'].isna()]
    for c in NATIVE_OSDA_COLS:
        mask = frame.columns.str.contains(c)
        frame.loc[:, mask] = frame.loc[:, mask].fillna(0)
    frame = frame.drop(columns=['osda1_osda smiles', 'osda2_osda smiles', 'osda3_osda smiles'])
    return frame.reset_index(drop=True)


def _imputer():
    from sklearn.experimental import enable_iterative_imputer  # noqa: F401
    from sklearn.impute import IterativeImputer
    return IterativeImputer(min_value=0., sample_posterior=True, skip_complete=True, random_state=0)


def imputation_columns(frame):
    return [c for c in frame.columns if c not in NATIVE_DROP and c != 'Unnamed: 0']


def impute(frame, fit_rows):
    """Native IterativeImputer over all retained numeric columns, fit on ``fit_rows``."""
    cols = imputation_columns(frame)
    x = frame[cols].apply(pd.to_numeric, errors='coerce')
    imp = _imputer().fit(x.iloc[fit_rows])
    return pd.DataFrame(imp.transform(x), columns=cols)


def labels(frame):
    return frame['Code1'].fillna('Failed').astype(str).to_numpy()


def rdkit_features(smiles_values):
    from rdkit import Chem, RDLogger
    from rdkit.Chem import Crippen, rdMolDescriptors
    RDLogger.DisableLog('rdApp.*')
    cache = {}
    rows = []
    for s in smiles_values:
        if not isinstance(s, str) or not s.strip():
            rows.append([0.] * len(RDKIT_INPUTS))
            continue
        if s not in cache:
            mol = Chem.MolFromSmiles(s)
            if mol is None:
                cache[s] = [np.nan] * len(RDKIT_INPUTS)
            else:
                atoms = [a for a in mol.GetAtoms()]
                sym = [a.GetSymbol() for a in atoms]
                quat = sum(1 for a in atoms if a.GetSymbol() in ('N', 'P') and a.GetFormalCharge() > 0
                           and a.GetTotalNumHs() == 0 and a.GetDegree() == 4)
                cache[s] = [float(sym.count('C')), float(sym.count('N')), float(quat), float(sym.count('O')),
                            float(sym.count('P')), float(mol.GetNumHeavyAtoms()),
                            float(rdMolDescriptors.CalcNumRings(mol)),
                            float(rdMolDescriptors.CalcNumAromaticRings(mol)),
                            float(rdMolDescriptors.CalcFractionCSP3(mol)), float(Crippen.MolLogP(mol)),
                            float(rdMolDescriptors.CalcTPSA(mol))]
        rows.append(cache[s])
    return pd.DataFrame(rows, columns=list(RDKIT_INPUTS))


def raw_inputs(frame, imputed):
    env = {k: imputed[k].to_numpy(float) for k in GEL_INPUTS + CONDITION_INPUTS}
    for short, col in OSDA_TABLE_INPUTS.items():
        env[short] = pd.to_numeric(frame[col], errors='coerce').fillna(0).to_numpy(float)
    rd = rdkit_features(frame['osda1 smiles'].tolist())
    for k in RDKIT_INPUTS:
        env[k] = rd[k].to_numpy(float)
    env['n_osda'] = sum(frame[f'osda{i} smiles'].notna().astype(float) for i in (1, 2, 3)).to_numpy(float)
    return env


def d0_matrix(imputed):
    return imputed[list(D0)].to_numpy(float)


def native_split(n):
    """The notebook split: 20% test, then 12.5% of the rest as validation (merged back for fitting)."""
    from sklearn.model_selection import train_test_split
    idx = np.arange(n)
    rest, test = train_test_split(idx, test_size=0.2, random_state=0)
    train, val = train_test_split(rest, test_size=0.125, random_state=0)
    return np.concatenate([train, val]), test


def doi_group_split(frame, *, test_fraction, seed):
    """Deterministic DOI-grouped split; rows without a DOI form one group per row."""
    dois = frame['doi'].map(normalize_doi)
    groups = np.array([d if isinstance(d, str) and d else f'row:{i}' for i, d in enumerate(dois)], dtype=object)
    unique = np.array(sorted(set(groups)), dtype=object)
    rng = np.random.default_rng(seed)
    order = unique[rng.permutation(len(unique))]
    sizes = pd.Series(groups).value_counts()
    target = test_fraction * len(frame)
    test_groups, total = set(), 0
    for g in order:
        if total >= target:
            break
        test_groups.add(g)
        total += int(sizes[g])
    is_test = np.array([g in test_groups for g in groups])
    test_dois = sorted(g for g in test_groups if not g.startswith('row:'))
    return np.flatnonzero(~is_test), np.flatnonzero(is_test), test_dois


@dataclass
class ZeoSynData:
    frame: pd.DataFrame
    y: np.ndarray
    source_hashes: dict


def load(root):
    root = Path(root)
    hashes = {f: file_sha256(root / f) for f in DATA_FILES}
    if hashes != EXPECTED_SHA256:
        raise ValueError(f'ZeoSyn source files differ from the frozen release: {hashes}')
    df, osda = load_tables(root)
    frame = native_frame(df, osda)
    return ZeoSynData(frame=frame, y=labels(frame), source_hashes=hashes)


def classification_metrics(y_true, y_pred):
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
    present = sorted(set(y_true))
    return {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'macro_f1': float(f1_score(y_true, y_pred, labels=present, average='macro', zero_division=0)),
        # classification_report convention (labels in y_true or y_pred), as printed in the notebook.
        'macro_f1_report': float(f1_score(y_true, y_pred, average='macro', zero_division=0)),
        'balanced_accuracy': float(balanced_accuracy_score(y_true, y_pred)),
        'n': int(len(y_true)), 'n_classes_present': len(present),
    }


def fit_predict(x_train, y_train, x_test, *, seed, n_jobs=1, n_estimators=100):
    """Native model: sklearn RandomForestClassifier with default depth."""
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=None,
                                   random_state=seed, n_jobs=n_jobs)
    model.fit(x_train, y_train)
    return model.predict(x_test)


def reproduce_native(root, *, n_jobs=1):
    data = load(root)
    train, test = native_split(len(data.frame))
    imputed = impute(data.frame, np.arange(len(data.frame)))  # authors fit on all rows
    x = d0_matrix(imputed)
    pred = fit_predict(x[train], data.y[train], x[test], seed=0, n_jobs=n_jobs)
    return {
        'rows': int(len(data.frame)), 'train': int(len(train)), 'test': int(len(test)),
        'published': {'accuracy': 0.7358361774744028, 'macro_f1_sklearn_report': 0.6232778595020666, 'test': 4395},
        'reproduced': classification_metrics(data.y[test], pred),
        'source_hashes': data.source_hashes,
    }


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    tmp.replace(path)


def prepare_matrices(root, output, *, test_fraction, split_seed):
    """Freeze split, train-only imputation, D0 and raw inputs once per run."""
    data = load(root)
    train, test, test_dois = doi_group_split(data.frame, test_fraction=test_fraction, seed=split_seed)
    imputed = impute(data.frame, train)
    env = raw_inputs(data.frame, imputed)
    arrays = {'train': train, 'test': test, 'y': data.y.astype(str), 'd0': d0_matrix(imputed),
              'doi': data.frame['doi'].map(normalize_doi).fillna('').to_numpy(str),
              'year': pd.to_numeric(data.frame['year'], errors='coerce').to_numpy(float)}
    arrays.update({'env__' + k: v for k, v in env.items()})
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output, **arrays)
    train_classes = set(data.y[train])
    return {
        'rows': int(len(data.frame)), 'train_rows': int(len(train)), 'test_rows': int(len(test)),
        'test_dois': test_dois, 'split_seed': split_seed, 'test_fraction': test_fraction,
        'test_classes': len(set(data.y[test])),
        'test_rows_with_class_unseen_in_train': int(sum(v not in train_classes for v in data.y[test])),
        'source_hashes': data.source_hashes, 'matrix_sha256': file_sha256(output),
        'd0_columns': list(D0), 'raw_inputs': list(raw_input_names()),
    }


def load_matrices(path):
    with np.load(path, allow_pickle=False) as z:
        out = {k: z[k] for k in z.files}
    out['env'] = {k[5:]: out.pop(k) for k in list(out) if k.startswith('env__')}
    return out
