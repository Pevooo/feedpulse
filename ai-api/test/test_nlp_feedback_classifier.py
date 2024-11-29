import unittest
from unittest.mock import Mock

from src.feedback_classification.nlp_feedback_classifier import NLPFeedbackClassifier


class TestNLPClassifier(unittest.TestCase):
    def setUp(self):
        self.nlp_classifier = NLPFeedbackClassifier(Mock())

    def test_extract_stars(self):
        result = [{"label": "3 stars", "score": 5.5}]
        self.assertEqual(self.nlp_classifier.extract_stars(result), 3)
