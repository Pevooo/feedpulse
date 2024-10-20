import unittest
from feedback_classifier import FeedbackClassifier


class TestFeedbackClassifier(unittest.TestCase):
    def test_wrap_text(self):
        feedback_classifier = FeedbackClassifier()
        self.assertEqual(
            feedback_classifier.wrap_text("hello"),
            (
                "You will be provided with a text. Respond in two parts as follows:\n"
                "1. Is it a complaint, a compliment, or neutral? Answer with 'complaint', 'compliment', or 'neutral'.\n"
                "2. Does the complaint or compliment have a specific topic? Answer with 'yes' or 'no'.\n\n"
                'Here is the text: "hello".'
            ),
        )

    def test_service_connection_complaint_with_topic(self):
        feedback_classifier = FeedbackClassifier()
        result = feedback_classifier("The service was bad, and the food was cold.")
        self.assertEqual(result.text_type, "complaint")
        self.assertTrue(result.has_topic)

    def test_service_connection_complaint_without_topic(self):
        feedback_classifier = FeedbackClassifier()
        result = feedback_classifier("This is really bad.")
        self.assertEqual(result.text_type, "complaint")
        self.assertFalse(result.has_topic)

    def test_service_connection_compliment_with_topic(self):
        feedback_classifier = FeedbackClassifier()
        result = feedback_classifier(
            "The food was amazing, and the service was excellent."
        )
        self.assertEqual(result.text_type, "compliment")
        self.assertTrue(result.has_topic)

    def test_service_connection_compliment_without_topic(self):
        feedback_classifier = FeedbackClassifier()
        result = feedback_classifier("This is wonderful.")
        self.assertEqual(result.text_type, "compliment")
        self.assertFalse(result.has_topic)
