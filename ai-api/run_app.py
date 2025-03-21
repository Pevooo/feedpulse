from transformers import pipeline

from api import FeedPulseAPI
from src.concurrency.concurrency_manager import ConcurrencyManager
from src.config.settings import Settings
from src.data_streamers.polling_data_streamer import PollingDataStreamer
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.models.hf_model_provider import HFModelProvider
from src.topics.topic_detector import TopicDetector
from src.data.data_manager import DataManager, SparkTable
from src.reports.report_handler import ReportHandler
from src.exception_handling.exception_reporter import ExceptionReporter


def run_app(
    stream_in=SparkTable.INPUT_COMMENTS,
    stream_out=SparkTable.PROCESSED_COMMENTS,
    paged_dir=SparkTable.PAGES,
    polling_streamer_trigger_time=60,
    global_model_provider_retry_delay=60,
):
    # Define the global model provider (and load balancer)
    model_provider = GlobalModelProvider(
        providers=[GoogleModelProvider(), HFModelProvider()],
        retry_delay=global_model_provider_retry_delay,
    )

    # Define Processing Components
    feedback_classifier = FeedbackClassifier(
        classifier=pipeline(
            "sentiment-analysis", "tabularisai/multilingual-sentiment-analysis"
        )
    )
    topic_detector = TopicDetector(model_provider)

    # Define Concurrency Manager
    concurrency_manager = ConcurrencyManager()

    # Define Data Manager Singleton
    data_manager = DataManager(
        stream_in=stream_in,
        stream_out=stream_out,
        feedback_classification_batch_function=feedback_classifier.classify,
        topic_detection_batch_function=topic_detector.detect,
        concurrency_manager=concurrency_manager,
        pages=paged_dir,
    )

    # Define Concurrency Manager
    concurrency_manager = ConcurrencyManager()

    report_handler = ReportHandler(model_provider, data_manager, stream_out)

    # Define Streamer
    data_streamer = PollingDataStreamer(
        data_manager=data_manager,
        trigger_time=polling_streamer_trigger_time,
        concurrency_manager=concurrency_manager,
    )

    # Define Exception Reporter
    exception_reporter = ExceptionReporter(data_manager)

    # Define the api class
    app = FeedPulseAPI(
        feedback_classifier=feedback_classifier,
        topic_detector=topic_detector,
        report_handler=report_handler,
        exception_reporter=exception_reporter,
        spark=data_manager,
        data_streamer=data_streamer,
    )

    Settings.register_observer(model_provider)
    Settings.register_observer(data_manager)
    Settings.register_observer(data_streamer)

    # Run the app
    app.run()


if __name__ == "__main__":
    run_app()
