"""Regression tests for observed contamination and evidence-policy failures."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from catalysis_research.experiments.jacs_au_sources import (
    assert_clean, contamination_reason, exclusion_closure,
)
from catalysis_research.experiments.jacs_au_knowledge import audit_dimensions, formula_environment
from catalysis_research.experiments.jacs_au_kg_v3 import (
    audit_bank, build_bank, load_budget_config, pack_graph, unpack_graph,
    render_evidence, select_evidence, scientific_check, validate_scientific_test,
    adaptive_query,
)
from catalysis_research.experiments.jacs_au import FEATURES, make_split, metrics, save_json

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT/'configs/experiments/jacs-au-kg-v3-pilot.json'


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/file)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


def candidate(formula='q_Vol*q_GeDi', **overrides):
    result = dict(name='test', formula=formula, hypothesis='Conditional geometry association',
                  rationale='A geometric proxy, with limitations', falsification_criteria='Opposite direction in declared regime',
                  novelty_status='uncertain', evidence_ids=[], scientific_test={
                      'mechanism_family':'translation','proxy_assumptions':'No exact molecular free volume inferred',
                      'physical_interpretation':'Vol and GeDi retain their native meaning',
                      'vary_input':'Vol','descriptor_direction':'increasing','regime_input':'lsd_p',
                      'regime_train_quantiles':[0.,1.], 'entropy_direction':'increasing'})
    result['scientific_test'].update(overrides)
    return result


class V3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = module('v3_runner_test', 'run_jacs_au.py')
        old = json.loads((ROOT/'reports/jacs_au_kg_v2_20260929/evidence/bank.json').read_text(encoding='utf-8'))
        review = json.loads((ROOT/'configs/experiments/jacs-au-kg-v3-source-review.json').read_text(encoding='utf-8'))
        cls.bank = build_bank(old, review, load_budget_config(CONFIG))

    def test_aliases_and_nested_results_blocked_without_exclusion_list(self):
        for value in [
            {'paper_id':'pmc:PMC11672123'}, {'pmid':'39735916'},
            {'url':'https://doi.org/10.1021/jacsau.4c00429'},
            {'title':'Elucidating Thermodynamically Driven Structure–Property Relations for Zeolite Adsorption'},
            {'path': {'support': [{'quote':'lsd_f exhibits the strongest variation in Shapley values'}]}},
            {'support': [{'document_id':'document:1887d169511f36a3f2d23905'}]},
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError): assert_clean(value)
        assert_clean({'quote':'SHAP is a method for explaining a model; confinement can affect entropy.'})

    def test_feedback_queries_use_whitelist_not_heldout_fields(self):
        history=[{'candidates':[{**candidate(),'scientific_check':{'target_association':'contradicted'},
                                'test_mae':'SECRET_TEST_METRIC'}], 'test':'SECRET_TEST_METRIC'}]
        query=adaptive_query(2,[],history)
        self.assertIn('counterexample',query)
        self.assertNotIn('SECRET_TEST_METRIC',query)

    def test_identity_closure_includes_alias_documents_and_si(self):
        papers=[{'paper_id':'pmc:pmc11672123','title':'missing metadata'}]
        docs=[{'document_id':'unknown-main','paper_id':'pmc:pmc11672123'},
              {'document_id':'unknown-si','paper_id':'pmc:pmc11672123'},
              {'document_id':'document:1887d169511f36a3f2d23905','paper_id':'alias:new'},
              {'document_id':'alias-si','paper_id':'alias:new'}]
        ids, document_ids = exclusion_closure(papers, docs)
        self.assertIn('alias:new', ids)
        self.assertTrue({'unknown-main','unknown-si','alias-si'} <= document_ids)

    def test_contaminated_archived_bank_is_rejected(self):
        old=json.loads((ROOT/'reports/jacs_au_kg_v2_20260929/evidence/bank.json').read_text(encoding='utf-8'))
        with self.assertRaisesRegex(ValueError,'Benchmark evidence leakage'): assert_clean(old['rag'])
        self.assertEqual(sum(contamination_reason(row) is not None for row in old['rag']), 11)

    def test_audited_bank_removes_leak_and_unsafe_scope(self):
        audit_bank(self.bank)
        assert_clean(self.bank['rag']); assert_clean(self.bank['kg'])
        self.assertEqual(len(self.bank['kg']), 6)
        self.assertEqual(len({r['paper_id'] for r in self.bank['kg']}), 3)
        self.assertTrue(all(r['applicability']['transfer_assumptions'] for r in self.bank['kg']))
        bad=deepcopy(self.bank)
        bad['kg'][0]['graph_paths'][0]['edges'][0]['support'][0]['quote']='PMCID: PMC11672123'
        with self.assertRaises(ValueError): audit_bank(bad)
        bad=deepcopy(self.bank)
        bad['rag'][0]['applicability']['status']='background_unverified'
        with self.assertRaisesRegex(ValueError,'Unreviewed source'):audit_bank(bad)

    def test_identical_rag_anchors_and_graph_facts_in_both_views(self):
        for budget in (8000,32000):
            with self.subTest(budget=budget):
                rag,_=select_evidence(self.bank,'rag_agent','rotational confinement entropy',token_budget=budget)
                kg,report=select_evidence(self.bank,'small_kg_rag_agent','rotational confinement entropy',token_budget=budget)
                text,text_report=select_evidence(self.bank,'small_kg_rag_agent','rotational confinement entropy',token_budget=budget,graph_view='text')
                self.assertEqual(kg[:len(rag)],rag)
                self.assertEqual(kg,text)
                self.assertLessEqual(report['lexical_tokens'],budget)
                self.assertLessEqual(text_report['lexical_tokens'],budget)

    def test_dedup_keeps_conflicting_versions_conditions_and_support(self):
        items,_=select_evidence(self.bank,'small_kg_rag_agent','entropy')
        repeated=deepcopy(items+items)
        # Even same source IDs with different qualification objects must survive.
        graph_item=next(x for x in repeated if x['graph_paths'])
        graph_item['graph_paths'][0]['edges'][0]['extra_condition']='Only at 298 K'
        packed=pack_graph(repeated)
        self.assertEqual(unpack_graph(packed),repeated)
        self.assertTrue(any(e.get('extra_condition')=='Only at 298 K' for e in packed['edges'].values()))
        flat=render_evidence(repeated,'text')
        self.assertEqual(len(flat['edges']),len(packed['edges']))

    def test_constant_fraction_exponents_and_invalid_exponents(self):
        self.assertEqual(audit_dimensions('Vol**(1/3)')['output_dimensions'],{'length':'1'})
        audit_dimensions('q_Vol**(-2/3)')
        for formula in ['Vol**(1/0)','Vol**q_MW','Vol**(9/1)','Vol**sqrt(1)']:
            with self.subTest(formula=formula),self.assertRaises(ValueError):audit_dimensions(formula)

    def test_scientific_checks_do_not_read_heldout_inputs_or_labels(self):
        rng=np.random.default_rng(21)
        x=rng.uniform(.1,5,(300,14)); train=np.arange(200)
        env,_=formula_environment({'x':x},train)
        entropy=x[:,8]*x[:,7]
        actual=scientific_check(candidate(),env,train,entropy,self.runner.evaluate_formula)
        self.assertEqual(actual['target_association'],'consistent')
        x[200:]=1e9;entropy[200:]=-1e100
        changed,_=formula_environment({'x':x},train)
        self.assertEqual(actual,scientific_check(candidate(),changed,train,entropy,self.runner.evaluate_formula))
        self.assertFalse(actual['mechanism_validated'])

    def test_false_proxy_direction_rejected_and_target_contradiction_reported(self):
        rng=np.random.default_rng(3); x=rng.uniform(.1,5,(250,14)); train=np.arange(250)
        env,_=formula_environment({'x':x},train);entropy=-x[:,8]*x[:,7]
        with self.assertRaisesRegex(ValueError,'contradicts'):
            scientific_check(candidate(descriptor_direction='decreasing'),env,train,entropy,self.runner.evaluate_formula)
        report=scientific_check(candidate(),env,train,entropy,self.runner.evaluate_formula)
        self.assertEqual(report['target_association'],'contradicted')
        self.assertFalse(report['mechanism_validated'])
        with self.assertRaises(ValueError):validate_scientific_test(candidate(regime_train_quantiles=[.01,.02]))

    def test_v3_closed_loop_uses_packed_evidence_and_scientific_feedback(self):
        rng=np.random.default_rng(7);x=rng.uniform(.2,3,(3690,14));gas=rng.uniform(20,40,3690)
        ratio=rng.uniform(.6,.8,3690)
        data={'x':x,'all_x':np.column_stack([x,gas]),'gas':gas,'ratio':ratio,'entropy':(1-ratio)*gas,
              'categories':np.full(3690,'alkane'),'order':rng.permutation(3690)}
        split=make_split(data);prompts=[]
        class FakeClient:
            def __init__(self,**kwargs):pass
            def chat_json(self,**kwargs):
                prompt=json.loads(kwargs['user']);prompts.append(prompt)
                cs=[candidate(),candidate('log(1+q_PBF)',vary_input='PBF',mechanism_family='shape'),candidate('log(Vol)')]
                for i,c in enumerate(cs):
                    c['name']=f'c{i}';c['evidence_ids']=[prompt['evidence']['items'][0]['id']]
                return SimpleNamespace(structured={'descriptor_candidates':cs,'next_retrieval_queries':[]},usage={},model='glm-5.3-flash',raw={'choices':[{'finish_reason':'stop'}]})
        def fake_fit(data,values,train,**kwargs):return data['ratio']+.1/(values.shape[1]-13),.01
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);base=root/'baseline';output=root/'discovery/kg.json'
            save_json(base/'baseline.json',{'status':'completed','epochs':4000,'controls':{k:{'score':metrics(data,split['score'],(ratio+.1)[split['score']])} for k in ['native14_ann','all_raw_ann','native14_hgb','all_raw_hgb']}})
            save_json(base/'reproduction.json',{'passed':True})
            save_json(base/'split.json',{k:v.tolist() for k,v in split.items()})
            for k in ['native14_ann','all_raw_ann','native14_hgb','all_raw_hgb']:np.save(base/(k+'.npy'),ratio+.1)
            save_json(root/'bank.json',self.bank)
            with patch('catalysis_research.models.glm.GlmClient',FakeClient),patch.object(self.runner,'fit',fake_fit):
                self.runner.discover(data,base,None,output,'small_kg_rag_agent',1,knowledge_bank=root/'bank.json',config_path=CONFIG)
            result=json.loads(output.read_text(encoding='utf-8'))
            summary=module('v3_summary_test','analyze_jacs_au_kg_v2.py').analyze(root,1)
            self.assertEqual(summary['profile'],'jacs-au-kg-v3')
        self.assertEqual(result['status'],'completed')
        self.assertEqual(result['knowledge_profile'],'jacs-au-kg-v3')
        self.assertEqual(len(result['rounds']),3)
        self.assertTrue(all('nodes' in p['evidence'] for p in prompts))
        self.assertTrue(any('scientific_check' in c for r in result['rounds'] for c in r['candidates']))
        self.assertIn('scientific_check',prompts[1]['previous_rounds'][0]['candidates'][0])
        self.assertTrue(all(not c['mechanism_validated'] for r in result['rounds'] for c in r['candidates']))


if __name__=='__main__':unittest.main()
