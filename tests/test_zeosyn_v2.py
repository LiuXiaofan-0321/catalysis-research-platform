import gzip
import json
import sys
from pathlib import Path

import numpy as np
import pytest

from catalysis_research.discovery import zeosyn_v2 as v2
from catalysis_research.discovery import zeosyn_v2_eval as ev
from catalysis_research.knowledge import kg_features as kf
from catalysis_research.knowledge import kg_synthesis as ks
from catalysis_research.knowledge.kg_facts import KgFactEngine
from catalysis_research.llm.glm import GlmResponse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'configs' / 'experiments' / 'zeosyn-v2.json'
sys.path.insert(0, str(ROOT / 'scripts'))


# ---------------------------------------------------------------- entity linking

def test_trailing_alias_is_split_but_nomenclature_parentheses_are_not():
    assert 'TPAOH' in ks.name_variants('tetrapropylammonium hydroxide (TPAOH)')
    v = ks.name_variants('1,4-bis(N-methylpyrrolidinium)butane')
    assert v == ['1,4-bis(N-methylpyrrolidinium)butane']
    v = ks.name_variants('1,6-hexamethylene bis(benzyl dimethyl ammonium hydroxide)')
    assert all('bis(' in x for x in v)


def test_abbreviation_rules():
    assert ks.abbreviation_expansion('TPAOH') == 'tetrapropylammonium'
    assert ks.abbreviation_expansion('HMI') == 'hexamethyleneimine'  # not HM + iodide
    assert ks.abbreviation_expansion('TEA') is None                   # triethylamine or tetraethylammonium
    assert ks.abbreviation_expansion('TEAOH') == 'tetraethylammonium'
    assert ks.abbreviation_expansion('TEA+') == 'tetraethylammonium'


def test_parent_only_alias_is_dropped():
    c = ks.candidate_names(['N,N-diisopropyl imidazolium', 'imidazolium'])
    assert 'imidazolium' not in c and 'N,N-diisopropyl imidazolium' in c


class FakeResolver:
    def __init__(self, table):
        self.table = table

    def resolve(self, name):
        return self.table.get(name)


def test_full_name_structure_takes_precedence_over_abbreviation_alias():
    pytest.importorskip('rdkit')
    deta = ks.canonical_osda('NCCNCCN')
    aliases = {ks.normalize_name('diethylenetriamine'): deta}
    reagents = {
        'e1': ['N-[3-(trimethoxysilyl)propyl]ethylenediamine (DETA)'],  # explicit silane name, DETA label is wrong
        'e2': ['DETA'],
        'e3': ['tetraalkylammonium bromides'],
    }
    resolver = FakeResolver({'N-[3-(trimethoxysilyl)propyl]ethylenediamine': 'CO[Si](CCCNCCN)(OC)OC'})
    links, how = ks.link_reagents(reagents, aliases, resolvers=[('opsin', resolver)], log=lambda *_: None)
    assert 'e1' not in links          # the silane is not a ZeoSyn OSDA
    assert links['e2'] == (deta, 'alias')
    assert 'e3' not in links          # generic class name


def test_osda_identity_merges_resonance_counterions_and_protonation():
    pytest.importorskip('rdkit')
    c = ks.canonical_osda
    assert c('CCCCCC[n+]1ccn(C)c1C') == c('CCCCCCn1cc[n+](C)c1C')
    assert c('CCC[N+](CCC)(CCC)CCC.[OH-]') == c('CCC[N+](CCC)(CCC)CCC')
    assert c('CC(C)[NH3+]') == c('CC(C)N')
    assert c('C1CCCNCC1') != c('C[N+](C)(C)CCCCCC[N+](C)(C)C')
    assert not ks.structure_is_single_organic('NCCN.NCCN.[Co+3]')


def test_framework_codes_are_iza_only():
    canon = ks.framework_canonicalizer(['*BEA', 'CHA', '-SVR'])
    assert canon('BEA') == '*BEA' and canon('cha') == 'CHA' and canon('SVR') == '-SVR'
    assert canon('SAPO') is None and canon('ALPO') is None


def _write_gz(path, rows):
    with gzip.open(path, 'wt', encoding='utf-8') as fh:
        fh.writelines(json.dumps(r) + '\n' for r in rows)


