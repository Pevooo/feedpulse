import unittest
from ComplaintFilter import ComplaintFilter


class TestComplaintFiler(unittest.TestCase):
    def test_wrap_text(self):
        complaint_filter = ComplaintFilter()
        self.assertEqual(
            complaint_filter.wrap_text("hello"),
            ("You will be provided with a text. Respond in two parts as follows:\n"
                "1. Is it a complaint? Answer with 'yes' or 'no'.\n"
                "2. Does the complaint have a specific topic? Answer with 'has a topic' or 'no topic'.\n\n"
                f"Here is the text: \"hello\".")
        )

    def test_service_connection_complaint_with_topic(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter("The service was bad, and the food was cold.")
        self.assertTrue(result["is_complaint"])
        self.assertTrue(result["has_topic"])

    def test_service_connection_complaint_without_topic(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter("This is really bad.")
        self.assertTrue(result["is_complaint"])
        self.assertFalse(result["has_topic"])

    def test_service_connection_not_complaint(self):
        complaint_filter = ComplaintFilter()
        result = complaint_filter("This place is really good.")
        self.assertFalse(result["is_complaint"])
        self.assertFalse(result["has_topic"])
