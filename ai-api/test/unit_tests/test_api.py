import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from api import FeedPulseAPI
from flask import jsonify

from src.config.response import Response


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

    @patch("src.config.environment.Environment.is_production_environment", True)
    def test_internal_route_in_production(self):
        """Test that the route returns 404 in production."""
        with self.app.test_request_context():
            response = self.client.get("/internal-route")
            self.assertEqual(response.status_code, 404)
            json_data = response.get_json()
            self.assertEqual(json_data["status"], "FAILURE")
            self.assertEqual(json_data["body"], "Endpoint does not exist")

    @patch("src.config.environment.Environment.is_production_environment", False)
    def test_internal_route_in_non_production(self):
        """Test that the route is accessible in non-production."""
        with self.app.test_request_context():
            response = self.client.get("/internal-route")
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data["status"], "SUCCESS")
            self.assertEqual(
                json_data["body"]["message"],
                "Accessible only in non-production environments",
            )

    def test_inject_query_string(self):
        """Test that query string parameters are injected into the function."""
        with self.app.test_request_context():
            response = self.client.get("/inject-route?param1=value1&param2=value2")
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data["status"], "SUCCESS")
            self.assertEqual(json_data["body"]["param1"], "value1")
            self.assertEqual(json_data["body"]["param2"], "value2")

    def test_inject_form_data(self):
        """Test that form parameters are injected into the function."""
        with self.app.test_request_context():
            response = self.client.post(
                "/inject-route",
                data={"param1": "form_value1", "param2": "form_value2"},
            )
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertEqual(json_data["status"], "SUCCESS")
            self.assertEqual(json_data["body"]["param1"], "form_value1")
            self.assertEqual(json_data["body"]["param2"], "form_value2")

    def test_exception_reporting(self):
        with self.app.test_request_context():
            response = self.client.get("/exception-endpoint")

        self.assertEqual(response.status_code, 500)
        self.mock_exception_reporter.report.assert_called_once()

    def test_report_handling_route(self):
        self.mock_report_handler.create = Mock(return_value="fake_report")

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
        self.mock_report_handler.create.assert_called_once_with(
            "fake_page_id",
            datetime(2024, 3, 4, 15, 30, 0),
            datetime(2025, 7, 10, 8, 15, 45),
        )
        self.assertEqual(response.get_json().get("status"), "SUCCESS")
        self.assertEqual(response.get_json().get("body"), "fake_report")
