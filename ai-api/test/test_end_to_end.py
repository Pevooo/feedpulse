import os
import logging
import unittest
from unittest.mock import patch
from api import FeedPulseAPI
from src.config.settings import Settings
from src.config.router import Router
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.report_handler import ReportHandler
from src.topic_detection.topic_detector import TopicDetector

FAKE_API_RESPONSE = {
    "posts": {
        "data": [
            {
                "message": "The food is perfect!",
                "created_time": "2024-11-17T20:27:21+0000",
                "comments": {
                    "data": [
                        {
                            "created_time": "2024-11-17T20:32:15+0000",
                            "message": "The staff treated me very very badly",
                        },
                        {
                            "created_time": "2024-11-17T20:31:50+0000",
                            "message": "The food is very good",
                        },
                    ],
                },
            },
        ]
    }
}


class TestEndToEnd(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """Set up the Flask app and test client."""
        self.feed_pulse_app = FeedPulseAPI(
            FeedbackClassifier(Settings.feedback_classification_model()),
            TopicDetector(Settings.topic_segmentation_model()),
            ReportHandler(Settings.report_creation_model()),
        )
        self.app = self.feed_pulse_app.flask_app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()  # Flask's test client for HTTP requests
        logging.getLogger("grpc").setLevel(logging.CRITICAL)
        os.environ["GRPC_VERBOSITY"] = "NONE"
        os.environ["GRPC_TRACE"] = "none"

    @patch("requests.get")
    @patch.object(ReportHandler, "create")
    def test_full_pipeline(self, mock_create_report, mock_get):
        """
        End-to-End test for the full pipeline.
        """
        mock_get.return_value.json.return_value = FAKE_API_RESPONSE
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
        self.assertIn("Mock Report Content", response.get_data(as_text=True))

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
        self.assertIn("Success", response.get_data(as_text=True))

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
        self.assertIn("Failure", response.get_data(as_text=True))

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
        self.assertIn("Failure", response.get_data(as_text=True))

    def test_remote_config_invalid_format(self):
        """Test the remote configuration update."""
        payload = {"hello": ["invalid_format", "invalid_value"]}
        response = self.client.post("/config", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Failure", response.get_data(as_text=True))
