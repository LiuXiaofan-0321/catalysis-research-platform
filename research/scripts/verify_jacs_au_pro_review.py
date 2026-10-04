"""Check the Pro review's sign-pair finding against saved V4 trajectories.

Zero API calls and zero model fits. Positive-grid checks illustrate algebra;
they are not replay on the original 3690 rows or evidence about optimization.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import sys

import numpy as np
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from catalysis_research.experiments.jacs_au import save_json
from catalysis_research.experiments.jacs_au_kg_v4 import evaluate_formula


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sign_identity_check(negative_formula, positive_formula):
    vol, diameter = np.meshgrid(np.geomspace(.05, 20, 31), np.geomspace(.05, 20, 29))
    env = {'q_Vol': vol.ravel(), 'q_lsd_f': diameter.ravel(), 'MW': np.ones(vol.size)}
    negative = evaluate_formula(negative_formula, env)
    positive = evaluate_formula(positive_formula, env)
    np.testing.assert_allclose(negative, -positive, atol=1e-12, rtol=1e-12)
    train = np.arange(0, len(positive), 2)
    zp = StandardScaler().fit(positive[train, None]).transform(positive[:, None])
    zn = StandardScaler().fit(negative[train, None]).transform(negative[:, None])
    np.testing.assert_allclose(zn, -zp, atol=1e-12, rtol=1e-12)
    # The first ANN layer is affine. Reverse the matching weight column too.
    rng = np.random.default_rng(20261001)
    base = rng.normal(size=(len(positive), 14))
    xp, xn = np.column_stack([base, zp]), np.column_stack([base, zn])
    wp = rng.normal(size=(191, 15))
    wn = wp.copy(); wn[:, -1] *= -1
    bias = rng.normal(size=191)
    pre_p, pre_n = xp @ wp.T + bias, xn @ wn.T + bias
    np.testing.assert_allclose(pre_p, pre_n, atol=1e-12, rtol=1e-12)
    np.testing.assert_allclose(np.abs(wp).sum(), np.abs(wn).sum())
    return {
        'domain': 'synthetic positive grid, not original data', 'grid_rows': len(positive),
        'max_abs_f_plus_f_minus': float(np.max(np.abs(negative + positive))),
        'max_abs_standardized_sign_residual': float(np.max(np.abs(zp + zn))),
        'max_abs_paired_first_layer_residual': float(np.max(np.abs(pre_p - pre_n))),
        'l1_weight_penalty_equal': True,
        'algebraic_identity': '2*log(d)-log(v) = -log(v/d**2), v>0,d>0',
        'training_performed': False,
    }


def verify(source):
    summary = read(source / 'summary.json')
    assert summary['complete'] is True
    raw = {}
    gains = {}
    for mode in ('agent', 'rag_agent', 'small_kg_rag_agent'):
        ds = [read(source / 'high' / 'discovery' / f'{mode}-replicate-{rep}.json')
              for rep in (1, 2, 3)]
        assert all(d['status'] == 'completed' and d['reasoning_effort'] == 'high' for d in ds)
        raw[mode] = ds
        values = np.array([d['score_improvement_pct'] for d in ds])
        reported = summary['groups']['high'][mode]['score_gain_pct']
        np.testing.assert_allclose(values.mean(), reported['mean'], atol=1e-12, rtol=0)
        np.testing.assert_allclose(values.std(ddof=1), reported['std'], atol=1e-12, rtol=0)
        gains[mode] = {'trace_gains_pct': values.tolist(), 'mean': float(values.mean()),
                       'sample_std_pp': float(values.std(ddof=1)), 'n': 3}
    negative, positive = raw['small_kg_rag_agent'][1:]
    assert negative['d0_score_mae_R'] == positive['d0_score_mae_R']
    for key in ('epochs', 'fit_seed', 'training_references', 'training_feature_domains'):
        assert negative[key] == positive[key], key
    assert negative['epochs'] == 4000 and negative['fit_seed'] == 3
    pair = []
    for d in (negative, positive):
        rd = d['rounds'][0]
        c = next(c for c in rd['candidates'] if c['slot_id'] == 'h1')
        assert c['status'] == 'scored' and rd['before_mae_R'] == d['d0_score_mae_R']
        gain = 100 * (d['d0_score_mae_R'] - c['score']['mae_R']) / d['d0_score_mae_R']
        np.testing.assert_allclose(gain, 100*c['marginal_improvement']/d['d0_score_mae_R'], atol=1e-10)
        pair.append({'source': f"high/discovery/small_kg_rag_agent-replicate-{d['replicate']}.json",
                     'round': 1, 'slot': 'h1', 'formula': c['formula'],
                     'score_mae_R': c['score']['mae_R'], 'gain_pct': gain,
                     'precheck_status': c['precheck']['status'],
                     'target_association': c['precheck']['scientific_check']['target_association']})
    return {'profile': 'pro-review-verification-20261001', 'status': 'saved-records-verified',
            'api_calls': 0, 'ann_fits': 0, 'high_groups': gains, 'sign_pair': pair,
            'sign_pair_gain_gap_pp': pair[1]['gain_pct'] - pair[0]['gain_pct'],
            'kg_minus_agent_mean_pp': gains['small_kg_rag_agent']['mean']-gains['agent']['mean'],
            'identity_check': sign_identity_check(pair[0]['formula'], pair[1]['formula']),
            'limits': ['No original-data ANN replay or paired optimizer test performed.',
                       'Sign-pair discovery is post hoc and illustrative, not a group effect estimate.',
                       'target_association=contradicted does not itself reject V4 candidates.',
                       'No attribution of the whole method ranking to initialization established.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise ValueError('Use a new verification output; preserve prior records')
    result = verify(a.source)
    save_json(a.output, result)
    print(json.dumps({k: result[k] for k in ('status', 'api_calls', 'ann_fits',
                     'sign_pair_gain_gap_pp', 'kg_minus_agent_mean_pp')}))
