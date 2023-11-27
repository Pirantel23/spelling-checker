import unittest

from levenshtein import levenshtein_distance_normalized


class TestLevenshteinDistanceNormalized(unittest.TestCase):

    def test_same_strings(self):
        self.assertEqual(levenshtein_distance_normalized("самовар", "самовар"), 1.0)

    def test_one_empty_string(self):
        self.assertEqual(levenshtein_distance_normalized("самовар", ""), 0.0)
        self.assertEqual(levenshtein_distance_normalized("", "чайник"), 0.0)

    def test_insertion(self):
        self.assertEqual(levenshtein_distance_normalized("самовар", "самоварь"), 0.875)

    def test_case_insensitive(self):
        self.assertEqual(levenshtein_distance_normalized("СамОвар", "самовар"), 1.0)

    def test_deletion(self):
        self.assertEqual(levenshtein_distance_normalized("самоварь", "самовар"), 0.875)

    def test_hyphenated_words(self):
        self.assertEqual(levenshtein_distance_normalized("пол-арбуза", "поларбуза"), 0.9)

    def test_missing_space(self):
        self.assertEqual(levenshtein_distance_normalized("как у тебя дела", "какутебядела"), 0.8)

    def test_substitution(self):
        self.assertEqual(levenshtein_distance_normalized("самовар", "симовар"),  0.8571428571428572)

    def test_custom_weights(self):
        weights = {'delete': 2, 'insert': 1, 'substitute': 0.5}
        self.assertEqual(levenshtein_distance_normalized("самовар", "симовар", weights), 0.9285714285714286)


if __name__ == '__main__':
    unittest.main()
