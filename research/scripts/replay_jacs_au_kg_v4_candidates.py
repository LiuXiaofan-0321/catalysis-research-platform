"""Offline paired ANN replay of blind/review/final candidates on frozen prefixes.

One block (0..53) per invocation. No model API, repairs, adaptive rollout, test
selection, or overwrite. Use the original data and the server ANN environment.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'scripts')]
from catalysis_research.experiments.jacs_au import fit, load_data, make_split, metrics, save_json
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v4 import checked_values, precheck
from diagnose_jacs_au_kg_v4 import read


def replay_block(data, split, block, historical, d0pred, fit_function=fit):
    rd = historical['rounds'][block['round'] - 1]
    expected_prefix = [c for previous in historical['rounds'][:block['round'] - 1]
                       for c in previous['final_candidates']
                       if c['slot_id'] in {x['slot_id'] for x in previous['candidates'] if x['retained']}]
    if (block['review_common']['drafts'] != rd['blind_drafts'] or
            block['fixed_prefix'] != expected_prefix):
        raise ValueError('Fixed drafts/prefix do not match historical provenance')
    env, _ = formula_environment(data, split['train'])
    reference = np.column_stack([data['x']] +
                                [checked_values(c['formula'], env) for c in block['fixed_prefix']])
    fit_calls = 0
    if block['fixed_prefix']:
        prefix_pred, _ = fit_function(data, reference, split['train'], epochs=4000, seed=3)
        fit_calls += 1
    else:
        prefix_pred = d0pred
    prefix_score = metrics(data, split['score'], prefix_pred[split['score']])
    d0 = historical['d0_score_mae_R']
    result = {'protocol': 'fixed-prefix-stage-replay-v1', 'block_id': block['block_id'],
              'status': 'completed', 'epochs': 4000, 'fit_seed': 3, 'api_calls': 0,
              'frozen_prefix': deepcopy(block['fixed_prefix']),
              'prefix_score': prefix_score, 'historical_prefix_mae_R': rd['before_mae_R'],
              'prefix_replay_delta_R': prefix_score['mae_R'] - rd['before_mae_R'],
              'test_is_development_diagnostic': True, 'stages': {}}
    cache = {}
    for stage in ('blind_drafts', 'reviewed_candidates', 'final_candidates'):
        best, winner = prefix_score['mae_R'], None
        rows = []
        for c in rd[stage]:
            check = precheck(c, env, split['train'], data['entropy'], reference)
            row = {'slot_id': c['slot_id'], 'formula': c['formula'], 'precheck': check}
            if check['status'] != 'passed':
                row.update(status='rejected', reason=check['reason'])
            else:
                try:
                    if c['formula'] not in cache:
                        values = checked_values(c['formula'], env)
                        pred, seconds = fit_function(data, np.column_stack([reference, values]),
                                                     split['train'], epochs=4000, seed=3)
                        fit_calls += 1
                        cache[c['formula']] = {'score': metrics(data, split['score'], pred[split['score']]),
                                               'seconds': seconds}
                        reused = False
                    else:
                        reused = True
                    saved = cache[c['formula']]
                    row.update(status='scored', score=deepcopy(saved['score']),
                               fit_seconds=saved['seconds'], exact_formula_fit_reused=reused)
                    if saved['score']['mae_R'] < best - 1e-10:
                        best, winner = saved['score']['mae_R'], c['slot_id']
                except (ValueError, RuntimeError, FloatingPointError) as error:
                    row.update(status='fit_failure', reason=str(error))
                    result['status'] = 'incomplete'
            rows.append(row)
        result['stages'][stage] = {'candidates': rows, 'best_including_prefix_mae_R': best,
                                  'retained_slot': winner,
                                  'gain_pp_of_D0': 100 * (prefix_score['mae_R'] - best) / d0}
    gains = {s: row['gain_pp_of_D0'] for s, row in result['stages'].items()}
    result.update(fit_calls=fit_calls, historical_final_mae_R=rd['after_mae_R'],
                  final_replay_delta_R=result['stages']['final_candidates']['best_including_prefix_mae_R'] - rd['after_mae_R'],
                  review_minus_blind_pp=gains['reviewed_candidates'] - gains['blind_drafts'],
                  final_minus_blind_pp=gains['final_candidates'] - gains['blind_drafts'])
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('data', 'baseline', 'source', 'blocks', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--block-index', type=int, required=True, choices=range(54))
    a = p.parse_args()
    if a.output.exists():
        raise ValueError('Use a new output file')
    manifest = read(a.blocks)
    if manifest['protocol'] != 'fixed-review-blocks-v1' or len(manifest['blocks']) != 54:
        raise ValueError('Require the complete fixed manifest')
    block = manifest['blocks'][a.block_index]
    historical = read(a.source / block['source_identity'])
    data = load_data(a.data)
    split = {k: np.asarray(v, dtype=int) for k, v in read(a.baseline / 'split.json').items()}
    if any(not np.array_equal(v, make_split(data)[k]) for k, v in split.items()):
        raise ValueError('Original split required')
    baseline = read(a.baseline / 'baseline.json')
    if baseline['epochs'] != 4000 or baseline['status'] != 'completed' or not read(a.baseline / 'reproduction.json')['passed']:
        raise ValueError('Completed original reproduction required')
    pred = np.load(a.baseline / 'native14_ann.npy', allow_pickle=False)
    d0 = metrics(data, split['score'], pred[split['score']])['mae_R']
    if abs(d0 - historical['d0_score_mae_R']) > 1e-9:
        raise ValueError('Baseline prediction mismatch')
    save_json(a.output, replay_block(data, split, block, historical, pred))
