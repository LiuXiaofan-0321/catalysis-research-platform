import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from catalysis_research.datasets import zeosyn as z
from catalysis_research.experiments import zeosyn_direct as zd
from catalysis_research.experiments import zeosyn_knowledge as zk
from catalysis_research.experiments.adszeo_nomination import DslError
from catalysis_research.models.glm import GlmResponse

CONFIG = Path(__file__).resolve().parents[1] / 'configs' / 'experiments' / 'zeosyn-direct-v1.json'


def matrices(n=200, seed=0):
    rng = np.random.default_rng(seed)
    env = {k: rng.random(n) for k in z.raw_input_names()}
    env['Al'][: n // 4] = 0.0
    d0 = np.column_stack([env[k] for k in z.GEL_INPUTS + z.CONDITION_INPUTS] + [rng.random(n) for _ in z.NATIVE_OSDA_D0])
    y = np.where(env['Si'] / (env['Al'] + 1e-3) > 3, 'MFI', 'FAU').astype(str)
    return {'train': np.arange(0, 150), 'test': np.arange(150, n), 'y': y, 'd0': d0, 'env': env}


class FakeClient:
    def __init__(self, replies):
        self.replies = list(replies)
        self.prompts = []

    def chat_json(self, **kw):
        self.prompts.append(kw['user'])
        reply = self.replies.pop(0)
        return GlmResponse(structured=reply, raw={'id': f'r{len(self.prompts)}', 'choices': [{'finish_reason': 'stop'}]},
                           provider='fake', model='fake', usage={})


def cand(formula, **kw):
    return {'descriptor': {'name': 'x', 'formula': formula, 'hypothesis': 'h', 'mechanism': 'm',
                           'target_frameworks': [], 'expected_effect': 'e', 'falsification': 'f',
                           'assumptions': ['a', 'b'], 'evidence_ids': [], 'knowledge_source': 'prior_knowledge',
                           'novelty': 'uncertain', **kw}}


def test_config_and_tasks():
    c = zd.load_config(CONFIG)
    t = zd.tasks(c)
    assert len(t) == 30 and t[0]['mode'] == 'agent' and t[-1] == {'index': 29, 'mode': 'small_kg_rag_agent', 'replicate': 10}


def test_list_text_fields_are_joined_not_rejected():
    c, notes = zd.normalize_candidate(cand('Si/(Al+1e-3)'), evidence_count=0)
    assert c['assumptions'] == 'a\nb' and notes == []


def test_invalid_evidence_ids_are_dropped_and_recorded():
    c, notes = zd.normalize_candidate(cand('Si', evidence_ids=[1, 7, 'x']), evidence_count=3)
    assert c['evidence_ids'] == [1] and notes and notes[0].startswith('dropped_invalid_evidence_ids')


def test_missing_formula_is_schema_failure():
    with pytest.raises(ValueError, match='schema_invalid'):
        zd.normalize_candidate({'descriptor': {'name': 'x', 'hypothesis': 'h'}}, evidence_count=0)


def test_precheck_codes():
    m = matrices()
    existing = zd.existing_columns(m, [])
    with pytest.raises(DslError) as e:
        zd.precheck('Si * unknown', m['env'], m['train'], existing)
    assert e.value.code == 'unsupported_input'
    with pytest.raises(DslError) as e:
        zd.precheck('__import__("os")', m['env'], m['train'], existing)
    assert e.value.code == 'unsafe_expression'
    with pytest.raises(DslError) as e:
        zd.precheck('log(Si) * 2 + 1', m['env'], m['train'], existing)  # monotone in a D0 column
    assert e.value.code == 'redundant'
    col, info = zd.precheck('Si / Al', m['env'], m['train'], {})  # 25% division by zero is allowed
    assert 0.2 < info['train_nonfinite_fraction'] < 0.5 and np.all(np.isfinite(col))
    col, info = zd.precheck('Si / (Al + 1e-3)', m['env'], m['train'], existing)
    assert np.all(np.isfinite(col)) and info['used_inputs'] == ['Al', 'Si']


def test_raw_input_outside_d0_is_allowed():
    m = matrices()
    col, _ = zd.precheck('osda_nN_quaternary', m['env'], m['train'], zd.existing_columns(m, []))
    assert np.allclose(col, m['env']['osda_nN_quaternary'])


def test_nonfinite_values_get_sentinel_below_training_range():
    v = np.array([1.0, 2.0, np.inf, np.nan, 3.0])
    out = zd.fill_column(v, np.array([0, 1, 4]))
    assert out[2] == out[3] < 1.0


def test_trajectory_repairs_once_then_skips_failed_slot():
    c = zd.load_config(CONFIG)
    m = matrices()
    client = FakeClient([
        cand('Si / (Al + 1e-3)'),                   # round 1 ok
        cand('Si * bogus'), cand('Si * bogus2'),    # round 2 fails twice -> skipped
        cand('Na / (Al + 1e-3)', hypothesis='h2'),  # round 3 ok
    ])
    g = zd.run_trajectory(config=c, mode='agent', replicate=1, matrices=m, knowledge={'bundles': {}},
                          client=client, log=lambda *_: None)
    assert [s['status'] for s in g['slots']] == ['appended', 'failed', 'appended']
    assert g['appended'] == 2 and len(client.prompts) == 4
    assert 'failed a technical check' in client.prompts[2]
    assert 'Si / (Al + 1e-3)' in client.prompts[3]          # history carries appended formulas
    assert 'EVIDENCE START' not in client.prompts[0]
    x = zd.final_matrix(m, g)
    assert x.shape == (len(m['y']), m['d0'].shape[1] + 2)


def test_redundant_with_previous_descriptor_is_rejected():
    c = zd.load_config(CONFIG)
    m = matrices()
    client = FakeClient([cand('Si / (Al + 1e-3)'), cand('log(Si / (Al + 1e-3))'), cand('2*log(Si/(Al+1e-3))'),
                         cand('K / (Al + 1e-3)')])
    g = zd.run_trajectory(config=c, mode='agent', replicate=1, matrices=m, knowledge={'bundles': {}},
                          client=client, log=lambda *_: None)
    assert g['slots'][1]['status'] == 'failed' and 'redundant' in g['slots'][1]['failure']


def test_knowledge_modes_see_their_own_bundle_only():
    c = zd.load_config(CONFIG)
    m = matrices()
    bundles = {mode: [{'context': f'[1 | {mode} round {r}]\nquote', 'items': [{}], 'bundle_hash': f'{mode}{r}'}
                      for r in range(1, 4)] for mode in ('rag_agent', 'small_kg_rag_agent')}
    client = FakeClient([cand('Si/(Al+1e-3)', evidence_ids=[1]), cand('Na/(Al+1e-3)'), cand('K/(Al+1e-3)')])
    g = zd.run_trajectory(config=c, mode='rag_agent', replicate=2, matrices=m, knowledge={'bundles': bundles},
                          client=client, log=lambda *_: None)
    assert 'rag_agent round 1' in client.prompts[0] and 'small_kg' not in client.prompts[0]
    assert g['slots'][0]['candidate']['evidence_ids'] == [1]
    assert g['slots'][2]['evidence_bundle_hash'] == 'rag_agent3'


def test_paired_delta_and_summary_keep_all_trajectories():
    c = zd.load_config(CONFIG)
    d0 = [{'seed': s, 'accuracy': .4, 'macro_f1': .3, 'balanced_accuracy': .3} for s in (3, 7)]
    evs, gens = [], []
    for mode, gain in (('agent', .01), ('rag_agent', .02), ('small_kg_rag_agent', -.01)):
        for rep in (1, 2):
            final = [{**r, 'accuracy': r['accuracy'] + gain * rep} for r in d0]
            evs.append({'mode': mode, 'replicate': rep, 'delta': zd.paired_delta(final, d0)})
            gens.append({'mode': mode, 'replicate': rep, 'appended': rep})
    s = zd.summarize({**c, 'replicates_per_mode': 2}, gens, evs)
    assert s['per_mode']['small_kg_rag_agent']['negative_trajectories'] == 2
    assert s['per_mode']['rag_agent']['accuracy']['mean'] == pytest.approx(.03)
    assert s['comparisons']['rag_agent-agent']['mean'] == pytest.approx(.015)


def test_doi_split_keeps_publications_together():
    frame = pd.DataFrame({'doi': ['10.1/A', '10.1/a', 'doi:10.1/A', '10.2/b', '10.3/c', None, '10.4/d'] * 3})
    train, test, test_dois = z.doi_group_split(frame, test_fraction=0.3, seed=1)
    groups = frame['doi'].map(z.normalize_doi)
    assert not set(groups.iloc[train].dropna()) & set(groups.iloc[test].dropna())
    assert set(test_dois) == set(groups.iloc[test].dropna())


def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(r) + '\n' for r in rows), encoding='utf-8')


