import unittest
from unittest.mock import Mock

from src.concurrency.concurrency_manager import ConcurrencyManager
from src.data_streamers.polling_data_streamer import PollingDataStreamer
from src.spark.spark import Spark


class TestPollingDataStreamer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.concurrency_manager = ConcurrencyManager()
        cls.spark = Spark(Mock(), Mock(), Mock(), Mock(), cls.concurrency_manager)
        cls.streamer = PollingDataStreamer(
            cls.spark, Mock(), Mock(), Mock(), Mock(), cls.concurrency_manager
        )

    def test_unique(self):
        df1 = self.spark.spark.createDataFrame(
            [
                {"comment_id": "123", "content": "hi1"},
                {"comment_id": "456", "content": "hi2"},
                {"comment_id": "789", "content": "hi3"},
            ]
        )

        df2 = self.spark.spark.createDataFrame(
            [
                {"comment_id": "123", "content": "fake"},
                {"comment_id": "789", "content": "fake"},
            ]
        )

        df_unique = self.streamer._get_unique(df1, df2)

        data = [row.asDict() for row in df_unique.collect()]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["content"], "hi2")
        self.assertEqual(data[0]["comment_id"], "456")

    @classmethod
    def tearDownClass(cls):
        cls.spark.spark.stop()
