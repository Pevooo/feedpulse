from transformers import pipeline

from api import FeedPulseAPI
from src.concurrency.concurrency_manager import ConcurrencyManager
from src.config.settings import Settings
from src.data_streamers.polling_data_streamer import PollingDataStreamer
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.models.groq_model_provider import GroqModelProvider
from src.models.hf_model_provider import HFModelProvider
from src.models.or_model_provider import ORModelProvider
from src.redis.redis_manager import RedisManager
from src.reports.lida_report_handler import LidaReportHandler
from src.topics.topic_detector import TopicDetector
from src.data.data_manager import DataManager, SparkTable
from src.exception_handling.exception_reporter import ExceptionReporter


def run_app(
    stream_in=SparkTable.INPUT_COMMENTS,
    stream_out=SparkTable.PROCESSED_COMMENTS,
    paged_dir=SparkTable.PAGES,
    polling_streamer_trigger_time=60,
    global_model_provider_retry_delay=60,
    spark_trigger_time="5 minutes",
):
    # Define the global model provider (and load balancer)
    model_provider = GlobalModelProvider(
        providers=[
            GoogleModelProvider(),
            ORModelProvider(),
            HFModelProvider(),
            GroqModelProvider(),
        ],
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
        spark_trigger_time=spark_trigger_time,
    )

    # Define Concurrency Manager
    concurrency_manager = ConcurrencyManager()

    redis_manager = RedisManager()

    report_handler = LidaReportHandler(data_manager, model_provider, redis_manager)

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
        data_manager=data_manager,
        data_streamer=data_streamer,
        redis_manager=redis_manager,
    )

    Settings.register_observer(model_provider)
    Settings.register_observer(data_manager)
    Settings.register_observer(data_streamer)

    # Run the app
    app.run()


if __name__ == "__main__":
    run_app()
