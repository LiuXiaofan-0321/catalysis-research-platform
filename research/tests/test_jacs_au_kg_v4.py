"""Observed-domain, source-boundary and low/high execution regressions."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import numpy as np

from catalysis_research.experiments.jacs_au import FEATURES, make_split, metrics, save_json
from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v4 import (
    ROLES, build_bank, training_domains, evaluate_formula, audit_formula, grounding_check,
    precheck, rotor_classes, scientific_graph, graph_paths_for, select_evidence, pack_evidence,
    FullIndexEvidence, load_config, validate_candidates,
)
ROOT=Path(__file__).resolve().parents[1]


def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


def candidate(formula='log(1+q_Vol)',slot='h1',family='translation',vary='Vol'):
    return {'slot_id':slot,'name':slot,'formula':formula,'hypothesis':'A fixed falsifiable proxy hypothesis '+slot,
            'rationale':'Empirical proxy, no causal or absolute free-volume claim','falsification_criteria':'Opposite declared association',
            'novelty_status':'uncertain','evidence_ids':[],'physical_claims':['empirical_proxy'],'variable_mappings':dict(ROLES),
            'scientific_test':{'mechanism_family':family,'proxy_assumptions':'Native heavy-atom geometric proxies only',
                'physical_interpretation':'Use native measured proxy meanings','boundary_behavior':'Finite single-site limit, not true atom inertia',
                'vary_input':vary,'descriptor_direction':'increasing','regime_input':'lsd_p',
                'regime_train_quantiles':[0.,1.],'entropy_direction':'increasing'}}


class V4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank=build_bank(json.loads((ROOT/'reports/jacs_au_kg_v3_repair_20260929/evidence-final/bank.json').read_text(encoding='utf-8')))
        cls.runner=module('v4_test_runner','run_jacs_au_kg_v4.py')

    def data(self,n=300):
        rng=np.random.default_rng(31);x=rng.uniform(.2,4,(n,14))
        x[:12,3:6]=0;x[:12,6:8]=0;x[:18,3]=0;x[:4,11]=0
        return {'x':x},np.arange(n)

    def test_domains_are_training_only_and_preserve_real_zeros(self):
        data,tr=self.data();tr=tr[:200];env,_=formula_environment(data,tr)
        expected=training_domains(env,tr)
        data['x'][200:]=1e90;changed,_=formula_environment(data,tr)
        self.assertEqual(expected,training_domains(changed,tr))
        self.assertEqual(expected['inputs']['PMI3']['zero_n'],12)
        self.assertEqual(expected['rotor_proxy_counts'],{'single_site':12,'linear':6,'nonlinear':182})

    def test_native_zero_log_rejected_and_explicit_rotor_branches_pass(self):
        data,tr=self.data();env,_=formula_environment(data,tr);entropy=data['x'][:,5]
        bad=candidate('log(q_PMI3)',family='rotation',vary='PMI3')
        r=precheck(bad,env,tr,entropy,data['x'])
        self.assertEqual(r['status'],'rejected');self.assertEqual(r['domain_failure']['invalid_n'],12)
        good=candidate('rotor_case(0, log(q_PMI2), log(q_PMI3))',family='rotation',vary='PMI3')
        r=precheck(good,env,tr,entropy,data['x'])
        self.assertEqual(r['status'],'passed')
        values=evaluate_formula(good['formula'],env)
        self.assertTrue(np.isfinite(values).all());self.assertTrue((values[:12]==0).all())
        self.assertEqual(audit_formula(good['formula'])['output_dimensions'],{})
        with self.assertRaises(ValueError):audit_formula('rotor_case(0, PMI2, Vol)')

    def test_role_and_derivative_failures_are_not_silently_repaired(self):
        data,tr=self.data();env,_=formula_environment(data,tr)
        c=candidate('q_lsd_f/q_lsd_p',vary='lsd_f');c['variable_mappings']['lsd_f']='cavity_Di'
        with self.assertRaisesRegex(ValueError,'mapping'):grounding_check(c)
        c=candidate();c['scientific_test']['descriptor_direction']='decreasing'
        report=precheck(c,env,tr,data['x'][:,8],data['x'])
        self.assertEqual(report['status'],'rejected');self.assertIn('direction',report['reason'])
        c=candidate('log(q_PMI3)',family='rotation',vary='PMI3');c['physical_claims']=['nonlinear_rotor_expression']
        with self.assertRaisesRegex(ValueError,'branches'):grounding_check(c)

    def test_partial_derivative_and_association_ignore_heldout_features_labels(self):
        data,tr=self.data();tr=tr[:200];env,_=formula_environment(data,tr);entropy=data['x'][:,8].copy()
        a=precheck(candidate(),env,tr,entropy,data['x'])
        data['x'][200:]=1e99;entropy[200:]=-1e99;changed,_=formula_environment(data,tr)
        self.assertEqual(a,precheck(candidate(),changed,tr,entropy,data['x']))

    def test_same_evidence_facts_and_shared_quantity_graph_no_quote_duplicates(self):
        c=load_config(ROOT/'configs/experiments/jacs-au-kg-v4-low.json')
        cs=[candidate()];e,t=select_evidence(self.bank,cs,[],c)
        self.assertEqual(len(e['items']),len({(x['paper_id'],x['document_id'],x['quote']) for x in e['items']}))
        packed=pack_evidence(e)
        self.assertEqual([x['quote'] for x in e['items']],[x['quote'] for x in packed['items']])
        self.assertTrue(all('applicability_ref' in x for x in packed['items']))
        graph=scientific_graph(self.bank);paths=graph_paths_for([candidate('q_PMI2*q_lsd_f',vary='PMI2')],graph)
        self.assertIn('lsd_f',paths['nodes']);self.assertIn('definition_ref',paths['nodes']['lsd_f'])
        self.assertGreater(sum(e['to']=='lsd_f' for e in graph['edges']),1)

    def test_full_index_rejects_benchmark_and_logs_unknown_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);paper=self.bank['rag'][0]['paper_id']
            files={'papers.jsonl':[{'paper_id':paper},{'paper_id':'pmc:pmc11672123'},{'paper_id':'unknown'}],
                   'documents.jsonl':[{'paper_id':paper,'document_id':'clean'},{'paper_id':'pmc:pmc11672123','document_id':'bad'}],
                   'chunks.jsonl':[{'record_id':'fresh','paper_id':paper,'document_id':'clean','text':'Adsorption entropy and rotational freedom under zeolite confinement require separate geometric proxy assumptions.'},
                                  {'record_id':'leak','paper_id':'pmc:pmc11672123','document_id':'bad','text':'Adsorption entropy in zeolites.'},
                                  {'record_id':'unknown','paper_id':'unknown','document_id':'unknown','text':'Adsorption entropy and rotational freedom in zeolite confinement differ across pore shapes and conditions.'}],
                   'evidence_records.jsonl':[]}
            for name,rows in files.items():p.joinpath(name).write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
            live=FullIndexEvidence(p,self.bank);rows,trace=live.search('rotational freedom entropy')
            self.assertEqual([r['record_id'] for r in rows],['fresh'])
            self.assertEqual(trace['pending_source_review'][0]['record_id'],'unknown')

    def test_locked_repair_cannot_replace_hypothesis_or_modify_passed_slot(self):
        a=[candidate(),candidate(slot='h2',family='shape'),candidate(slot='h3',family='rotation')]
        b=deepcopy(a);b[0]['hypothesis']='Different scientific hypothesis'
        with self.assertRaisesRegex(ValueError,'preserve'):self.runner.locked_revision(a,b)
        b=deepcopy(a);b[0]['scientific_test']['entropy_direction']='decreasing'
        with self.assertRaises(ValueError):self.runner.locked_revision(a,b)
        b=deepcopy(a);b[0]['scientific_test']['regime_train_quantiles']=[.5,1]
        with self.assertRaisesRegex(ValueError,'Repair'):self.runner.locked_revision(a,b,strict=True)

    def test_full_low_high_flow_uses_config_and_preserves_scoring_best(self):
        rng=np.random.default_rng(7);x=rng.uniform(.2,4,(3690,14));x[:100,3:6]=0
        gas=rng.uniform(20,40,3690);ratio=rng.uniform(.6,.8,3690)
        data={'x':x,'all_x':np.column_stack([x,gas]),'gas':gas,'ratio':ratio,'entropy':(1-ratio)*gas,
              'categories':np.full(3690,'alkane'),'order':rng.permutation(3690)}
        split=make_split(data);calls=[]
        class Client:
            def __init__(self,**kw):calls.append(('timeout',kw['timeout_seconds']))
            def chat_json(self,**kw):
                req=json.loads(kw['user']);calls.append((kw['reasoning_effort'],kw['max_tokens']))
                if req['task'].startswith('Propose'):
                    rd=req['round'];cs=[candidate(f'log(q_PMI3)*q_Vol**{rd}',family='rotation',vary='PMI3'),
                        candidate(f'log(1+q_PBF*q_Vol**{rd})',slot='h2',family='shape',vary='PBF'),
                        candidate(f'(q_lsd_p/q_lsd_f)*q_Vol**{rd}',slot='h3',family='connectivity',vary='lsd_p')]
                    structured={'descriptor_candidates':cs}
                elif req['task'].startswith('Review'):
                    structured={'candidate_patches':[{'slot_id':c['slot_id']} for c in req['drafts']]}
                else:
                    cs=deepcopy(req['candidates']);power=cs[0]['formula'].split('**')[-1]
                    structured={'candidate_patches':[{'slot_id':'h1','formula':f'rotor_case(0,log(q_PMI2)*q_Vol**{power},log(q_PMI3)*q_Vol**{power})'}]}
                return SimpleNamespace(structured=structured,usage={'prompt_tokens':50,'completion_tokens':80,'total_tokens':130},
                    model='glm-5.3-flash',raw={'choices':[{'finish_reason':'stop'}]})
        def fake_fit(data,values,train,**kw):return data['ratio']+.1/(values.shape[1]-13),.01
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);base=p/'baseline';initial=ratio+.1
            save_json(base/'baseline.json',{'status':'completed','epochs':4000,'controls':{k:{'score':metrics(data,split['score'],initial[split['score']])} for k in ['native14_ann','native14_hgb','all_raw_hgb']}})
            save_json(base/'reproduction.json',{'passed':True});save_json(base/'split.json',{k:v.tolist() for k,v in split.items()})
            for k in ['native14_ann','native14_hgb','all_raw_hgb']:np.save(base/(k+'.npy'),initial)
            save_json(p/'bank.json',self.bank)
            for effort in ['low','high']:
                c=load_config(ROOT/f'configs/experiments/jacs-au-kg-v4-{effort}.json');c['require_live_index']=False
                save_json(p/(effort+'.json'),c)
                result=self.runner.discover(data,base,p/'bank.json',p/(effort+'.json'),p/effort/'discovery/agent-replicate-1.json','agent',1,
                                             client_factory=Client,fit_function=fake_fit)
                self.assertEqual(result['status'],'completed');self.assertEqual(len(result['rounds']),3)
                self.assertEqual(result['api_calls'],9)
                self.assertTrue(all(rd['after_mae_R']<=rd['before_mae_R'] for rd in result['rounds']))
                self.assertTrue(all(len(rd['candidates'])==3 for rd in result['rounds']))
                if effort=='low':
                    failed=deepcopy(result);failed['status']='failed';failed['rounds']=failed['rounds'][:2]
                    failed['active_round']=deepcopy(result['rounds'][2]);failed['active_round']['generation_events']=failed['active_round']['generation_events'][:1]
                    save_json(p/'failed.json',failed);before=len(calls)
                    recovered=self.runner.discover(data,base,p/'bank.json',p/(effort+'.json'),p/'recovered.json','agent',1,
                        client_factory=Client,fit_function=fake_fit,resume_source=p/'failed.json')
                    self.assertEqual(len(calls)-before,3) # Client construction + review + pre-fit repair.
                    self.assertEqual(recovered['score_improvement_pct'],result['score_improvement_pct'])
                    self.assertEqual(recovered['recovery']['replayed_stages'],7)
            summary=module('v4_summary_test','summarize_jacs_au_kg_v4.py').summarize(p,1)
            self.assertFalse(summary['complete'])
        self.assertIn(('high',65536),calls);self.assertIn(('low',32768),calls)
        self.assertIn(('timeout',1800),calls)

    def test_partial_updates_preserve_hypotheses_and_passed_slots(self):
        cs=[candidate(),candidate(slot='h2',family='shape'),candidate(slot='h3',family='rotation')]
        patched=self.runner.apply_patches(cs,{'candidate_patches':[{'slot_id':'h1','formula':'log(1+q_Vol**2)'}]},['h1'],strict=True)
        self.assertEqual(patched[0]['hypothesis'],cs[0]['hypothesis'])
        self.assertEqual(patched[0]['scientific_test'],cs[0]['scientific_test'])
        self.assertEqual(patched[1:],cs[1:])
        with self.assertRaisesRegex(ValueError,'locked'):
            self.runner.apply_patches(cs,{'candidate_patches':[{'slot_id':'h1','hypothesis':'A paraphrase'}]},['h1'])
        with self.assertRaisesRegex(ValueError,'locked'):
            self.runner.apply_patches(cs,{'candidate_patches':[{'slot_id':'h1','scientific_test':{'entropy_direction':'decreasing'}}]},['h1'])
        with self.assertRaisesRegex(ValueError,'slots'):
            self.runner.apply_patches(cs,{'candidate_patches':[{'slot_id':'h2','formula':'log(q_PMI3)'}]},['h1'],strict=True)

    def test_format_recovery_is_bounded_and_checkpoint_replay_makes_no_call(self):
        from catalysis_research.models.glm import GlmMalformedJson
        payload={'task':'fixed slots'};events=[];calls=[]
        raw={'model':'glm-5.3-flash','choices':[{'finish_reason':'stop','message':{'content':'{} {}'}}],'usage':{'total_tokens':7}}
        class Client:
            def chat_json(self,**kw):
                calls.append(kw)
                if len(calls)==1:raise GlmMalformedJson(raw,'GLM returned malformed JSON')
                return SimpleNamespace(model='glm-5.3-flash',structured={'candidate_patches':[]},usage={'total_tokens':9},raw={'choices':[{'finish_reason':'stop','message':{'content':'{"candidate_patches":[]}'}}]})
        config=load_config(ROOT/'configs/experiments/jacs-au-kg-v4-low.json')
        self.assertEqual(self.runner.ask(Client(),payload,config,'review',events,lambda v:v),{'candidate_patches':[]})
        self.assertEqual(events[0]['attempts'][0]['raw_content'],'{} {}')
        self.assertEqual(len(calls),2)
        replay=[]
        self.runner.ask(Client(),payload,config,'review',replay,lambda v:v,replay_event=events[0])
        self.assertEqual(len(calls),2)
        self.assertTrue(replay[0]['replayed_from_checkpoint'])
        with self.assertRaisesRegex(ValueError,'differs'):
            self.runner.ask(Client(),{'task':'changed'},config,'review',[],lambda v:v,replay_event=events[0])
        class AlwaysBad:
            def chat_json(self,**kw):raise GlmMalformedJson(raw,'malformed')
        failed=[]
        with self.assertRaises(GlmMalformedJson):self.runner.ask(AlwaysBad(),payload,config,'review',failed,lambda v:v)
        self.assertEqual(len(failed[0]['attempts']),2)

    def test_decorated_claim_types_do_not_reject_valid_math_or_lose_annotations(self):
        cs=[candidate(),candidate(slot='h2',family='shape'),candidate('rotor_case(0,log(1+q_PMI2),log(1+q_PMI3))',slot='h3',family='rotation',vary='PMI3')]
        cs[2]['physical_claims']=['empirical_proxy: normalized inertia proxy','nonlinear_rotor_expression: dimensionless branches','rotor_case branches: explicit native categories']
        result=validate_candidates({'descriptor_candidates':cs})
        self.assertEqual(result[2]['physical_claims'],['empirical_proxy','nonlinear_rotor_expression'])
        self.assertEqual(result[2]['physical_claims_original'],cs[2]['physical_claims'])
        self.assertEqual(len(result[2]['physical_claim_annotations']),3)
        grounding_check(result[2])
        bad=deepcopy(cs);bad[2]['physical_claims']=['proven_causal_law']
        with self.assertRaisesRegex(ValueError,'Unsupported'):validate_candidates({'descriptor_candidates':bad})

    def test_q_definition_is_explicit_and_native_over_q_is_rejected_as_constant(self):
        data,tr=self.data();env,_=formula_environment(data,tr)
        c=candidate('Vol/q_Vol')
        self.assertIn('Constant',precheck(c,env,tr,data['x'][:,8],data['x'])['reason'])
        prompt=self.runner.common_prompt(training_domains(env,tr),[],[],1)
        self.assertIn('q_X = X / X_ref',prompt['normalization'])
        self.assertIn('never X/q_X',prompt['normalization'])


if __name__=='__main__':unittest.main()
