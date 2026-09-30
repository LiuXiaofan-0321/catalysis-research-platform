"""JACS Au 10.1021/jacsau.4c00429: native entropy baseline and paired fits.

The SI is input data, never executable code. The original network, target,
loss and 4000-epoch schedule are transcribed here for an auditable adapter.
"""
from __future__ import annotations

import json
import csv
import time
from pathlib import Path
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

FEATURES = ['MW', 'LabuteASA', 'PBF', 'PMI1', 'PMI2', 'PMI3', 'SPAN',
            'GeDi', 'Vol', 'density', 'ASA', 'AV', 'lsd_f', 'lsd_p']
UNITS = ['g/mol', 'angstrom^2', 'angstrom', 'angstrom^2*amu',
         'angstrom^2*amu', 'angstrom^2*amu', 'angstrom', 'angstrom',
         'angstrom^3', 'source density (native numerical scale)', 'm^2/g',
         'cm^3/g', 'angstrom', 'angstrom']
DOI = '10.1021/jacsau.4c00429'
R = 8.31446261815324


def save_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    temp.replace(path)


def load_data(root):
    root = Path(root)
    p = root / 's_ads' / 'training_model'
    x = np.load(p / 'X_15.npy', allow_pickle=False)
    y = np.load(p / 'y_15.npy', allow_pickle=False)
    keys = np.load(p / 'y_keys_15.npy', allow_pickle=False)
    order = np.load(p / 'train_inds.npy', allow_pickle=False).astype(int)
    assert x.shape == (3690, 15) and y.shape == (3690, 5)
    assert len(np.unique(order)) == len(x)
    assert np.isfinite(x).all() and np.isfinite(y).all()
    gas = x[:, 14]
    assert (gas > 0).all()
    # y[:,1] is negative Delta S/R. Target is s_ads/s_gas.
    ratio = 1 + y[:, 1] / gas
    assert ((ratio >= 0) & (ratio <= 1)).all()
    with (root / 'raw_data.csv').open(encoding='utf-8-sig') as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == len(x)
    assert all((row['frmwrk'], row['molecule']) == tuple(key) for row, key in zip(rows, keys))
    categories = np.array([row['category'] for row in rows])
    return dict(x=x[:, :14], all_x=x, categories=categories, gas=gas, ratio=ratio,
                entropy=-y[:, 1], uncertainty=y[:, 0] / gas,
                keys=keys, order=order, root=root)


def make_split(data):
    # Keep the author's outer test intact. Inner scoring rows are never fitted.
    order = data['order']; end = int(.8 * len(order))
    development = order[:end].copy()
    rng = np.random.default_rng(20260928); rng.shuffle(development)
    score_n = int(np.ceil(.2 * len(development)))
    split = {'train': development[score_n:], 'score': development[:score_n], 'test': order[end:]}
    assert len(set(split['train']) & set(split['score'])) == 0
    assert len(set(np.concatenate([split['train'], split['score']])) & set(split['test'])) == 0
    return split


def network(n_features):
    import torch
    from torch import nn
    class EntropyNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(n_features, 191)
            self.fc2 = nn.Linear(191, 181)
            self.fc3 = nn.Linear(181, 181)
            self.fc4 = nn.Linear(181, 1)
        def forward(self, x):
            for layer in (self.fc1, self.fc2, self.fc3):
                x = torch.relu(layer(x))
            # Preserve the published implementation (range [0.5,1]), even
            # though the paper describes the more general [0,1] bound.
            return torch.sigmoid(torch.relu(self.fc4(x)))
    return EntropyNet()


def all_raw_matrix(data, train):
    # Categories are pre-adsorption molecular classes. Identifiers, SHAP,
    # predictions, thermodynamic outcomes and convergence columns are excluded.
    from sklearn.preprocessing import OneHotEncoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoder.fit(data['categories'][train, None])
    return np.column_stack([data['all_x'], encoder.transform(data['categories'][:, None])])


def metrics(data, idx, ratio_pred):
    prediction = (1 - np.asarray(ratio_pred).reshape(-1)) * data['gas'][idx]
    truth = data['entropy'][idx]
    mae = float(mean_absolute_error(truth, prediction))
    return {'mae_R': mae, 'mae_J_mol_K': mae * R,
            'r2': float(r2_score(truth, prediction)), 'n': len(idx)}


