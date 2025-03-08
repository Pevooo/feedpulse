from datetime import datetime

from flask import Flask, request, jsonify

from src.config.settings import Settings
from src.config.response import Response
from src.config.router import Router
from src.data_streamers.data_streamer import DataStreamer
from src.exception_handling.exception_reporter import ExceptionReporter
from src.feedback_classification.feedback_classifier import FeedbackClassifier
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

    def run(self):
        self.spark.start_streaming_job()  # Will run on another thread
        self.data_streamer.start_streaming()  # Will run on another thread
        self.flask_app.run()  # Will run on the main thread

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
            return Response.success("Success")

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
