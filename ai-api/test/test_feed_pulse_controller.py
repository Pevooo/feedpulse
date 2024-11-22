import unittest
from unittest.mock import Mock, patch, AsyncMock
from src.data.pipeline_result import PipelineResult
from src.data.feedback_result import FeedbackResult
from src.data.data_unit import DataUnit
from src.data.feedback_data_unit import FeedbackDataUnit
from src.data_providers.x_data_provider import XDataProvider
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.topic_detection.topic_detector import TopicDetector
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.control.feed_pulse_controller import FeedPulseController


class TestFeedPulseController(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.feedback_classifier = Mock(spec=FeedbackClassifier)
        self.topic_detector = Mock(spec=TopicDetector)
        self.data_provider = (
            Mock()
        )  # Generic DataProvider; specific tests will mock specific providers
        self.controller = FeedPulseController(
            feedback_classifier=self.feedback_classifier,
            topic_detector=self.topic_detector,
            data_provider=self.data_provider,
        )

    def test_run_pipeline(self):
        data_unit = Mock(spec=FeedbackDataUnit)
        all_topics = {"topic1", "topic2"}

        # Mock process method to return a DataResult for testing
        with patch.object(
            self.controller, "process", return_value=FeedbackResult(True, ("topic1",))
        ):
            result = self.controller.run_pipeline([data_unit], all_topics, None)

        self.assertIsInstance(result, PipelineResult)
        self.assertEqual(len(result.items), 1)

    def test_process_with_impression_and_topics(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}

        # Mock the classify and detect methods to control the output
        with patch.object(self.controller, "classify", return_value=True), patch.object(
            self.controller, "detect", return_value=("topic1",)
        ):
            result = self.controller.process(data_unit, org_topics)

        self.assertIsInstance(result, FeedbackResult)
        self.assertEqual(result.impression, True)
        self.assertEqual(result.topics, ("topic1",))

    def test_process_neutral_text(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}

        with patch.object(self.controller, "classify", return_value=None):
            result = self.controller.process(data_unit, org_topics)

        self.assertIsNone(result)

    def test_classify_neutral_text(self):
        data_unit = Mock(spec=DataUnit)
        self.feedback_classifier.classify = Mock(return_value=None)

        result = self.controller.classify(data_unit)

        self.assertIsNone(result)

    def test_classify_complaint_text(self):
        data_unit = Mock(spec=DataUnit)
        self.feedback_classifier.classify = Mock(return_value=False)

        result = self.controller.classify(data_unit)

        self.assertFalse(result)

    def test_detect_with_topics(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}
        self.topic_detector.detect = Mock(return_value=("topic1",))

        result = self.controller.detect(data_unit, org_topics)

        self.assertEqual(result, ("topic1",))

    def test_detect_no_topics(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}
        self.topic_detector.detect = Mock(return_value=tuple())

        result = self.controller.detect(data_unit, org_topics)

        self.assertIsNone(result)

    def test_get_facebook_data_and_run_pipeline(self):
        self.controller.data_provider = Mock(spec=FacebookDataProvider)
        page_id = "123"
        org_topics = {"topic1", "topic2"}
        data_unit = Mock(spec=DataUnit)
        self.controller.data_provider.get_posts.return_value = [data_unit]

        with patch.object(
            self.controller, "run_pipeline", return_value=PipelineResult(org_topics)
        ) as mock_run_pipeline:
            result = self.controller.get_facebook_data_and_run_pipeline(
                page_id, org_topics
            )

        self.controller.data_provider.get_posts.assert_called_once_with(page_id)
        mock_run_pipeline.assert_called_once_with([data_unit], org_topics)
        self.assertIsInstance(result, PipelineResult)

    async def test_get_x_data_and_run_pipeline_success(self):
        self.controller.data_provider = AsyncMock(spec=XDataProvider)
        search_query = "hello, world!"
        org_topics = {"topic1", "topic2"}
        num_tweets = 20

        data_unit = Mock(spec=FeedbackDataUnit)
        self.controller.data_provider.get_tweets.return_value = [data_unit]

        with patch.object(
            self.controller, "run_pipeline", return_value=PipelineResult(org_topics)
        ) as mock_run_pipeline:
            result = await self.controller.get_x_data_and_run_pipeline(
                search_query, org_topics, num_tweets
            )

        self.controller.data_provider.get_tweets.assert_called_once_with(
            num_tweets, search_query
        )
        mock_run_pipeline.assert_called_once_with([data_unit], org_topics)
        self.assertIsInstance(result, PipelineResult)
