"""Scientific safety checks for the JACS adapter, no external SI dependency."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from catalysis_research.experiments.jacs_au import make_split, metrics

spec=importlib.util.spec_from_file_location('jacs_runner',Path(__file__).resolve().parents[1]/'scripts/run_jacs_au.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)

class JacsTests(unittest.TestCase):
    def test_author_test_never_enters_search(self):
        order=np.random.default_rng(10).permutation(3690)
        split=make_split({'order':order})
        self.assertTrue(np.array_equal(split['test'],order[2952:]))
        self.assertEqual(len(set(split['train'])&set(split['score'])),0)
        self.assertEqual(len(set(np.concatenate(list(split.values())))),3690)

    def test_entropy_units_and_direction(self):
        data={'gas':np.array([30.,40.]),'entropy':np.array([6.,12.])}
        result=metrics(data,np.array([0,1]),np.array([.8,.7]))
        self.assertAlmostEqual(result['mae_R'],0.)

    def test_dsl_cannot_read_targets_or_execute_code(self):
        env={'MW':np.array([10.,20.])}
        for formula in ['Sgas/MW', '__import__("os")', 'MW[0]', 'MW.__class__', 'MW**MW', 'MW**1000']:
            with self.assertRaises(ValueError,msg=formula):runner.evaluate_formula(formula,env)
        np.testing.assert_allclose(runner.evaluate_formula('sqrt(MW*MW)',env),env['MW'])

    def test_quality_checks_use_training_rows_only(self):
        env={'MW':np.array([1.,2.,3.,0.])}
        v=runner.checked_feature('1/MW',env,np.zeros((4,1)),np.array([0,1,2]))
        self.assertTrue(np.isfinite(v).all())
        self.assertAlmostEqual(v[-1],.5)

    def test_citations_are_not_fabricated(self):
        c=dict(name='a',formula='MW/Vol',hypothesis='h',rationale='r',falsification_criteria='f',novelty_status='uncertain',evidence_ids=['E99'])
        with self.assertRaises(ValueError):runner.validate_generation({'descriptor_candidates':[c]*3},{'E01'})

if __name__=='__main__':unittest.main()
