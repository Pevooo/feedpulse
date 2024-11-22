import json
import unittest
from unittest.mock import patch, Mock

from src.models.gemini_model import GeminiModel
from src.reports.report_handler import ReportHandler


FAKE_TOPIC_COUNTS = json.dumps(
    {
        "cleanliness": {True: 2, False: 1},
        "food": {True: 0, False: 4},
    }
)


class TestReportHandler(unittest.TestCase):

    def setUp(self):
        self.report_handler = ReportHandler(Mock(spec=GeminiModel))

    @patch("requests.post")
    def test_post_request(self, mock_post):
        mock_post.return_value = None

        self.report_handler.send_report("hello", "url")

        mock_post.assert_called_with("url", json="hello", timeout=0.1)

    def test_wrap_text(self):
        self.assertEqual(
            self.report_handler.wrap_text(FAKE_TOPIC_COUNTS),
            f"""
            Please generate a well-structured report summarizing the positive and negative feedback counts
            for multiple topics based on the provided data.
            The data is in JSON format, where each key represents a topic name,
            and its value is another dictionary containing the counts of 'positive_feedback' and 'negative_feedback' for that topic.

            Here is the data in JSON format:

           {FAKE_TOPIC_COUNTS}

            The report should include:
            1.	A section for each topic with its name.
            2.	The counts of positive and negative feedback.
            3.	A summary line for each topic, like: 'The topic [TOPIC_NAME] received [X] positive and [Y] negative feedback entries.'
            4.	Make the report organized, neat, and easy to read.
            """,
        )
