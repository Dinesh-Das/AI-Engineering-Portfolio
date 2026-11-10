import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from maxsim import rank_documents, score_document


class MaxSimTests(unittest.TestCase):
    def test_token_maxima_are_summed(self):
        self.assertEqual(score_document([[1, 0], [0, 1]], [[2, 0], [0, 3]]), 5)

    def test_padding_cannot_outscore_negative_real_tokens(self):
        self.assertEqual(score_document([[1]], [[-2], [0]], [True, False]), -2)

    def test_top_k_is_respected_with_stable_ties(self):
        self.assertEqual(rank_documents([[1]], [[[2]], [[3]], [[3]]], 2), [(1, 3.0), (2, 3.0)])

    def test_bad_shapes_empty_masks_and_nonfinite_values_fail(self):
        for query, document, mask in [([], [[1]], None), ([[1, 2]], [[1]], None),
                                      ([[1]], [[float('nan')]], None), ([[1]], [[1]], [False])]:
            with self.subTest(query=query), self.assertRaises(ValueError):
                score_document(query, document, mask)


if __name__ == '__main__':
    unittest.main()
