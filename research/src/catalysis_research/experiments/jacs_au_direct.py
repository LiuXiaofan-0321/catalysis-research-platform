"""Label-free single-descriptor discovery contracts, separate from historical V4.

All routines in this module accept feature-only inputs. Scientific support and
numerical execution are separate; neither is a causal mechanism validation.
"""
from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

import numpy as np

from .jacs_au import FEATURES
from .jacs_au_kg_v4 import (
    INPUTS, ROLES, audit_formula, evaluate_formula, formula_symbols,
    grounding_check, rotor_classes, scientific_graph, pack_evidence,
    audit_bank, select_evidence,
)

PROFILE = 'jacs-au-direct-v5'
REVISION = 'label-free-preservation-canonical-20261004'
MODES = ('agent', 'rag_agent', 'small_kg_rag_agent')
DIRECTIONS = ('increasing', 'decreasing')
CLAIMS = {'empirical_proxy', 'nonlinear_rotor_expression', 'probe_volume_proxy', 'geometric_path_contrast'}


class ScientificRevisionRequired(ValueError):
    """A scientifically different output cannot be treated as format recovery."""


def load_config(path):
    c = json.loads(Path(path).read_text(encoding='utf-8'))
    expected = {'profile': PROFILE, 'execution_revision': REVISION, 'model': 'glm-5.3-flash',
                'reasoning_effort': 'high', 'thinking': 'enabled', 'temperature': .2,
                'rounds': 3, 'proposals_per_round': 1, 'replicates_per_mode': 10,
                'review_policy': 'preserve_valid_draft', 'label_feedback': False,
                'score_after_all_rounds_frozen': True, 'technical_repair_attempts': 1}
    for k, v in expected.items():
        if c.get(k) != v:
            raise ValueError('Direct protocol configuration mismatch: ' + k)
    if c['evaluation']['fit_seeds'] != [3, 7, 11, 17, 23] or c['evaluation']['epochs'] != 4000:
        raise ValueError('Predeclared seeds and ANN schedule required')
    if c['evaluation']['fitting_failure_policy'] != 'explicit_d0_prediction_fallback':
        raise ValueError('Explicit fitting fallback required')
    if c['evaluation']['input_representation'] != 'train-only-affine-sign-v1':
        raise ValueError('Frozen label-free representation rule required')
    for group in ('generation', 'retrieval'):
        if any(type(v) is not int or v <= 0 for v in c[group].values()):
            raise ValueError('Positive integer budgets required')
    if c['generation']['max_tokens_on_truncation'] < c['generation']['max_tokens']:
        raise ValueError('Invalid output recovery cap')
    return c


def candidate_template():
    return {'slot_id': 'h1', 'name': 'identifier', 'formula': 'one executable expression',
            'hypothesis': 'falsifiable conditional physical hypothesis',
            'rationale': 'proxy limitations and mechanism, not predicted MAE',
            'falsification_criteria': 'boundary or competing explanation',
            'novelty_status': 'known_relation|new_combination|uncertain', 'evidence_ids': [],
            'physical_claims': ['empirical_proxy'],
            'variable_mappings': {'each native input actually used': 'exact input quantity_role'},
            'mechanism_family': 'translation|rotation|shape|connectivity|coupling',
            'proxy_assumptions': 'explicit assumptions; not established causality',
            'physical_prediction': {'vary_input': 'native input', 'hold_fixed': ['other inputs used'],
                                    'loss_direction': 'increasing|decreasing'},
            'expression_check': {'vary_input': 'same native input',
                                 'descriptor_direction': 'increasing|decreasing',
                                 'regime_input': 'native input', 'regime_train_quantiles': [0., 1.]},
            'conditional_proxy_target_direction': 'increasing|decreasing|unknown',
            'boundary_behavior': 'finite training support; legitimate physical zeros preserved',
            'limit_tests': [{'vary_input': 'native input', 'approach': 'positive_infinity',
                             'expected_value': 0.0}]}


