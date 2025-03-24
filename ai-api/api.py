from datetime import datetime

from flask import Flask, request, jsonify

from src.config.settings import Settings
from src.config.response import Response
from src.config.router import Router
from src.data_streamers.data_streamer import DataStreamer
from src.exception_handling.exception_reporter import ExceptionReporter
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.lida_report_handler import LidaReportHandler
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.models.groq_model_provider import GroqModelProvider
from src.models.hf_model_provider import HFModelProvider
from src.reports.report_handler import ReportHandler
from src.data.data_manager import DataManager, SparkTable
from src.topics.topic_detector import TopicDetector
from src.webhooks.facebook_webhook_handler import FacebookWebhookHandler


class FeedPulseAPI:
    def __init__(
        self,
        feedback_classifier: FeedbackClassifier,
        topic_detector: TopicDetector,
        report_handler: ReportHandler,
        exception_reporter: ExceptionReporter,
        data_manager: DataManager,
        data_streamer: DataStreamer,
    ):
        self.flask_app = Flask(__name__)
        self.report_handler = report_handler
        self.topic_detector = topic_detector
        self.feedback_classifier = feedback_classifier
        self.reporter = exception_reporter
        self.data_manager = data_manager
        self.data_streamer = data_streamer
        self.model_providers = [
            GoogleModelProvider(),
            HFModelProvider(),
            GroqModelProvider(),
        ]
        self.global_model_provider = GlobalModelProvider(self.model_providers)
        self.lida_report_handler = LidaReportHandler(
            self.data_manager, self.global_model_provider
        )

        self.__setup_routes()
        self.__setup_exception_reporter()

    def run(self):
        self.data_manager.start_streaming_job()  # Will run on another thread
        self.flask_app.run(threaded=True)  # Will run on the main thread

    def __setup_exception_reporter(self):
        @self.flask_app.errorhandler(Exception)
        def handle_exception(e):
            """
            Global exception handler for the Flask app.
            """
            self.reporter.report(e)
            return Response.server_error(e)

    def __setup_routes(self):
        @self.flask_app.route(Router.INSTAGRAM_WEBHOOK, methods=["GET", "POST"])
        def instagram_webhook():
            # TODO: Implement Instagram Webhook

            # 1) Get the data changes and process them into a unit format
            # 2) Save the data in the streaming folder
            return Response.success("Success")

        @self.flask_app.route(Router.FACEBOOK_WEBHOOK, methods=["GET", "POST"])
        def facebook_webhook():
            # This method does not return responses from the `Response` class due to compatability issues with graph api
            if request.method == "GET":
                # Extract the query parameters sent by Facebook
                mode = request.args.get("hub.mode")
                token = request.args.get("hub.verify_token")
                challenge = request.args.get("hub.challenge")

                # Check if the mode is 'subscribe' and the verify token matches
                if mode == "subscribe" and token == "test":
                    # Respond with the challenge token from the request
                    return challenge, 200
                else:
                    # Token mismatch or wrong mode; return an error
                    return "Verification token mismatch", 403
            elif request.method == "POST":
                FacebookWebhookHandler(self.data_manager).handle(request.get_json())
                return "Event received", 200

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
                platform = data.get("platform")

                if not access_token or not page_id:
                    return Response.failure(
                        "Error occurred: Please check your access token or page_id."
                    )

                pages_df = self.data_manager.read(SparkTable.PAGES)
                existing_entry_df = None
                if pages_df is not None:
                    pages_df.cache()
                    existing_entry_df = pages_df.filter(pages_df.page_id == page_id)

                if existing_entry_df and not existing_entry_df.isEmpty():
                    self.data_manager.update(
                        SparkTable.PAGES,
                        "page_id",
                        page_id,
                        {"access_token": access_token},
                    )
                else:
                    row = [
                        {
                            "page_id": page_id,
                            "access_token": access_token,
                            "platform": platform,
                        }
                    ]
                    self.data_manager.add(SparkTable.PAGES, row).result()

                return Response.success("Registered successfully")
            except Exception as e:
                return Response.failure(f"Error occurred: {str(e)}")

        @self.flask_app.route(Router.REPORT, methods=["GET", "POST"])
        def get_report():
            try:
                data = request.json
                page_id = data.get("page_id")
                start_date = datetime.fromisoformat(data.get("start_date"))
                end_date = datetime.fromisoformat(data.get("end_date"))
                report = self.lida_report_handler.generate_report(
                    page_id, start_date, end_date
                )
                return Response.success(report)
            except Exception as e:
                print(e)
                return Response.failure(str(e))
