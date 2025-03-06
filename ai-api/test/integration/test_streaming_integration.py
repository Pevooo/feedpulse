import os
import unittest
import time
import shutil
import threading

from run_app import run_app
from enum import Enum
from typing import Iterable
from unittest.mock import ANY

from transformers import pipeline

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from src.spark.spark import Spark


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
    def test_integration(self):
        os.makedirs(FakeTable.PAGES_DIR.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_IN.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)
        spark = configure_spark_with_delta_pip(
            SparkSession.builder.appName("FeedPulse")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
        ).getOrCreate()
        pages_df = spark.createDataFrame(
            [
                {
                    "platform": "facebook",
                    "ac_token": os.getenv("TEST_AC_TOKEN"),
                },
                {
                    "platform": "facebook",
                    "ac_token": "fake_ac_token",  # Added to ensure an exception would cause no problem
                },
            ]
        )
        pages_df.write.format("delta").mode("overwrite").save(FakeTable.PAGES_DIR.value)
        spark.stop()

        thread = threading.Thread(target=run_app, args=(
            FakeTable.TEST_STREAMING_IN,
            FakeTable.TEST_STREAMING_OUT,
            FakeTable.PAGES_DIR,))
        
        thread.start()
        time.sleep(80)

        result_df = Spark.instance.spark.read.format("delta").load(
            FakeTable.TEST_STREAMING_OUT.value
        )

        data = [row.asDict() for row in result_df.collect()]
        self.assertTrue(isinstance(data[0]["related_topics"], Iterable))
        self.assertTrue(isinstance(data[1]["related_topics"], Iterable))
        self.assertIn(data[0]["sentiment"], ["positive", "negative", "neutral"])
        self.assertIn(data[1]["sentiment"], ["positive", "negative", "neutral"])
        self.assertIn(
            {
                "comment_id": ANY,
                "post_id": ANY,
                "content": "The service was really really bad :(",
                "created_time": ANY,
                "platform": "facebook",
                "sentiment": ANY,
                "related_topics": ANY,
            },
            data,
        )

        self.assertIn(
            {
                "comment_id": ANY,
                "post_id": ANY,
                "content": "yes, it really was very bad, but the food was mid",
                "created_time": ANY,
                "platform": "facebook",
                "sentiment": ANY,
                "related_topics": ANY,
            },
            data,
        )

    def tearDown(self):
        for query in self.spark.spark.streams.active:
            query.stop()
        self.spark.spark.stop()

        if os.path.exists(os.path.join(base_path, "test_streaming_integration")):
            shutil.rmtree(os.path.join(base_path, "test_streaming_integration"))
        