"""Exploratory first-round single-descriptor audit, without selecting by MAE.

All nine high first-round final formulas per arm are included. This is neither
a three-round direct-addition replay nor a new single-output generation trial.
"""
import argparse
import json
from pathlib import Path
import statistics


def audit(source, output):
    if output.exists():
        raise ValueError('Use a fresh audit output')
    groups = {}
    for mode in ('agent', 'rag_agent', 'small_kg_rag_agent'):
        rows = []
        for rep in (1, 2, 3):
            identity = f'high/discovery/{mode}-replicate-{rep}.json'
            d = json.loads((source / identity).read_text(encoding='utf-8'))
            if (d['status'] != 'completed' or d['reasoning_effort'] != 'high' or
                    d['fit_seed'] != 3 or d['epochs'] != 4000):
                raise ValueError('Wrong historical execution contract')
            rd = d['rounds'][0]
            if abs(rd['before_mae_R'] - d['d0_score_mae_R']) > 1e-12:
                raise ValueError('First round must start from D0')
            if {c['slot_id'] for c in rd['candidates']} != {'h1', 'h2', 'h3'}:
                raise ValueError('All three fixed slots required')
            for c in rd['candidates']:
                if c['status'] != 'scored':
                    raise ValueError('This audit requires all first-round slots; do not filter failures')
                rows.append({'source_identity': identity, 'replicate': rep,
                             'round': 1, 'slot_id': c['slot_id'], 'formula': c['formula'],
                             'd0_score_mae_R': d['d0_score_mae_R'],
                             'score_mae_R': c['score']['mae_R'],
                             'gain_pct': 100 * (d['d0_score_mae_R'] - c['score']['mae_R']) / d['d0_score_mae_R']})
        groups[mode] = {'n_slots': len(rows), 'n_generation_batches': 3,
                        'mean_gain_pct_all_slots': statistics.mean(r['gain_pct'] for r in rows),
                        'mean_score_mae_R_all_slots': statistics.mean(r['score_mae_R'] for r in rows),
                        'positive_slots': sum(r['gain_pct'] > 0 for r in rows),
                        'slot_position_means': {slot: statistics.mean(r['gain_pct'] for r in rows if r['slot_id'] == slot)
                                                for slot in ('h1', 'h2', 'h3')},
                        'rows': rows}
    result = {'profile': 'high-first-round-all-slots-no-selection-diagnostic',
              'status': 'completed_from_existing_scores', 'api_calls': 0, 'fits': 0,
              'metric': 'Scoring MAE reduction relative to common D0; negative values included',
              'selection': 'None: equal weight over all three slots and all three generation batches',
              'groups': groups,
              'ranking': sorted(groups, key=lambda m: -groups[m]['mean_gain_pct_all_slots']),
              'limitations': ['Exploratory analysis specified after historical results were viewed.',
                              'Nine slots are nested in three generation batches, not nine full independent trajectories.',
                              'Every historical batch generated three diverse formulas; this is not direct one-formula generation.',
                              'Historical review used training-label association reports.',
                              'Rounds two and three depend on selected historical prefixes and cannot reconstruct a direct-addition final result.',
                              'Do not choose a slot position by its favorable retrospective ranking.']}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = audit(a.source, a.output)
    print(json.dumps({m: g['mean_gain_pct_all_slots'] for m, g in r['groups'].items()}))
