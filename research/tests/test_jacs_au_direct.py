"""Information isolation, direct append, science contracts and failure accounting."""
from copy import deepcopy
import inspect
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'scripts')]
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v4 import build_bank
from catalysis_research.experiments.jacs_au_direct import (
    ROLES, load_config, candidate_template, validate_candidate, precheck,
    technical_patch, frozen_knowledge, common_prompt, ScientificRevisionRequired, canonicalize_added_columns,
)
from catalysis_research.models.glm import GlmError, GlmMalformedJson
import run_jacs_au_direct as runner


def candidate(formula='log(1+q_Vol)', axis='Vol', direction='increasing', used=('Vol',)):
    c = candidate_template()
    c.update(name='empirical_volume', formula=formula, hypothesis='A conditional entropy-loss proxy hypothesis.',
             rationale='Empirical geometric proxy; not a new observation or validated causal mechanism.',
             falsification_criteria='Competing geometry or energy mechanism changes the conditional direction.',
             novelty_status='uncertain', proxy_assumptions='Native heavy-atom/probe proxies, no absolute free volume.',
             variable_mappings={k:ROLES[k] for k in used}, mechanism_family='translation', limit_tests=[])
    c['physical_prediction'] = {'vary_input':axis,'hold_fixed':[k for k in used if k != axis], 'loss_direction':direction}
    c['expression_check'] = {'vary_input':axis,'descriptor_direction':direction,'regime_input':'lsd_f','regime_train_quantiles':[0.,1.]}
    c['conditional_proxy_target_direction'] = 'increasing'
    c['boundary_behavior'] = 'Finite observed support without physical zero imputation.'
    return c


class Client:
    def __init__(self, callback=None):
        self.requests = []; self.callback = callback
    def chat_json(self, **kwargs):
        req = json.loads(kwargs['user']); self.requests.append(req)
        if self.callback: value = self.callback(req)
        elif req['task'].startswith('Preservation'): value = {'review_issues':[]}
        elif req['task'].startswith('ONE technical'): value = {'technical_patch':{}}
        else: value = {'descriptor_candidate':candidate()}
        raw = {'id':'response-'+str(len(self.requests)), 'model':'glm-5.3-flash',
               '_response_request_ids':{'x-request-id':'request-id'},
               'choices':[{'finish_reason':'stop','message':{'content':json.dumps(value)}}],
               'usage':{'prompt_tokens':10,'completion_tokens':5,'total_tokens':15}}
        return SimpleNamespace(structured=value, raw=raw, usage=raw['usage'], model=raw['model'])


