import json
import os
import shutil
import unittest
import uuid

from enum import Enum
from time import sleep
from unittest.mock import MagicMock

from pyspark.sql.types import StructType, StructField, StringType

from src.spark.spark import Spark


class FakeTable(Enum):
    TEST_ADD = "test_spark/test_add"
    TEST_CONCURRENT = "test_spark/test_concurrent"
    TEST_STREAMING_IN = "test_spark/test_streaming_in"
    TEST_STREAMING_OUT = "test_spark/test_streaming_out"


class TestSpark(unittest.TestCase):
    def setUp(self):
        def fake_function(batch: list[str]) -> list[str]:
            return ["neutral"] * len(batch)

        self.spark = Spark(
            FakeTable.TEST_STREAMING_IN, FakeTable.TEST_STREAMING_OUT, fake_function
        )

        self.spark.start_streaming_job()

    def test_singleton(self):
        new_spark = Spark(
            FakeTable.TEST_STREAMING_IN, FakeTable.TEST_STREAMING_OUT, MagicMock()
        )
        self.assertIs(new_spark, self.spark)
        self.assertEqual(self.spark.stream_in, FakeTable.TEST_STREAMING_IN)
        self.assertEqual(self.spark.stream_out, FakeTable.TEST_STREAMING_OUT)

    def test_add(self):
        self.init_paths()

        # Writing random data to test on
        df = self.spark.spark.getActiveSession().createDataFrame(
            [{"hi": "random_data", "hello": 2}, {"hi": "random_data2", "hello": 241}]
        )
        df.write.mode("overwrite").option("header", "true").parquet(
            "test_spark/test_add"
        )

        future = self.spark.add(
            FakeTable.TEST_ADD, [{"hi": "random_data3", "hello": 3}]
        )
        future.result()

        df = (
            self.spark.spark.read.option("header", "true")
            .option("inferSchema", "true")
            .parquet("test_spark/test_add")
        )

        data = [row.asDict() for row in df.collect()]

        self.assertIn({"hi": "random_data3", "hello": 3}, data)
        self.assertEqual(df.count(), 3)

    def test_concurrent_exceeds_num_workers(self):
        self.init_paths()

        # Writing random data to test on
        df = self.spark.spark.getActiveSession().createDataFrame(
            [{"hi": "random_data", "hello": 2}, {"hi": "random_data2", "hello": 241}]
        )
        df.write.mode("overwrite").option("header", "true").parquet(
            "test_spark/test_concurrent"
        )

        # Adding 6 times so that it's over the number of maximum workers
        futures = [
            self.spark.add(FakeTable.TEST_CONCURRENT, [{"hi": "1", "hello": 1}]),
            self.spark.add(FakeTable.TEST_CONCURRENT, [{"hi": "2", "hello": 2}]),
            self.spark.add(FakeTable.TEST_CONCURRENT, [{"hi": "3", "hello": 3}]),
            self.spark.add(FakeTable.TEST_CONCURRENT, [{"hi": "4", "hello": 4}]),
            self.spark.add(FakeTable.TEST_CONCURRENT, [{"hi": "5", "hello": 5}]),
            self.spark.add(FakeTable.TEST_CONCURRENT, [{"hi": "6", "hello": 6}]),
        ]

        # Wait for all the jobs to complete
        for future in futures:
            future.result()  # This will block until the individual job is done

        df = (
            self.spark.spark.read.option("header", "true")
            .option("inferSchema", "true")
            .parquet("test_spark/test_concurrent")
        )

        data = [row.asDict() for row in df.collect()]

        self.assertIn({"hi": "1", "hello": 1}, data)
        self.assertIn({"hi": "2", "hello": 2}, data)
        self.assertIn({"hi": "3", "hello": 3}, data)
        self.assertIn({"hi": "4", "hello": 4}, data)
        self.assertIn({"hi": "5", "hello": 5}, data)
        self.assertIn({"hi": "6", "hello": 6}, data)

        self.assertEqual(df.count(), 8)

    def test_streaming_read_1_item(self):
        self.init_paths()

        folder_path = "test_spark/test_streaming_in"
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        data_in = [
            {
                "hashed_comment_id": "1251",
                "platform": "facebook",
                "content": "hello, world!",
            }
        ]

        with open(os.path.join(folder_path, f"{uuid.uuid4()}.json"), "w") as f:
            json.dump(data_in, f, indent=4)

        sleep(30)

        output_stream_schema = StructType(
            [
                StructField("hashed_comment_id", StringType(), False),
                StructField("platform", StringType(), False),
                StructField("content", StringType(), False),
                StructField("sentiment", StringType(), False),
            ]
        )

        df = (
            self.spark.spark.read.option("header", "true")
            .schema(output_stream_schema)
            .parquet("test_spark/test_streaming_out")
        )

        data = [row.asDict() for row in df.collect()]
        self.assertIn(
            {
                "hashed_comment_id": "1251",
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
            },
            data,
        )

    def test_streaming_read_32_items_same_file(self):
        self.init_paths()

        folder_path = "test_spark/test_streaming_in"
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        data_in = [
            {
                "hashed_comment_id": "1251",
                "platform": "facebook",
                "content": "hello, world!",
            }
        ] * 32

        with open(os.path.join(folder_path, f"{uuid.uuid4()}.json"), "w") as f:
            json.dump(data_in, f, indent=4)

        sleep(30)

        output_stream_schema = StructType(
            [
                StructField("hashed_comment_id", StringType(), False),
                StructField("platform", StringType(), False),
                StructField("content", StringType(), False),
                StructField("sentiment", StringType(), False),
            ]
        )

        df = (
            self.spark.spark.read.option("header", "true")
            .schema(output_stream_schema)
            .parquet("test_spark/test_streaming_out")
        )

        data = [row.asDict() for row in df.collect()]
        print(data)
        self.assertIn(
            {
                "hashed_comment_id": "1251",
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
            },
            data,
        )

        self.assertEqual(df.count(), 32)

    def reset_paths(self):
        if os.path.exists("test_spark"):
            shutil.rmtree("test_spark")
            os.makedirs("test_spark/streaming_in")

    def init_paths(self):
        os.makedirs(FakeTable.TEST_STREAMING_IN.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_ADD.value, exist_ok=True)
        os.makedirs(FakeTable.TEST_CONCURRENT.value, exist_ok=True)