def test_stream_synthesis_records_keeps_synthesis_experiments_with_products(tmp_path):
    (tmp_path / 'papers.jsonl').write_text(json.dumps({'paper_id': 'doi:10.1/a', 'doi': '10.1/A', 'year': 2010}) + '\n')
    ent = lambda i, t, name, code=None: {'id': i, 'node_type': 'entity', 'canonical_name': name,
                                          'data': {'type': t, 'aliases': [], 'identifiers': {'framework_code': code},
                                                   'attributes': {'si_al_ratio': 30}}}
    exp = lambda i, t, conds: {'id': i, 'node_type': 'experiment', 'label': '',
                               'data': {'experiment_type': t, 'objective': '', 'conditions': conds}}
    _write_gz(tmp_path / 'nodes.jsonl.gz', [
        ent('osda', 'synthesis_reagent', 'TPAOH'), ent('hf', 'synthesis_reagent', 'HF'),
        ent('prod', 'catalyst_sample', 'ZSM-5', 'MFI'),
        exp('x1', 'hydrothermal synthesis', [{'name': 'temperature', 'value': 443, 'unit': 'K'},
                                             {'name': 'time', 'value': 3, 'unit': 'd'}]),
        exp('x2', 'catalytic_test', []),
    ])
    edge = lambda f, t, et: {'from_node_id': f, 'to_node_id': t, 'edge_type': et, 'source_paper_id': 'doi:10.1/a'}
    _write_gz(tmp_path / 'edges.jsonl.gz', [
        edge('x1', 'osda', 'EXPERIMENT_USES_MATERIAL'), edge('x1', 'hf', 'EXPERIMENT_USES_MATERIAL'),
        edge('x1', 'prod', 'EXPERIMENT_USES_SAMPLE'), edge('x2', 'prod', 'EXPERIMENT_USES_SAMPLE'),
    ])
    records, reagents, papers, names = ks.stream_synthesis_records(tmp_path, canonical_code=ks.framework_canonicalizer(['MFI']))
    assert len(records) == 1
    r = records[0]
    assert r['products'] == ['MFI'] and r['fluoride'] and r['year'] == 2010 and r['doi'] == '10.1/a'
    assert r['temperature_c'] == pytest.approx(169.85) and r['time_h'] == 72
    assert set(reagents) == {'osda', 'hf'} and names == {'ZSM-5': 'MFI'}


# ---------------------------------------------------------------- literature features

def _records():
    rec = lambda e, doi, year, prods, osda='A': {'experiment': e, 'paper_id': 'p:' + doi, 'doi': doi, 'year': year,
                                                'reagents': [osda], 'products': prods, 'fluoride': e.endswith('f'),
                                                'heteroatoms': [], 'temperature_c': 150.0, 'product_si_al': None}
    return [rec('x1', 'd1', 2000, ['CHA']), rec('x2f', 'd2', 2005, ['CHA']), rec('x3', 'd3', 2010, ['AEI']),
            rec('x4', 'd4', 2001, ['MFI'], 'B'), rec('x5', 'd5', 2003, ['MFI'], 'B')]


LINKS = {'A': ('KEY_A', 'alias'), 'B': ('KEY_B', 'alias')}


def _feats(**kw):
    by = kf.osda_experiments(_records(), LINKS)
    vocab = kf.framework_vocabulary(_records())
    base = dict(osda_keys=['KEY_A', 'KEY_A', None], dois=['d1', 'd9', 'd9'], years=[2006, 2004, 2006], by_osda=by, vocab=vocab)
    base.update(kw)
    return kf.recipe_features(**base), vocab


def col(f, name):
    return f[:, kf.FEATURE_NAMES.index(name)]


def test_own_paper_is_excluded_and_unknown_osda_is_finite():
    f, _ = _feats()
    assert col(f, 'kg_osda_n_experiments').tolist() == [2, 3, 0]   # recipe 0 is from d1, so x1 is not counted
    assert np.isfinite(f).all()
    assert col(f, 'kg_osda_median_temperature_c')[2] == -1


