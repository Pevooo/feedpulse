import unittest
from unittest.mock import Mock

from src.feedback_classification.nlp_classifier import NLPClassifier


class TestNLPClassifier(unittest.TestCase):
    def setUp(self):
        self.nlp_classifier = NLPClassifier(Mock())

    def test_extract_stars(self):
        result = [{"label": "3 stars", "score": 5.5}]
        self.assertEqual(self.nlp_classifier.extract_stars(result), 3)
