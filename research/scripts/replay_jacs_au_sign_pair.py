"""Predeclared sign-equivalent ANN diagnostic, not candidate or seed selection.

Each seed fits positive/negative with paired initial functions, plus the old
same-seed unpaired negative control. All arms reported; no winner selected.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import time

import numpy as np
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from catalysis_research.experiments.jacs_au import network, fit, metrics, load_data, make_split, save_json
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v4 import checked_values

SEEDS = (3, 7, 11, 17, 23)


def paired_sign_fit(data, positive, negative, train, *, seed, epochs=4000):
    import torch
    start = time.monotonic()
    xp = StandardScaler().fit(positive[train]).transform(positive).astype('float32')
    xn = StandardScaler().fit(negative[train]).transform(negative).astype('float32')
    expected = xp.copy(); expected[:, -1] *= -1
    np.testing.assert_allclose(xn, expected, atol=1e-6, rtol=1e-6)
    residual = float(np.max(np.abs(xn-expected)))
    # Enforce the exact algebraic mirror in this controlled arm. The old unpaired
    # arm below retains independently evaluated/scaled negative expression.
    xn = expected
    torch.manual_seed(seed); torch.set_num_threads(2)
    p = network(xp.shape[1]); n = deepcopy(p)
    with torch.no_grad(): n.fc1.weight[:, -1].neg_()
    tp, tn = torch.from_numpy(xp[train]), torch.from_numpy(xn[train])
    ty = torch.tensor(data['ratio'][train, None], dtype=torch.float32)
    error = torch.tensor(data['uncertainty'][train, None], dtype=torch.float32)
    with torch.no_grad():
        hidden = tp
        for layer in (p.fc1,p.fc2,p.fc3): hidden = torch.relu(layer(hidden))
        shift = max(0., .1-float(p.fc4(hidden).min()))
        p.fc4.bias.add_(shift); n.fc4.bias.add_(shift)
        initial_difference = float(torch.max(torch.abs(p(tp)-n(tn))))
        l1p = torch.norm(torch.cat([x.flatten() for x in p.fc1.parameters()]),1)
        l1n = torch.norm(torch.cat([x.flatten() for x in n.fc1.parameters()]),1)
        l1_difference = float(torch.abs(l1p-l1n))
    if initial_difference > 1e-6 or l1_difference > 1e-6:
        raise ValueError('Function-equivalent initialization verification failed')
    predictions = {}
    for label, model, train_x, full_x in [('positive',p,tp,xp),('paired_negative',n,tn,xn)]:
        optimizer = torch.optim.Adam(model.parameters(),lr=1e-4)
        for _ in range(epochs):
            out = model(train_x)
            weighted = torch.square((out-ty).abs()/(error.abs()+.5)).sum()
            l1 = .5*torch.norm(torch.cat([x.flatten() for x in model.fc1.parameters()]),1)
            loss = weighted+l1
            if not torch.isfinite(loss): raise ValueError('Nonfinite paired diagnostic loss')
            optimizer.zero_grad(); loss.backward(); optimizer.step()
        model.eval()
        with torch.no_grad(): pred = model(torch.from_numpy(full_x)).numpy().reshape(-1)
        if not np.isfinite(pred).all() or np.std(pred[train]) < 1e-6:
            raise ValueError('Invalid or collapsed paired diagnostic fit')
        predictions[label] = pred
    return predictions, {'initial_prediction_max_abs_difference': initial_difference,
                         'initial_fc1_l1_difference': l1_difference, 'initial_output_bias_shift': shift,
                         'independent_standardization_sign_residual': residual,
                         'paired_input_rule': 'Exact float32 sign mirror after verifying independently scaled expressions',
                         'seconds': time.monotonic()-start}


def run(data, split, source, seed, fit_function=fit, paired_function=paired_sign_fit):
    ds = [json.loads((source/'high'/'discovery'/f'small_kg_rag_agent-replicate-{r}.json').read_text(encoding='utf-8')) for r in (2,3)]
    candidates = [next(c for c in d['rounds'][0]['candidates'] if c['slot_id']=='h1') for d in ds]
    if any(d['rounds'][0]['before_mae_R'] != d['d0_score_mae_R'] for d in ds):
        raise ValueError('Both historical sign-pair prefixes must be D0')
    env,_ = formula_environment(data,split['train'])
    fm,fp = [checked_values(c['formula'],env) for c in candidates]
    np.testing.assert_allclose(fm,-fp,atol=1e-12,rtol=1e-12)
    positive,negative = np.column_stack([data['x'],fp]),np.column_stack([data['x'],fm])
    result = {'protocol':'fixed-sign-pair-v1','fit_seed':seed,'epochs':4000,'api_calls':0,
              'status':'completed','formula_positive':candidates[1]['formula'],
              'formula_negative':candidates[0]['formula'],'arms':{},'no_outcome_selection':True,
              'outer_is_development_diagnostic':True}
    try:
        pred,init = paired_function(data,positive,negative,split['train'],seed=seed,epochs=4000)
        result['paired_initialization'] = init
        for arm in ('positive','paired_negative'):
            result['arms'][arm] = {'status':'scored',
                'score':metrics(data,split['score'],pred[arm][split['score']]),
                'outer':metrics(data,split['test'],pred[arm][split['test']])}
        result['paired_final_prediction_max_abs_difference'] = float(np.max(np.abs(pred['positive']-pred['paired_negative'])))
    except (ValueError,RuntimeError,FloatingPointError,AssertionError) as error:
        result.update(status='incomplete',paired_failure=str(error))
    try:
        original,seconds = fit_function(data,negative,split['train'],seed=seed,epochs=4000)
        result['arms']['original_unpaired_negative'] = {'status':'scored','seconds':seconds,
            'score':metrics(data,split['score'],original[split['score']]),
            'outer':metrics(data,split['test'],original[split['test']])}
    except (ValueError,RuntimeError,FloatingPointError) as error:
        result['arms']['original_unpaired_negative'] = {'status':'fit_failure','reason':str(error)}
        result['status'] = 'incomplete'
    if seed == 3:
        result['historical_seed3_scores'] = {'negative':candidates[0]['score']['mae_R'],'positive':candidates[1]['score']['mae_R']}
        for arm,idx in [('positive',1),('original_unpaired_negative',0)]:
            if result['arms'].get(arm,{}).get('status') == 'scored':
                result['arms'][arm]['historical_replay_delta_R'] = result['arms'][arm]['score']['mae_R']-candidates[idx]['score']['mae_R']
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('data','baseline','source','output'): p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--seed-index',type=int,choices=range(5),required=True)
    a=p.parse_args()
    if a.output.exists(): raise ValueError('New diagnostic output required')
    data=load_data(a.data)
    split={k:np.asarray(v,dtype=int) for k,v in json.loads((a.baseline/'split.json').read_text()).items()}
    if any(not np.array_equal(v,make_split(data)[k]) for k,v in split.items()): raise ValueError('Original split required')
    save_json(a.output,run(data,split,a.source,SEEDS[a.seed_index]))
