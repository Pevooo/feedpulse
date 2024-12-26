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
