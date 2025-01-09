import unittest
from unittest.mock import patch, MagicMock
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.gemini_model import GeminiModel


class TestFeedbackClassifier(unittest.TestCase):

    @patch.object(GeminiModel, "generate_content")
    def test_complaint(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "0"
        result = feedback_classifier.classify(MagicMock())

        mock_generate_content.assert_called_once()
        self.assertListEqual(result, [False])

    @patch.object(GeminiModel, "generate_content")
    def test_compliment(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "1"
        result = feedback_classifier.classify(MagicMock())

        mock_generate_content.assert_called_once()
        self.assertListEqual(result, [True])

    @patch.object(GeminiModel, "generate_content")
    def test_neutral(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "2"
        result = feedback_classifier.classify(MagicMock())

        mock_generate_content.assert_called_once()
        self.assertListEqual(result, [None])

    @patch.object(GeminiModel, "generate_content")
    def test_multiple(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = "0,1,2"
        result = feedback_classifier.classify(MagicMock())

        mock_generate_content.assert_called_once()
        self.assertListEqual(result, [False, True, None])

    @patch.object(GeminiModel, "generate_content")
    def test_empty_string(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = ""
        result = feedback_classifier.classify(MagicMock())

        mock_generate_content.assert_called_once()
        self.assertListEqual(result, [])

    @patch.object(GeminiModel, "generate_content")
    def test_text_passed_to_generate_content(self, mock_generate_content):
        feedback_classifier = FeedbackClassifier(GeminiModel())
        mock_generate_content.return_value = ""
        fake_list = ["hello"]
        result = feedback_classifier.classify(fake_list)

        mock_generate_content.assert_called_once_with(
            feedback_classifier._generate_prompt(fake_list)
        )
        self.assertListEqual(result, [])
