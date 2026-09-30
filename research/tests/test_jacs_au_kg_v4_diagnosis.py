"""Guard fixed review inputs, graph fact parity and non-adaptive stage replay."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import diagnose_jacs_au_kg_v4 as audit
import replay_jacs_au_kg_v4_candidates as replay


class FixedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = audit.read(ROOT / 'reports/jacs_au_kg_v4_diagnosis_20260930/fixed-review-blocks.json')

    def test_complete_population_and_historical_prefix_provenance(self):
        blocks = self.manifest['blocks']
        self.assertEqual(len({b['block_id'] for b in blocks}), 54)
        self.assertEqual(sum(len(b['review_common']['drafts']) for b in blocks), 162)
        source = ROOT / 'reports/jacs_au_kg_v4_20260930/complete-server-results'
        for b in blocks:
            d = audit.read(source / b['source_identity'])
            rd = d['rounds'][b['round'] - 1]
            self.assertEqual(b['review_common']['drafts'], rd['blind_drafts'])
            self.assertEqual(b['review_common']['training_only_prechecks'], rd['blind_checks'])
            prefix = [c['formula'] for prev in d['rounds'][:b['round'] - 1]
                      for c in prev['candidates'] if c['retained']]
            self.assertEqual([c['formula'] for c in b['fixed_prefix']], prefix)
            self.assertNotIn('final_candidates', b['review_common'])
            self.assertNotIn('current_candidates_scores', b['review_common'])

    def test_evidence_arms_receive_identical_facts_checks_and_drafts(self):
        for b in self.manifest['blocks']:
            requests = [audit.review_request(b, arm) for arm in audit.ARMS]
            self.assertTrue(all(r['drafts'] == requests[0]['drafts'] for r in requests))
            self.assertTrue(all(r['training_only_prechecks'] == requests[0]['training_only_prechecks'] for r in requests))
            self.assertTrue(all(r['evidence'] == requests[1]['evidence'] for r in requests[1:]))
            self.assertEqual(requests[0]['evidence']['items'], [])
            self.assertNotIn('graph_tool_result', requests[1])

    def test_flat_graph_is_lossless_and_condition_references_resolve(self):
        for b in self.manifest['blocks']:
            graph = b['graph_paths']
            flat = audit.flat_graph(graph)
            rebuilt = {}
            for fact in flat['node_facts']:
                rebuilt.setdefault(fact['node_id'], {})[fact['property']] = fact['value']
            self.assertEqual(rebuilt, graph['nodes'])
            self.assertEqual(flat['relation_facts'], graph['edges'])
            self.assertEqual(flat['note'], graph['note'])
            self.assertNotIn('executed_checks', graph)
            for node in graph['nodes'].values():
                if node['type'] == 'conditional_mechanism':
                    ref = node['conditions_ref'].split('.')[-1]
                    self.assertIn(ref, b['evidence']['source_conditions'])

    def test_request_builder_does_not_mutate_frozen_block(self):
        b = deepcopy(self.manifest['blocks'][0])
        previous = deepcopy(b)
        request = audit.review_request(b, 'graph')
        request['drafts'][0]['formula'] = 'CHANGED'
        self.assertEqual(b, previous)

    def synthetic(self):
        rng = np.random.default_rng(53)
        data = {'x': rng.uniform(.3, 3, (100, 14)), 'entropy': np.ones(100)}
        split = {'train': np.arange(70), 'score': np.arange(70, 90), 'test': np.arange(90, 100)}
        cs = [{'slot_id': 'h1', 'formula': 'q_Vol**2'}, {'slot_id': 'h2', 'formula': 'q_AV**2'},
              {'slot_id': 'h3', 'formula': 'q_PMI1'}]
        prefix = {'slot_id': 'h1', 'formula': 'q_lsd_f**2'}
        rd = {'before_mae_R': .5, 'after_mae_R': .4,
              'blind_drafts': cs, 'reviewed_candidates': deepcopy(cs), 'final_candidates': deepcopy(cs)}
        historical = {'d0_score_mae_R': .7, 'rounds': [
            {'final_candidates': [prefix], 'candidates': [{**prefix, 'retained': True}]}, rd]}
        block = {'block_id': 'synthetic/round-2', 'round': 2,
                 'fixed_prefix': [prefix], 'review_common': {'drafts': cs}}
        return data, split, block, historical

    def test_stage_replay_never_appends_trial_winner_or_fits_rejected_slot(self):
        data, split, block, historical = self.synthetic()
        matrices = []
        def fitter(data, x, train, **kw):
            matrices.append(x.copy())
            return np.full(100, [.5, .4, .6][len(matrices) - 1]), 0.
        def check(c, *args):
            return {'status': 'rejected', 'reason': 'direction'} if c['slot_id'] == 'h3' else {'status': 'passed'}
        with patch.object(replay, 'precheck', side_effect=check), patch.object(replay, 'metrics', side_effect=lambda d, idx, pred: {'mae_R': float(pred[0])}):
            result = replay.replay_block(data, split, block, historical, np.full(100, .7), fitter)
        self.assertEqual([x.shape[1] for x in matrices], [15, 16, 16])
        np.testing.assert_equal(matrices[1][:, :15], matrices[2][:, :15])
        self.assertEqual(result['fit_calls'], 3)
        self.assertEqual(result['final_minus_blind_pp'], 0)
        self.assertTrue(all(s['retained_slot'] == 'h1' for s in result['stages'].values()))
        self.assertTrue(all(s['candidates'][2]['status'] == 'rejected' for s in result['stages'].values()))

    def test_wrong_prefix_provenance_rejected_before_fitting(self):
        data, split, block, historical = self.synthetic()
        block['fixed_prefix'] = []
        with self.assertRaisesRegex(ValueError, 'provenance'):
            replay.replay_block(data, split, block, historical, np.full(100, .7), lambda *a, **k: self.fail('must not fit'))


if __name__ == '__main__':
    unittest.main()
