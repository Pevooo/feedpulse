import unittest
from src.topic_detection.topic_detector import TopicDetector
from src.loaded_models.phi_model import PhiModel

class TestTopicDetector(unittest.TestCase):
    def setUp(self):
        self.org_topics = ["customer service", "delivery", "product quality"]
        self.topic_detector = TopicDetector(model=PhiModel(), org_topics=self.org_topics)

    def test_detect_known_topic(self):
        text = "I am unhappy with the slow delivery and lack of customer service."
        result = self.topic_detector(text)
        self.assertIn("customer service", result.topics)
        #print("Detected Topics:", result.topics)
        self.assertIn("delivery", result.topics)

    def test_no_matching_topic(self):
        text = "I love the new features!"
        result = self.topic_detector(text)
        print("Detected Topics:", result.topics)
        self.assertEqual(result.topics, [])

