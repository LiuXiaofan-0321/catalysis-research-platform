"""Keep scientific statements while repairing the observed list/string mismatch."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests')]
from test_jacs_au_direct import candidate
from catalysis_research.experiments.jacs_au_direct import validate_candidate, technical_patch
from catalysis_research.experiments.jacs_au_direct_interface import validate_candidate_with_proxy_adapter


class InterfaceTests(unittest.TestCase):
    def test_nonempty_list_repairs_representation_without_scientific_rewrite(self):
        original = {'descriptor_candidate':candidate()}
        original['descriptor_candidate']['proxy_assumptions'] = ['Heavy-atom geometry is an empirical proxy.', 'The framework is conditionally rigid.']
        saved = deepcopy(original)
        with self.assertRaisesRegex(ValueError,'proxy_assumptions'): validate_candidate(original)
        c,audit = validate_candidate_with_proxy_adapter(original)
        self.assertEqual(original,saved)
        self.assertEqual(c['proxy_assumptions'],'\n'.join(saved['descriptor_candidate']['proxy_assumptions']))
        for k,v in saved['descriptor_candidate'].items():
            if k!='proxy_assumptions': self.assertEqual(c[k],v)
        self.assertEqual(audit['llm_calls'],0)
        self.assertEqual(audit['items_preserved'],2)
        self.assertEqual(technical_patch(c,{'technical_patch':{'boundary_behavior':'Valid observed support'}})['proxy_assumptions'],c['proxy_assumptions'])

    def test_missing_assumptions_and_other_invalid_science_are_not_filled(self):
        for value in (None, '', [], [''], ['valid',3]):
            c=candidate(); c['proxy_assumptions']=value
            with self.assertRaises(ValueError): validate_candidate_with_proxy_adapter({'descriptor_candidate':c})
        c=candidate(); c['proxy_assumptions']=['No causality established']; c['physical_prediction']['loss_direction']='unknown'
        with self.assertRaises(ValueError): validate_candidate_with_proxy_adapter({'descriptor_candidate':c})


if __name__=='__main__': unittest.main()
