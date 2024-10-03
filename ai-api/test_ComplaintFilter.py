import unittest
from ComplaintFilter import ComplaintFilter


class TestComplaintFiler(unittest.TestCase):
    def test_wrap_text(self):
        complaint_filter = ComplaintFilter()
        self.assertEqual(
            complaint_filter.wrap_text("hello"),
            "You will be some text and you have to tell if it's a complaint or not using only one word (YES or NO).\nHere is the text: \"hello\"."
        )
