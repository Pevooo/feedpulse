import unittest
from ComplaintFilter import ComplaintFilter


class TestComplaintFiler(unittest.TestCase):
    def test_wrap_text(self):
        complaint_filter = ComplaintFilter()
        self.assertEqual(
            complaint_filter.wrap_text("hello"),
            "You will be provided with some text and you have to tell if it's a complaint or not using only one word (YES or NO).\n Here is the text: \"hello\"."
        )

    def test_service_connection_complaint(self):
        complaint_filter = ComplaintFilter()
        self.assertTrue(complaint_filter("This place is really bad"))

    def test_service_connection_not_complaint(self):
        complaint_filter = ComplaintFilter()
        self.assertFalse(complaint_filter("This place is really good"))
