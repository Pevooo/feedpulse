import unittest
from complaint_filter import ComplaintFilter


class TestComplaintFiler(unittest.TestCase):
    def test_wrap_text(self):
        complaint_filter = ComplaintFilter()
        self.assertEqual(
            complaint_filter.wrap_text("hello"),
            (
                "You will be provided with a text. Respond in two parts as follows:\n"
                "1. Is it a complaint, a compliment, or neutral? Answer with 'complaint', 'compliment', or 'neutral'.\n"
                "2. Does the complaint or compliment have a specific topic? Answer with 'yes' or 'no'.\n\n"
                'Here is the text: "hello".'
            ),
        )

    def test_service_connection_complaint_with_topic(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter("The service was bad, and the food was cold.")
        self.assertEqual(result.type, "complaint")
        self.assertTrue(result.has_topic)

    def test_service_connection_complaint_without_topic(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter("This is really bad.")
        self.assertEqual(result.type, "complaint")
        self.assertFalse(result.has_topic)

    def test_service_connection_compliment_with_topic(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter(
            "The food was amazing, and the service was excellent."
        )
        self.assertEqual(result.type, "compliment")
        self.assertTrue(result.has_topic)

    def test_service_connection_compliment_without_topic(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter("This is wonderful.")
        self.assertEqual(result.type, "compliment")
        self.assertFalse(result.has_topic)
