import unittest
from unittest.mock import patch

from src.reports.report_handler import ReportHandler


class TestReportHandler(unittest.TestCase):

    def setUp(self):
        self.report_handler = ReportHandler()

    @patch("requests.post")
    def test_post_request(self, mock_post):
        mock_post.return_value = None

        self.report_handler.send_report("hello", "url")

        mock_post.assert_called_with("url", json="hello")
