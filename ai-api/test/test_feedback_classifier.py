import unittest
from unittest.mock import patch, Mock
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.gemini_model import GeminiModel


class TestFeedbackClassifier(unittest.TestCase):

    @patch.object(GeminiModel, "generate_content")
    def test_complaint(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Complaint"
        result = feedback_classifier.classify(Mock())

        mock_generate_content.assert_called_once()
        self.assertFalse(result)

    @patch.object(GeminiModel, "generate_content")
    def test_compliment(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Compliment"
        result = feedback_classifier.classify(Mock())

        mock_generate_content.assert_called_once()
        self.assertTrue(result)

    @patch.object(GeminiModel, "generate_content")
    def test_neutral(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Neutral"
        result = feedback_classifier.classify(Mock())

        mock_generate_content.assert_called_once()
        self.assertIsNone(result)

    @patch.object(GeminiModel, "generate_content")
    def test_empty_string(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = ""
        result = feedback_classifier.classify(Mock())

        mock_generate_content.assert_called_once()
        self.assertIsNone(result)

    @patch.object(GeminiModel, "generate_content")
    def test_text_passed_to_generate_content(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = ""
        result = feedback_classifier.classify("hello")

        mock_generate_content.assert_called_once_with(
            feedback_classifier._generate_prompt("hello")
        )
        self.assertIsNone(result)
