import unittest
from unittest.mock import MagicMock

from src.models.global_model_provider import GlobalModelProvider
from src.topics.feedback_topic import FeedbackTopic
from src.topics.topic_detector import TopicDetector


class TestTopicDetector(unittest.TestCase):
    def setUp(self):
        self.org_topics = [
            FeedbackTopic.FOOD,
            FeedbackTopic.WIFI,
            FeedbackTopic.STAFF,
            FeedbackTopic.ACCESSIBILITY,
        ]
        self.mock_provider = MagicMock(spec=GlobalModelProvider)
        self.topic_detector = TopicDetector(self.mock_provider)

    def test_detect_known_topic(self):
        self.mock_provider.generate_content.return_value = "food,wifi"
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(result, [(FeedbackTopic.FOOD, FeedbackTopic.WIFI)])

    def test_detect_multiple_known_topic(self):
        self.mock_provider.generate_content.return_value = (
            "food|accessibility,staff|wifi"
        )
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(
            result,
            [
                (FeedbackTopic.FOOD,),
                (FeedbackTopic.ACCESSIBILITY, FeedbackTopic.STAFF),
                (FeedbackTopic.WIFI,),
            ],
        )

    def test_detect_multiple_known_topic_and_no_matching_topic(self):
        self.mock_provider.generate_content.return_value = (
            "food|wifi,staff|no relevant topics found."
        )
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(
            result,
            [(FeedbackTopic.FOOD,), (FeedbackTopic.WIFI, FeedbackTopic.STAFF), tuple()],
        )

    def test_no_matching_topic(self):
        self.mock_provider.generate_content.return_value = "no relevant topics found."
        result = self.topic_detector.detect(MagicMock(), self.org_topics)
        self.assertListEqual(result, [tuple()])