def test_exclusion_counts_and_doi_matching(tmp_path):
    papers = ['doi:10.1/A', 'doi:10.2/b', 'doi:10.1126/science.ads7290', 'sha:xyz']
    write_jsonl(tmp_path / 'papers.jsonl', [{'paper_id': p} for p in papers])
    write_jsonl(tmp_path / 'documents.jsonl', [{'paper_id': p, 'document_id': p + ':m'} for p in papers]
                + [{'paper_id': 'doi:10.1/A', 'document_id': 'doi:10.1/A:si'}])
    write_jsonl(tmp_path / 'chunks.jsonl', [{'paper_id': p} for p in papers for _ in range(3)])
    write_jsonl(tmp_path / 'evidence_records.jsonl', [{'paper_id': 'doi:10.1/A'}, {'paper_id': 'sha:xyz'}])
    matched = zk.match_index_papers(tmp_path, ['10.1/a', '10.9/absent'])
    assert matched == ['doi:10.1/A']
    counts = zk.exclusion_counts(tmp_path, {'doi:10.1/A', 'doi:10.1126/science.ads7290'})
    assert counts == {'expected_excluded_documents': 3, 'expected_excluded_records': 7,
                      'expected_retained_papers': 2, 'expected_retained_documents': 2,
                      'expected_retained_chunks': 6}
    base = {'retrieval_id': 'r', 'rag': {'excluded_paper_ids': ['doi:10.1126/science.ads7290']}}
    rc = zk.retrieval_config(base, matched_ids=matched, counts=counts, test_dois=['10.1/a', '10.9/absent'],
                             matrix_sha256='h')
    assert rc['rag']['excluded_paper_ids'] == ['doi:10.1/A', 'doi:10.1126/science.ads7290']
    assert base['rag']['excluded_paper_ids'] == ['doi:10.1126/science.ads7290']


def test_bundle_leak_check_fails_closed():
    class R:
        def retrieve(self, *, query, experiment_mode, budget):
            return {'items': [{'paper_id': 'doi:10.1/A'}]}
    with pytest.raises(RuntimeError, match='Held-out'):
        zk.freeze_bundles(R(), queries=['q'], budget=None, held_out_dois=['10.1/a'])
