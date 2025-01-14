import threading
from functools import wraps

from flask import Flask, render_template, request, jsonify

from src.config.environment import Environment
from src.config.settings import Settings
from src.config.response import Response
from src.config.router import Router
from src.control.feed_pulse_controller import FeedPulseController
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.exception_handling.ExceptionReporter import ExceptionReporter
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.report_handler import ReportHandler
from src.topics.topic_detector import TopicDetector


class FeedPulseAPI:
    def __init__(
        self,
        feedback_classifier: FeedbackClassifier,
        topic_detector: TopicDetector,
        report_handler: ReportHandler,
        exception_reporter: ExceptionReporter,
    ):
        self.flask_app = Flask(__name__)
        self.__setup_routes()
        self.report_handler = report_handler
        self.topic_detector = topic_detector
        self.feedback_classifier = feedback_classifier
        self.reporter = exception_reporter

    def run(self):
        self.flask_app.run()

    def update_config(self):
        """
        Updates the config from `FeedPulseSettings`
        """
        self.report_handler = ReportHandler(Settings.report_creation_model())
        self.topic_detector = TopicDetector(Settings.topic_segmentation_model())
        self.feedback_classifier = FeedbackClassifier(
            Settings.feedback_classification_model()
        )

    def __setup_exception_reporter(self):
        @self.flask_app.errorhandler(Exception)
        def handle_exception(e):
            """
            Global exception handler for the Flask app.
            """
            self.reporter.report(e)
            return Response.server_error()

    def __setup_routes(self):

        @self.flask_app.route(Router.MAIN_TESTING_ROUTE, methods=["POST", "GET"])
        @self.internal
        def index():
            if request.method == "GET":
                return render_template("index.html")
            else:
                access_token = request.form["access_token"]
                topics = {"cleanliness", "staff", "food", "wifi"}

                controller = FeedPulseController(
                    self.feedback_classifier,
                    self.topic_detector,
                    FacebookDataProvider(access_token),
                    self.report_handler,
                )

                data_units = controller.fetch_facebook_data()
                result = controller.run_pipeline(data_units, topics)
                report = controller.report_handler.create(result)

                return render_template("index.html", report=report)

        @self.flask_app.route(Router.FACEBOOK_DATA_PROCESSING_ROUTE, methods=["GET"])
        @self.inject
        def process_facebook_data(
            page_id: str, access_token: str, topics: str, url: str
        ):
            topics = set(topics.split(","))
            controller = FeedPulseController(
                self.feedback_classifier,
                self.topic_detector,
                FacebookDataProvider(access_token),
                self.report_handler,
            )

            process_thread = threading.Thread(
                target=controller.run_all_steps_facebook,
                args=(page_id, topics, url),
                daemon=True,
            )
            process_thread.start()
            return Response.success("Successfully Started Processing")

        @self.flask_app.route(Router.REMOTE_CONFIG_ROUTE, methods=["GET", "POST"])
        def remote_config():
            if request.method == "GET":
                return jsonify(Settings.get_settings())
            elif request.method == "POST":
                try:
                    updated = Settings.update_settings(request.get_json())
                    if updated:
                        return "Success", 200

                    return "Failure", 400
                except Exception as e:
                    print(e)
                    return "Failure", 400

    @staticmethod
    def internal(func):
        """Mark this route as internal and hide it when the app is on production."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            if Environment.is_production_environment:
                return Response.not_found()
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def inject(func):
        """Injects form and string parameters into the function parameters"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs.update(request.args)  # For query string parameters
            kwargs.update(request.form)  # For form data in POST requests
            return func(*args, **kwargs)

        return wrapper


if __name__ == "__main__":
    app = FeedPulseAPI(
        FeedbackClassifier(Settings.feedback_classification_model()),
        TopicDetector(Settings.topic_segmentation_model()),
        ReportHandler(Settings.report_creation_model()),
        ExceptionReporter(),
    )
    app.run()