def validate_candidate(value):
    if not isinstance(value, dict) or set(value) != {'descriptor_candidate'}:
        raise ValueError('Return exactly one descriptor_candidate, not an external menu')
    c = deepcopy(value['descriptor_candidate'])
    if not isinstance(c, dict) or c.get('slot_id') != 'h1':
        raise ValueError('One h1 descriptor object required')
    keys = set(candidate_template())
    if set(c) != keys:
        raise ValueError('Candidate keys mismatch: missing=' + ','.join(sorted(keys-set(c))) +
                         '; unexpected=' + ','.join(sorted(set(c)-keys)))
    for k in ('name', 'formula', 'hypothesis', 'rationale', 'falsification_criteria',
              'proxy_assumptions', 'boundary_behavior'):
        if not isinstance(c[k], str) or not c[k].strip():
            raise ValueError('Missing candidate text: ' + k)
    if c['novelty_status'] not in ('known_relation', 'new_combination', 'uncertain'):
        raise ValueError('Invalid novelty status')
    if c['mechanism_family'] not in ('translation', 'rotation', 'shape', 'connectivity', 'coupling'):
        raise ValueError('Invalid mechanism family')
    if not isinstance(c['variable_mappings'], dict):
        raise ValueError('Variable mappings required')
    for k in ('evidence_ids', 'physical_claims'):
        if not isinstance(c[k], list) or any(not isinstance(x, str) for x in c[k]):
            raise ValueError('String list required: ' + k)
    if not set(c['physical_claims']) <= CLAIMS:
        raise ValueError('Unknown physical claim type')
    p, e = c['physical_prediction'], c['expression_check']
    if not isinstance(p, dict) or set(p) != {'vary_input', 'hold_fixed', 'loss_direction'}:
        raise ValueError('Physical prediction fields must be separate')
    if not isinstance(e, dict) or set(e) != {'vary_input', 'descriptor_direction', 'regime_input', 'regime_train_quantiles'}:
        raise ValueError('Expression derivative fields must be separate')
    if p['vary_input'] not in FEATURES or p['vary_input'] != e['vary_input'] or e['regime_input'] not in FEATURES:
        raise ValueError('Unknown or mismatched native prediction/derivative axis')
    if not isinstance(p['hold_fixed'], list) or not set(p['hold_fixed']) <= set(FEATURES) or p['vary_input'] in p['hold_fixed']:
        raise ValueError('Invalid hold-fixed variables')
    if p['loss_direction'] not in DIRECTIONS or e['descriptor_direction'] not in DIRECTIONS:
        raise ValueError('Invalid declared physical or expression direction')
    if c['conditional_proxy_target_direction'] not in (*DIRECTIONS, 'unknown'):
        raise ValueError('Invalid conditional proxy-target direction')
    q = e['regime_train_quantiles']
    if not isinstance(q, list) or len(q) != 2 or any(type(x) not in (int, float) or not np.isfinite(x) for x in q) or not 0 <= q[0] < q[1] <= 1 or q[1]-q[0] < .25:
        raise ValueError('Declared regime must cover at least 25% of training quantiles')
    if not isinstance(c['limit_tests'], list):
        raise ValueError('Use a list of structured limits, or [] when none declared')
    for t in c['limit_tests']:
        if not isinstance(t, dict) or set(t) != {'vary_input', 'approach', 'expected_value'} or t['vary_input'] not in FEATURES or t['approach'] != 'positive_infinity' or type(t['expected_value']) not in (int, float) or not np.isfinite(t['expected_value']):
            raise ValueError('Invalid structured finite limit')
    return c


def used_inputs(formula):
    symbols = formula_symbols(formula)
    return {k for k in FEATURES if k in symbols or 'q_'+k in symbols}


def formula_identity(formula):
    """Syntax normalization flags duplicates; no performance-dependent rejection."""
    return ast.dump(ast.parse(formula, mode='eval'), include_attributes=False)


def canonicalize_added_columns(columns, train):
    """Label-free affine/sign convention on the PREDICTOR inputs after freezing.

    Scientific formulas, hypotheses and their directions are never rewritten.
    The first nonzero centered training value fixes sign, not MAE/correlation.
    All methods share the rule; no alternate representation is fitted/selected.
    """
    transformed, records = [], []
    for values in columns:
        values = np.asarray(values, dtype=float)
        if values.ndim != 1 or not np.isfinite(values).all():
            raise ValueError('Finite frozen descriptor values required')
        center = float(np.mean(values[train])); scale = float(np.std(values[train]))
        if scale < 1e-12: raise ValueError('Constant frozen descriptor')
        z = (values-center)/scale
        nonzero = np.flatnonzero(np.abs(z[train]) > 1e-12)
        if not len(nonzero): raise ValueError('No training sign anchor')
        anchor = int(np.asarray(train)[nonzero[0]])
        sign = 1 if z[anchor] > 0 else -1
        transformed.append(sign*z)
        records.append({'training_center':center,'training_scale':scale,'model_input_sign':sign,
                        'training_anchor_row':anchor,'rule':'first nonzero centered training value positive',
                        'labels_or_scoring_used':False,'scientific_expression_unchanged':True})
    return transformed, records


