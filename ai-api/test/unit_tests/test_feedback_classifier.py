import unittest
from unittest.mock import Mock, MagicMock

from src.feedback_classification.feedback_classifier import FeedbackClassifier


class TestNLPClassifier(unittest.TestCase):
    def setUp(self):
        self.nlp_classifier = FeedbackClassifier(Mock())
        self.nlp_classifier._get_sentiments = Mock()

    def test_extract_positive_label(self):
        self.nlp_classifier._get_sentiments.return_value = [
            {"label": "Very Positive", "score": 0.9528169631958008}
        ]
        self.assertListEqual(self.nlp_classifier.classify(MagicMock()), [True])

    def test_extract_negative_label(self):
        self.nlp_classifier._get_sentiments.return_value = [
            {"label": "Negative", "score": 0.34671148657798767}
        ]
        self.assertListEqual(self.nlp_classifier.classify(MagicMock()), [False])

    def test_extract_neutral_label(self):
        self.nlp_classifier._get_sentiments.return_value = [
            {"label": "Neutral", "score": 0.5609035491943359}
        ]
        self.assertListEqual(self.nlp_classifier.classify(MagicMock()), [None])

    def test_extract_multiple_labels(self):
        self.nlp_classifier._get_sentiments.return_value = [
            {"label": "Very Positive", "score": 0.9528169631958008},
            {"label": "Neutral", "score": 0.5609035491943359},
            {"label": "Negative", "score": 0.34671148657798767},
            {"label": "Very Negative", "score": 0.875544011592865},
            {"label": "Very Positive", "score": 0.6028310060501099},
            {"label": "Very Negative", "score": 0.6521781086921692},
            {"label": "Negative", "score": 0.37015214562416077},
            {"label": "Very Negative", "score": 0.6255631446838379},
            {"label": "Very Positive", "score": 0.6727625131607056},
            {"label": "Very Negative", "score": 0.9308859705924988},
        ]
        self.assertListEqual(
            self.nlp_classifier.classify(MagicMock()),
            [True, None, False, False, True, False, False, False, True, False],
        )
