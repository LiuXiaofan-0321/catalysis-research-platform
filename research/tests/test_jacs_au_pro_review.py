"""Protect the distinction between recorded results and unrun ANN diagnostics."""
from pathlib import Path
import sys
import unittest

import numpy as np

from catalysis_research.experiments.jacs_au_knowledge import formula_environment
from catalysis_research.experiments.jacs_au_kg_v4 import precheck, ROLES

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import verify_jacs_au_pro_review as review


class ProReviewTests(unittest.TestCase):
    def test_saved_scores_verified_without_training_or_generation(self):
        result = review.verify(ROOT / 'reports/jacs_au_kg_v4_20260930/complete-server-results')
        self.assertEqual(result['ann_fits'], 0)
        self.assertEqual(result['api_calls'], 0)
        self.assertAlmostEqual(result['sign_pair_gain_gap_pp'], 3.301048166453813, places=10)
        self.assertAlmostEqual(result['kg_minus_agent_mean_pp'], .17482275774199785, places=10)
        self.assertFalse(result['identity_check']['training_performed'])
        self.assertEqual(result['sign_pair'][1]['precheck_status'], 'passed')
        self.assertEqual(result['sign_pair'][1]['target_association'], 'contradicted')

    def test_non_equivalent_expression_cannot_pass_sign_identity(self):
        with self.assertRaises(AssertionError):
            review.sign_identity_check('2*log(q_lsd_f)-log(q_Vol)', 'log(q_Vol/q_lsd_f)')

    def test_association_flag_is_not_a_v4_rejection_rule(self):
        rng = np.random.default_rng(20261001)
        data = {'x': rng.uniform(.2, 4, size=(100, 14))}
        train = np.arange(100)
        env, _ = formula_environment(data, train)
        c = {'formula': 'log(1+q_Vol)', 'hypothesis': 'Empirical proxy',
             'rationale': 'Not causal', 'variable_mappings': {'Vol': ROLES['Vol']},
             'physical_claims': ['empirical_proxy'],
             'scientific_test': {'vary_input': 'Vol', 'descriptor_direction': 'increasing',
                                 'entropy_direction': 'decreasing', 'regime_input': 'lsd_f',
                                 'regime_train_quantiles': [0., 1.],
                                 'physical_interpretation': 'Dimensionless volume proxy'}}
        result = precheck(c, env, train, np.log1p(env['q_Vol']), data['x'])
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['scientific_check']['target_association'], 'contradicted')


if __name__ == '__main__':
    unittest.main()
