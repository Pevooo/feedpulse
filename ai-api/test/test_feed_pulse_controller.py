import unittest
from unittest.mock import Mock, AsyncMock, patch
from src.control.pipeline_result import PipelineResult
from src.data.data_result import DataResult
from src.data.data_unit import DataUnit
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.topic_detection.topic_detector import TopicDetector
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.control.feed_pulse_controller import FeedPulseController


class TestFeedPulseController(unittest.TestCase):
    def setUp(self):
        self.feedback_classifier = Mock(spec=FeedbackClassifier)
        self.topic_detector = Mock(spec=TopicDetector)
        self.data_provider = Mock()  # Generic DataProvider; specific tests will mock specific providers
        self.controller = FeedPulseController(
            feedback_classifier=self.feedback_classifier,
            topic_detector=self.topic_detector,
            data_provider=self.data_provider
        )

    def test_run_pipeline(self):
        data_unit = Mock(spec=DataUnit)
        all_topics = {"topic1", "topic2"}

        # Mock process method to return a DataResult for testing
        with patch.object(self.controller, 'process', return_value=DataResult(True, ("topic1",))):
            result = self.controller.run_pipeline([data_unit], all_topics)

        self.assertIsInstance(result, PipelineResult)
        self.assertEqual(len(result.items), 1)

    def test_process_with_impression_and_topics(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}

        # Mock the classify and detect methods to control the output
        with patch.object(self.controller, 'classify', return_value=True), \
                patch.object(self.controller, 'detect', return_value=("topic1",)):
            result = self.controller.process(data_unit, org_topics)

        self.assertIsInstance(result, DataResult)
        self.assertEqual(result.impression, True)
        self.assertEqual(result.topics, ("topic1",))

    def test_process_neutral_text(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}

        with patch.object(self.controller, 'classify', return_value=None):
            result = self.controller.process(data_unit, org_topics)

        self.assertIsNone(result)

    def test_classify_neutral_text(self):
        data_unit = Mock(spec=DataUnit)
        self.feedback_classifier.return_value = Mock(text_type="neutral", has_topic=False)

        result = self.controller.classify(data_unit)

        self.assertIsNone(result)

    def test_classify_complaint_text(self):
        data_unit = Mock(spec=DataUnit)
        self.feedback_classifier.return_value = Mock(text_type="complaint", has_topic=True)

        result = self.controller.classify(data_unit)

        self.assertFalse(result)

    def test_detect_with_topics(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}
        self.topic_detector.return_value = Mock(topics=("topic1",))

        result = self.controller.detect(data_unit, org_topics)

        self.assertEqual(result, ("topic1",))

    def test_detect_no_topics(self):
        data_unit = Mock(spec=DataUnit)
        org_topics = {"topic1", "topic2"}
        self.topic_detector.return_value = Mock(topics=())

        result = self.controller.detect(data_unit, org_topics)

        self.assertIsNone(result)

    def test_get_facebook_data_and_run_pipeline(self):
        self.controller.data_provider = Mock(spec=FacebookDataProvider)
        page_id = "123"
        org_topics = {"topic1", "topic2"}
        data_unit = Mock(spec=DataUnit)
        self.controller.data_provider.get_posts.return_value = [data_unit]

        with patch.object(self.controller, 'run_pipeline',
                          return_value=PipelineResult(org_topics)) as mock_run_pipeline:
            result = self.controller.get_facebook_data_and_run_pipeline(page_id, org_topics)

        self.controller.data_provider.get_posts.assert_called_once_with(page_id)
        mock_run_pipeline.assert_called_once_with([data_unit], org_topics)
        self.assertIsInstance(result, PipelineResult)

    # @patch('src.control.feed_pulse_controller.XDataProvider')
    # def test_get_x_data_and_run_pipeline(self, MockXDataProvider):
    #     self.controller.data_provider = Mock(spec=MockXDataProvider)
    #     query = "example"
    #     org_topics = {"topic1", "topic2"}
    #     data_unit = Mock(spec=DataUnit)
    #     self.controller.data_provider.get_tweets = AsyncMock(return_value=[data_unit])
    #
    #     with patch.object(self.controller, 'run_pipeline',
    #                       return_value=PipelineResult(org_topics)) as mock_run_pipeline:
    #         result = self.controller.get_x_data_and_run_pipeline(query, org_topics)
    #
    #     #self.controller.data_provider.get_tweets.assert_called_once_with(20, query)
    #     mock_run_pipeline.assert_called_once_with([data_unit], org_topics)
    #     self.assertIsInstance(result, PipelineResult)


if __name__ == "__main__":
    unittest.main()
