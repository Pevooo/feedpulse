import unittest
from unittest.mock import patch, MagicMock

from src.topics.feedback_topic import FeedbackTopic
from src.topics.topic_detector import TopicDetector
from src.models.gemini_model import GeminiModel


class TestTopicDetector(unittest.TestCase):
    def setUp(self):
        self.org_topics = [
            FeedbackTopic.FOOD,
            FeedbackTopic.WIFI,
            FeedbackTopic.STAFF,
            FeedbackTopic.ACCESSIBILITY,
        ]
        self.topic_detector = TopicDetector(GeminiModel())

    @patch.object(GeminiModel, "generate_content")
    def test_detect_known_topic(self, mock_generate_content):
        mock_generate_content.return_value = "food,wifi"
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(result, [(FeedbackTopic.FOOD, FeedbackTopic.WIFI)])

    @patch.object(GeminiModel, "generate_content")
    def test_detect_multiple_known_topic(self, mock_generate_content):
        mock_generate_content.return_value = "food|accessibility,staff|wifi"
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(
            result,
            [
                (FeedbackTopic.FOOD,),
                (FeedbackTopic.ACCESSIBILITY, FeedbackTopic.STAFF),
                (FeedbackTopic.WIFI,),
            ],
        )

    @patch.object(GeminiModel, "generate_content")
    def test_detect_multiple_known_topic_and_no_matching_topic(
        self, mock_generate_content
    ):
        mock_generate_content.return_value = "food|wifi,staff|no relevant topics found."
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(
            result,
            [(FeedbackTopic.FOOD,), (FeedbackTopic.WIFI, FeedbackTopic.STAFF), tuple()],
        )

    @patch.object(GeminiModel, "generate_content")
    def test_no_matching_topic(self, mock_generate_content):
        mock_generate_content.return_value = "no relevant topics found."
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(result, [tuple()])
