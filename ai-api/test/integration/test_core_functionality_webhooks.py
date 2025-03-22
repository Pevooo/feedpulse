import json
import os
import multiprocessing
import unittest
import time
import shutil
import requests
from pyspark.sql.types import StructField, StringType, StructType

from run_app import run_app
from enum import Enum
from typing import Iterable
from unittest.mock import ANY

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql import Row

from src.data.spark_table import SparkTable

base_path = os.path.dirname(__file__)


class FakeTable(Enum):
    TEST_STREAMING_IN = os.path.join(
        base_path, "test_streaming_integration", "test_streaming_in"
    )
    TEST_STREAMING_OUT = os.path.join(
        base_path, "test_streaming_integration", "test_streaming_out"
    )


# Tests in this class have an order of execution that is sorted alphanumerically according to the test name
class TestCoreFunctionality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(SparkTable.PAGES.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_IN.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)

        cls.app_process = multiprocessing.Process(
            target=run_app,
            args=(
                FakeTable.TEST_STREAMING_IN,
                FakeTable.TEST_STREAMING_OUT,
                SparkTable.PAGES,
                5,
            ),
        )

        cls.spark = configure_spark_with_delta_pip(
            SparkSession.builder.appName("TestFeedPulse")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
        ).getOrCreate()
        # Initiate pages table so no conflicts happen
        schema = StructType(
            [
                StructField("page_id", StringType(), False),
                StructField("access_token", StringType(), False),
                StructField("platform", StringType(), False),
            ]
        )

        cls.spark.createDataFrame([], schema).write.format("delta").mode(
            "overwrite"
        ).save(SparkTable.PAGES.value)

        cls.app_process.start()

        time.sleep(25)

    def test_01_push_to_webhook(self):
        response = requests.post(
            url="http://127.0.0.1:5000/facebook_webhook",
            json={
                "entry": [
                    {
                        "id": "448242228374517",
                        "time": 1742667607,
                        "changes": [
                            {
                                "value": {
                                    "from": {
                                        "id": "448242228374517",
                                        "name": "SuperTester",
                                    },
                                    "post": {
                                        "status_type": "mobile_status_update",
                                        "is_published": True,
                                        "updated_time": "2025-03-22T18:20:04+0000",
                                        "promotion_status": "inactive",
                                        "id": "448242228374517_122131676912594941",
                                    },
                                    "message": "meow 2",
                                    "post_id": "448242228374517_122131676912594941",
                                    "comment_id": "122131676912594941_1213590066982748",
                                    "created_time": 1742667604,
                                    "item": "comment",
                                    "parent_id": "122131676912594941_542072878449250",
                                    "verb": "add",
                                },
                                "field": "feed",
                            }
                        ],
                    }
                ],
                "object": "page",
            },
        )
        json_data = []

        self.assertTrue(response.ok)
        for filename in os.listdir(FakeTable.TEST_STREAMING_IN.value):
            if filename.endswith(".json"):  # Process only JSON files
                file_path = os.path.join(FakeTable.TEST_STREAMING_IN.value, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    json_data.append(data)

        self.assertEqual(len(json_data), 1)

        data = json_data[0][0]

        self.assertEqual(data["comment_id"], "122131676912594941_1213590066982748")
        self.assertEqual(data["content"], "meow 2")
        self.assertEqual(data["platform"], "facebook")
        self.assertEqual(data["created_time"], "2025-03-22T18:20:04+00:00")
        self.assertEqual(data["post_id"], "448242228374517_122131676912594941")

    def test_02_processed_data(self):
        time.sleep(30)
        processed_comments = (
            self.spark.read.format("delta")
            .load(FakeTable.TEST_STREAMING_OUT.value)
            .collect()
        )
        processed_comments = [row.asDict() for row in processed_comments]
        self.assertTrue(isinstance(processed_comments[0]["related_topics"], Iterable))
        self.assertIn(
            processed_comments[0]["sentiment"], ["positive", "negative", "neutral"]
        )
        self.assertIn(
            Row(
                comment_id="122131676912594941_1213590066982748",
                content="meow 2",
                created_time=ANY,
                platform="facebook",
                post_id="448242228374517_122131676912594941",
                sentiment=ANY,
                related_topics=ANY,
            ).asDict(),
            processed_comments,
        )

    def test_03_report_handling(self):
        response = requests.get(
            url="http://127.0.0.1:5000/report",
            json={
                "page_id": "448242228374517",
                "start_date": "2024-03-04T15:30:00",
                "end_date": "2025-07-10T08:15:45",
            },
        )
        self.assertTrue(response.ok)
        self.assertTrue(isinstance(response.json()["body"], str))

    @classmethod
    def tearDownClass(cls):
        cls.app_process.terminate()
        time.sleep(2)
        if os.path.exists(os.path.join(base_path, "test_streaming_integration")):
            shutil.rmtree(os.path.join(base_path, "test_streaming_integration"))
