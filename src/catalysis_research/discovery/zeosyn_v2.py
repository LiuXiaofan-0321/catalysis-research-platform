"""ZeoSyn V2: model-driven retrieval and a KG information channel (see docs/experiments/ZEOSYN_V2_PLAN.md).

Every round has the same three steps in every condition:

1. plan    - the model chooses the synthesis factor to encode next and, where a knowledge source
             exists, writes up to ``max_queries`` search queries of its own;
2. evidence - the condition's source answers those queries (none for Agent);
3. propose - the model proposes one descriptor; evidence is optional.

KG conditions additionally see literature-prior inputs (kg_* columns) that formulas may use.
Labels, scores and other trajectories are never shown. Failed slots are kept, never resampled.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from ..knowledge.kg_features import FEATURES as KG_FEATURES
from . import zeosyn_direct as v1
from .dsl import DslError

PROFILE = 'zeosyn-v2'
MODES = ('agent', 'rag', 'kg', 'kg_shuffled')
OPTIONAL_MODES = ('kg_flat',)
KG_MODES = ('kg', 'kg_shuffled', 'kg_flat')
# What each knowledge source can answer (tool documentation shown to the model; accurate, not prescriptive).
SOURCE_SCOPE = {
    'rag': 'It returns passages from zeolite papers that match your query text.',
    'kg': ('It answers questions about named OSDAs, frameworks (IZA codes or material names such as SSZ-13, ZSM-5) '
           'and gel conditions (fluoride medium; Ge, B, Ti, Sn, Ga, Zn or P in the gel): which frameworks were '
           'obtained, with which OSDAs, how often and in how many papers. It does not contain gel ratios such as '
           'OH/Si or H2O/Si.'),
}
SOURCE_SCOPE['kg_shuffled'] = SOURCE_SCOPE['kg_flat'] = SOURCE_SCOPE['kg']
SOURCE_NAME = {'rag': 'a full-text retrieval index of 6,691 zeolite papers',
               'kg': 'a knowledge graph of zeolite synthesis experiments from 6,691 papers',
               'kg_shuffled': 'a knowledge graph of zeolite synthesis experiments from 6,691 papers',
               'kg_flat': 'a knowledge graph of zeolite synthesis experiments from 6,691 papers'}


def load_config(path):
    c = json.loads(Path(path).read_text(encoding='utf-8'))
    if c.get('profile') != PROFILE:
        raise ValueError('Unexpected profile: ' + str(c.get('profile')))
    for k in ('model', 'thinking', 'reasoning_effort', 'temperature', 'rounds', 'replicates_per_mode', 'modes',
              'max_queries', 'evidence_token_budget', 'split', 'kg', 'rag', 'evaluation', 'generation', 'protocol'):
        if k not in c:
            raise ValueError('Missing config key: ' + k)
    bad = set(c['modes']) - set(MODES) - set(OPTIONAL_MODES)
    if bad:
        raise ValueError(f'Unknown modes: {sorted(bad)}')
    if c.get('label_feedback') is not False:
        raise ValueError('This protocol is label-free')
    if c['evaluation']['primary_metric'] not in ('accuracy', 'macro_f1', 'balanced_accuracy'):
        raise ValueError('Unsupported primary metric')
    return c


def tasks(config):
    out = []
    for mode in config['modes']:
        for rep in range(1, config['replicates_per_mode'] + 1):
            out.append({'index': len(out), 'mode': mode, 'replicate': rep})
    return out


# ---------------------------------------------------------------- prompts

def kg_catalog():
    return '\n'.join(f'  {name} ({desc})' for name, desc in KG_FEATURES.items())


def _common_header(*, config, mode, round_no, history, frequent_labels):
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
        f'Round {round_no} of {config["rounds"]}. One descriptor will be appended per round without any '
        'intermediate scoring; you will not see any results.',
        'Allowed raw inputs (use these exact names; no other names exist):',
        v1.input_catalog(),
    ]
    if mode in KG_MODES:
        parts.append('Literature-prior inputs from the knowledge graph. For each recipe they summarise the synthesis '
                     'experiments that OTHER publications report with the same OSDA1 (aggregated from thousands of '
                     'experiments), so they carry information that D0 does not contain, such as which frameworks this '
                     'OSDA has produced elsewhere. Values are 0 or -1 when the OSDA is absent from the graph. They are '
                     'allowed inputs too:\n' + kg_catalog())
    parts.append('Formula rules: one Python-style arithmetic expression over the allowed inputs and numeric '
                 'constants. Operators + - * / ** and functions log, log10, log2, exp, sqrt, abs, floor, ceil, '
                 'minimum(a,b), maximum(a,b). Add a small constant where a denominator can be zero. Do not reproduce '
                 'a D0 column or a monotone transform of a single D0 column; other allowed inputs may be used directly.')
    if history:
        parts.append('Descriptors already appended in this trajectory (do not repeat them or their monotone transforms):')
        parts += [f'- {h["name"]}: {h["formula"]} | {h["hypothesis"]}' for h in history]
    else:
        parts.append('No descriptor has been appended yet.')
    return parts


PLAN_TEMPLATE = {'plan': {'factor': 'the synthesis factor you will encode this round',
                          'why': 'why it should carry information the classifier lacks',
                          'queries': ['up to N short search queries for the knowledge source, or []']}}


def plan_prompt(*, config, mode, round_no, history, frequent_labels):
    parts = _common_header(config=config, mode=mode, round_no=round_no, history=history,
                           frequent_labels=frequent_labels)
    parts.append('Step 1 of 2: choose the ONE synthesis factor you consider most informative to encode next. '
                 'Choose freely among all aspects of the synthesis.')
    if mode == 'agent':
        parts.append('No external knowledge source is available in this condition; set "queries" to [].')
    else:
        parts.append(f'Before proposing the descriptor you may consult {SOURCE_NAME[mode]}. {SOURCE_SCOPE[mode]} Write up to '
                     f'{config["max_queries"]} short, specific search queries about what you want to check '
                     '(for example an OSDA, a framework, or a gel condition). Write [] if you do not need it.')
    template = json.loads(json.dumps(PLAN_TEMPLATE).replace('up to N', f'up to {config["max_queries"]}'))
    parts.append('Return JSON exactly in this shape (values are instructions):\n' + json.dumps(template, indent=1))
    return '\n\n'.join(parts)


def propose_prompt(*, config, mode, round_no, history, frequent_labels, plan, evidence):
    parts = _common_header(config=config, mode=mode, round_no=round_no, history=history,
                           frequent_labels=frequent_labels)
    parts.append(f'Step 2 of 2. Your plan for this round: factor = {plan["factor"]!r}; reason = {plan["why"]!r}.')
    if mode == 'agent':
        parts.append('No literature evidence is available in this condition. Use your own scientific knowledge; '
                     'evidence_ids must be [] and knowledge_source must be "prior_knowledge".')
    else:
        parts.append(f'Your queries: {json.dumps(plan["queries"], ensure_ascii=False)}. Results from '
                     f'{SOURCE_NAME[mode]} are numbered below. Use them only where they add information beyond your '
                     'own knowledge; do not build a descriptor merely because an item mentions a quantity, and '
                     'ignore items that are irrelevant. Cite the items you actually rely on in evidence_ids '
                     '(possibly []), and set knowledge_source to "evidence", "prior_knowledge" or "both".')
        parts.append('EVIDENCE START\n' + (evidence.get('context') or '(nothing matched the queries)') + '\nEVIDENCE END')
    parts.append('Propose exactly ONE new descriptor. Return JSON exactly in this shape (values are instructions):\n'
                 + json.dumps(v1.OUTPUT_TEMPLATE, ensure_ascii=False, indent=1))
    return '\n\n'.join(parts)


def normalize_plan(value, max_queries):
    p = value.get('plan', value) if isinstance(value, dict) else None
    if not isinstance(p, dict):
        raise ValueError('schema_invalid: missing plan object')
    factor = v1._text(p.get('factor')) or ''
    why = v1._text(p.get('why')) or ''
    if not factor:
        raise ValueError('schema_invalid: missing factor')
    q = p.get('queries') or []
    q = [q] if isinstance(q, str) else q
    queries = [str(x).strip() for x in q if isinstance(x, (str, int, float)) and str(x).strip()][:max_queries]
    return {'factor': factor, 'why': why, 'queries': queries}


# ---------------------------------------------------------------- evidence providers

class NoEvidence:
    def __call__(self, queries):
        return {'items': [], 'context': '', 'tokens': 0}


class KgEvidence:
    def __init__(self, engine, *, token_budget, flat=False):
        self.engine, self.token_budget, self.flat = engine, token_budget, flat

    def __call__(self, queries):
        return self.engine.evidence(queries, token_budget=self.token_budget, flat=self.flat)


class RagEvidence:
    """Wraps KnowledgeModeRetriever (mode rag_agent) and merges per-query bundles into one budgeted context."""

    def __init__(self, retriever, *, budget, token_budget, lock=None):
        self.retriever, self.budget, self.token_budget, self.lock = retriever, budget, token_budget, lock

    def __call__(self, queries):
        from ..knowledge.retrieval.bundle import count_tokens
        items, used, seen = [], 0, set()
        for q in queries:
            if self.lock:
                with self.lock:
                    b = self.retriever.retrieve(query=q, experiment_mode='rag_agent', budget=self.budget)
            else:
                b = self.retriever.retrieve(query=q, experiment_mode='rag_agent', budget=self.budget)
            for it in b['items']:
                if it['record_id'] in seen:
                    continue
                text = f'(paper={it["paper_id"]}) {it["quote"]}'
                n = count_tokens(text)
                if used + n > self.token_budget:
                    continue
                seen.add(it['record_id'])
                items.append({'id': len(items) + 1, 'key': it['record_id'], 'paper_id': it['paper_id'],
                              'text': text, 'tokens': n})
                used += n
        return {'items': items, 'context': '\n\n'.join(f'[{i["id"]}] {i["text"]}' for i in items), 'tokens': used}


# ---------------------------------------------------------------- generation

def env_for_mode(split, mode):
    """Allowed inputs of a condition: raw inputs, plus the matching kg_* table for KG conditions."""
    env = dict(split['env'])
    if mode in KG_MODES:
        table = split['kg_tables']['kg_shuffled' if mode == 'kg_shuffled' else 'kg']
        env.update(table)
    return env


def run_trajectory(*, config, mode, replicate, split, evidence_provider, client, log=print):
    from ..llm.glm import GlmMalformedJson, GlmOutputTruncated
    env = env_for_mode(split, mode)
    train = split['train']
    labels_top = v1.frequent_labels({'y': split['y'], 'train': train})
    added, slots, history = [], [], []
    gen = config['generation']

    def call(user):
        try:
            return v1._call(client, config, user, gen['max_tokens'])
        except GlmOutputTruncated:
            return v1._call(client, config, user, gen['max_tokens_on_truncation'])

    for round_no in range(1, config['rounds'] + 1):
        slot = {'round': round_no, 'attempts': [], 'status': None}
        # step 1: plan
        p_prompt = plan_prompt(config=config, mode=mode, round_no=round_no, history=history, frequent_labels=labels_top)
        plan, plan_record = None, {'kind': 'plan', 'prompt_sha256': hashlib.sha256(p_prompt.encode()).hexdigest()}
        for attempt in range(2):
            try:
                resp = call(p_prompt if attempt == 0 else p_prompt + '\n\nReturn only the JSON object.')
                plan = normalize_plan(resp.structured, config['max_queries'])
                plan_record.update({'response_id': resp.raw.get('id'), 'usage': resp.usage, 'raw_structured': resp.structured})
                break
            except (GlmMalformedJson, GlmOutputTruncated, ValueError) as exc:
                plan_record.setdefault('errors', []).append(f'{type(exc).__name__}: {exc}')
        slot['attempts'].append(plan_record)
        if plan is None:
            slot.update({'status': 'failed', 'failure': 'plan_failed'})
            slots.append(slot)
            log(f'{mode} r{replicate} round {round_no}: plan failed')
            continue
        if mode == 'agent':
            plan['queries'] = []
        slot['plan'] = plan
        # step 2: evidence
        evidence = evidence_provider(plan['queries']) if plan['queries'] else {'items': [], 'context': '', 'tokens': 0}
        slot['evidence'] = {'items': [{k: v for k, v in i.items() if k != 'text'} for i in evidence['items']],
                            'tokens': evidence.get('tokens', 0), 'linking': evidence.get('linking'),
                            'context_sha256': hashlib.sha256((evidence.get('context') or '').encode()).hexdigest()}
        # step 3: propose (+ at most one technical repair)
        prompt = propose_prompt(config=config, mode=mode, round_no=round_no, history=history,
                                frequent_labels=labels_top, plan=plan, evidence=evidence)
        slot['propose_prompt_sha256'] = hashlib.sha256(prompt.encode()).hexdigest()
        user, candidate, error, column = prompt, None, None, None
        n_items = len(evidence['items'])
        for attempt in range(1 + config['technical_repair_attempts']):
            record = {'kind': 'proposal' if attempt == 0 else 'technical_repair'}
            try:
                resp = call(user)
            except GlmMalformedJson as exc:
                record.update({'error': 'malformed_json', 'content': exc.content})
                slot['attempts'].append(record)
                error, user = 'malformed_json', prompt + '\n\nYour previous reply was not a valid JSON object. Return only the JSON object.'
                continue
            except GlmOutputTruncated:
                record['error'] = 'output_truncated'
                slot['attempts'].append(record)
                error = 'output_truncated'
                break
            record.update({'response_id': resp.raw.get('id'), 'usage': resp.usage, 'model': resp.model,
                           'finish_reason': resp.raw['choices'][0].get('finish_reason'), 'raw_structured': resp.structured})
            try:
                cand, notes = v1.normalize_candidate(resp.structured, evidence_count=n_items)
                if mode == 'agent' and cand['evidence_ids']:
                    notes.append('agent_cited_nonexistent_evidence')
                    cand['evidence_ids'] = []
                column, info = v1.precheck(cand['formula'], env, train, existing_columns(split, added))
            except (ValueError, DslError) as exc:
                record['error'] = str(exc)
                slot['attempts'].append(record)
                error = str(exc)
                last = resp.structured.get('descriptor', resp.structured) if isinstance(resp.structured, dict) else {}
                user = v1.repair_prompt(prompt, last, error)
                continue
            record.update({'normalization_notes': notes, 'precheck': info})
            slot['attempts'].append(record)
            cand['uses_kg_inputs'] = sorted(set(info['used_inputs']) & set(KG_FEATURES))
            cand['cited_evidence_keys'] = [evidence['items'][i - 1]['key'] for i in cand['evidence_ids']]
            candidate = cand
            break
        if candidate is None:
            slot.update({'status': 'failed', 'failure': error})
            log(f'{mode} r{replicate} round {round_no}: failed ({error})')
        else:
            slot.update({'status': 'appended', 'candidate': candidate})
            added.append({'name': candidate['name'], 'formula': candidate['formula'], 'column': column})
            history.append(candidate)
            log(f'{mode} r{replicate} round {round_no}: [{plan["factor"][:50]}] {candidate["formula"]}')
        slots.append(slot)
    return {'profile': PROFILE, 'mode': mode, 'replicate': replicate, 'split': split['name'], 'slots': slots,
            'final_formulas': [{'name': a['name'], 'formula': a['formula']} for a in added],
            'appended': len(added), 'label_feedback': False}


def existing_columns(split, added):
    cols = {name: split['d0'][:, i] for i, name in enumerate(split['d0_names'])}
    cols.update({'added:' + a['name']: a['column'] for a in added})
    return cols


def final_matrix(split, generation):
    env = env_for_mode(split, generation['mode'])
    cols, existing = [split['d0']], {}
    for f in generation['final_formulas']:
        column, _ = v1.precheck(f['formula'], env, split['train'], existing)
        existing[f['name']] = column
        cols.append(column[:, None])
    return np.hstack(cols)
