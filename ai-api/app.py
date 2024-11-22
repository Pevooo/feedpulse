import threading
from functools import wraps

from flask import Flask, render_template, request, jsonify

from src.config.feed_pulse_environment import FeedPulseEnvironment
from src.config.feed_pulse_settings import FeedPulseSettings
from src.config.response import Response
from src.config.router import Router
from src.control.feed_pulse_controller import FeedPulseController
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.report_creator import ReportCreator
from src.topic_detection.topic_detector import TopicDetector


class FeedPulseAPI:
    def __init__(
        self,
        feedback_classifier: FeedbackClassifier,
        topic_detector: TopicDetector,
        report_creator: ReportCreator,
    ):
        self.flask_app = Flask(__name__)
        self.__setup_routes()
        self.report_creator = report_creator
        self.topic_detector = topic_detector
        self.feedback_classifier = feedback_classifier

    def run(self):
        self.flask_app.run()

    def update_config(self):
        """
        Updates the config from `FeedPulseSettings`
        """
        self.report_creator = ReportCreator(FeedPulseSettings.report_creation_model())
        self.topic_detector = TopicDetector(
            FeedPulseSettings.topic_segmentation_model()
        )
        self.feedback_classifier = FeedbackClassifier(
            FeedPulseSettings.feedback_classification_model()
        )

    def __setup_routes(self):

        @self.flask_app.route(Router.MAIN_TESTING_ROUTE, methods=["POST", "GET"])
        @self.internal
        def index():
            if request.method == "GET":
                return render_template("index.html")
            else:
                access_token = request.form["access_token"]
                page_id = request.form["page_id"]
                topics = {"cleanliness", "staff", "food", "activities"}

                controller = FeedPulseController(
                    self.feedback_classifier,
                    self.topic_detector,
                    FacebookDataProvider(access_token),
                )

                result = controller.get_facebook_data_and_run_pipeline(
                    page_id,
                    topics,
                )

                report = self.report_creator.create(result)

                return render_template("index.html", report=report)

        @self.flask_app.route(Router.FACEBOOK_DATA_PROCESSING_ROUTE, methods=["GET"])
        @self.inject
        def process_facebook_data(page_id, access_token, topics):
            topics = set(topics.split(","))
            controller = FeedPulseController(
                self.feedback_classifier,
                self.topic_detector,
                FacebookDataProvider(access_token),
            )

            process_thread = threading.Thread(
                target=controller.get_facebook_data_and_run_pipeline,
                args=(page_id, topics),
                daemon=True,
            )
            process_thread.start()
            return Response.success("Successfully Started Processing")

        @self.flask_app.route(Router.REMOTE_CONFIG_ROUTE, methods=["GET", "POST"])
        def remote_config():
            if request.method == "GET":
                return jsonify(FeedPulseSettings.get_settings())
            elif request.method == "POST":
                try:
                    updated = FeedPulseSettings.update_settings(request.get_json())
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
            if FeedPulseEnvironment.is_production_environment:
                return jsonify({"error": "Endpoint does not exist"}), 404
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
        FeedbackClassifier(FeedPulseSettings.feedback_classification_model()),
        TopicDetector(FeedPulseSettings.topic_segmentation_model()),
        ReportCreator(FeedPulseSettings.report_creation_model()),
    )
    app.run()
