"""Audited, anchor-preserving scientific evidence and executable hypotheses.

V3 is an explicit new protocol. Historical V2 trajectories are not rewritten.
No performance or causality claim follows from these engineering gates.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import html
import json
from pathlib import Path
import re

import numpy as np
from scipy.stats import spearmanr

from .jacs_au import FEATURES
from .jacs_au_sources import assert_clean, contamination_reason, BENCHMARK_IDS, BENCHMARK_DOCUMENTS
from .jacs_au_knowledge import relevance, scope_tags
from .jacs_au_knowledge import adaptive_query as base_adaptive_query
from ..retrieval.bundle import count_tokens

PROFILE = 'jacs-au-kg-v3'


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def token_count(value):
    return count_tokens(encode(value))


def load_budget_config(path):
    if path is None: raise ValueError('V3 requires an explicit configuration')
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('profile') != PROFILE: raise ValueError('V3 configuration required')
    for group in ('retrieval', 'generation'):
        for key, val in config[group].items():
            if type(val) is not int or val <= 0: raise ValueError('Invalid budget: ' + key)
    if config['generation']['max_tokens_on_truncation'] < config['generation']['max_tokens']:
        raise ValueError('Recovery cap must be at least the initial output cap')
    return {k: config[k] for k in ('retrieval', 'generation')}


def complete_quote(text):
    # Preserve every paragraph, including qualifications without entropy keywords.
    text = re.sub(r'<[^>]+>', ' ', html.unescape(str(text)))
    return re.sub(r'\s+', ' ', text).strip()


def pack_graph(items):
    packed = {'items': [], 'nodes': {}, 'edges': {}, 'supports': {}}
    indexes = {kind: {} for kind in ('nodes', 'edges', 'supports')}
    def intern(kind, value):
        encoded = encode(value)
        if encoded not in indexes[kind]:
            ref = kind[0] + str(len(indexes[kind]) + 1)
            indexes[kind][encoded] = ref
            packed[kind][ref] = deepcopy(value)
        return indexes[kind][encoded]
    for original in items:
        item = {k: deepcopy(v) for k, v in original.items() if k != 'graph_paths'}
        if 'graph_paths' in original: item['graph_paths'] = []
        packed['items'].append(item)
        for original_path in original.get('graph_paths', []):
            path = {k: deepcopy(v) for k, v in original_path.items() if k not in {'nodes','edges'}}
            item['graph_paths'].append(path)
            path['nodes'] = [intern('nodes', node) for node in original_path['nodes']]
            refs = []
            for original_edge in original_path['edges']:
                edge = deepcopy(original_edge)
                edge['support'] = [intern('supports', s) for s in edge['support']]
                refs.append(intern('edges', edge))
            path['edges'] = refs
    if unpack_graph(packed) != items: raise ValueError('Lossy graph serialization')
    return packed


def unpack_graph(packed):
    items = deepcopy(packed['items'])
    for item in items:
        for path in item.get('graph_paths', []):
            path['nodes'] = [deepcopy(packed['nodes'][ref]) for ref in path['nodes']]
            path['edges'] = [deepcopy(packed['edges'][ref]) for ref in path['edges']]
            for edge in path['edges']:
                edge['support'] = [deepcopy(packed['supports'][ref]) for ref in edge['support']]
    return items


def render_evidence(items, view='paths'):
    if view not in {'paths', 'text'}: raise ValueError('Unknown evidence view')
    packed = pack_graph(items)
    if view == 'paths': return packed
    # Same complete facts and provenance. Only path grouping is flattened.
    # Retain node/edge memberships as flat ID lists so the control is lossless.
    for item in packed['items']:
        if 'graph_paths' in item:
            item['flat_fact_groups'] = item.pop('graph_paths')
    packed['nodes'] = [dict(fact_id=k, fact=v) for k, v in packed['nodes'].items()]
    packed['edges'] = [dict(fact_id=k, fact=v) for k, v in packed['edges'].items()]
    packed['supports'] = [dict(fact_id=k, fact=v) for k, v in packed['supports'].items()]
    return packed


def build_bank(old, reviews, budget):
    """Re-audit complete source passages. No old selection/score influences this."""
    review_map = {(r['paper_id'], r['source_quote']): r for r in reviews['rows']}
    reviewed_records = {r['source_record_id']: r for r in reviews['rows'] if r.get('source_record_id')}
    rag_reviews = {r['record_id']: r for r in reviews['rag_rows']}
    excluded = set(old['source_audit'].get('excluded_paper_ids', [])) | set(BENCHMARK_IDS)
    docs = set(old['source_audit'].get('excluded_document_ids', [])) | set(BENCHMARK_DOCUMENTS)
    result = {'profile': PROFILE, 'budget_config': budget, 'rag': [], 'kg': [], 'rejected': [],
              'review_revision': '20260929-scope2',
              'source_audit': {'excluded_paper_ids': sorted(excluded), 'excluded_document_ids': sorted(docs),
                               'independent_identity_guard': True},
              'review_protocol': reviews['protocol'],
              'retrieval_policy': 'Frozen audited pool; query reranking cannot fetch new papers.'}
    blocked = reviews['out_of_scope_papers']
    for channel in ('rag', 'kg'):
        seen = set()
        source_rows = list(old[channel])
        if channel == 'kg':
            # Reconstruct reviewed mechanism associations from original text;
            # record this origin instead of pretending generic graph traversal
            # already extracted a qualified scientific relation.
            source_rows += [{**r, 'channel': 'kg'} for r in old['rag'] if r['record_id'] in reviewed_records]
        for original in source_rows:
            row = deepcopy(original)
            reason = contamination_reason(row)
            if row['paper_id'] in excluded or row['document_id'] in docs: reason = 'excluded_identity'
            if not reason and row['paper_id'] in blocked: reason = blocked[row['paper_id']]
            full_quote = complete_quote(row.get('original_quote') or row['quote'])
            if not reason and not relevance(full_quote)[0]: reason = 'missing_target_mechanism'
            review = reviewed_records.get(row['record_id']) or review_map.get((row['paper_id'], row['quote']))
            rag_review = rag_reviews.get(row['record_id'])
            if channel == 'rag' and not reason and (not rag_review or rag_review['decision'] != 'conditional_use'):
                reason = (rag_review or {}).get('reason', 'unreviewed_rag_applicability')
            if channel == 'kg' and not reason:
                if not review or review['decision'] != 'conditional_use':
                    reason = (review or {}).get('reason', 'unreviewed_graph_evidence')
            if reason:
                result['rejected'].append({'channel': channel, 'record_id': row['record_id'], 'reason': reason})
                continue
            identity = (row['paper_id'], row['document_id'], full_quote)
            if identity in seen: continue
            seen.add(identity)
            row['quote'] = full_quote
            row['quote_transform'] = 'HTML and whitespace cleanup only; all paragraphs retained'
            row['scope_tags'] = scope_tags(full_quote)
            row['graph_paths'] = []
            row['applicability'] = deepcopy(rag_review) if channel == 'rag' else {}
            row['applicability']['status'] = 'conditional_use'
            if channel == 'kg':
                if not review.get('transfer_assumptions') or not review.get('source_conditions'):
                    raise ValueError('Conditional mechanism requires conditions and explicit transfer assumptions')
                if complete_quote(review['source_quote']) not in full_quote:
                    raise ValueError('Reviewed quote does not occur in the preserved source')
                if not set(review['proxy_inputs']) <= set(FEATURES): raise ValueError('Unknown mechanism proxy input')
                # Curated scientific association, explicitly separate from original
                # generic paper paths. No generic hub or cross-paper inference.
                card_id = review['mechanism_id']
                nodes = [{'id': card_id + ':' + name, 'type': 'physical_quantity', 'label': label}
                         for name, label in [('source', review['subject']), ('target', review['object'])]]
                edge = {'id': card_id, 'source': nodes[0]['id'], 'target': nodes[1]['id'],
                        'relation': review['relation'], 'source_paper_id': row['paper_id'],
                        'review_status': 'curated_conditional_association_not_causality',
                        'source_conditions': review['source_conditions'],
                        'transfer_assumptions': review['transfer_assumptions'],
                        'support': [{'quote': review['source_quote'], 'document_id': row['document_id'],
                                     'locator': row['locator']}]}
                row['graph_paths'] = [{'nodes': nodes, 'edges': [edge],
                                      'interpretation': 'Source-qualified association; target-regime validity unproven.'}]
                row['applicability'] = {k: deepcopy(review[k]) for k in (
                    'source_conditions', 'transfer_assumptions', 'proxy_inputs', 'proxy_caveat')}
                row['applicability']['status'] = 'conditional_use'
                row['mechanism_id'] = card_id
            assert_clean(row, excluded, docs)
            result[channel].append(row)
    result['eligible_counts'] = {c: len(result[c]) for c in ('rag', 'kg')}
    result['paper_counts'] = {c: len({r['paper_id'] for r in result[c]}) for c in ('rag', 'kg')}
    result['status'] = 'ready' if result['rag'] and result['kg'] else 'insufficient_reviewed_evidence'
    return result


def audit_bank(bank):
    if bank.get('profile') != PROFILE or bank.get('status') != 'ready':
        raise ValueError('An audited ready V3 bank is required')
    if bank.get('review_revision') != '20260929-scope2':
        raise ValueError('Obsolete or missing source review revision')
    audit = bank['source_audit']
    for channel in ('rag', 'kg'):
        if not bank[channel]: raise ValueError('Empty channel: ' + channel)
        assert_clean(bank[channel], audit['excluded_paper_ids'], audit['excluded_document_ids'])
        for row in bank[channel]:
            if row['channel'] != channel: raise ValueError('Wrong evidence channel')
            scope = row.get('applicability', {})
            if scope.get('status') != 'conditional_use' or not scope.get('transfer_assumptions'):
                raise ValueError('Unreviewed source applicability')
            if row['quote'] != complete_quote(row.get('original_quote') or row['quote']):
                raise ValueError('A source qualification was removed from the passage')
            if channel == 'kg':
                if not row['graph_paths']: raise ValueError('Missing scientific relation')
                for path in row['graph_paths']:
                    ids = {n['id'] for n in path['nodes']}
                    for edge in path['edges']:
                        if edge['relation'].startswith('PAPER_') or edge['source'] not in ids or edge['target'] not in ids:
                            raise ValueError('Generic or disconnected scientific relation')
                        if not edge.get('support'): raise ValueError('Unsupported scientific relation')
                        if edge['source_paper_id'] != row['paper_id']: raise ValueError('Cross-paper mechanism join')
                        if not edge.get('source_conditions') or not edge.get('transfer_assumptions'):
                            raise ValueError('Missing edge applicability conditions')
                        for support in edge['support']:
                            if complete_quote(support['quote']) not in row['quote']:
                                raise ValueError('Relation support is not in its source passage')
                            if support['document_id'] != row['document_id']:
                                raise ValueError('Relation support document mismatch')


def adaptive_query(round_no, retained, history, requested_queries=()):
    base = base_adaptive_query(round_no, retained, [], requested_queries)
    feedback = []
    for rd in history[-1:]:
        for c in rd.get('candidates', []):
            # Whitelisted fields only; never serialize arbitrary history/test data.
            spec = c.get('scientific_test', {})
            check = c.get('scientific_check', {})
            family = spec.get('mechanism_family')
            if family not in {'translation','rotation','shape','connectivity','coupling'}: continue
            if check.get('target_association') == 'contradicted':
                feedback.append(f'{family} adsorption entropy counterexample conditions proxy limitations')
            elif c.get('retained'):
                feedback.append(f'{family} competing adsorption entropy mechanism independent evidence')
            elif c.get('status') == 'rejected':
                feedback.append(f'{family} physical variable mapping finite difference dimensional consistency')
    # Put actionable feedback first; the retained-variable text cannot truncate it.
    return ' '.join(dict.fromkeys([*feedback, base]))[:2000]


def select_evidence(bank, mode, query, *, graph_view='paths', token_budget=32000,
                    item_limit=32, candidate_limit=120, paper_limit=32, kg_priority_items=None,
                    max_kg_items=12):
    if mode == 'agent':
        return [], {'query': query, 'items': 0, 'lexical_tokens': 0, 'graph_paths': 0, 'kg_selected_items': 0}
    audit_bank(bank)
    words = set(re.findall(r'[a-z]{3,}', query.lower()))
    def rank(rows):
        # Normalize each retrieval channel separately; preserve available source
        # rank without comparing incompatible dense and graph score scales.
        source_order = {r['record_id']: i for i, r in enumerate(sorted(rows, key=lambda r: -r.get('source_score', 0)))}
        return sorted(rows, key=lambda r: (
            -(len(words & set(re.findall(r'[a-z]{3,}', r['quote'].lower())))
              + 1 / (1 + source_order[r['record_id']])), r['record_id']))[:candidate_limit]
    def item(row, index):
        return {**{k: deepcopy(row[k]) for k in ('paper_id', 'document_id', 'quote', 'locator',
                 'scope_tags', 'quote_transform', 'applicability', 'graph_paths')},
                'id': f"R{bank.get('active_round', 1)}E{index+1:02d}", 'channels': [row['channel']]}
    def cost(items):
        # Select ONCE against the larger rendering; paths/text cannot change facts.
        return max(token_count(render_evidence(items, v)) for v in ('paths', 'text'))
    anchors = []; counts = Counter(); skipped = 0
    for row in rank(bank['rag']):
        if counts[row['paper_id']] >= paper_limit: continue
        proposed = item(row, len(anchors))
        if cost([*anchors, proposed]) > token_budget: skipped += 1; continue
        anchors.append(proposed); counts[row['paper_id']] += 1
        if len(anchors) == item_limit: break
    selected = deepcopy(anchors); kg_count = 0
    if mode == 'small_kg_rag_agent':
        for row in rank(bank['kg']):
            proposed = item(row, len(selected))
            if cost([*selected, proposed]) > token_budget: skipped += 1; continue
            selected.append(proposed); kg_count += 1
            if kg_count == max_kg_items: break
    if selected[:len(anchors)] != anchors: raise ValueError('RAG anchor replaced')
    rendered = render_evidence(selected, graph_view)
    assert_clean(rendered)
    return selected, {'query': query, 'items': len(selected), 'lexical_tokens': token_count(rendered),
                     'context_token_budget': token_budget, 'kg_selected_items': kg_count,
                     'graph_paths': sum(len(x['graph_paths']) for x in selected), 'graph_view': graph_view,
                     'rag_anchor_items': len(anchors), 'rag_anchor_preserved': len(anchors),
                     'whole_items_skipped_for_budget': skipped, 'selection_independent_of_graph_view': True,
                     'knowledge_policy': 'Exact RAG anchors plus conditional mechanisms; no KG priority quota',
                     'raw_serialized_tokens': token_count(selected)}


def validate_scientific_test(candidate):
    spec = candidate.get('scientific_test')
    if not isinstance(spec, dict): raise ValueError('scientific_test is required')
    for field in ('mechanism_family', 'proxy_assumptions', 'physical_interpretation'):
        if not isinstance(spec.get(field), str) or not spec[field].strip(): raise ValueError('Missing '+field)
    if spec['mechanism_family'] not in {'translation','rotation','shape','connectivity','coupling'}:
        raise ValueError('Unknown mechanism family')
    for field in ('vary_input', 'regime_input'):
        if spec.get(field) not in FEATURES: raise ValueError('Test requires native input: '+field)
    for field in ('descriptor_direction', 'entropy_direction'):
        if spec.get(field) not in ('increasing', 'decreasing'): raise ValueError('Invalid test direction')
    interval = spec.get('regime_train_quantiles')
    if (not isinstance(interval, list) or len(interval) != 2 or
            any(type(v) not in (int, float) or not np.isfinite(v) for v in interval)
            or not 0 <= interval[0] < interval[1] <= 1 or interval[1]-interval[0] < .25):
        raise ValueError('Predeclared regime must cover at least 25% of training quantiles')
    return spec


def scientific_check(candidate, env, train, entropy, evaluate):
    """No scoring/test rows or labels used. Checks are diagnostics, not causality.

    Contradiction of the proposed formula direction rejects a candidate before
    fitting. Observed target association is reported separately (confounding is
    possible), so a training correlation is never called a verified mechanism.
    """
    spec = validate_scientific_test(candidate)
    local = {k: np.asarray(v)[train].copy() for k, v in env.items()}
    target = np.asarray(entropy)[train]
    axis = local[spec['regime_input']]
    low, high = np.quantile(axis, spec['regime_train_quantiles'])
    mask = (axis >= low) & (axis <= high)
    if mask.sum() < 64: raise ValueError('Insufficient training cases in predeclared regime')
    variable = spec['vary_input']
    vals = local[variable]
    step = max(float(np.quantile(vals, .9)-np.quantile(vals, .1)) * .01, 1e-8)
    plus = {k: v.copy() for k, v in local.items()}
    plus[variable] = vals + step
    plus['q_'+variable] = plus[variable] / plus[variable+'_ref']
    before = evaluate(candidate['formula'], local)
    after = evaluate(candidate['formula'], plus)
    finite = mask & np.isfinite(before) & np.isfinite(after)
    if finite.sum() < .99 * mask.sum(): raise ValueError('Formula unstable inside declared physical regime')
    delta = (after-before)[finite]
    sign = 1 if spec['descriptor_direction'] == 'increasing' else -1
    tol = 1e-10 * max(1., float(np.std(before[finite])))
    if np.any(sign*delta < -tol) or np.mean(sign*delta > tol) < .5:
        raise ValueError('Formula contradicts its declared finite-difference direction')
    correlation = float(spearmanr(before[finite], target[finite]).statistic)
    direction = 1 if spec['entropy_direction'] == 'increasing' else -1
    observed = 'inconclusive' if not np.isfinite(correlation) or abs(correlation) < .05 else (
        'consistent' if direction*correlation > 0 else 'contradicted')
    return {'status': 'passed_formula_check', 'regime_n': int(mask.sum()),
            'native_regime_bounds': [float(low), float(high)], 'perturbation': step,
            'training_spearman': correlation if np.isfinite(correlation) else None,
            'target_association': observed, 'mechanism_validated': False,
            'interpretation': 'Finite difference checks the declared proxy; training association is observational and may be confounded.'}
