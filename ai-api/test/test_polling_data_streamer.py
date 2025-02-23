import os
import unittest
import shutil
from unittest.mock import patch, MagicMock

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.data_streamers.polling_data_streamer import PollingDataStreamer
from enum import Enum


class FakeTable(Enum):
    STREAM = "test_polling_data_streamer"


class TestPollingDataStreamer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        builder = (
            SparkSession.builder.appName("session")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
            .master("local[1]")
        )

        cls.spark = configure_spark_with_delta_pip(builder).getOrCreate()
        cls.mock_spark = MagicMock()
        cls.mock_spark.read = MagicMock()
        cls.mock_spark.spark = cls.spark
        cls.polling_streamer = PollingDataStreamer(
            cls.mock_spark,
            20,
            FakeTable.STREAM,
            MagicMock(),
            MagicMock(),
        )

    @patch.object(FacebookDataProvider, "get_posts")
    def test_process_page_facebook(self, mock_get_posts):
        mock_get_posts.return_value = {
            "comment_id": "fake_id",
            "content": "fake_content",
        }
        result = self.polling_streamer.process_page(
            {"ac_token": "test_token", "platform": "facebook"}
        )
        self.assertEqual(result, ({"comment_id": "fake_id", "content": "fake_content"}))

    def test_processed(self):
        self.polling_streamer.process_page = lambda row: [
            {"comment_id": "fake_id1", "content": "fake_content1"},
            {"comment_id": "fake_id2", "content": "fake_content2"},
        ]

        df = self.spark.createDataFrame(
            [
                {"ac_token": "fake_id1", "platform": "facebook"},
                {"ac_token": "fake_id2", "platform": "facebook"},
            ]
        )

        flattened_df = self.polling_streamer._get_flattened(df)

        data = [row.asDict() for row in flattened_df.collect()]

        self.assertEqual(len(data), 4)
        self.assertIn({"comment_id": "fake_id1", "content": "fake_content1"}, data)
        self.assertIn({"comment_id": "fake_id2", "content": "fake_content2"}, data)

    def test_get_unique(self):
        """Test that _get_unique removes already processed comments."""
        new_df = self.spark.createDataFrame(
            [
                {"comment_id": "id1", "content": "Comment 1"},
                {"comment_id": "id2", "content": "Comment 2"},
                {"comment_id": "id3", "content": "Comment 3"},
            ]
        )

        old_df = self.spark.createDataFrame(
            [
                {
                    "comment_id": "id2",
                    "content": "Comment 2",
                },  # Already processed
            ]
        )

        unique_df = self.polling_streamer._get_unique(new_df, old_df)

        result = {row["comment_id"] for row in unique_df.collect()}
        expected = {"id1", "id3"}  # id2 should be removed

        self.assertSetEqual(result, expected, f"Expected {expected}, but got {result}")

    @classmethod
    def tearDownClass(cls):
        for query in cls.spark.streams.active:
            query.stop()
        cls.spark.stop()

        if os.path.exists("test_polling_data_streamer"):
            shutil.rmtree("test_polling_data_streamer")
