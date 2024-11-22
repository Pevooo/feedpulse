import unittest
from unittest.mock import patch
from app import FeedPulseAPI
from src.config.feed_pulse_settings import FeedPulseSettings
from src.config.router import Router
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.report_creator import ReportCreator
from src.topic_detection.topic_detector import TopicDetector

FAKE_API_RESPONSE = {
    "posts": {
        "data": [
            {
                "message": "hello 2",
                "created_time": "2024-10-28T11:06:11+0000",
            },
            {
                "comments": {
                    "data": [
                        {"created_time": "2024-10-28T10:53:26+0000", "message": "test"}
                    ],
                },
                "message": "hello, world!",
                "created_time": "2024-10-24T16:17:02+0000",
            },
        ]
    }
}


class TestEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test client."""
        cls.feed_pulse_app = FeedPulseAPI(
            FeedbackClassifier(FeedPulseSettings.feedback_classification_model()),
            TopicDetector(FeedPulseSettings.topic_segmentation_model()),
            ReportCreator(FeedPulseSettings.report_creation_model()),
        )
        cls.app = cls.feed_pulse_app.flask_app
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()  # Flask's test client for HTTP requests

    @patch.object(FacebookDataProvider, "get_posts")
    @patch.object(ReportCreator, "create")
    def test_full_pipeline(self, mock_create_report, mock_get_posts):
        """
        End-to-End test for the full pipeline.
        Mock the Facebook API.
        """
        mock_get_posts.return_value = FAKE_API_RESPONSE
        mock_create_report.return_value = "Mock Report Content"

        # Send a POST request to the index route
        response = self.client.post(
            Router.MAIN_TESTING_ROUTE,
            data={
                "access_token": "mock_access_token",
                "page_id": "123456",
            },
        )

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mock Report Content", response.data)

    def test_remote_config_valid_update(self):
        """Test the remote configuration update."""
        payload = {
            "settingsList": [
                {
                    "settingName": "enable_x_data_collection",
                    "settingValue": "false",
                }
            ]
        }
        response = self.client.post("/config", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Success", response.data)

    def test_remote_config_invalid_value_update(self):
        """Test the remote configuration update."""
        payload = {
            "settingsList": [
                {
                    "settingName": "enable_x_data_collection",
                    "settingValue": "hello",
                }
            ]
        }
        response = self.client.post("/config", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Failure", response.data)

    def test_remote_config_invalid_name_update(self):
        """Test the remote configuration update."""
        payload = {
            "settingsList": [
                {
                    "settingName": "invalid_name",
                    "settingValue": "false",
                }
            ]
        }
        response = self.client.post("/config", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Failure", response.data)

    def test_remote_config_invalid_format(self):
        """Test the remote configuration update."""
        payload = {"hello": ["invalid_format", "invalid_value"]}
        response = self.client.post("/config", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Failure", response.data)
