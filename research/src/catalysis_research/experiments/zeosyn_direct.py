"""ZeoSyn label-free direct-addition descriptor discovery (Agent / RAG / KG+RAG).

Each trajectory proposes one descriptor per round for a fixed number of rounds.
A proposal that passes the technical checks is appended directly; no labels,
scores or other trajectories are shown to the model, and nothing is scored until
the trajectory is frozen. Failed slots are kept and skipped, never resampled.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np

from ..datasets import zeosyn as z
from .adszeo_nomination import DslError, compile_formula

PROFILE = 'zeosyn-direct-v1'
MODES = ('agent', 'rag_agent', 'small_kg_rag_agent')
NOVELTY = ('known_relation', 'new_combination', 'uncertain')
KNOWLEDGE_SOURCES = ('evidence', 'prior_knowledge', 'both')
MISSING_LIMIT = 0.5
RANK_REDUNDANCY_LIMIT = 0.9999
FLOAT32_LIMIT = 1e30


def load_config(path):
    c = json.loads(Path(path).read_text(encoding='utf-8'))
    if c.get('profile') != PROFILE:
        raise ValueError('Unexpected profile: ' + str(c.get('profile')))
    for k in ('model', 'thinking', 'reasoning_effort', 'temperature', 'rounds', 'replicates_per_mode',
              'modes', 'queries', 'split', 'evaluation', 'generation', 'retrieval'):
        if k not in c:
            raise ValueError('Missing config key: ' + k)
    if tuple(c['modes']) != MODES:
        raise ValueError('Modes must be agent, rag_agent, small_kg_rag_agent in this order')
    if len(c['queries']) != c['rounds']:
        raise ValueError('One frozen retrieval query per round is required')
    if c.get('label_feedback') is not False:
        raise ValueError('This protocol is label-free')
    ev = c['evaluation']
    if ev['primary_metric'] not in ('accuracy', 'macro_f1', 'balanced_accuracy'):
        raise ValueError('Unsupported primary metric')
    if not ev['fit_seeds'] or len(set(ev['fit_seeds'])) != len(ev['fit_seeds']):
        raise ValueError('Distinct fit seeds required')
    return c


def tasks(config):
    out = []
    for mode in config['modes']:
        for rep in range(1, config['replicates_per_mode'] + 1):
            out.append({'index': len(out), 'mode': mode, 'replicate': rep})
    return out


# ---------------------------------------------------------------- prompts

SYSTEM = (
    'You are an expert in zeolite hydrothermal synthesis and a careful scientist. '
    'You propose one physically or chemically meaningful descriptor at a time. '
    'Return one JSON object only.'
)

OUTPUT_TEMPLATE = {
    'descriptor': {
        'name': 'short_snake_case_identifier',
        'formula': 'one expression using only the listed raw input names',
        'hypothesis': 'falsifiable synthesis hypothesis explaining why this quantity steers the product phase',
        'mechanism': 'chemical or physical mechanism behind the hypothesis',
        'target_frameworks': ['IZA codes or Failed most affected; [] if general'],
        'expected_effect': 'which outcomes should change as the descriptor increases',
        'falsification': 'observation that would contradict the hypothesis',
        'assumptions': 'proxy assumptions and limits of the formula',
        'evidence_ids': [1],
        'knowledge_source': 'evidence|prior_knowledge|both',
        'novelty': 'known_relation|new_combination|uncertain',
    }
}


def input_catalog():
    lines = []
    groups = (('Gel composition (normalized mole fractions; all gel species sum to 1)', z.GEL_INPUTS),
              ('Reaction conditions', z.CONDITION_INPUTS),
              ('OSDA1 conformer descriptors from the dataset authors (0 when no OSDA)', tuple(z.OSDA_TABLE_INPUTS)),
              ('OSDA1 composition from its SMILES (0 when no OSDA)', z.RDKIT_INPUTS),
              ('Other', z.COUNT_INPUTS))
    notes = {'sda1': 'OSDA1 amount', 'OH': 'hydroxide', 'F': 'fluoride', 'H2O': 'water',
             'osda_nN_quaternary': 'number of quaternary ammonium/phosphonium centres',
             'osda_fraction_sp3': 'fraction of sp3 carbons'}
    for title, names in groups:
        lines.append(f'- {title}:')
        for n in names:
            extra = '; '.join(x for x in (notes.get(n), z.INPUT_UNITS.get(n)) if x)
            lines.append(f'  {n}' + (f' ({extra})' if extra else ''))
    return '\n'.join(lines)


def build_prompt(*, config, mode, round_no, history, evidence, frequent_labels):
    rounds = config['rounds']
    parts = [
        'Task: a fixed RandomForest classifier predicts the main product of a zeolite hydrothermal synthesis '
        '(the IZA framework code, or "Failed" for amorphous/dense products) from the synthesis record. '
        'Evaluation uses held-out publications, so descriptors must transfer to recipes from unseen papers.',
        'The classifier already receives D0: every gel mole fraction listed below, crystallization time and '
        'temperature, and 14 OSDA1 conformer descriptors (asphericity, two principal axes, formal charge, SASA, '
        'molecular weight, NPR1, NPR2, rotatable bonds, PMI1-3, sphericity, volume). Tree ensembles split on '
        'one column at a time, so quantities that only emerge from combining inputs are not directly available '
        'to the model.',
        f'Most frequent training outcomes (labels only, no statistics by feature): {", ".join(frequent_labels)}.',
        f'Round {round_no} of {rounds}. Propose exactly ONE new descriptor that you hypothesize carries '
        'synthesis-relevant information for this classification. It will be appended to the classifier input '
        'without any intermediate scoring; you will not see any results.',
        'Allowed raw inputs (use these exact names; no other names exist):',
        input_catalog(),
        'Formula rules: one Python-style arithmetic expression over the raw inputs and numeric constants. '
        'Operators + - * / ** and functions log, log10, log2, exp, sqrt, abs, floor, ceil, minimum(a,b), '
        'maximum(a,b). Add a small constant where a denominator can be zero (many gels contain no Al, F or OSDA). '
        'Do not reproduce a D0 column or a monotone transform of a single D0 column; raw inputs that are not '
        'part of D0 (for example the OSDA composition counts) may be used directly.',
    ]
    if history:
        parts.append('Descriptors already appended in this trajectory (do not repeat them or their monotone transforms):')
        for h in history:
            parts.append(f'- {h["name"]}: {h["formula"]} | {h["hypothesis"]}')
    else:
        parts.append('No descriptor has been appended yet.')
    if mode == 'agent':
        parts.append('No literature evidence is provided in this condition. Use your own scientific knowledge; '
                     'evidence_ids must be [] and knowledge_source must be "prior_knowledge".')
    else:
        parts.append('Literature evidence retrieved for this round is given below as numbered items [k | ...]. '
                     'Ground the hypothesis in this evidence where it is relevant and list the supporting item '
                     'numbers in evidence_ids; you may also use your own knowledge (knowledge_source "both"). '
                     'Items describe other publications; do not assume they report results for this dataset.')
        parts.append('EVIDENCE START\n' + (evidence.get('context') or '(no items retrieved)') + '\nEVIDENCE END')
    parts.append('Return JSON exactly in this shape (values are instructions):\n'
                 + json.dumps(OUTPUT_TEMPLATE, ensure_ascii=False, indent=1))
    return '\n\n'.join(parts)


def repair_prompt(original_prompt, candidate, error):
    return (original_prompt + '\n\nYour previous answer was:\n' + json.dumps({'descriptor': candidate}, ensure_ascii=False)
            + f'\n\nIt failed a technical check: {error}\nReturn the same JSON shape once more. Keep the same '
            'hypothesis and change only what is needed so the formula is valid, finite on most recipes and not '
            'equivalent to an existing input.')


# ---------------------------------------------------------- validation

def _text(value):
    """Accept a string or a list of strings (joined line by line)."""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return '\n'.join(v.strip() for v in value if v.strip())
    return None


def normalize_candidate(value, *, evidence_count):
    """Return (candidate, notes). Raises ValueError for unusable structure."""
    if not isinstance(value, dict):
        raise ValueError('schema_invalid: response is not an object')
    c = value.get('descriptor', value if 'formula' in value else None)
    if not isinstance(c, dict):
        raise ValueError('schema_invalid: missing descriptor object')
    notes = []
    out = {}
    for k in ('name', 'formula', 'hypothesis'):
        t = _text(c.get(k))
        if not t:
            raise ValueError(f'schema_invalid: missing {k}')
        out[k] = t
    out['name'] = re.sub(r'[^a-z0-9_]+', '_', out['name'].lower()).strip('_') or 'descriptor'
    for k in ('mechanism', 'expected_effect', 'falsification', 'assumptions'):
        t = _text(c.get(k))
        if t is None:
            notes.append('missing_or_non_text:' + k)
        out[k] = t or ''
    tf = c.get('target_frameworks', [])
    out['target_frameworks'] = [str(x) for x in tf] if isinstance(tf, list) else [str(tf)]
    ids, bad = [], []
    for x in c.get('evidence_ids') or []:
        try:
            i = int(x)
        except (TypeError, ValueError):
            bad.append(x)
            continue
        (ids if 1 <= i <= evidence_count else bad).append(i)
    if bad:
        notes.append('dropped_invalid_evidence_ids:' + json.dumps(bad, default=str))
    out['evidence_ids'] = sorted(set(ids))
    ks = c.get('knowledge_source')
    out['knowledge_source'] = ks if ks in KNOWLEDGE_SOURCES else 'unspecified'
    nv = c.get('novelty')
    out['novelty'] = nv if nv in NOVELTY else 'uncertain'
    return out, notes


def materialize(values):
    v = np.asarray(values, dtype=float)
    if v.ndim == 0:
        raise DslError('zero_variance', 'formula evaluates to a constant')
    return v


def precheck(formula, env, train, existing):
    """Compile and evaluate on all rows; quality checks use training rows only."""
    fn, used = compile_formula(formula, set(env))
    if not used:
        raise DslError('unsupported_input', 'formula uses no raw input')
    v = materialize(fn(env))
    finite = np.isfinite(v)
    missing = float(1 - finite[train].mean())
    if missing > MISSING_LIMIT:
        raise DslError('non_finite', f'{missing:.1%} of training recipes give a non-finite value')
    vt = v[train][finite[train]]
    if np.nanstd(vt) == 0 or np.unique(vt).size < 2:
        raise DslError('zero_variance', 'constant on training recipes')
    filled = fill_column(v, train)
    rank = _ranks(filled[train])
    for name, col in existing.items():
        r = abs(np.corrcoef(rank, _ranks(col[train]))[0, 1])
        if np.isfinite(r) and r >= RANK_REDUNDANCY_LIMIT:
            raise DslError('redundant', f'rank-equivalent to existing column {name} (|rho|={r:.5f})')
    return filled, {'used_inputs': sorted(used), 'train_nonfinite_fraction': missing}


def _ranks(x):
    order = np.argsort(x, kind='mergesort')
    r = np.empty(len(x))
    r[order] = np.arange(len(x))
    return r


def fill_column(v, train):
    """Non-finite values get a sentinel below the finite training range; clip to float32-safe range."""
    v = np.asarray(v, dtype=float).copy()
    finite = np.isfinite(v)
    tv = v[train][finite[train]]
    lo, hi = (float(tv.min()), float(tv.max())) if tv.size else (0., 0.)
    v[~finite] = lo - 1 - abs(hi - lo)
    return np.clip(v, -FLOAT32_LIMIT, FLOAT32_LIMIT)


def existing_columns(m, added):
    cols = {name: m['d0'][:, i] for i, name in enumerate(z.D0)}
    cols.update({'added:' + a['name']: a['column'] for a in added})
    return cols


def frequent_labels(m, k=20):
    labels, counts = np.unique(m['y'][m['train']], return_counts=True)
    return [str(labels[i]) for i in np.argsort(-counts, kind='mergesort')[:k]]


# ---------------------------------------------------------- generation

def run_trajectory(*, config, mode, replicate, matrices, knowledge, client, log=print):
    from ..models.glm import GlmMalformedJson, GlmOutputTruncated
    m = matrices
    train = m['train']
    gen = config['generation']
    labels_top = frequent_labels(m)
    added, slots, history = [], [], []
    for round_no in range(1, config['rounds'] + 1):
        evidence = knowledge['bundles'][mode][round_no - 1] if mode != 'agent' else {'context': '', 'items': []}
        n_items = len(evidence.get('items') or [])
        prompt = build_prompt(config=config, mode=mode, round_no=round_no, history=history,
                              evidence=evidence, frequent_labels=labels_top)
        slot = {'round': round_no, 'evidence_bundle_hash': evidence.get('bundle_hash'), 'evidence_items': n_items,
                'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(), 'attempts': [], 'status': None}
        user, candidate, error = prompt, None, None
        for attempt in range(1 + config['technical_repair_attempts']):
            kind = 'proposal' if attempt == 0 else 'technical_repair'
            record = {'kind': kind}
            try:
                resp = _call(client, config, user, gen['max_tokens'])
            except GlmOutputTruncated:
                record['truncated_at'] = gen['max_tokens']
                try:
                    resp = _call(client, config, user, gen['max_tokens_on_truncation'])
                except (GlmOutputTruncated, GlmMalformedJson) as exc:
                    record['error'] = 'api_output:' + type(exc).__name__
                    slot['attempts'].append(record)
                    error = record['error']
                    break
            except GlmMalformedJson as exc:
                record['error'] = 'malformed_json'
                record['content'] = exc.content
                slot['attempts'].append(record)
                error = 'malformed_json: return a single JSON object'
                user = prompt + '\n\nYour previous reply was not a valid JSON object. Return only the JSON object.'
                continue
            record.update({'response_id': resp.raw.get('id'), 'usage': resp.usage, 'model': resp.model,
                           'finish_reason': resp.raw['choices'][0].get('finish_reason'), 'raw_structured': resp.structured})
            try:
                cand, notes = normalize_candidate(resp.structured, evidence_count=n_items)
                if mode == 'agent' and cand['evidence_ids']:
                    notes.append('agent_cited_nonexistent_evidence')
                    cand['evidence_ids'] = []
                column, info = precheck(cand['formula'], m['env'], train, existing_columns(m, added))
            except (ValueError, DslError) as exc:
                record['error'] = str(exc)
                slot['attempts'].append(record)
                error = str(exc)
                last = resp.structured.get('descriptor', resp.structured) if isinstance(resp.structured, dict) else {}
                user = repair_prompt(prompt, last, error)
                continue
            record.update({'normalization_notes': notes, 'precheck': info})
            slot['attempts'].append(record)
            candidate = cand
            if attempt > 0:
                first = next((a.get('raw_structured') for a in slot['attempts'] if a.get('raw_structured')), None)
                first_c = first.get('descriptor', first) if isinstance(first, dict) else {}
                candidate['repair_changed_hypothesis'] = _text(first_c.get('hypothesis')) != cand['hypothesis']
            break
        if candidate is None:
            slot['status'] = 'failed'
            slot['failure'] = error
            log(f'{mode} r{replicate} round {round_no}: failed ({error})')
        else:
            slot['status'] = 'appended'
            slot['candidate'] = candidate
            added.append({'name': candidate['name'], 'formula': candidate['formula'], 'column': column})
            history.append(candidate)
            log(f'{mode} r{replicate} round {round_no}: {candidate["formula"]}')
        slots.append(slot)
    return {
        'profile': PROFILE, 'mode': mode, 'replicate': replicate, 'slots': slots,
        'final_formulas': [{'name': a['name'], 'formula': a['formula']} for a in added],
        'appended': len(added), 'label_feedback': False,
    }


def _call(client, config, user, max_tokens):
    return client.chat_json(model=config['model'], system=SYSTEM, user=user,
                            temperature=config['temperature'], max_tokens=max_tokens,
                            thinking=config['thinking'], reasoning_effort=config['reasoning_effort'])


# ---------------------------------------------------------- evaluation

def final_matrix(matrices, generation):
    m = matrices
    cols = [m['d0']]
    existing = {}
    for f in generation['final_formulas']:
        column, _ = precheck(f['formula'], m['env'], m['train'], existing)
        existing[f['name']] = column
        cols.append(column[:, None])
    return np.hstack(cols)


def evaluate_matrix(matrices, x, *, seeds, n_jobs, n_estimators):
    m = matrices
    tr, te, y = m['train'], m['test'], m['y']
    out = []
    for s in seeds:
        pred = z.fit_predict(x[tr], y[tr], x[te], seed=s, n_jobs=n_jobs, n_estimators=n_estimators)
        out.append({'seed': s, **z.classification_metrics(y[te], pred)})
    return out


METRICS = ('accuracy', 'macro_f1', 'balanced_accuracy')


def paired_delta(final, d0):
    by_seed = {r['seed']: r for r in d0}
    rows = []
    for r in final:
        b = by_seed[r['seed']]
        rows.append({'seed': r['seed'], **{k: r[k] - b[k] for k in METRICS}})
    return {'per_seed': rows, 'mean': {k: float(np.mean([r[k] for r in rows])) for k in METRICS}}


def bootstrap_mean(values, *, n=10000, seed=20261007, level=0.95):
    v = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = v[rng.integers(0, len(v), size=(n, len(v)))].mean(axis=1)
    a = (1 - level) / 2
    return {'mean': float(v.mean()), 'ci': [float(np.quantile(means, a)), float(np.quantile(means, 1 - a))], 'n': int(len(v))}


def bootstrap_difference(a, b, *, n=10000, seed=20261007, level=0.975):
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    d = (a[rng.integers(0, len(a), size=(n, len(a)))].mean(1) - b[rng.integers(0, len(b), size=(n, len(b)))].mean(1))
    q = (1 - level) / 2
    return {'mean': float(a.mean() - b.mean()), 'ci': [float(np.quantile(d, q)), float(np.quantile(d, 1 - q))], 'level': level}


def summarize(config, generations, evaluations):
    primary = config['evaluation']['primary_metric']
    per_mode = {}
    for mode in config['modes']:
        ev = [e for e in evaluations if e['mode'] == mode]
        gens = [g for g in generations if g['mode'] == mode]
        per_mode[mode] = {
            'trajectories_evaluated': len(ev), 'trajectories_expected': config['replicates_per_mode'],
            'appended_slots': sum(g['appended'] for g in gens),
            'total_slots': len(gens) * config['rounds'],
            'zero_append_trajectories': sum(g['appended'] == 0 for g in gens),
            **{k: bootstrap_mean([e['delta']['mean'][k] for e in ev]) for k in METRICS if ev},
            'negative_trajectories': sum(e['delta']['mean'][primary] < 0 for e in ev),
        }
    vals = {mode: [e['delta']['mean'][primary] for e in evaluations if e['mode'] == mode] for mode in config['modes']}
    comps = {}
    if all(vals.values()):
        comps = {'small_kg_rag_agent-rag_agent': bootstrap_difference(vals['small_kg_rag_agent'], vals['rag_agent']),
                 'rag_agent-agent': bootstrap_difference(vals['rag_agent'], vals['agent']),
                 'small_kg_rag_agent-agent': bootstrap_difference(vals['small_kg_rag_agent'], vals['agent'])}
    return {'profile': PROFILE, 'primary_metric': primary, 'unit': 'generation trajectory (seeds averaged within)',
            'per_mode': per_mode, 'comparisons': comps,
            'note': 'Deltas are absolute metric differences versus D0 at the same fit seed; failed slots, '
                    'zero-append and negative trajectories are all included.'}

