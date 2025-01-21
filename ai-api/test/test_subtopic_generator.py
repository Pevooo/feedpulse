import unittest
from unittest.mock import MagicMock, Mock

from src.models.gemini_model import GeminiModel
from src.topics.feedback_topic import FeedbackTopic
from src.topics.subtopic_generator import SubtopicGenerator


class TestSubtopicGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock(spec=GeminiModel)
        self.subtopic_generator = SubtopicGenerator(self.mock_model)

    def test_no_subtopics(self):
        self.mock_model.generate_content.return_value = "NONE"

        topics = self.subtopic_generator.generate(Mock())
        self.assertEqual(len(topics), 0)

    def test_one_subtopic(self):
        self.mock_model.generate_content.return_value = "cleanliness"

        topics = self.subtopic_generator.generate(Mock())
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0], FeedbackTopic.CLEANLINESS)

    def test_multiple_subtopics(self):
        self.mock_model.generate_content.return_value = "cleanliness,staff"

        topics = self.subtopic_generator.generate(Mock())
        self.assertEqual(len(topics), 2)
        self.assertEqual(topics[0], FeedbackTopic.CLEANLINESS)
        self.assertEqual(topics[1], FeedbackTopic.STAFF)