def symbolic_limit(formula, axis, references):
    """Exact positive-domain limit using the safe AST translator."""
    import sympy as s
    return s.limit(_symbolic_parse(formula, references), s.Symbol(axis, positive=True), s.oo)


def precheck(c, env, train):
    """Training-feature-only execution; no entropy, ratio, gas, MAE or history."""
    result = {'status': 'rejected', 'scientific_consistency': 'unverified',
              'source_support': 'requires_independent_review', 'mechanism_validated': False}
    try:
        result['dimensions'] = audit_formula(c['formula'])
        axis = c['expression_check']['vary_input']
        # Reuse definition/rotor checks, not V4 target association or redundancy rejection.
        adapter = {**c, 'scientific_test': {'vary_input': axis, 'physical_interpretation': c['proxy_assumptions']}}
        result['grounding'] = grounding_check(adapter)
        used = used_inputs(c['formula'])
        if set(c['variable_mappings']) != used:
            raise ValueError('Mappings must match exactly the actual proxy inputs')
        if set(c['physical_prediction']['hold_fixed']) != used-{axis}:
            raise ValueError('Conditional prediction must hold other used inputs fixed')
        local = {k: np.asarray(v)[train].copy() for k, v in env.items()}
        local['_rotor_class'] = rotor_classes(local)
        before = evaluate_formula(c['formula'], local)
        if not np.isfinite(before).all():
            raise ValueError('Formula undefined on training support; physical zeros are not imputed')
        if np.std(before) < 1e-12:
            raise ValueError('Constant training descriptor')
        e = c['expression_check']
        lo, hi = np.quantile(local[e['regime_input']], e['regime_train_quantiles'])
        mask = (local[e['regime_input']] >= lo) & (local[e['regime_input']] <= hi)
        if mask.sum() < 64:
            raise ValueError('Insufficient cases in declared regime')
        step = max(float(np.quantile(local[axis], .9)-np.quantile(local[axis], .1))*.01, 1e-8)
        plus = {k: v.copy() for k, v in local.items()}
        plus[axis] += step
        plus['q_'+axis] = plus[axis]/plus[axis+'_ref']
        after = evaluate_formula(c['formula'], plus)
        if not np.isfinite(after[mask]).all():
            raise ValueError('Perturbed descriptor undefined')
        delta = after[mask]-before[mask]
        sign = 1 if e['descriptor_direction'] == 'increasing' else -1
        tol = 1e-10*max(1., float(np.std(before[mask])))
        result['derivative_check'] = {'opposite_n': int(np.sum(sign*delta < -tol)),
                                      'nonzero_fraction': float(np.mean(sign*delta > tol)),
                                      'perturbation': step, 'regime_n': int(mask.sum())}
        if np.any(sign*delta < -tol) or np.mean(sign*delta > tol) < .5:
            raise ValueError('Formula contradicts declared expression derivative; do not invert physics to satisfy metadata')
        bridge = c['conditional_proxy_target_direction']
        consistency = []
        if bridge != 'unknown':
            physical = 1 if c['physical_prediction']['loss_direction'] == 'increasing' else -1
            predicted = sign*(1 if bridge == 'increasing' else -1)
            if predicted != physical:
                consistency.append('Conditional chain directions disagree; not an empirical correlation test')
        references = {k: float(local[k+'_ref'][0]) for k in FEATURES}
        limits = []
        for t in c['limit_tests']:
            try:
                actual = symbolic_limit(c['formula'], t['vary_input'], references)
                import sympy as s
                difference = s.simplify(actual-s.Rational(str(t['expected_value'])))
                state = 'passed' if difference == 0 else ('failed' if difference.is_zero is False else 'unverified')
                if state == 'failed': consistency.append('Incorrect structured limit: '+t['vary_input'])
                limits.append({**t, 'computed_limit': str(actual), 'status': state})
            except (ValueError, NotImplementedError, TypeError, ImportError) as error:
                limits.append({**t, 'status': 'unverified', 'reason': str(error)})
        result.update(status='passed', structured_limit_checks=limits,
                      scientific_consistency='failed' if consistency else 'structural_checks_passed_semantics_unverified',
                      scientific_issues=consistency)
    except (ValueError, SyntaxError, OverflowError, FloatingPointError, TypeError) as error:
        result['reason'] = str(error)
    return result


