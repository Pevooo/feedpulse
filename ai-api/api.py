from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify
from transformers import pipeline

from src.config.environment import Environment
from src.config.settings import Settings
from src.config.response import Response
from src.config.router import Router
from src.data_streamers.data_streamer import DataStreamer
from src.data_streamers.polling_data_streamer import PollingDataStreamer
from src.exception_handling.exception_reporter import ExceptionReporter
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.models.hf_model_provider import HFModelProvider
from src.reports.report_handler import ReportHandler
from src.spark.spark import Spark, SparkTable
from src.topics.topic_detector import TopicDetector


class FeedPulseAPI:
    def __init__(
        self,
        feedback_classifier: FeedbackClassifier,
        topic_detector: TopicDetector,
        report_handler: ReportHandler,
        exception_reporter: ExceptionReporter,
        spark: Spark,
        data_streamer: DataStreamer,
    ):
        self.flask_app = Flask(__name__)
        self.report_handler = report_handler
        self.topic_detector = topic_detector
        self.feedback_classifier = feedback_classifier
        self.reporter = exception_reporter
        self.spark = spark
        self.data_streamer = data_streamer

        self.__setup_routes()
        self.__setup_exception_reporter()

        spark.start_streaming_job()
        data_streamer.start_streaming()

    def run(self):
        self.flask_app.run()

    def __setup_exception_reporter(self):
        @self.flask_app.errorhandler(Exception)
        def handle_exception(e):
            """
            Global exception handler for the Flask app.
            """
            self.reporter.report(e)
            return Response.server_error()

    def __setup_routes(self):
        @self.flask_app.route(Router.INSTAGRAM_WEBHOOK, methods=["POST"])
        def instagram_webhook():
            # TODO: Implement Instagram Webhook

            # 1) Get the data changes and process them into a unit format
            # 2) Save the data in the streaming folder
            pass

        @self.flask_app.route(Router.FACEBOOK_WEBHOOK, methods=["POST"])
        def facebook_webhook():
            # TODO: Implement Facebook Webhook

            # 1) Get the data changes and process them into a unit format
            # 2) Save the data in the streaming folder
            pass

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

        @self.flask_app.route(Router.REGISTER_AC_TOKEN, methods=["POST"])
        def register_ac_token():
            """
            Register the access token
            """
            try:
                data = request.json
                access_token = data.get("access_token")
                page_id = data.get("page_id")

                if not access_token or not page_id:
                    return Response.failure("Error occurred: ")

                pages_df = self.spark.read(SparkTable.PAGES)
                existing_entry = None
                if pages_df is not None:
                    existing_entry = pages_df.filter(
                        pages_df.page_id == page_id
                    ).first()
                if existing_entry:
                    self.spark.update(
                        SparkTable.PAGES,
                        "page_id",
                        page_id,
                        {"access_token": access_token},
                    )
                else:
                    row = [{"page_id": page_id, "access_token": access_token}]
                    self.spark.add(SparkTable.PAGES, row)

                return Response.success()
            except Exception as e:
                print(e)
                return Response.failure("Error occurred: ")

        @self.flask_app.route(Router.REPORT, methods=["GET", "POST"])
        def get_report():
            try:
                data = request.json
                page_id = data.get("page_id")
                start_date = datetime.fromisoformat(data.get("start_date"))
                end_date = datetime.fromisoformat(data.get("end_date"))
                report = self.report_handler.create(page_id, start_date, end_date)
                return Response.success(report)
            except Exception as e:
                print(e)
                return Response.failure(str(e))

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

    # Define the global model provider (and load balancer)
    model_provider = GlobalModelProvider(
        providers=[GoogleModelProvider(), HFModelProvider()],
        retry_delay=60,
    )

    # Define Processing Components
    feedback_classifier = FeedbackClassifier(
        classifier=pipeline(
            "sentiment-analysis", "tabularisai/multilingual-sentiment-analysis"
        )
    )
    topic_detector = TopicDetector(model_provider)

    # Define Spark Singleton
    spark = Spark(
        stream_in=SparkTable.INPUT_COMMENTS,
        stream_out=SparkTable.PROCESSED_COMMENTS,
        feedback_classification_batch_function=feedback_classifier.classify,
        topic_detection_batch_function=topic_detector.detect,
    )

    report_handler = ReportHandler(
        provider=model_provider,
        spark=spark,
        comments_table=SparkTable.PROCESSED_COMMENTS,
    )

    # Define Streamer
    data_streamer = PollingDataStreamer(
        spark=spark,
        trigger_time=60,
        streaming_in=SparkTable.INPUT_COMMENTS,
        streaming_out=SparkTable.PROCESSED_COMMENTS,
        pages_dir=SparkTable.PAGES,
    )

    # Define Exception Reporter
    exception_reporter = ExceptionReporter(spark)

    # Define the api class
    app = FeedPulseAPI(
        feedback_classifier=feedback_classifier,
        topic_detector=topic_detector,
        report_handler=report_handler,
        exception_reporter=exception_reporter,
        spark=spark,
        data_streamer=data_streamer,
    )

    # Run the app
    app.run()