def test_evaluation_papers_are_removed_and_temporal_variant_uses_earlier_papers():
    f, _ = _feats(excluded_dois={'d3'})
    assert col(f, 'kg_osda_share_CHA').tolist()[:2] == [1.0, 1.0]
    f, _ = _feats(temporal=True)
    assert col(f, 'kg_osda_n_experiments').tolist() == [1, 1, 0]   # 2006: d2 only (d1 is own); 2004: d1 only


def test_top_framework_index_and_shares():
    f, vocab = _feats()
    assert vocab[int(col(f, 'kg_osda_top_framework')[1])] == 'CHA'
    assert col(f, 'kg_osda_top_share')[1] == pytest.approx(2 / 3)
    assert col(f, 'kg_osda_share_small_pore')[1] == pytest.approx(1.0)
    assert col(f, 'kg_osda_fluoride_share')[1] == pytest.approx(1 / 3)


def test_shuffled_links_keep_counts_per_osda():
    recs = _records()
    real = kf.osda_experiments(recs, LINKS)
    shuf = kf.osda_experiments_shuffled(recs, LINKS, seed=1)
    assert {k: len(v) for k, v in real.items()} == {k: len(v) for k, v in shuf.items()}


# ---------------------------------------------------------------- KG facts

def _engine(**kw):
    recs = _records()
    for r in recs:
        r['heteroatoms'] = ['Ge'] if r['experiment'] == 'x3' else []
    return KgFactEngine(records=recs, links=LINKS, reagent_names={'A': ['TMAdaOH (TMAda+)'], 'B': ['TPAOH']},
                        osda_display={'KEY_A': 'trimethyladamantammonium', 'KEY_B': 'tetrapropylammonium'},
                        framework_names={'SSZ-13': 'CHA', 'zeolite': 'MOR'}, **kw)


def test_query_linking_and_rendering():
    e = _engine()
    osdas, fws, conds = e.link_query('Which zeolite does TMAda+ give? SSZ-13 in fluoride medium with germanium')
    assert osdas == ['KEY_A'] and fws == ['CHA'] and conds == ['fluoride medium', 'germanium in the gel']
    out = e.evidence(['TMAda+ products'], token_budget=500)
    assert out['items'][0]['text'].startswith('OSDA "trimethyladamantammonium"') and '3 KG synthesis experiments' in out['items'][0]['text']
    assert 'kg-node' not in out['context']


def test_facts_exclude_evaluation_papers_and_respect_budget():
    e = _engine(excluded_dois={'d1', 'd2'})
    text = e.evidence(['TMAda+'], token_budget=500)['context']
    assert '1 KG synthesis experiments' in text and 'AEI 100%' in text
    assert e.evidence(['TMAda+'], token_budget=5)['items'] == []


def test_flat_and_shuffled_variants():
    flat = _engine().evidence(['TMAda+'], token_budget=500, flat=True)['context']
    assert flat.count('Paper ') == 3 and '%' not in flat
    override = {('x1', 'A'): ('KEY_B', 'shuffled'), ('x2f', 'A'): ('KEY_B', 'shuffled'), ('x3', 'A'): ('KEY_B', 'shuffled'),
                ('x4', 'B'): ('KEY_A', 'shuffled'), ('x5', 'B'): ('KEY_A', 'shuffled')}
    shuffled = _engine(link_override=override).evidence(['TMAda+'], token_budget=500)['context']
    assert 'MFI 100%' in shuffled


# ---------------------------------------------------------------- generation

def _split(n=120, seed=0):
    rng = np.random.default_rng(seed)
    from catalysis_research.benchmarks import zeosyn as z
    env = {k: rng.random(n) for k in z.raw_input_names()}
    d0 = np.column_stack([env[k] for k in z.GEL_INPUTS + z.CONDITION_INPUTS] + [rng.random(n) for _ in z.NATIVE_OSDA_D0])
    y = np.where(env['Si'] > 0.5, 'MFI', 'FAU').astype(str)
    kg = {f: rng.random(n) for f in kf.FEATURE_NAMES}
    return {'name': 'dev', 'train': np.arange(90), 'eval': np.arange(90, n), 'y': y, 'd0': d0, 'd0_names': list(z.D0),
            'env': env, 'kg_tables': {'kg': kg, 'kg_shuffled': {f: v[::-1].copy() for f, v in kg.items()}},
            'kg_variants': {'temporal': kg, 'external': kg}, 'osda_keys': ['K'] * n, 'excluded_dois': set()}