def technical_patch(original, response):
    """Repair syntax/expression only; scientific fields and proxies are immutable.

Even a same-proxy change can alter the hypothesis (divide -> multiply). Require
symbolic equivalence on the positive native domain, otherwise explicit revision.
Zero-boundary extensions with unchanged positive-domain meaning are permitted.
"""
    if not isinstance(response, dict) or set(response) != {'technical_patch'}:
        raise ValueError('One technical_patch required')
    p = response['technical_patch']
    if not isinstance(p, dict):
        raise ValueError('technical_patch must be an object')
    if set(p)-{'formula', 'boundary_behavior', 'repair_reason', 'variable_mappings', 'descriptor_direction'}:
        raise ScientificRevisionRequired('Scientific revision is forbidden in technical repair')
    c = deepcopy(original)
    if 'formula' in p and p['formula'] != original['formula']:
        if used_inputs(p['formula']) != used_inputs(original['formula']):
            raise ScientificRevisionRequired('Proxy substitution is a hypothesis_revision')
        # If the old formula cannot be parsed/proved, do not silently change science.
        import sympy as s
        # Keep reference symbols independent; X and q_X are not interchangeable.
        a = _symbolic_parse(original['formula'])
        b = _symbolic_parse(p['formula'])
        if s.simplify(a-b) != 0:
            raise ScientificRevisionRequired('Non-equivalent expression is a hypothesis_revision')
        c['formula'] = p['formula']
    if 'boundary_behavior' in p: c['boundary_behavior'] = p['boundary_behavior']
    if 'variable_mappings' in p:
        if p['variable_mappings'] != {k: ROLES[k] for k in used_inputs(c['formula'])}:
            raise ScientificRevisionRequired('Mapping correction must use authoritative definitions, not changed proxies')
        c['variable_mappings'] = deepcopy(p['variable_mappings'])
    if 'descriptor_direction' in p:
        # This field describes the mathematical expression, not the physical
        # prediction. The next actual derivative check must pass; physical claim
        # and conditional target bridge remain unchanged and separately audited.
        c['expression_check']['descriptor_direction'] = p['descriptor_direction']
    return validate_candidate({'descriptor_candidate': c})


def _symbolic_parse(formula, references=None):
    import sympy as s
    if not isinstance(formula, str) or len(formula) > 1500:
        raise ValueError('Invalid symbolic formula size')
    tree = ast.parse(formula, mode='eval')
    if len(list(ast.walk(tree))) > 160:
        raise ValueError('Symbolic formula too complex')
    names = {k: s.Symbol(k, positive=True) for k in FEATURES}
    refs = {k: s.Symbol(k+'_ref', positive=True) if references is None else s.Rational(str(references[k])) for k in FEATURES}
    funcs = {'log': s.log, 'log10': lambda x: s.log(x, 10), 'sqrt': s.sqrt,
             'abs': s.Abs, 'exp': s.exp, 'minimum': s.Min, 'maximum': s.Max}
    def rec(n):
        if isinstance(n, ast.Expression): return rec(n.body)
        if isinstance(n, ast.Constant) and type(n.value) in (int, float): return s.Rational(str(n.value))
        if isinstance(n, ast.Name):
            if n.id in names: return names[n.id]
            for k in FEATURES:
                if n.id == k+'_ref': return refs[k]
                if n.id == 'q_'+k: return names[k]/refs[k]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            return -rec(n.operand) if isinstance(n.op, ast.USub) else rec(n.operand)
        if isinstance(n, ast.BinOp):
            a,b=rec(n.left),rec(n.right)
            if isinstance(n.op, ast.Add): return a+b
            if isinstance(n.op, ast.Sub): return a-b
            if isinstance(n.op, ast.Mult): return a*b
            if isinstance(n.op, ast.Div): return a/b
            if isinstance(n.op, ast.Pow): return a**b
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in funcs and not n.keywords:
            return funcs[n.func.id](*(rec(a) for a in n.args))
        raise ValueError('Symbolic proof unsupported; preserve original, classify proposed change separately')
    return rec(tree)


def hypothesis_revision(original, revised, *, reason, evidence_spans):
    """Separate contract for future revision ablations; main runner never calls it."""
    new = validate_candidate({'descriptor_candidate': revised})
    if not reason or not evidence_spans:
        raise ValueError('Scientific revision needs reason and supporting evidence spans')
    scientific = ('hypothesis', 'rationale', 'falsification_criteria', 'proxy_assumptions')
    if any(new[k] == original[k] for k in scientific):
        raise ValueError('Hypothesis revision must atomically update scientific explanations')
    return {'edit_type': 'hypothesis_revision', 'candidate': new,
            'reason': reason, 'supporting_evidence_spans': deepcopy(evidence_spans)}


