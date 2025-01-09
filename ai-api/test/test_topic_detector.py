import unittest
from unittest.mock import Mock, patch, MagicMock
from src.topic_detection.topic_detector import TopicDetector
from src.models.gemini_model import GeminiModel


class TestTopicDetector(unittest.TestCase):
    def setUp(self):
        self.org_topics = ["customer service", "delivery", "product quality"]
        self.topic_detector = TopicDetector(GeminiModel())

    @patch.object(GeminiModel, "generate_content")
    def test_detect_known_topic(self, mock_generate_content):
        mock_generate_content.return_value = "customer service,delivery"
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(result, [("customer service", "delivery")])

    @patch.object(GeminiModel, "generate_content")
    def test_detect_multiple_known_topic(self, mock_generate_content):
        mock_generate_content.return_value = (
            "food quality|customer service,wait time|service"
        )
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(
            result, [("food quality",), ("customer service", "wait time"), ("service",)]
        )

    @patch.object(GeminiModel, "generate_content")
    def test_detect_multiple_known_topic_and_no_matching_topic(
        self, mock_generate_content
    ):
        mock_generate_content.return_value = (
            "food quality|customer service,wait time|no relevant topics found."
        )
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(
            result, [("food quality",), ("customer service", "wait time"), tuple()]
        )

    @patch.object(GeminiModel, "generate_content")
    def test_no_matching_topic(self, mock_generate_content):
        mock_generate_content.return_value = "no relevant topics found."
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(result, [tuple()])
