import unittest
from unittest.mock import patch, Mock
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.gemini_model import GeminiModel


class TestFeedbackClassifier(unittest.TestCase):
    def test_wrap_text(self):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        self.assertEqual(
            feedback_classifier._generate_prompt("hello"),
            (
                "You will be provided with a text. Respond as follows:\n"
                "Is it a complaint, a compliment, or neutral? Answer only with 'complaint', 'compliment', or 'neutral'.\n\n"
                'Here is the text: "hello".'
            ),
        )

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
