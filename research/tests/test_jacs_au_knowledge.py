"""Check scientific units, source scope, and connected graph provenance."""
from collections import defaultdict
import json
import unittest

import numpy as np

from catalysis_research.experiments.jacs_au import FEATURES
from catalysis_research.experiments.jacs_au_knowledge import (
    audit_dimensions, formula_environment, prepare_bank_rows, adaptive_query,
    select_evidence,
    load_budget_config,
)
from catalysis_research.retrieval import FrozenKgRetriever, RetrievalBudget, build_evidence_bundle
from catalysis_research.retrieval.bundle import count_tokens


class JacsKnowledgeTests(unittest.TestCase):
    def test_dimensional_logs_and_guards_are_rejected(self):
        for formula in ['log(Vol)', 'exp(-MW)', 'Vol + 1', 'maximum(lsd_p, .1)', 'PMI1 + MW', 'Sgas/MW', 'density/Vol']:
            with self.assertRaises(ValueError, msg=formula): audit_dimensions(formula)
        for formula in ['log(Vol / Vol_ref)', 'sqrt(PBF**2 + GeDi**2)',
                        'maximum(PBF, PBF_ref * 1e-6)', 'log(1 + q_Vol)', 'PMI1/PMI3']:
            self.assertEqual(audit_dimensions(formula)['status'], 'passed')

    def test_reference_values_ignore_score_and_test_rows(self):
        x = np.tile(np.arange(1, 6, dtype=float)[:, None], (1, len(FEATURES)))
        env, refs = formula_environment({'x': x}, np.array([0, 1, 2]))
        changed = x.copy(); changed[3:] = 1e9
        _, other = formula_environment({'x': changed}, np.array([0, 1, 2]))
        self.assertEqual(refs, other)
        np.testing.assert_allclose(env['q_MW'][:3], [.5, 1, 1.5])

    def _retriever(self):
        evidence = [{'document_id': 'doc:entropy', 'document_type': 'main', 'pdf_page_index': 2,
                     'quote': 'Molecular confinement in zeolite pores reduces rotational and translational adsorption entropy.',
                     'evidence_validation': 'exact'}]
        nodes = [
            {'id': 'shape', 'node_type': 'property', 'label': 'molecular shape', 'data': {}, 'evidence': []},
            {'id': 'experiment', 'node_type': 'experiment', 'label': 'adsorption experiment',
             'data': {'temperature': '298 K', 'material': 'protonic zeolite'}, 'evidence': []},
            {'id': 'entropy', 'node_type': 'observation', 'label': 'adsorption entropy', 'data': {}, 'evidence': evidence},
        ]
        edges = [
            {'id': 'e1', 'from_node_id': 'experiment', 'to_node_id': 'shape', 'edge_type': 'has_descriptor',
             'source_paper_id': 'paper:entropy', 'evidence': evidence},
            {'id': 'e2', 'from_node_id': 'experiment', 'to_node_id': 'entropy', 'edge_type': 'has_observation',
             'source_paper_id': 'paper:entropy', 'evidence': evidence},
        ]
        r = FrozenKgRetriever.__new__(FrozenKgRetriever)
        r.nodes = {n['id']: n for n in nodes}; r.edges = edges; r.adjacency = defaultdict(list)
        for edge in edges:
            r.adjacency[edge['from_node_id']].append(edge); r.adjacency[edge['to_node_id']].append(edge)
        return r

    def test_paths_preserve_direction_conditions_and_provenance_after_fusion(self):
        r = self._retriever()
        rows = r.retrieve(query='shape adsorption entropy', include_graph_semantics=True)
        paths = [p for row in rows for p in row['kg_paths'] if len(p['edges']) == 2]
        self.assertTrue(paths)
        for path in paths:
            node_ids = [n['id'] for n in path['nodes']]
            for i, edge in enumerate(path['edges']):
                self.assertEqual({edge['source'], edge['target']}, set(node_ids[i:i+2]))
                self.assertEqual(edge['source'], 'experiment')
                self.assertTrue(edge['evidence'])
            condition = next(n for n in path['nodes'] if n['id'] == 'experiment')
            self.assertEqual(condition['data']['temperature'], '298 K')
        bundle = build_evidence_bundle(query='entropy', mode='small_kg_rag', budget=RetrievalBudget(), kg_candidates=rows)
        self.assertTrue(any(row.get('kg_paths') for row in bundle['items']))
        self.assertEqual(r.retrieve(query='entropy', include_graph_semantics=True,
                                    excluded_paper_ids={'paper:entropy'}), [])

    def test_shared_node_quote_uses_document_source_and_excludes_that_paper(self):
        r = self._retriever()
        r.document_paper_ids = {'doc:entropy': 'paper:cited-document'}
        rows = r.retrieve(query='shape entropy', include_graph_semantics=True)
        self.assertTrue(rows)
        self.assertTrue(all(row['paper_id'] == 'paper:cited-document' for row in rows))
        self.assertEqual(r.retrieve(query='shape entropy', include_graph_semantics=True,
                                    excluded_paper_ids={'paper:cited-document'}), [])

    def test_pipeline_gate_blocks_wrong_citation_identity_and_disconnected_paths(self):
        import copy
        import importlib.util
        from pathlib import Path
        from catalysis_research.experiments.jacs_au_knowledge import PROFILE
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location('jacs_bank_audit', root/'scripts/audit_jacs_au_kg_v2_bank.py')
        gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
        config = root/'configs/experiments/jacs-au-kg-v2-pilot.json'
        kg, _ = prepare_bank_rows(self._retriever().retrieve(query='shape entropy', include_graph_semantics=True), 'kg', set())
        rag = [{**kg[0], 'channel': 'rag', 'graph_paths': [], 'record_id': 'rag:source'}]
        bank = {'profile':PROFILE,'status':'ready','budget_config':load_budget_config(config),
                'source_audit':{'excluded_paper_ids':[]},'kg':kg,'rag':rag,
                'eligible_counts':{'rag':len(rag),'kg':len(kg)},'paper_counts':{'rag':1,'kg':1}}
        self.assertEqual(gate.audit(bank,config,{'doc:entropy':'paper:entropy'})['status'],'passed')
        with self.assertRaisesRegex(ValueError,'attributed paper differ'):
            gate.audit(bank,config,{'doc:entropy':'paper:different'})
        broken = copy.deepcopy(bank)
        broken['kg'][0]['graph_paths'][0]['edges'][0]['source'] = 'unconnected-node'
        with self.assertRaisesRegex(ValueError,'Disconnected'):
            gate.audit(broken,config)

    def test_scope_filter_removes_known_failure_modes(self):
        def row(record, quote):
            return {'record_id': record, 'paper_id': 'paper:' + record, 'document_id': 'doc:' + record,
                    'quote': quote, 'page': 1}
        rows = [
            row('good', 'Confinement of adsorbed molecules in zeolite pores restricts rotational entropy and accessible volume.'),
            row('isotherm', 'The zeolite three angstrom pore adsorbent exhibits a type one adsorption isotherm in this experiment.'),
            row('water', 'Water reorganization in zeolite solvent pores raises entropy during epoxidation and catalytic turnover.'),
            row('table', 'FER 0.83 2.19 1.21 0.4'),
            row('excluded', 'Adsorption entropy in zeolite pores depends on confinement and molecular rotational freedom.'),
        ]
        eligible, rejected = prepare_bank_rows(rows, 'rag', {'paper:excluded'})
        self.assertEqual([r['record_id'] for r in eligible], ['good'])
        self.assertEqual(len(rejected), 4)

    def test_prompt_budget_counts_serialized_relations(self):
        kg, _ = prepare_bank_rows(self._retriever().retrieve(query='shape entropy', include_graph_semantics=True), 'kg', set())
        self.assertTrue(kg)
        bank = {'rag': [], 'kg': kg, 'active_round': 2}
        evidence, report = select_evidence(bank, 'small_kg_rag_agent', 'entropy', token_budget=1800)
        self.assertTrue(evidence)
        self.assertEqual(report['lexical_tokens'], count_tokens(json.dumps(evidence, ensure_ascii=False)))
        self.assertLessEqual(report['lexical_tokens'], 1800)
        self.assertTrue(all(e['id'].startswith('R2E') for e in evidence))
        self.assertTrue(any(e.get('graph_paths') for e in evidence))
        self.assertEqual(select_evidence(bank, 'agent', 'entropy')[0], [])

    def test_long_qualified_passages_are_preserved_under_configured_budget(self):
        from pathlib import Path
        from catalysis_research.experiments.jacs_au_knowledge import clean_excerpt, compact_paths
        quote = ('Adsorption entropy and rotational confinement in zeolite pores depend on molecular shape. ' * 50
                 + 'This conclusion applies only at infinite dilution in pure-silica rigid frameworks.')
        self.assertGreater(len(quote), 2400)
        self.assertEqual(clean_excerpt(quote), quote)
        retriever = self._retriever()
        retriever.edges[0]['evidence'][0]['quote'] = quote
        retriever.nodes['experiment']['data']['qualification'] = 'A' * 1000
        rows = retriever.retrieve(query='shape entropy', include_graph_semantics=True)
        kg, _ = prepare_bank_rows(rows, 'kg', set())
        evidence, report = select_evidence({'rag': [], 'kg': kg}, 'small_kg_rag_agent', 'entropy')
        self.assertTrue(any(e['quote'].endswith('rigid frameworks.') for e in evidence))
        self.assertTrue(any(edge['support'][0]['quote'] == quote
                            for e in evidence for p in e['graph_paths'] for edge in p['edges']))
        self.assertEqual(report['context_token_budget'], 32000)
        config = load_budget_config(Path(__file__).resolve().parents[1]/'configs/experiments/jacs-au-kg-v2-pilot.json')
        self.assertEqual(config['retrieval']['context_lexical_tokens'], 32000)
        self.assertEqual(config['generation']['max_tokens'], 16000)

    def test_adaptive_search_never_serializes_test_results(self):
        history = [{'candidates': [{'status': 'rejected', 'test_mae': 'HIDDEN_TEST_VALUE'}],
                    'test': 'HIDDEN_TEST_VALUE'}]
        query = adaptive_query(2, [{'formula': 'q_PBF * q_Vol'}], history, ['rotational restriction'])
        self.assertIn('planarity', query)
        self.assertIn('rotational restriction', query)
        self.assertNotIn('HIDDEN_TEST_VALUE', query)

    def test_closed_loop_profile_transfers_frozen_formulas_to_trees(self):
        import importlib.util
        from pathlib import Path
        import tempfile
        from types import SimpleNamespace
        from unittest.mock import patch
        from catalysis_research.experiments.jacs_au import make_split, metrics, save_json
        from catalysis_research.experiments.jacs_au_knowledge import PROFILE
        spec = importlib.util.spec_from_file_location('jacs_v2_integration', Path(__file__).resolve().parents[1]/'scripts/run_jacs_au.py')
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        rng = np.random.default_rng(5)
        x = rng.uniform(.2, 3, (3690, 14)); gas = rng.uniform(20, 40, 3690)
        ratio = rng.uniform(.6, .8, 3690)
        data = {'x': x, 'all_x': np.column_stack([x, gas]), 'gas': gas, 'ratio': ratio,
                'entropy': (1-ratio)*gas, 'categories': np.full(3690, 'alkane'),
                'order': rng.permutation(3690)}
        split = make_split(data); prompts = []; kinds = []; output_caps = []
        class FakeClient:
            def __init__(self, **kwargs): pass
            def chat_json(self, **kwargs):
                from catalysis_research.models.glm import GlmOutputTruncated
                output_caps.append(kwargs['max_tokens'])
                if len(output_caps) == 1:
                    raise GlmOutputTruncated({'completion_tokens': kwargs['max_tokens']})
                p = json.loads(kwargs['user']); prompts.append(p)
                citations = [p['evidence'][0]['id']] if p['evidence'] else []
                candidates = [dict(name=f'x{i}', formula=f, hypothesis='conditional geometry relation',
                                   rationale='requires physical verification', falsification_criteria='No scoring gain',
                                   novelty_status='uncertain', evidence_ids=citations)
                              for i, f in enumerate(['sqrt(q_MW)*q_Vol', 'log(1+q_PBF)', 'log(Vol)'])]
                return SimpleNamespace(structured={'descriptor_candidates': candidates,
                                                    'next_retrieval_queries': ['rotational confinement']},
                                       usage={}, model='glm-5.3-flash')
        def fake_fit(data, values, train, **kwargs):
            kinds.append(kwargs.get('kind', 'ann'))
            return data['ratio'] + .1/(values.shape[1]-13), .01
        kg, _ = prepare_bank_rows(self._retriever().retrieve(query='shape entropy', include_graph_semantics=True), 'kg', set())
        rag = [{**kg[0], 'channel': 'rag', 'graph_paths': [], 'record_id': 'rag:example'}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); base = root/'baseline'
            result_path = root/'discovery/small_kg_rag_agent-replicate-1.json'
            save_json(base/'baseline.json', {'status':'completed','epochs':4000,'controls':{
                k:{'score':metrics(data,split['score'],(ratio+.1)[split['score']])}
                for k in ['native14_ann','all_raw_ann','native14_hgb','all_raw_hgb']}})
            save_json(base/'reproduction.json', {'passed':True})
            save_json(base/'split.json', {k:v.tolist() for k,v in split.items()})
            for k in ['native14_ann','all_raw_ann','native14_hgb','all_raw_hgb']: np.save(base/(k+'.npy'),ratio+.1)
            save_json(root/'bank.json', {'profile':PROFILE,'status':'ready','source_audit':{'excluded_paper_ids':[]},'rag':rag,'kg':kg})
            with patch('catalysis_research.models.glm.GlmClient',FakeClient), patch.object(runner,'fit',fake_fit):
                runner.discover(data,base,None,result_path,'small_kg_rag_agent',1,knowledge_bank=root/'bank.json')
            result=json.loads(result_path.read_text())
            summary_spec=importlib.util.spec_from_file_location('jacs_v2_summary',Path(__file__).resolve().parents[1]/'scripts/analyze_jacs_au_kg_v2.py')
            summary_module=importlib.util.module_from_spec(summary_spec);summary_spec.loader.exec_module(summary_module)
            summary=summary_module.analyze(root,1)
            self.assertFalse(summary['complete'])
            self.assertEqual(summary['groups']['small_kg_rag_agent']['completed'],1)
            self.assertEqual(summary['groups']['agent']['completed'],0)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(len(result['evidence_by_round']),3)
        self.assertEqual(len(result['retained']),2)
        self.assertEqual(kinds.count('hgb'),2)
        self.assertTrue(result['test_is_development_diagnostic'])
        self.assertEqual(output_caps[:2], [16000, 32000])
        self.assertEqual(result['rounds'][0]['completion_attempts'][0]['finish_reason'], 'length')
        self.assertTrue(all(c['status']=='rejected' for r in result['rounds'] for c in r['candidates'] if c['formula']=='log(Vol)'))
        self.assertTrue(all('test' not in p and 'test_mae_R' not in json.dumps(p) for p in prompts))


if __name__ == '__main__': unittest.main()