class FakeClient:
    def __init__(self, replies):
        self.replies, self.prompts = list(replies), []

    def chat_json(self, **kw):
        self.prompts.append(kw['user'])
        return GlmResponse(structured=self.replies.pop(0), raw={'id': f'r{len(self.prompts)}', 'choices': [{'finish_reason': 'stop'}]},
                           provider='fake', model='fake', usage={'prompt_tokens': 1, 'completion_tokens': 1})


def plan(queries=()):
    return {'plan': {'factor': 'OSDA literature prior', 'why': 'w', 'queries': list(queries)}}


def cand(formula, **kw):
    return {'descriptor': {'name': 'x', 'formula': formula, 'hypothesis': 'h', 'mechanism': 'm', 'target_frameworks': [],
                           'expected_effect': 'e', 'falsification': 'f', 'assumptions': 'a', 'evidence_ids': [],
                           'knowledge_source': 'both', 'novelty': 'uncertain', **kw}}


class FakeEvidence:
    def __init__(self):
        self.calls = []

    def __call__(self, queries):
        self.calls.append(queries)
        return {'items': [{'id': 1, 'key': 'osda:K', 'text': 'fact', 'tokens': 1}], 'context': '[1] fact', 'tokens': 1}


def test_kg_mode_can_use_literature_inputs_and_cite_evidence():
    cfg = v2.load_config(CONFIG)
    client = FakeClient([plan(['TMAda+']), cand('kg_osda_top_share * Si / (Al + 0.01)', evidence_ids=[1]),
                         plan([]), cand('kg_osda_share_CHA'), plan(['q']), cand('Na / (Al + 0.01)')])
    evid = FakeEvidence()
    g = v2.run_trajectory(config=cfg, mode='kg', replicate=1, split=_split(), evidence_provider=evid, client=client, log=lambda *_: None)
    assert g['appended'] == 3
    assert g['slots'][0]['candidate']['uses_kg_inputs'] == ['kg_osda_top_share']
    assert g['slots'][0]['candidate']['cited_evidence_keys'] == ['osda:K']
    assert evid.calls == [['TMAda+'], ['q']]                      # no retrieval when the plan asks for none
    assert 'Literature-prior inputs' in client.prompts[0] and 'EVIDENCE START' in client.prompts[1]
    assert v2.final_matrix(_split(), g).shape[1] == _split()['d0'].shape[1] + 3


def test_agent_cannot_use_literature_inputs_and_never_retrieves():
    cfg = v2.load_config(CONFIG)
    client = FakeClient([plan(['should be ignored']), cand('kg_osda_top_share'), cand('Si / (Al + 0.01)'),
                         plan([]), cand('Na / (Al + 0.01)'), plan([]), cand('K / (Al + 0.01)')])
    evid = FakeEvidence()
    g = v2.run_trajectory(config=cfg, mode='agent', replicate=1, split=_split(), evidence_provider=evid, client=client, log=lambda *_: None)
    assert evid.calls == []
    assert 'unsupported_input' in g['slots'][0]['attempts'][1]['error']   # repaired once
    assert g['appended'] == 3 and 'Literature-prior inputs' not in client.prompts[0]
    assert 'No external knowledge source' in client.prompts[0] and 'EVIDENCE START' not in client.prompts[1]


def test_shuffled_mode_uses_the_shuffled_table():
    s = _split()
    env = v2.env_for_mode(s, 'kg_shuffled')
    assert np.array_equal(env['kg_osda_top_share'], s['kg_tables']['kg_shuffled']['kg_osda_top_share'])
    assert 'kg_osda_top_share' not in v2.env_for_mode(s, 'rag')


def test_plan_normalization_caps_queries():
    p = v2.normalize_plan({'plan': {'factor': 'f', 'why': ['a', 'b'], 'queries': ['q1', 'q2', 'q3']}}, 2)
    assert p == {'factor': 'f', 'why': 'a\nb', 'queries': ['q1', 'q2']}
    assert v2.normalize_plan({'plan': {'factor': 'f', 'queries': 'one'}}, 2)['queries'] == ['one']
    with pytest.raises(ValueError):
        v2.normalize_plan({'plan': {'why': 'w'}}, 2)


