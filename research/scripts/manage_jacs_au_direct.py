"""Prepare the fixed V5 plan, compute D0, enforce prerequisites, summarize all 30 traces.

No step selects a seed, formula, method or outcome to produce a desired ranking.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'scripts')]
from catalysis_research.experiments.jacs_au import fit, load_data, make_split, metrics, save_json
from catalysis_research.experiments.jacs_au_direct import MODES, PROFILE, REVISION, load_config, frozen_knowledge
from catalysis_research.experiments.jacs_au_kg_v4 import build_bank


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require_new(path):
    path = Path(path)
    if path.exists(): raise ValueError('New output required; preserve earlier records')
    return path


def prepare(config, bank, output):
    output = require_new(output)
    knowledge = frozen_knowledge(build_bank(bank), config)
    tasks = [{'index': i, 'mode': mode, 'replicate': replicate}
             for i, (mode, replicate) in enumerate((m,r) for m in MODES for r in range(1,11))]
    output.mkdir(parents=True)
    save_json(output/'config.json', config)
    save_json(output/'knowledge.json', knowledge)
    save_json(output/'tasks.json', {'profile': PROFILE, 'execution_revision': REVISION,
        'status': 'prepared_not_launched', 'tasks': tasks, 'generation_trajectories': 30,
        'descriptor_slots': 90, 'final_combination_fits_maximum': 150,
        'd0_fits': 5, 'fit_seeds': config['evaluation']['fit_seeds'],
        'source_policy': knowledge['policy'], 'outcome_selection': False,
        'resume_policy': 'Never regenerate completed proposals; interrupted records require explicit event-preserving recovery, not a new replicate',
        'uncertainty': {'unit': 'generation trajectory; five fitting seeds averaged within each trajectory',
            'bootstrap_resamples': 20000, 'bootstrap_seed': 20261004,
            'comparisons': ['small_kg_rag_agent-rag_agent', 'rag_agent-agent'],
            'intervals': '95% per-method descriptive; 97.5% per contrast for two prespecified comparisons',
            'scope': 'Conditional on this reused dataset/split and stochastic generation; not independent external validation'},
        'engineering_gate_is_not_a_method_ranking_test': True})
    return tasks


def baseline(data, split, config, output, fit_function=fit):
    output = require_new(output); output.mkdir(parents=True)
    result = {'profile': PROFILE, 'execution_revision': REVISION, 'config': deepcopy(config), 'status': 'running', 'fit_seeds': config['evaluation']['fit_seeds'],
              'epochs': 4000, 'input_count': 14, 'split': {k:v.tolist() for k,v in split.items()}, 'seeds': []}
    for seed in result['fit_seeds']:
        try:
            prediction, seconds = fit_function(data, data['x'], split['train'], epochs=4000, seed=seed)
            if prediction.shape != (len(data['x']),) or not np.isfinite(prediction).all():
                raise ValueError('Invalid D0 predictions')
            np.save(output/f'd0-seed-{seed}.npy', prediction, allow_pickle=False)
            result['seeds'].append({'seed': seed, 'status': 'completed', 'seconds': seconds,
                'score': metrics(data, split['score'], prediction[split['score']]),
                'outer': metrics(data, split['test'], prediction[split['test']])})
        except (ValueError, RuntimeError, FloatingPointError) as error:
            result['seeds'].append({'seed': seed, 'status': 'failed', 'reason': str(error)})
        save_json(output/'baseline.json', result)
    result['status'] = 'completed' if all(s['status']=='completed' for s in result['seeds']) else 'incomplete'
    save_json(output/'baseline.json', result)
    return result


def prerequisite_gate(replay, sign_results, config):
    """Engineering checks on every predeclared result; no gain/ranking thresholds."""
    checks = {
        'faithful_54_blocks': replay.get('status')=='completed' and replay.get('blocks')==54 and replay.get('candidate_slots')==162,
        'prefix_reproduction': abs(replay.get('max_abs_prefix_replay_delta_R', float('inf'))) <= 1e-6,
        'final_reproduction': abs(replay.get('max_abs_final_replay_delta_R', float('inf'))) <= 1e-6,
        'all_five_sign_seeds': sorted(r.get('fit_seed',-1) for r in sign_results)==config['evaluation']['fit_seeds'],
        'sign_results_complete': len(sign_results)==5 and all(r.get('status')=='completed' for r in sign_results),
    }
    for r in sign_results:
        seed = r.get('fit_seed', 'unknown'); init = r.get('paired_initialization', {})
        checks[f'seed_{seed}_paired_initial_function'] = abs(init.get('initial_prediction_max_abs_difference', float('inf'))) <= 1e-6
        checks[f'seed_{seed}_paired_initial_l1'] = abs(init.get('initial_fc1_l1_difference', float('inf'))) <= 1e-6
        checks[f'seed_{seed}_paired_final_predictions'] = abs(r.get('paired_final_prediction_max_abs_difference', float('inf'))) <= 1e-6
        checks[f'seed_{seed}_all_arms_scored'] = all(r.get('arms',{}).get(k,{}).get('status')=='scored'
            for k in ('positive','paired_negative','original_unpaired_negative'))
    return {'profile': PROFILE, 'execution_revision': REVISION, 'config': deepcopy(config),
        'gate_protocol': 'faithful-replay-and-paired-sign-v1',
        'status': 'passed' if all(checks.values()) else 'blocked', 'checks': checks,
        'uses_method_ranking_or_gain': False, 'historical_formula_scores_unchanged': True,
        'scope': 'One fixed sign pair across five seeds, not every possible nonlinear representation',
        'sign_result_diagnostics': deepcopy(sign_results)}


def validate_gate(gate, config):
    if (gate.get('status') != 'passed' or gate.get('profile') != PROFILE or
        gate.get('execution_revision') != REVISION or gate.get('config') != config or
        gate.get('gate_protocol') != 'faithful-replay-and-paired-sign-v1' or
        gate.get('uses_method_ranking_or_gain') is not False):
        raise ValueError('Full engineering gate matching the frozen configuration required')
    rebuilt = prerequisite_gate(gate.get('replay_summary', {}), gate.get('sign_result_diagnostics', []), config)
    if rebuilt['status'] != 'passed' or rebuilt['checks'] != gate.get('checks'):
        raise ValueError('Gate checks do not match completed prerequisite records')


def summarize(plan, generations, evaluations):
    """All thirty are required. Missing records stay missing, never imputed."""
    expected = {(t['mode'],t['replicate']) for t in plan['tasks']}
    if expected != {(m,r) for m in MODES for r in range(1,11)}:
        raise ValueError('Full frozen 30-task plan required')
    def keyed(records):
        mapped = {(r['mode'],r['replicate']): r for r in records}
        if len(mapped) != len(records) or set(mapped) != expected:
            raise ValueError('Exactly one record for each of all thirty traces required')
        return mapped
    gs, es = keyed(generations), keyed(evaluations)
    config = next(iter(gs.values()))['config']; seeds = config['evaluation']['fit_seeds']
    values = {}; groups = {}; rng = np.random.default_rng(20261004)
    for mode in MODES:
        traces = []
        for rep in range(1,11):
            g,e = gs[mode,rep],es[mode,rep]
            if g['status']!='frozen' or g['config']!=config or e['status']!='completed' or e['evaluation']!=config['evaluation']:
                raise ValueError('Every trace must be frozen and scored under the same configuration')
            if [s['seed'] for s in e['seeds']] != seeds or len(g['rounds'])!=3:
                raise ValueError('No seed or round removal')
            mean = float(np.mean([s['gain_pct'] for s in e['seeds']]))
            if abs(mean-e['mean_gain_pct']) > 1e-10: raise ValueError('Mean is not the all-seed mean')
            traces.append({'replicate':rep,'mean_gain_pct':mean, 'input_count':e['input_count'],
                'successful_additions':e['successful_additions'], 'fallbacks':e['fallbacks'],
                'formulas':[c['formula'] for c in g['appended']],
                'scientific_flags':[r.get('final_check',{}).get('scientific_consistency') for r in g['rounds']],
                'review_issues':sum(len(r.get('review_issues',[])) for r in g['rounds']),
                'api_calls':g['api_calls'], 'usage_totals':g['usage_totals'],
                'usage_unavailable_attempts':g['usage_unavailable_attempts'],
                'seeds':deepcopy(e['seeds'])})
        a = np.array([t['mean_gain_pct'] for t in traces]); values[mode] = a
        bootstrap = np.mean(a[rng.integers(0,10,size=(20000,10))],axis=1)
        signatures = Counter(tuple(t['formulas']) for t in traces)
        groups[mode] = {'n_generation_traces':10,'mean_gain_pct':float(a.mean()),
            'sample_sd_pp':float(a.std(ddof=1)), 'descriptive_95pct_bootstrap_interval_pp':np.quantile(bootstrap,[.025,.975]).tolist(),
            'fallback_seed_fits':sum(t['fallbacks'] for t in traces),
            'successful_additions_distribution':dict(Counter(t['successful_additions'] for t in traces)),
            'distinct_ordered_formula_sequences':len(signatures),
            'duplicate_sequences': [{'formulas':list(k),'count':v} for k,v in signatures.items() if v>1],
            'api_calls':sum(t['api_calls'] for t in traces),
            'usage_unavailable_attempts':sum(t['usage_unavailable_attempts'] for t in traces), 'traces':traces}
    contrasts = {}
    for left,right in [('small_kg_rag_agent','rag_agent'),('rag_agent','agent')]:
        # Replicate numbering does not establish matched stochastic generation.
        boot = values[left][rng.integers(0,10,size=(20000,10))].mean(axis=1)-values[right][rng.integers(0,10,size=(20000,10))].mean(axis=1)
        contrasts[left+'-'+right] = {'mean_difference_pp':float(values[left].mean()-values[right].mean()),
            'descriptive_97_5pct_bootstrap_interval_pp':np.quantile(boot,[.0125,.9875]).tolist(),
            'sampling':'Independent resampling of generation traces; seed fits are not independent discovery units'}
    return {'profile':PROFILE,'execution_revision':REVISION,'status':'completed','groups':groups,'contrasts':contrasts,
        'primary_includes_all_30_and_all_predeclared_seeds':True,
        'limitations':['Bootstrap is conditional on reused data/split and assumes exchangeable stochastic traces.',
            'Ten trajectories do not guarantee separation or independent validation.',
            'Formula equality alone neither proves nor rules out API response caching.',
            'Fallbacks are explicit D0 predictions; incomplete baseline or trace records block this summary.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase', choices=['prepare','baseline','gate','summarize'])
    p.add_argument('--output', type=Path, required=True)
    for key in ('config','bank','data','baseline','replay_summary','sign_results','plan','generations','evaluations'):
        p.add_argument('--'+key.replace('_','-'), type=Path)
    a = p.parse_args()
    config = load_config(a.config) if a.config else None
    if a.phase=='prepare': prepare(config,read(a.bank),a.output)
    elif a.phase=='baseline':
        data = load_data(a.data)
        split = {k:np.array(v,dtype=int) for k,v in read(a.baseline/'split.json').items()}
        if set(split)!=set(make_split(data)) or any(not np.array_equal(v,make_split(data)[k]) for k,v in split.items()):
            raise ValueError('Original split required')
        baseline(data,split,config,a.output)
    elif a.phase=='gate':
        require_new(a.output); replay = read(a.replay_summary)
        signs = [read(f) for f in sorted(a.sign_results.glob('seed-index-*.json'))]
        g = prerequisite_gate(replay, signs, config); g['replay_summary'] = replay
        save_json(a.output,g)
        if g['status']!='passed': raise SystemExit('Prerequisites incomplete; generation remains blocked')
    else:
        require_new(a.output)
        result = summarize(read(a.plan), [read(f) for f in a.generations.glob('*.json')], [read(f) for f in a.evaluations.glob('*.json')])
        save_json(a.output,result)