def frozen_knowledge(bank, config):
    """Task-wide retrieval before any candidate, common to every method block."""
    audit_bank(bank)
    evidence, trace = select_evidence(bank, [{'hypothesis':
        'translational rotational shape confinement entropy native zero rotor bottleneck accessible probe volume',
        'formula': ''}], [], config, live=None)
    evidence = pack_evidence(evidence)
    raw = scientific_graph(bank)
    refs = {c['mechanism_id']: c['applicability_ref'] for c in evidence['mechanism_cards']}
    nodes = {}
    for key, node in raw['nodes'].items():
        if node['type'] == 'conditional_mechanism':
            if key not in refs: continue
            nodes[key] = {'id': key, 'type': node['type'], 'conditions_ref': 'evidence.source_conditions.'+refs[key]}
        elif key in FEATURES:
            nodes[key] = {'id': key, 'type': node['type'], 'definition_ref': 'inputs.'+key}
        else: nodes[key] = deepcopy(node)
    graph = {'nodes': nodes, 'edges': [deepcopy(e) for e in raw['edges'] if e['from'] in nodes and e['to'] in nodes],
             'check_rule_names': [r['id'] for r in raw['rules']],
             'note': 'Conditional proxy assumptions, not causal edges or executed check results.'}
    # Applicability paragraphs occur once; edges point back to the packed registry.
    for edge in graph['edges']:
        edge.pop('assumptions', None); edge.pop('caveat', None)
    flat = {'node_facts': [{'node_id': k, 'property': p, 'value': deepcopy(v)} for k,n in nodes.items() for p,v in n.items()],
            'relation_facts': deepcopy(graph['edges']), 'check_rule_names': graph['check_rule_names'], 'note': graph['note']}
    return {'evidence': evidence, 'graph': graph, 'flat_graph': flat, 'retrieval': trace,
            'status': 'prepared_before_generation', 'policy': 'fixed reviewed bank; no outcome-conditioned retrieval'}


def common_prompt(domains, history, round_no, mode, knowledge):
    """Whitelist history; labels/outcomes never accepted as prompt fields."""
    if mode not in MODES: raise ValueError('Unknown method')
    prior = []
    for row in history:
        c = row.get('final_candidate')
        prior.append({'round': row['round'], 'appended': row['appended'],
                      'formula': c['formula'] if c else None,
                      'hypothesis': c['hypothesis'] if c else None})
    request = {'task': 'Propose exactly ONE open descriptor; no scored candidate menu.',
        'round': round_no, 'inputs': deepcopy(INPUTS), 'training_feature_domains': deepcopy(domains),
        'prior_formulas': prior,
        'target_definition': 'entropy_loss_over_R=(Sgas-Sads)/R; ANN predicts Sads/Sgas. Loss is NOT -log(Sads/Sgas). No target values are provided.',
        'normalization': 'q_X=X/X_ref, fixed positive reference from training features. Native zeros remain valid; q_X is not X_ref.',
        'formula_rules': ['Use native inputs, q_NAME, NAME_ref, fixed constants; + - * / **, log log10 sqrt abs exp minimum maximum; no indexing or imports. Fixed numerical exponents in [-8,8].',
            'D0 already contains all fourteen inputs. A formula re-expresses information, not a new observation.',
            'Logs/exp require dimensionless arguments; explicit rotor_case for native single-site/linear/nonlinear inertia.',
            'No gas entropy, labels, fitted constants, scores, target correlations, imports or IDs as formula inputs.',
            'Passing Df is not cavity Di; included-along-path Dif is not the passing bottleneck.',
            'AV is mass-specific fixed-probe accessibility, not molecule-specific free volume.',
            'Hold other actually used native inputs fixed in the conditional physical prediction.',
            'Do not copy a previously appended descriptor. Duplicates occupy the slot and will not be resampled.',
            'Unknown graph support is allowed; absent edge does not disprove a proxy or mechanism.',
            'State empirical choices and unverified mechanisms honestly. Structured limits may be empty.'],
        'schema': {'descriptor_candidate': candidate_template()}}
    if mode != 'agent':
        request['evidence'] = deepcopy(knowledge['evidence'])
        # Main RAG is the strengthened, lossless flat-fact control, not weakened text.
        request['knowledge_relations'] = deepcopy(knowledge['graph'] if mode == 'small_kg_rag_agent' else knowledge['flat_graph'])
    return request
