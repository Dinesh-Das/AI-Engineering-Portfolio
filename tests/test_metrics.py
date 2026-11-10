import unittest

from tools.evaluate import summarize


class EvaluationTests(unittest.TestCase):
    def test_missing_labels_do_not_become_perfect_scores(self):
        result = summarize([{'id': 'a', 'latency_ms': 20}])
        self.assertIsNone(result['exact_match'])
        self.assertIsNone(result['recall_at_k'])
        self.assertEqual(result['coverage']['exact_match'], 0)

    def test_retrieval_duplicate_ids_do_not_inflate_recall(self):
        result = summarize([{'id': 'a', 'relevant_ids': ['x', 'y'], 'retrieved_ids': ['x', 'x', 'z']}])
        self.assertEqual(result['recall_at_k'], 0.5)
        self.assertEqual(result['mrr'], 1.0)

    def test_exact_answers_abstention_and_latency(self):
        result = summarize([
            {'id': 'a', 'expected': '42', 'actual': '42', 'should_abstain': False, 'abstained': False, 'latency_ms': 10, 'cost_usd': 0.1},
            {'id': 'b', 'expected': 'yes', 'actual': 'no', 'should_abstain': True, 'abstained': False, 'latency_ms': 30, 'cost_usd': 0.2},
        ])
        self.assertEqual(result['exact_match'], 0.5)
        self.assertEqual(result['abstention_accuracy'], 0.5)
        self.assertEqual(result['latency_p95_ms'], 30)
        self.assertAlmostEqual(result['reported_cost_usd'], 0.3)

    def test_invalid_observations_fail_instead_of_skipping(self):
        invalid_sets = [[], [{'id': 'x'}, {'id': 'x'}], [{'id': 'a', 'latency_ms': -1}],
                        [{'id': 'a', 'cost_usd': float('nan')}],
                        [{'id': 'a', 'relevant_ids': []}],
                        [{'id': 'a', 'should_abstain': 'yes', 'abstained': True}],
                        [{'id': 'a', 'expected': 'answer'}]]
        for rows in invalid_sets:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                summarize(rows)


if __name__ == '__main__':
    unittest.main()