def fit(data, x, train, *, epochs=4000, seed=3, kind='ann'):
    import torch
    start = time.monotonic()
    scaler = StandardScaler().fit(x[train])
    xt = scaler.transform(x).astype('float32')
    if not np.isfinite(xt).all():
        raise ValueError('Nonfinite scaled inputs')
    if kind == 'hgb':
        from sklearn.ensemble import HistGradientBoostingRegressor
        model = HistGradientBoostingRegressor(max_iter=250, max_leaf_nodes=15,
                    l2_regularization=1., early_stopping=False, random_state=seed)
        model.fit(xt[train], data['ratio'][train])
        return model.predict(xt), time.monotonic() - start
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    model = network(x.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    tx = torch.from_numpy(xt[train])
    ty = torch.tensor(data['ratio'][train, None], dtype=torch.float32)
    error = torch.tensor(data['uncertainty'][train, None], dtype=torch.float32)
    # The source's extra output ReLU can put EVERY training sample in its
    # zero-gradient region at random initialization (confirmed in first pilot).
    # Preserve its architecture, but deterministically shift only the initial
    # output bias so all train logits are >= .1. No labels or scoring rows used.
    # Apply the identical initialization rule to D0, all-raw and every D0+X fit.
    with torch.no_grad():
        hidden = tx
        for layer in (model.fc1, model.fc2, model.fc3):
            hidden = torch.relu(layer(hidden))
        minimum_logit = float(model.fc4(hidden).min())
        model.fc4.bias.add_(max(0., .1 - minimum_logit))
    for _ in range(epochs):
        output = model(tx)
        weighted = torch.square((output - ty).abs() / (error.abs() + .5)).sum()
        l1 = .5 * torch.norm(torch.cat([p.flatten() for p in model.fc1.parameters()]), 1)
        loss = weighted + l1
        if not torch.isfinite(loss):
            raise ValueError('Nonfinite training loss')
        optimizer.zero_grad(); loss.backward(); optimizer.step()
    model.eval()
    with torch.no_grad():
        prediction = model(torch.from_numpy(xt)).numpy().reshape(-1)
    if float(np.std(prediction[train])) < 1e-6:
        raise ValueError('Collapsed ANN: constant predictions on training rows')
    return prediction, time.monotonic() - start


def reproduce(data):
    import torch
    torch.set_num_threads(2)
    p = data['root'] / 's_ads' / 'best_model'
    original_order = np.load(p / 'train_inds.npy', allow_pickle=False).astype(int)
    idx = original_order[int(.8 * len(original_order)):]
    model = network(14)
    model.load_state_dict(torch.load(p / 'ANN_param.pt', map_location='cpu', weights_only=True))
    model.eval()
    # Only legacy replay uses whole-data normalization to match saved weights.
    x = StandardScaler().fit_transform(data['x']).astype('float32')
    with torch.no_grad():
        pred = model(torch.from_numpy(x[idx])).numpy().reshape(-1)
    saved = torch.load(p / 'y_pred_best.pt', map_location='cpu', weights_only=True).numpy().reshape(-1)
    truth = torch.load(p / 'y_test_best.pt', map_location='cpu', weights_only=True).numpy().reshape(-1)
    out = {'checkpoint_metrics': metrics(data, idx, pred),
           'saved_prediction_metrics': metrics(data, idx, saved),
           'prediction_max_abs_diff': float(np.max(np.abs(pred - saved))),
           'target_max_abs_diff': float(np.max(np.abs(truth - data['ratio'][idx]))),
           'paper_reported_mae_R': .57,
           'notes': ['Legacy scaler fits all 3690 rows; new experiments fit train only.',
                     'Native network uses sigmoid(ReLU(output)), with range [0.5,1].',
                     'Convergence error weights are training-label uncertainty, not model inputs.',
                     'Sgas is an independent molecular quantity used in target conversion; not a native input.',
                     'Author erroranalysis calls squared Pearson correlation R2; we report sklearn R2.',
                     'Density numerical values appear mass-density-like; retain native values and do not assert units before SI verification.']}
    out['passed'] = (out['prediction_max_abs_diff'] < 1e-4 and out['target_max_abs_diff'] < 1e-5
                     and abs(out['checkpoint_metrics']['mae_R'] - .57) < .03)
    return out


def baseline(data, output, epochs=4000):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    replay = reproduce(data); save_json(output / 'reproduction.json', replay)
    print(json.dumps({'reproduction': replay}), flush=True)
    if not replay['passed']:
        raise RuntimeError('Published checkpoint replay failed; discovery must not start')
    split = make_split(data)
    save_json(output / 'split.json', {k:v.tolist() for k,v in split.items()})
    dummy = float(mean_absolute_error(data['entropy'][split['score']],
                  np.full(len(split['score']),np.median(data['entropy'][split['train']]))))
    result = {'status':'running', 'epochs':epochs, 'seed':3, 'features':FEATURES,
              'initialization':'train-feature-only positive output-logit bias, minimum .1',
              'dummy_train_median_score_mae_R':dummy,
              'split_counts':{k:len(v) for k,v in split.items()}, 'controls':{}}
    all_x = all_raw_matrix(data, split['train'])
    result['all_raw_features'] = '14 native + independent Sgas + train-fitted molecular-category one-hot'
    for name, x, kind in [('native14_ann',data['x'],'ann'), ('all_raw_ann',all_x,'ann'),
                          ('native14_hgb',data['x'],'hgb'), ('all_raw_hgb',all_x,'hgb')]:
        pred, seconds = fit(data,x,split['train'],epochs=epochs,kind=kind)
        # Cache predictions but do not expose test metrics to hypothesis calls.
        np.save(output / (name + '.npy'), pred)
        result['controls'][name] = {'score':metrics(data,split['score'],pred[split['score']]),'seconds':seconds}
        save_json(output / 'baseline.json', result)
        print(json.dumps({name:result['controls'][name]}),flush=True)
        if kind == 'ann' and result['controls'][name]['score']['mae_R'] >= dummy:
            raise RuntimeError(name+' does not outperform constant training-median predictor; block discovery')
    result['status']='completed'; save_json(output / 'baseline.json', result)
    return result
