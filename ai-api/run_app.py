from transformers import pipeline

from api import FeedPulseAPI
from src.concurrency.concurrency_manager import ConcurrencyManager
from src.data_streamers.polling_data_streamer import PollingDataStreamer
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.models.hf_model_provider import HFModelProvider
from src.topics.topic_detector import TopicDetector
from src.spark.spark import Spark, SparkTable
from src.reports.report_handler import ReportHandler
from src.exception_handling.exception_reporter import ExceptionReporter


def run_app(
    stream_in=SparkTable.INPUT_COMMENTS,
    stream_out=SparkTable.PROCESSED_COMMENTS,
    paged_dir=SparkTable.PAGES,
):
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

    # Define Concurrency Manager
    concurrency_manager = ConcurrencyManager()

    # Define Spark Singleton
    spark = Spark(
        stream_in=stream_in,
        stream_out=stream_out,
        feedback_classification_batch_function=feedback_classifier.classify,
        topic_detection_batch_function=topic_detector.detect,
        concurrency_manager=concurrency_manager,
    )

    # Define Concurrency Manager
    concurrency_manager = ConcurrencyManager(spark)

    report_handler = ReportHandler(model_provider, spark, stream_out)

    # Define Streamer
    data_streamer = PollingDataStreamer(
        spark=spark,
        trigger_time=60,
        streaming_in=stream_in,
        streaming_out=stream_out,
        pages_dir=paged_dir,
        concurrency_manager=concurrency_manager,
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


if __name__ == "__main__":
    run_app()
