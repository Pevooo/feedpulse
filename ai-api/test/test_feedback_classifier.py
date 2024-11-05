import unittest
from unittest.mock import patch, Mock
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.loaded_models.gemini_model import GeminiModel


class TestFeedbackClassifier(unittest.TestCase):
    def test_wrap_text(self):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        self.assertEqual(
            feedback_classifier.wrap_text("hello"),
            (
                "You will be provided with a text. Respond in two parts as follows:\n"
                "1. Is it a complaint, a compliment, or neutral? Answer with 'complaint', 'compliment', or 'neutral'.\n"
                "2. Does the complaint or compliment have a specific topic? Answer with 'yes' or 'no'.\n\n"
                'Here is the text: "hello".'
            ),
        )

    @patch.object(GeminiModel, "generate_content")
    def test_complaint_with_topic(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Complaint, Yes"
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "complaint")
        self.assertTrue(result.has_topic)

    @patch.object(GeminiModel, "generate_content")
    def test_complaint_without_topic(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Complaint, No"
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "complaint")
        self.assertFalse(result.has_topic)

    @patch.object(GeminiModel, "generate_content")
    def test_compliment_with_topic(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Compliment, Yes"
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "compliment")
        self.assertTrue(result.has_topic)

    @patch.object(GeminiModel, "generate_content")
    def test_compliment_without_topic(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Compliment, No"
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "compliment")
        self.assertFalse(result.has_topic)

    @patch.object(GeminiModel, "generate_content")
    def test_neutral_without_topic(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Neutral, No"
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "neutral")
        self.assertFalse(result.has_topic)

    @patch.object(GeminiModel, "generate_content")
    def test_neutral_with_topic(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "Neutral, Yes"
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "neutral")
        self.assertTrue(result.has_topic)

    @patch.object(GeminiModel, "generate_content")
    def test_empty_string(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = ""
        result = feedback_classifier(Mock())

        mock_generate_content.assert_called_once()
        self.assertEqual(result.text_type, "neutral")
        self.assertFalse(result.has_topic)
