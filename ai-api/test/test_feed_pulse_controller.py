import unittest
from unittest.mock import Mock, patch, MagicMock
from src.data.pipeline_result import PipelineResult
from src.data.feedback_result import FeedbackResult
from src.data.feedback_data_unit import FeedbackDataUnit
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.report_handler import ReportHandler
from src.topics.feedback_topic import FeedbackTopic
from src.topics.topic_detector import TopicDetector
from src.control.feed_pulse_controller import FeedPulseController


class TestFeedPulseController(unittest.TestCase):
    def setUp(self):
        self.feedback_classifier = Mock(spec=FeedbackClassifier)
        self.topic_detector = Mock(spec=TopicDetector)
        self.data_provider = (
            Mock()
        )  # Generic DataProvider; specific tests will mock specific providers
        self.report_handler = Mock(spec=ReportHandler)

        self.controller = FeedPulseController(
            feedback_classifier=self.feedback_classifier,
            topic_detector=self.topic_detector,
            data_provider=self.data_provider,
            report_handler=self.report_handler,
        )

    def test_run_pipeline(self):
        data_unit = MagicMock(spec=FeedbackDataUnit)
        all_topics = {"wifi", "cleanliness"}

        # Mock process method to return a DataResult for testing
        with patch.object(
            self.controller,
            "process",
            return_value=FeedbackResult(True, (FeedbackTopic.WIFI,)),
        ):
            result = self.controller.run_pipeline([data_unit], all_topics, None)

        self.assertIsInstance(result, PipelineResult)
        self.assertEqual(len(result.items), 1)