class FakeRetriever:
    def retrieve(self, *, query, experiment_mode, budget):
        assert experiment_mode == 'rag_agent'
        return {'items': [{'record_id': 'c1', 'paper_id': 'p1', 'quote': 'gel with TPA gave MFI'},
                          {'record_id': 'c2', 'paper_id': 'p2', 'quote': 'long ' * 400}]}


def test_rag_evidence_merges_queries_deduplicates_and_keeps_budget():
    out = v2.RagEvidence(FakeRetriever(), budget=None, token_budget=50)(['a', 'b'])
    assert [i['key'] for i in out['items']] == ['c1'] and out['tokens'] <= 50


# ---------------------------------------------------------------- evaluation and statistics

def test_paired_strata_and_decision_rule():
    s = _split()
    s['osda_keys'] = ['A'] * 60 + ['B'] * 60
    masks = ev.stratum_masks(s)
    assert masks['osda_common_in_training'].sum() + masks['osda_rare_in_training'].sum() == 30
    yev = s['y'][s['eval']]
    base = [np.array(['FAU'] * 30, dtype=object)]
    better = [yev.astype(object)]
    d = ev.stratified_deltas(s, better, base)
    assert d['kg_covered']['n'] + d['kg_not_covered']['n'] == 30
    cfg = v2.load_config(CONFIG)
    mk = lambda mode, rep, gain: {'mode': mode, 'replicate': rep, 'appended': 1,
                                  'delta': {'mean': {m: gain for m in ev.METRICS}}, 'strata': d}
    evs = [mk('agent', r, 0.004) for r in range(1, 6)] + [mk('kg', r, 0.012 + r * 1e-4) for r in range(1, 6)]
    gens = [{'mode': e['mode'], 'replicate': e['replicate'], 'appended': 1, 'slots': []} for e in evs]
    out = ev.summarize({**cfg, 'modes': ['agent', 'kg'], 'replicates_per_mode': 5}, gens, evs, d0={}, library={})
    assert out['hypotheses']['H2_kg_vs_agent']['H2_supported'] is True
    assert out['hypotheses']['H1_agent_vs_d0']['supported'] is True


# ---------------------------------------------------------------- protocol

def test_test_split_needs_a_frozen_matching_preregistration(tmp_path, monkeypatch):
    import run_zeosyn_v2 as r
    doc = tmp_path / 'prereg.md'
    doc.write_text('final text')
    monkeypatch.setattr(r, 'ROOT', tmp_path)
    cfg = {'protocol': {'prereg': 'prereg.md', 'prereg_sha256': None, 'frozen': False}}
    assert not r.protocol_frozen(cfg)
    cfg['protocol'].update({'frozen': True, 'prereg_sha256': r.sha(doc)})
    assert r.protocol_frozen(cfg)
    doc.write_text('edited after freezing')
    assert not r.protocol_frozen(cfg)


def test_freeze_refuses_unconfirmed_items(tmp_path, monkeypatch):
    import run_zeosyn_v2 as r
    (tmp_path / 'p.md').write_text('primary metric: TO BE CONFIRMED')
    conf = tmp_path / 'c.json'
    conf.write_text(json.dumps({'protocol': {'prereg': 'p.md'}}))
    monkeypatch.setattr(r, 'ROOT', tmp_path)
    with pytest.raises(SystemExit, match='TO BE CONFIRMED'):
        r.cmd_freeze(type('A', (), {'config': str(conf)}))


def test_allowlist_rule():
    import run_zeosyn_v2 as r
    body = 'The gel was crystallized hydrothermally in a Teflon-lined autoclave at 150 C with TPAOH as template. ' * 3
    assert r.synthesis_score('Experimental', body) >= 2
    assert r.synthesis_score('Acknowledgements', body) == -1
    assert r.synthesis_score('Results', '<img src="imgs/a.jpg"> synthesis gel ' * 5) == -1
    assert r.synthesis_score('Results', 'Catalytic conversion of methanol over H-ZSM-5 at 450 C. ' * 5) < 2
