
import unittest

from candidate_generator import trl1, trl2, trlm2
from automation import RepeatedLetterDFA
from pattern_classifier import classify_pattern
from symspell_corrector import create_symspell
from normalizer import normalize_word


class TestTextNormalizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sym_spell = create_symspell()
        cls.detector = RepeatedLetterDFA()

    
    def test_repeated_letter_detection(self):
        self.assertTrue(self.detector.detect("soooo"))
        self.assertTrue(self.detector.detect("hello"))
        self.assertFalse(self.detector.detect("world"))


    def test_trl1(self):
        self.assertEqual(trl1("soooo"), "so")
        self.assertEqual(trl1("helllo"), "helo")

    def test_trl2(self):
        self.assertEqual(trl2("soooo"), "soo")
        self.assertEqual(trl2("helllo"), "hello")

    def test_trlm2_example(self):
        self.assertEqual(trlm2("cccccaaaaannnnn"), "caann")

    def test_no_repetition(self):
        self.assertIsNone(classify_pattern("abc"))
        self.assertEqual(
            normalize_word("abc", self.sym_spell),
            "abc",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
