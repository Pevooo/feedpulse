import unittest
from unittest.mock import Mock
from api import FeedPulseAPI
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.reports.report_handler import ReportHandler
from src.topics.topic_detector import TopicDetector


class TestEndToEnd(unittest.TestCase):

    def setUp(self):
        """Set up the Flask app and test client."""

        providers = [
            GoogleModelProvider(),
        ]

        self.feed_pulse_app = FeedPulseAPI(
            FeedbackClassifier(Mock()),
            TopicDetector(GlobalModelProvider(providers)),
            ReportHandler(GlobalModelProvider(providers)),
            Mock(),
        )
        self.app = self.feed_pulse_app.flask_app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()  # Flask's test client for HTTP requests

    def test_remote_config_valid_update(self):
        """Test the remote configuration update."""
        payload = {
            "settingsList": [
                {
                    "settingName": "enable_facebook_data_collection",
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
                    "settingName": "enable_facebook_data_collection",
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
