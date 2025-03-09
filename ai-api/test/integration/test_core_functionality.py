import os
import multiprocessing
import unittest
import time
import shutil
import requests

from run_app import run_app
from enum import Enum
from typing import Iterable
from unittest.mock import ANY

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from src.spark.spark import Spark
from pyspark.sql import Row

base_path = os.path.dirname(__file__)


class FakeTable(Enum):
    TEST_STREAMING_IN = os.path.join(
        base_path, "test_streaming_integration", "test_streaming_in"
    )
    TEST_STREAMING_OUT = os.path.join(
        base_path, "test_streaming_integration", "test_streaming_out"
    )
    PAGES_DIR = os.path.join(base_path, "test_streaming_integration", "pages")


# Tests in this class have an order of execution that is sorted alphanumerically according to the test name
class TestCoreFunctionality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(FakeTable.PAGES_DIR.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_IN.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)

        cls.app_process = multiprocessing.Process(
            target=run_app,
            args=(
                FakeTable.TEST_STREAMING_IN,
                FakeTable.TEST_STREAMING_OUT,
                FakeTable.PAGES_DIR,
            ),
        )

        cls.app_process.start()

        cls.spark = configure_spark_with_delta_pip(
            SparkSession.builder.appName("TestFeedPulse")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
        ).getOrCreate()

        time.sleep(30)

    def test_01_add_valid_token(self):
        # Send a requesst to register a valid access token
        response = requests.post(
            url="http://127.0.0.1:5000/register_token/",
            json={
                "platform": "facebook",
                "ac_token": os.getenv("TEST_AC_TOKEN"),
            },
        )

        data = (
            self.spark.read.format("delta")
            .load(FakeTable.PAGES_DIR.value)
            .coalesce(1)
            .collect()
        )

        self.assertTrue(response.ok)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["platform"], "facebook")
        self.assertEqual(data[0]["ac_token"], os.getenv("TEST_AC_TOKEN"))

    def test_02_add_invalid_token(self):
        # Send a requesst to register an invalid access token
        response = requests.post(
            url="http://127.0.0.1:5000/register_token/",
            json={
                "platform": "facebook",
                "ac_token": "fake_ac_token",
            },
        )

        data = (
            self.spark.read.format("delta")
            .load(FakeTable.PAGES_DIR.value)
            .coalesce(1)
            .collect()
        )

        self.assertTrue(response.ok)
        self.assertEqual(len(data), 2)
        self.assertIn(Row(platform="facebook", ac_token="fake_ac_token"), data)
        self.assertIn(
            Row(platform="facebook", ac_token=os.getenv("TEST_AC_TOKEN")), data
        )
        self.assertEqual(data[0]["platform"], "facebook")
        self.assertEqual(data[0]["ac_token"], os.getenv("TEST_AC_TOKEN"))

    def test_03_streamed_data(self):
        # Sleep for 70 seconds so that we are sure that it pass a streaming cycle
        time.sleep(70)

        raw_comments = (
            self.spark.read.format("delta")
            .load(FakeTable.TEST_STREAMING_IN.value)
            .coalesce(1)
            .collect()
        )
        self.assertIn(
            Row(
                comment_id=ANY,
                post_id=ANY,
                content="The service was really really bad :(",
                created_time=ANY,
                platform="facebook",
            ),
            raw_comments,
        )

    def test_04_processed_data(self):
        processed_comments = (
            Spark.instance.spark.read.format("delta")
            .load(FakeTable.TEST_STREAMING_OUT.value)
            .collect()
        )

        self.assertTrue(isinstance(processed_comments[0]["related_topics"], Iterable))
        self.assertTrue(isinstance(processed_comments[1]["related_topics"], Iterable))
        self.assertIn(
            processed_comments[0]["sentiment"], ["positive", "negative", "neutral"]
        )
        self.assertIn(
            processed_comments[1]["sentiment"], ["positive", "negative", "neutral"]
        )
        self.assertIn(
            Row(
                comment_id=ANY,
                post_id=ANY,
                content="The service was really really bad :(",
                created_time=ANY,
                platform="facebook",
                sentiment=ANY,
                related_topics=ANY,
            ),
            processed_comments,
        )

        self.assertIn(
            Row(
                comment_id=ANY,
                post_id=ANY,
                content="yes, it really was very bad, but the food was mid",
                created_time=ANY,
                platform="facebook",
                sentiment=ANY,
                related_topics=ANY,
            ),
            processed_comments,
        )

    @classmethod
    def tearDownClass(cls):
        cls.app_process.terminate()
        if os.path.exists(os.path.join(base_path, "test_streaming_integration")):
            shutil.rmtree(os.path.join(base_path, "test_streaming_integration"))
