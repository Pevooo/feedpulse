import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from api import FeedPulseAPI
from flask import jsonify

from src.config.environment import Environment
from src.config.response import Response
from src.reports.report import Report


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.mock_exception_reporter = Mock()
        self.mock_exception_reporter.report = Mock()
        self.mock_report_handler = Mock()
        self.feed_pulse_app = FeedPulseAPI(
            Mock(),
            Mock(),
            self.mock_report_handler,
            self.mock_exception_reporter,
            Mock(),
            Mock(),
            Mock(),
        )
        self.app = self.feed_pulse_app.flask_app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()  # Flask's test client for HTTP requests

        # Example route for testing
        @self.app.route("/deprecated-endpoint")
        @Response.deprecated
        def deprecated_endpoint():
            return Response.success({"message": "This is a deprecated endpoint"})

        @self.app.errorhandler(Exception)
        def handle_exception(e):
            self.mock_exception_reporter.report(e)
            response = jsonify({"error": "Internal Server Error", "message": str(e)})
            return response, 500

        @self.app.route("/exception-endpoint")
        def exception_endpoint():
            raise Exception()

    def test_deprecated_response(self):
        # Simulate a request to the deprecated endpoint
        with self.app.test_request_context():
            response = self.client.get("/deprecated-endpoint")
            self.assertEqual(response.status_code, 200)

            # Parse the JSON response
            json_data = response.get_json()
            self.assertIn("deprecation_warning", json_data)
            self.assertEqual(
                json_data["deprecation_warning"],
                "This endpoint is deprecated and will be removed in future versions.",
            )
            self.assertEqual(json_data["status"], "SUCCESS")
            self.assertEqual(
                json_data["body"]["message"], "This is a deprecated endpoint"
            )

    def test_exception_reporting(self):
        with self.app.test_request_context():
            response = self.client.get("/exception-endpoint")

        self.assertEqual(response.status_code, 500)
        self.mock_exception_reporter.report.assert_called_once()

    def test_report_handling_route(self):

        fake_report = Report()
        fake_report.goals.append("Goal 1: g1")
        fake_report.chart_rasters.append("r1")

        self.mock_report_handler.generate_report = Mock(return_value=fake_report)

        with self.app.test_request_context():
            response = self.client.post(
                "/report",
                json={
                    "page_id": "fake_page_id",
                    "start_date": "2024-03-04T15:30:00",
                    "end_date": "2025-07-10T08:15:45",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.mock_report_handler.generate_report.assert_called_once_with(
            "fake_page_id",
            datetime(2024, 3, 4, 15, 30, 0),
            datetime(2025, 7, 10, 8, 15, 45),
        )
        self.assertEqual(response.get_json().get("status"), "SUCCESS")
        self.assertEqual(
            response.get_json().get("body"),
            {
                "goals": ["Goal 1: g1"],
                "chart_rasters": ["r1"],
                "metrics": {},
                "summary": "",
            },
        )

    def test_facebook_webhook_get(self):
        """Test GET request for Facebook webhook verification."""
        valid_token = Environment.webhook_token
        challenge_value = "123456"

        response = self.client.get(
            "/facebook_webhook",  # Ensure this matches `Router.FACEBOOK_WEBHOOK`
            query_string={
                "hub.mode": "subscribe",
                "hub.verify_token": valid_token,
                "hub.challenge": challenge_value,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), challenge_value)

    def test_facebook_webhook_get_invalid_token(self):
        """Test GET request with an invalid verification token."""
        response = self.client.get(
            "/facebook_webhook",
            query_string={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong_token",
                "hub.challenge": "123456",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.decode("utf-8"), "Verification token mismatch")

    @patch("src.webhooks.facebook_webhook_handler.FacebookWebhookHandler.handle")
    def test_facebook_webhook_post(self, mock_handle):
        """Test POST request handling an event."""

        response = self.client.post("/facebook_webhook", json={"some": "event_data"})

        mock_handle.assert_called_once_with({"some": "event_data"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Event received")

    def test_instagram_webhook_get(self):
        """Test GET request for Instagram webhook verification."""
        valid_token = Environment.webhook_token
        challenge_value = "123456"

        response = self.client.get(
            "/instagram_webhook",
            query_string={
                "hub.mode": "subscribe",
                "hub.verify_token": valid_token,
                "hub.challenge": challenge_value,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), challenge_value)

    def test_instagram_webhook_get_invalid_token(self):
        """Test GET request with an invalid verification token."""
        response = self.client.get(
            "/instagram_webhook",
            query_string={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong_token",
                "hub.challenge": "123456",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.decode("utf-8"), "Verification token mismatch")

    @patch("src.webhooks.instagram_webhook_handler.InstagramWebhookHandler.handle")
    def test_instagram_webhook_post(self, mock_handle):
        """Test POST request handling an event."""

        response = self.client.post("/instagram_webhook", json={"some": "event_data"})

        mock_handle.assert_called_once_with({"some": "event_data"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Event received")