class DirectTests(unittest.TestCase):
    def test_interruption_reuses_proposal_and_does_not_reset_failed_review_budget(self):
        data,split=self.data()
        def crash(req):
            if req['task'].startswith('Preservation'): raise RuntimeError('simulated process interruption')
            return {'descriptor_candidate':candidate()}
        with tempfile.TemporaryDirectory() as tmp:
            first=Path(tmp)/'original.json'; recovered=Path(tmp)/'recovered.json'
            with self.assertRaises(RuntimeError):
                runner.generate(data['x'],split['train'],self.knowledge,self.config,'agent',1,first,Client(crash))
            original=first.read_bytes(); client=Client()
            result=runner.generate(data['x'],split['train'],self.knowledge,self.config,'agent',1,recovered,client,resume_source=first)
            self.assertEqual(first.read_bytes(),original)
            self.assertEqual(len(client.requests),4)
            self.assertEqual(result['api_calls'],6)
            self.assertEqual(result['inherited_api_calls'],2)
            self.assertEqual(result['api_attempts_without_recorded_outcome'],1)
            self.assertEqual(result['successful_additions'],3)
            self.assertEqual(result['rounds'][0]['review_status'],'api_failure_draft_preserved')
            self.assertTrue(result['rounds'][0]['events'][0]['reused_recorded_response'])
            with self.assertRaises(ValueError):
                runner.generate(data['x'],split['train'],self.knowledge,self.config,'agent',2,Path(tmp)/'wrong-task.json',Client(),resume_source=first)

    @classmethod
    def setUpClass(cls):
        cls.config = load_config(ROOT/'configs/experiments/jacs-au-direct-v5-high.json')
        bank = json.loads((ROOT/'reports/jacs_au_kg_v3_repair_20260929/evidence-final/bank.json').read_text(encoding='utf-8'))
        cls.knowledge = frozen_knowledge(build_bank(bank), cls.config)

    def data(self):
        rng = np.random.default_rng(61)
        x = rng.uniform(.2,4,size=(120,14))
        split = {'train':np.arange(80),'score':np.arange(80,100),'test':np.arange(100,120)}
        data = {'x':x,'ratio':np.full(120,.75),'gas':np.ones(120),'entropy':np.full(120,.25),
                'uncertainty':np.ones(120)}
        return data, split

    def generate(self, data, split, client=None, mode='agent'):
        client = client or Client()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(runner,'fit',side_effect=AssertionError('Generation must never fit')):
                result = runner.generate(data['x'],split['train'],self.knowledge,self.config,mode,1,Path(tmp)/'generation.json',client)
        return result, client

    def test_sources_and_graph_flat_facts_identical_and_references_resolve(self):
        data,split=self.data(); env,_=formula_environment(data,split['train'])
        from catalysis_research.experiments.jacs_au_kg_v4 import training_domains
        domains=training_domains(env,split['train'])
        rag=common_prompt(domains,[],1,'rag_agent',self.knowledge)
        kg=common_prompt(domains,[],1,'small_kg_rag_agent',self.knowledge)
        self.assertEqual(rag['evidence'],kg['evidence'])
        rebuilt={}
        for f in rag['knowledge_relations']['node_facts']:
            rebuilt.setdefault(f['node_id'],{})[f['property']]=f['value']
        self.assertEqual(rebuilt,kg['knowledge_relations']['nodes'])
        self.assertEqual(rag['knowledge_relations']['relation_facts'],kg['knowledge_relations']['edges'])
        self.assertNotIn('executed_checks',kg['knowledge_relations'])
        for node in rebuilt.values():
            if 'conditions_ref' in node:
                self.assertIn(node['conditions_ref'].split('.')[-1],kg['evidence']['source_conditions'])
        self.assertNotIn('evidence',common_prompt(domains,[],1,'agent',self.knowledge))

    def test_target_permutation_and_history_scores_do_not_change_requests(self):
        data,split=self.data(); a,client_a=self.generate(data,split)
        modified=deepcopy(data)
        for key in ('ratio','entropy','gas','uncertainty'): modified[key]=np.arange(120,dtype=float)[::-1]
        b,client_b=self.generate(modified,split)
        self.assertEqual(client_a.requests,client_b.requests)
        self.assertEqual(a['appended'],b['appended'])
        for p in inspect.signature(precheck).parameters: self.assertNotIn(p,('entropy','ratio','gas'))
        row=deepcopy(a['rounds'][0]); row['after_mae_R']=999; row['training_spearman']=-1
        self.assertEqual(common_prompt(a['training_feature_domains'],[row],2,'agent',self.knowledge),
                         common_prompt(a['training_feature_domains'],a['rounds'][:1],2,'agent',self.knowledge))

    def test_predictor_sign_rule_is_affine_invariant_and_training_only(self):
        values=np.array([3.,1.,7.,4.,2.,-9.]); train=np.array([1,3,0,2])
        a,meta_a=canonicalize_added_columns([values],train)
        b,meta_b=canonicalize_added_columns([-values],train)
        c,meta_c=canonicalize_added_columns([-2.5*values+11.],train)
        np.testing.assert_allclose(a[0],b[0],atol=1e-12)
        np.testing.assert_allclose(a[0],c[0],atol=1e-12)
        changed=values.copy(); changed[4:]=[1000.,-5000.]
        _,meta_d=canonicalize_added_columns([changed],train)
        self.assertEqual(meta_a,meta_d)
        self.assertFalse(meta_a[0]['labels_or_scoring_used'])
        self.assertTrue(meta_a[0]['scientific_expression_unchanged'])

    def test_canonicalization_keeps_reference_symbols_independent(self):
        with self.assertRaises(ScientificRevisionRequired):
            technical_patch(candidate('q_Vol**2'),{'technical_patch':{'formula':'Vol**2'}})

    def test_worse_scores_do_not_remove_any_of_three_direct_additions(self):
        data,split=self.data(); frozen,client=self.generate(data,split)
        self.assertEqual(frozen['successful_additions'],3)
        self.assertEqual(frozen['input_count'],17)
        self.assertFalse(frozen['scoring_performed'])
        self.assertEqual(len(client.requests),6)
        self.assertEqual(frozen['rounds'][2]['syntax_duplicate_prior_rounds'],[1,2])
        calls=[]
        def fit(data,x,train,**kwargs):
            calls.append((x.shape[1],kwargs['seed']))
            return np.full(120,.4),.01
        baselines={seed:np.full(120,.72) for seed in [3,7,11,17,23]}
        result=runner.evaluate(data,split,frozen,baselines,fit)
        self.assertLess(result['mean_gain_pct'],0)
        self.assertEqual(calls,[(17,s) for s in [3,7,11,17,23]])
        self.assertEqual(frozen['successful_additions'],3)

    def test_scoring_rejects_unfrozen_or_tampered_provenance_before_fit(self):
        data,split=self.data(); frozen,_=self.generate(data,split)
        broken=deepcopy(frozen); broken['status']='generating'
        with self.assertRaisesRegex(ValueError,'frozen'):
            runner.evaluate(data,split,broken,{},lambda *args,**kw:self.fail('Must not fit'))
        broken=deepcopy(frozen); broken['appended'][0]['formula']='q_MW'
        with self.assertRaisesRegex(ValueError,'provenance'):
            runner.evaluate(data,split,broken,{},lambda *args,**kw:self.fail('Must not fit'))

    def test_fitting_failure_uses_explicit_predictions_and_all_seeds(self):
        data,split=self.data(); frozen,_=self.generate(data,split)
        baselines={seed:np.full(120,.72) for seed in [3,7,11,17,23]}
        def fail(*args,**kw): raise ValueError('Synthetic numerical failure')
        result=runner.evaluate(data,split,frozen,baselines,fail)
        self.assertEqual(result['fallbacks'],5)
        self.assertEqual(result['mean_gain_pct'],0)
        self.assertTrue(all(s['status']=='explicit_d0_prediction_fallback' and s['failure_reason'] for s in result['seeds']))
        del baselines[23]
        with self.assertRaisesRegex(ValueError,'baseline'):
            runner.evaluate(data,split,frozen,baselines,fail)

    def test_formula_and_metadata_repair_cannot_replace_physics(self):
        c=candidate('log(1+q_Vol/q_lsd_f)','lsd_f','decreasing',('Vol','lsd_f'))
        with self.assertRaises(ScientificRevisionRequired):
            technical_patch(c,{'technical_patch':{'formula':'log(1+q_Vol*q_lsd_f)'}})
        with self.assertRaises(ScientificRevisionRequired):
            technical_patch(c,{'technical_patch':{'formula':'log(1+q_Vol/q_lsd_p)'}})
        with self.assertRaises(ScientificRevisionRequired):
            technical_patch(c,{'technical_patch':{'hypothesis':'changed'}})
        valid=technical_patch(c,{'technical_patch':{'formula':'log(1+(Vol/Vol_ref)/(lsd_f/lsd_f_ref))'}})
        self.assertEqual(valid['physical_prediction'],c['physical_prediction'])
        self.assertEqual(valid['hypothesis'],c['hypothesis'])
        bad=candidate(); bad['expression_check']['descriptor_direction']='decreasing'
        repaired=technical_patch(bad,{'technical_patch':{'descriptor_direction':'increasing'}})
        self.assertEqual(repaired['formula'],bad['formula'])
        self.assertEqual(repaired['physical_prediction'],bad['physical_prediction'])
        data,split=self.data(); env,_=formula_environment(data,split['train'])
        self.assertEqual(precheck(repaired,env,split['train'])['status'],'passed')

    def test_structured_wrong_log2_limit_is_scientific_failure_not_label_test(self):
        data,split=self.data(); env,_=formula_environment(data,split['train'])
        c=candidate('log(1+q_Vol/(0.1+q_AV))','AV','decreasing',('Vol','AV'))
        c['limit_tests']=[{'vary_input':'AV','approach':'positive_infinity','expected_value':float(np.log(2))}]
        check=precheck(c,env,split['train'])
        self.assertEqual(check['status'],'passed')
        self.assertEqual(check['scientific_consistency'],'failed')
        self.assertEqual(check['structured_limit_checks'][0]['computed_limit'],'0')
        c['limit_tests'][0]['expected_value']=0
        self.assertEqual(precheck(c,env,split['train'])['structured_limit_checks'][0]['status'],'passed')

    def test_single_slot_cannot_become_three_candidates(self):
        with self.assertRaisesRegex(ValueError,'one descriptor_candidate'):
            validate_candidate({'descriptor_candidates':[candidate(),candidate(),candidate()]})

    def test_scientific_replacement_is_not_resampled_as_format_error(self):
        events=[]; client=Client(lambda req:{'technical_patch':{'formula':'log(1+q_MW)'}})
        with self.assertRaises(GlmError):
            runner.ask(client,{'task':'one repair'},self.config,'technical_repair',events,lambda:None,
                       lambda value:technical_patch(candidate(),value))
        self.assertEqual(len(client.requests),1)
        self.assertEqual(events[0]['api_calls'],1)

    def test_structure_recovery_cannot_overwrite_existing_hypothesis_or_formula(self):
        first=candidate(); del first['novelty_status']
        second=candidate('log(1+q_MW)','MW','increasing',('MW',))
        outputs=iter([{'descriptor_candidate':first},{'descriptor_candidate':second}])
        client=Client(lambda req:next(outputs)); events=[]
        with self.assertRaises(GlmError):
            runner.ask(client,{'task':'proposal'},self.config,'proposal',events,lambda:None,validate_candidate)
        self.assertEqual(len(client.requests),2)
        self.assertIn('changed an already recorded',events[0]['attempts'][-1]['scientific_revision_rejected'])

    def test_no_infinite_replacement_after_invalid_slots(self):
        data,split=self.data(); data['x'][:80,11]=0; data['x'][70:80,11]=1
        bad=candidate('log(q_AV)','AV','increasing',('AV',))
        def callback(req):
            if req['task'].startswith('Preservation'): return {'review_issues':[]}
            if req['task'].startswith('ONE technical'): return {'technical_patch':{}}
            return {'descriptor_candidate':bad}
        frozen,client=self.generate(data,split,Client(callback))
        self.assertEqual(frozen['successful_additions'],0)
        self.assertEqual(len(client.requests),9)
        self.assertEqual(sum(e['stage']=='technical_repair' for r in frozen['rounds'] for e in r['events']),3)

    def test_raw_malformed_usage_and_ids_survive_bounded_format_recovery(self):
        raw={'id':'bad-response','model':'glm-5.3-flash','_response_request_ids':{'x-request-id':'bad-id'},
             'choices':[{'finish_reason':'stop','message':{'content':'{} {}'}}],'usage':{'total_tokens':7}}
        class Malformed(Client):
            def chat_json(self,**kw):
                if not self.requests:
                    self.requests.append(json.loads(kw['user']))
                    raise GlmMalformedJson(raw,'multiple JSON objects')
                return super().chat_json(**kw)
        client=Malformed(); events=[]
        runner.ask(client,{'task':'proposal'},self.config,'proposal',events,lambda:None,lambda x:x)
        self.assertEqual(events[0]['api_calls'],2)
        self.assertEqual(events[0]['attempts'][0]['response_id'],'bad-response')
        self.assertEqual(events[0]['attempts'][0]['raw_content'],'{} {}')
        self.assertEqual(events[0]['attempts'][0]['usage']['total_tokens'],7)


if __name__=='__main__':
    unittest.main()
