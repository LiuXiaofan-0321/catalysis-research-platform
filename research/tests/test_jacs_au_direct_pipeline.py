"""Plan completeness, provenance gate and all-trace statistics regressions."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'),str(ROOT/'scripts')]
from catalysis_research.experiments.jacs_au_direct import load_config, MODES
import manage_jacs_au_direct as pipeline


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.config = load_config(ROOT/'configs/experiments/jacs-au-direct-v5-high.json')

    def signs(self):
        return [{'fit_seed':s,'status':'completed','paired_initialization':{
            'initial_prediction_max_abs_difference':0.,'initial_fc1_l1_difference':0.},
            'paired_final_prediction_max_abs_difference':0.,
            'arms':{k:{'status':'scored'} for k in ('positive','paired_negative','original_unpaired_negative')}}
            for s in self.config['evaluation']['fit_seeds']]

    def replay(self):
        return {'status':'completed','blocks':54,'candidate_slots':162,
            'max_abs_prefix_replay_delta_R':0.,'max_abs_final_replay_delta_R':0.}

    def test_gate_missing_seed_or_changed_checks_cannot_pass(self):
        gate = pipeline.prerequisite_gate(self.replay(), self.signs(), self.config)
        gate['replay_summary'] = self.replay()
        pipeline.validate_gate(gate,self.config)
        bad = deepcopy(gate); bad['sign_result_diagnostics'].pop()
        with self.assertRaises(ValueError): pipeline.validate_gate(bad,self.config)
        bad = deepcopy(gate); bad['checks']['prefix_reproduction'] = False
        with self.assertRaises(ValueError): pipeline.validate_gate(bad,self.config)
        self.assertEqual(pipeline.prerequisite_gate(self.replay(), [], self.config)['status'],'blocked')
        signs = self.signs(); signs[0]['paired_final_prediction_max_abs_difference']=1e-3
        self.assertEqual(pipeline.prerequisite_gate(self.replay(), signs, self.config)['status'],'blocked')

    def test_baseline_failure_keeps_seed_and_blocks_completion(self):
        data={'x':np.ones((12,14)),'gas':np.ones(12),'entropy':np.ones(12)*.3}
        split={'train':np.arange(6),'score':np.arange(6,9),'test':np.arange(9,12)}
        def fitter(data,x,train,epochs,seed):
            if seed==11: raise RuntimeError('declared test failure')
            return np.ones(12)*.7,1.
        with tempfile.TemporaryDirectory() as tmp:
            result=pipeline.baseline(data,split,self.config,Path(tmp)/'d0',fitter)
            self.assertEqual(result['status'],'incomplete')
            self.assertEqual([s['seed'] for s in result['seeds']],[3,7,11,17,23])
            self.assertEqual(result['seeds'][2]['status'],'failed')
            self.assertFalse((Path(tmp)/'d0/d0-seed-11.npy').exists())

    def records(self):
        plan={'tasks':[]}; gs=[]; es=[]
        for mode in MODES:
            for rep in range(1,11):
                plan['tasks'].append({'mode':mode,'replicate':rep})
                gs.append({'mode':mode,'replicate':rep,'status':'frozen','config':deepcopy(self.config),
                    'rounds':[{'final_check':{},'review_issues':[]} for _ in range(3)],'appended':[],
                    'api_calls':6,'usage_totals':{},'usage_unavailable_attempts':0})
                gains=[0. if rep==10 else -float(rep)]*5
                es.append({'mode':mode,'replicate':rep,'status':'completed','evaluation':deepcopy(self.config['evaluation']),
                    'seeds':[{'seed':s,'gain_pct':v} for s,v in zip([3,7,11,17,23],gains)],
                    'mean_gain_pct':float(np.mean(gains)),'input_count':14,'successful_additions':0,
                    'fallbacks':5 if rep==10 else 0})
        return plan,gs,es

    def test_summary_uses_all_negative_and_fallback_traces_not_fifty_units(self):
        plan,gs,es=self.records(); result=pipeline.summarize(plan,gs,es)
        for g in result['groups'].values():
            self.assertEqual(g['n_generation_traces'],10)
            self.assertEqual(g['mean_gain_pct'],-4.5)
            self.assertEqual(g['fallback_seed_fits'],5)
            self.assertEqual(g['distinct_ordered_formula_sequences'],1)
        self.assertEqual(result['contrasts']['rag_agent-agent']['mean_difference_pp'],0.)
        with self.assertRaises(ValueError): pipeline.summarize(plan,gs[:-1],es)
        es[0]['seeds'].pop()
        with self.assertRaises(ValueError): pipeline.summarize(plan,gs,es)


if __name__=='__main__': unittest.main()
