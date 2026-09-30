"""Read every complete V4 trajectory; export stage changes and fixed review blocks.

No API, fitting, source-result writes, outcome filtering, or hash scans. The fixed
blocks use one deterministic frozen-bank retrieval per blind batch for all arms.
They measure local review effects conditional on the historical retained prefix,
not counterfactual adaptive discovery trajectories.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import csv
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'scripts')]
from catalysis_research.experiments.jacs_au_kg_v4 import (
    audit_bank, build_bank, graph_paths_for, ground_symbols, pack_evidence,
    scientific_graph, select_evidence,
)

MODES = ('agent', 'rag_agent', 'small_kg_rag_agent')
ARMS = ('self', 'source', 'flat_graph', 'graph')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False) + '\n', encoding='utf-8')


def changed_fields(a, b, prefix=''):
    result = []
    for key in sorted(set(a) | set(b)):
        x, y = a.get(key), b.get(key)
        if isinstance(x, dict) and isinstance(y, dict):
            result.extend(changed_fields(x, y, prefix + key + '.'))
        elif x != y:
            result.append(prefix + key)
    return result


def linked_graph(drafts, graph, evidence):
    """Fix only reference serialization for the NEW ablation, not V4 records.

    V4 conditions_ref addressed an ID as an array property; resolve the existing
    packed registry directly. Advertised check names are not execution results.
    Actual per-candidate reports remain training_only_prechecks in every arm.
    """
    paths = graph_paths_for(drafts, graph)
    refs = {c['mechanism_id']: c['applicability_ref']
            for c in evidence['mechanism_cards']}
    for key, node in paths['nodes'].items():
        if node['type'] == 'conditional_mechanism':
            node['conditions_ref'] = 'evidence.source_conditions.' + refs[key]
    paths.pop('executed_checks')
    return paths


def flat_graph(paths):
    """Lossless fact tuples, without node/edge adjacency containers."""
    return {'node_facts': [{'node_id': key, 'property': prop, 'value': deepcopy(value)}
                           for key, node in paths['nodes'].items()
                           for prop, value in node.items()],
            'relation_facts': deepcopy(paths['edges']), 'note': paths['note']}


def review_request(block, arm):
    if arm not in ARMS:
        raise ValueError('Unknown review arm')
    req = deepcopy(block['review_common'])
    req['review_mode'] = {'self': 'self_review', 'source': 'source_conditions_review',
                          'flat_graph': 'source_and_flat_relations_review',
                          'graph': 'source_and_graph_paths_review'}[arm]
    req['evidence'] = (deepcopy(block['evidence']) if arm != 'self'
                       else {'items': [], 'mechanism_cards': [], 'source_conditions': {}})
    if arm == 'graph':
        req['graph_tool_result'] = deepcopy(block['graph_paths'])
    if arm == 'flat_graph':
        req['flat_relation_result'] = flat_graph(block['graph_paths'])
    return req


def diagnose(source, bank_path, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError('Use a fresh diagnosis output directory')
    bank = read(bank_path)
    if bank['profile'] == 'jacs-au-kg-v3':
        bank = build_bank(bank)
    audit_bank(bank)
    graph = scientific_graph(bank)
    loaded = []
    expected = {f'{e}/discovery/{m}-replicate-{n}.json'
                for e in ('low', 'high') for m in MODES for n in (1, 2, 3)}
    actual = {p.relative_to(source).as_posix() for p in source.glob('*/discovery/*.json')}
    if actual != expected:
        raise ValueError('Require all fixed 18 trajectory identities, no extras')
    rows, blocks, rounds, detail = [], [], [], []
    groups = defaultdict(list)
    for identity in sorted(expected):
        d = read(source / identity)
        e, _, file = identity.split('/')
        if (d['status'] != 'completed' or d['reasoning_effort'] != e or
                d['execution_revision'] != 'explicit-normalization-20260930c' or
                d['model'] != 'glm-5.3-flash' or d['fit_seed'] != 3 or d['epochs'] != 4000 or
                len(d['rounds']) != 3 or file != f"{d['mode']}-replicate-{d['replicate']}.json"):
            raise ValueError('Trajectory contract mismatch: ' + identity)
        loaded.append(d)
        prefix, seen_scored = [], []
        for rd in d['rounds']:
            maps = [{c['slot_id']: c for c in rd[key]} for key in
                    ('blind_drafts', 'reviewed_candidates', 'final_candidates', 'candidates')]
            if any(set(m) != {'h1', 'h2', 'h3'} for m in maps):
                raise ValueError('Wrong fixed slots')
            checks = [{c['slot_id']: ch for c, ch in zip(rd[key], rd[check])} for key, check in
                      [('blind_drafts', 'blind_checks'), ('reviewed_candidates', 'reviewed_checks')]]
            # Read, never rewrite the original summary or retained decisions.
            best = min([rd['before_mae_R']] +
                       [c['score']['mae_R'] for c in rd['candidates'] if c['status'] == 'scored'])
            if abs(best - rd['after_mae_R']) > 1e-9:
                raise ValueError('Stored best-of-round mismatch')
            bid = f"{e}/{d['mode']}/replicate-{d['replicate']}/round-{rd['round']}"
            event = next(ev for ev in rd['generation_events'] if ev['stage'] == 'review')
            review_common = deepcopy(event['request'])
            for key in ('review_mode', 'evidence', 'graph_tool_result'):
                review_common.pop(key, None)
            evidence, trace = select_evidence(bank, rd['blind_drafts'],
                                             d['rounds'][:rd['round'] - 1], d['config'])
            packed = pack_evidence(evidence)
            blocks.append({'block_id': bid, 'source_identity': identity,
                           'origin_effort': e, 'origin_mode': d['mode'],
                           'replicate': d['replicate'], 'round': rd['round'],
                           'fixed_prefix': deepcopy(prefix),
                           'review_common': review_common, 'evidence': packed,
                           'graph_paths': linked_graph(rd['blind_drafts'], graph, packed),
                           'evidence_policy': 'One frozen-bank retrieval shared by all evidence arms; not historical live-index replay',
                           'retrieval': trace})
            for sid in ('h1', 'h2', 'h3'):
                a, b, f, c = [m[sid] for m in maps]
                ac, bc = [m[sid] for m in checks]
                for version in (b, f):
                    if (a['hypothesis'] != version['hypothesis'] or
                        any(a['scientific_test'][k] != version['scientific_test'][k]
                            for k in ('mechanism_family', 'entropy_direction'))):
                        raise ValueError('Stored locked content changed')
                symbols = [sorted(ground_symbols(v['formula'])) for v in (a, b, f)]
                row = {'candidate_id': bid + '/' + sid, 'source_identity': identity,
                       'effort': e, 'mode': d['mode'], 'replicate': d['replicate'],
                       'round': rd['round'], 'slot_id': sid,
                       'mechanism_family': a['scientific_test']['mechanism_family'],
                       'blind_formula': a['formula'], 'review_formula': b['formula'],
                       'final_formula': f['formula'], 'blind_status': ac['status'],
                       'review_status': bc['status'], 'final_status': c['status'],
                       'blind_reason': ac.get('reason'), 'review_reason': bc.get('reason'),
                       'final_reason': c.get('reason'),
                       'review_formula_changed': a['formula'] != b['formula'],
                       'repair_formula_changed': b['formula'] != f['formula'],
                       'review_support_changed': symbols[0] != symbols[1],
                       'blind_variables': symbols[0], 'review_variables': symbols[1],
                       'final_variables': symbols[2],
                       'review_changes': changed_fields(a, b), 'repair_changes': changed_fields(b, f),
                       'retained': c['retained'], 'final_score_mae_R': c.get('score', {}).get('mae_R'),
                       'marginal_gain_pp_of_D0': 100 * c['marginal_improvement'] / d['d0_score_mae_R']
                           if c['status'] == 'scored' else None,
                       'review_exact_reuse_from_prior_scored_slots': [x['id'] for x in seen_scored
                           if b['formula'] == x['formula']],
                       'evidence_ids': c.get('evidence_ids', [])}
                rows.append(row)
                groups[(e, d['mode'])].append(row)
                detail.append({**row, 'blind': a, 'reviewed': b, 'final': f,
                               'blind_check': ac, 'review_check': bc, 'final_check': c['precheck'],
                               'frozen_prefix': deepcopy(prefix),
                               'historical_evidence': d['evidence_by_round'][rd['round'] - 1],
                               'counterfactual_blind_ann_score': None})
            rounds.append({'block_id': bid, 'source_identity': identity,
                           'before_mae_R': rd['before_mae_R'], 'after_mae_R': rd['after_mae_R'],
                           'gain_pp_of_D0': 100 * (rd['before_mae_R'] - rd['after_mae_R']) / d['d0_score_mae_R'],
                           'retained_formula': rd['retained_formula'],
                           'events': [{'stage': ev['stage'], 'replayed': ev.get('replayed_from_checkpoint', False),
                                       'attempts': len(ev['attempts']),
                                       'errors': [a.get('validation_error') for a in ev['attempts'] if a.get('validation_error')]}
                                      for ev in rd['generation_events']]})
            seen_scored.extend({'id': bid + '/' + c['slot_id'], 'formula': c['formula']}
                               for c in rd['candidates'] if c['status'] == 'scored')
            prefix.extend(deepcopy(c) for c in rd['final_candidates']
                          if c['slot_id'] in {x['slot_id'] for x in rd['candidates'] if x['retained']})
    summary = {}
    for (effort, mode), cs in groups.items():
        trajectories = [d for d in loaded if (d['reasoning_effort'], d['mode']) == (effort, mode)]
        events = [ev for d in trajectories for rd in d['rounds'] for ev in rd['generation_events']]
        pos = [c['marginal_gain_pp_of_D0'] for c in cs
               if c['marginal_gain_pp_of_D0'] is not None and c['marginal_gain_pp_of_D0'] > 1e-8]
        summary[effort + '/' + mode] = {
            'score_gain_pct_by_replicate': [d['score_improvement_pct'] for d in trajectories],
            'score_gain_pct_mean': statistics.mean(d['score_improvement_pct'] for d in trajectories),
            'blind_passed': sum(c['blind_status'] == 'passed' for c in cs),
            'review_passed': sum(c['review_status'] == 'passed' for c in cs),
            'scored': sum(c['final_status'] == 'scored' for c in cs),
            'review_formula_changed': sum(c['review_formula_changed'] for c in cs),
            'passed_draft_formula_changed': sum(c['review_formula_changed'] and c['blind_status'] == 'passed' for c in cs),
            'review_support_changed': sum(c['review_support_changed'] for c in cs),
            'transition_counts': dict(Counter(c['blind_status'] + '->' + c['review_status'] for c in cs)),
            'positive_marginal_slots': len(pos),
            'positive_marginal_pp_mean': statistics.mean(pos),
            'retained': sum(c['retained'] for c in cs),
            'rotation_retained': sum(c['retained'] and c['mechanism_family'] == 'rotation' for c in cs),
            'repair_batches': sum(ev['stage'] == 'pre_fit_repair' for ev in events),
            'finish_reasons': dict(Counter(a.get('finish_reason') for ev in events for a in ev['attempts'])),
            'reported_reasoning_tokens_by_stage': {stage: sum(a.get('usage', {}).get('completion_tokens_details', {}).get('reasoning_tokens', 0)
                for ev in events if ev['stage'] == stage for a in ev['attempts'])
                for stage in ('blind_proposal', 'review', 'pre_fit_repair')},
            'blind_rejection_reasons': dict(Counter(c['blind_reason'] for c in cs if c['blind_status'] == 'rejected')),
        }
    evidence_rows = [r for d in loaded if d['mode'] != 'agent' for r in d['evidence_by_round']]
    first_six_equal = all(r['items'][:6] == evidence_rows[0]['items'][:6] for r in evidence_rows)
    cards_equal = all(r['mechanism_cards'] == evidence_rows[0]['mechanism_cards'] for r in evidence_rows)
    metadata = {'source_root': source.as_posix(), 'trajectories': 18, 'round_blocks': len(blocks),
                'candidate_slots': len(rows), 'groups': summary,
                'first_round_blind_requests_identical_within_effort': {
                    e: all(d['rounds'][0]['generation_events'][0]['request'] == next(x for x in loaded if x['reasoning_effort'] == e)['rounds'][0]['generation_events'][0]['request']
                           for d in loaded if d['reasoning_effort'] == e) for e in ('low', 'high')},
                'historical_evidence': {'knowledge_rounds': len(evidence_rows),
                    'first_six_items_identical': first_six_equal, 'mechanism_cards_identical': cards_equal,
                    'unique_record_sets': len({tuple(sorted(x['record_id'] for x in r['items'])) for r in evidence_rows}),
                    'source_papers': sorted({x['paper_id'] for r in evidence_rows for x in r['items']})},
                'api_calls_made': 0, 'fits_made': 0,
                'limits': ['Only final candidates were ANN-scored historically; no observed blind-to-final ANN delta.',
                           'Association reports use training labels; they are not source facts or causal checks.',
                           'Formula string/support changes flag review targets, not automatic mechanism violations.',
                           'Recovered event usage excludes old unavailable failed responses; seconds are not comparable.',
                           'Fixed blocks use frozen-bank evidence, corrected graph references, and historical prefixes; no adaptive rollout claim.']}
    output.mkdir(parents=True)
    write(output / 'audit-summary.json', metadata)
    write(output / 'candidate-audit.json', detail)
    write(output / 'round-audit.json', rounds)
    write(output / 'fixed-review-blocks.json', {'protocol': 'fixed-review-blocks-v1', 'status': 'prepared_not_run',
        'arms': ARMS, 'review_efforts': ['low', 'high'], 'review_replicates': [1, 2, 3],
        'blocks': blocks, 'limitations': metadata['limits']})
    fields = list(rows[0])
    with (output / 'candidate-audit.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                             for k, v in row.items()})
    md = ['# V4 全部 162 槽的初稿、复核与最终评分', '',
          '只引用原始最终评分；初稿/复核稿未训练，不能将最终增益解释为复核因果收益。边际增益单位为相对 D0 的百分点。', '']
    for rd in rounds:
        md += ['## ' + rd['block_id'], '',
               f"该轮最佳保留增益：{rd['gain_pp_of_D0']:.4f} pp；保留 `{rd['retained_formula']}`。", '']
        for c in [r for r in rows if r['candidate_id'].rsplit('/', 1)[0] == rd['block_id']]:
            gain = f"{c['marginal_gain_pp_of_D0']:+.4f}" if c['marginal_gain_pp_of_D0'] is not None else '未评分'
            md += [f"### {c['slot_id']} ({c['mechanism_family']})", '',
                   f"- 初稿 `{c['blind_formula']}`：{c['blind_status']}；{c['blind_reason'] or ''}",
                   f"- 复核 `{c['review_formula']}`：{c['review_status']}；{c['review_reason'] or ''}",
                   f"- 最终 `{c['final_formula']}`：{c['final_status']}；边际 {gain} pp；保留={c['retained']}",
                   f"- 复核字段变化：{', '.join(c['review_changes']) or '无'}", '']
    (output / 'ALL_TRAJECTORIES.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return metadata


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--bank', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = diagnose(a.source, a.bank, a.output)
    print(json.dumps({k: r[k] for k in ('trajectories', 'round_blocks', 'candidate_slots', 'api_calls_made', 'fits_made')}))
