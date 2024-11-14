import unittest
from unittest.mock import Mock, patch
from src.topic_detection.topic_detector import TopicDetector
from fake_phi_model import FakePhiModel


class TestTopicDetector(unittest.TestCase):
    def setUp(self):
        self.org_topics = ["customer service", "delivery", "product quality"]
        self.topic_detector = TopicDetector(FakePhiModel())

    @patch.object(FakePhiModel, "generate_content")
    def test_detect_known_topic(self, mock_generate_content):
        mock_generate_content.return_value = "customer service, delivery"
        result = self.topic_detector(Mock(), self.org_topics)
        self.assertIn("customer service", result.topics)
        self.assertIn("delivery", result.topics)

    @patch.object(FakePhiModel, "generate_content")
    def test_no_matching_topic(self, mock_generate_content):
        mock_generate_content.return_value = ""
        result = self.topic_detector(Mock(), self.org_topics)
        self.assertEqual(result.topics, tuple())
