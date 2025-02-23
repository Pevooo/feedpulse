import os
import unittest
import time
import datetime

from enum import Enum
from typing import Iterable
from unittest.mock import ANY

from transformers import pipeline

from src.data_streamers.polling_data_streamer import PollingDataStreamer
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from src.spark.spark import Spark
from src.topics.topic_detector import TopicDetector

base_path = os.path.dirname(__file__)


class FakeTable(Enum):
    TEST_STREAMING_IN = os.path.join(
        base_path, "test_streaming_integration", "test_streaming_in"
    )
    TEST_STREAMING_OUT = os.path.join(
        base_path, "test_streaming_integration", "test_streaming_out"
    )
    PAGES_DIR = os.path.join(base_path, "test_streaming_integration", "pages")


class TestStreamingIntegration(unittest.TestCase):
    def setUp(self):
        self.feedback_classifier = FeedbackClassifier(
            pipeline(
                "sentiment-analysis", "tabularisai/multilingual-sentiment-analysis"
            )
        )
        self.model_provider = GlobalModelProvider([GoogleModelProvider()])
        self.topic_detector = TopicDetector(self.model_provider)
        self.spark = Spark(
            FakeTable.TEST_STREAMING_IN,
            FakeTable.TEST_STREAMING_OUT,
            self.feedback_classifier.classify,
            self.topic_detector.detect,
        )
        self.streamer = PollingDataStreamer(
            spark=self.spark,
            trigger_time=30,
            streaming_in=FakeTable.TEST_STREAMING_IN,
            streaming_out=FakeTable.TEST_STREAMING_OUT,
            pages_dir=FakeTable.PAGES_DIR,
        )

        os.makedirs(FakeTable.PAGES_DIR.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_IN.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)

    def test_integration(self):
        pages_df = self.spark.spark.createDataFrame(
            [{"platform": "facebook", "ac_token": "fake_ac_token"}]
        )
        pages_df.write.format("delta").mode("overwrite").save(FakeTable.PAGES_DIR.value)
        created_time_str = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        ).isoformat()
        self.streamer.process_page = lambda row: (
            {
                "comment_id": "fake_id1",
                "post_id": "fake_post_id1",
                "content": "this place is not clean",
                "created_time": created_time_str,
                "platform": "facebook",
            },
            {
                "comment_id": "fake_id2",
                "post_id": "fake_post_id2",
                "content": "this place is the best",
                "created_time": created_time_str,
                "platform": "facebook",
            },
        )

        self.spark.start_streaming_job()
        time.sleep(5)
        self.streamer.start_streaming()

        # Sleeping until streamer streams data successfully and receiver receives data and process it and saves it successfully
        time.sleep(60)

        result_df = self.spark.spark.read.format("delta").load(
            FakeTable.TEST_STREAMING_OUT.value
        )

        data = [row.asDict() for row in result_df.collect()]
        print(data)
        self.assertTrue(isinstance(data[0]["related_topics"], Iterable))
        self.assertTrue(isinstance(data[1]["related_topics"], Iterable))
        self.assertIn(data[0]["sentiment"], ["positive", "negative", "neutral"])
        self.assertIn(data[1]["sentiment"], ["positive", "negative", "neutral"])
        self.assertIn(
            {
                "comment_id": "fake_id1",
                "post_id": "fake_post_id1",
                "content": "this place is not clean",
                "created_time": created_time_str,
                "platform": "facebook",
                "sentiment": ANY,
                "related_topics": ANY,
            },
            data,
        )

        self.assertIn(
            {
                "comment_id": "fake_id2",
                "post_id": "fake_post_id2",
                "content": "this place is the best",
                "created_time": created_time_str,
                "platform": "facebook",
                "sentiment": ANY,
                "related_topics": ANY,
            },
            data,
        )
