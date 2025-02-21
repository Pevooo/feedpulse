import json
import os
import unittest
import uuid
import shutil

from enum import Enum
from time import sleep
from unittest.mock import MagicMock


from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from src.spark.spark import Spark
from src.topics.feedback_topic import FeedbackTopic


class FakeTable(Enum):
    TEST_ADD = "test_spark/test_add"
    TEST_CONCURRENT = "test_spark/test_concurrent"
    TEST_STREAMING_IN = "test_spark/test_streaming_in"
    TEST_STREAMING_OUT = "test_spark/test_streaming_out"
    TEST_T1 = "test_spark/test_t1"
    TEST_T2 = "test_spark/test_t2"


class TestSpark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists("test_spark"):
            shutil.rmtree("test_spark")

    def setUp(self):
        def fake_classification_function(batch: list[str]) -> list[bool | None]:
            return [None] * len(batch)

        def fake_topic_detection_function(
            batch: list[str],
        ) -> list[list[FeedbackTopic]]:
            return [[FeedbackTopic.CLEANLINESS]] * len(batch)

        self.spark = Spark(
            FakeTable.TEST_STREAMING_IN,
            FakeTable.TEST_STREAMING_OUT,
            fake_classification_function,
            fake_topic_detection_function,
        )

        self.spark.start_streaming_job()

    def test_singleton(self):
        new_spark = Spark(
            FakeTable.TEST_STREAMING_IN,
            FakeTable.TEST_STREAMING_OUT,
            MagicMock(),
            MagicMock(),
        )
        self.assertIs(new_spark, self.spark)
        self.assertEqual(self.spark.stream_in, FakeTable.TEST_STREAMING_IN)
        self.assertEqual(self.spark.stream_out, FakeTable.TEST_STREAMING_OUT)

    def test_add(self):
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

        self.assert_concurrent_jobs(1)

        future.result()

        df = (
            self.spark.spark.read.option("header", "true")
            .option("inferSchema", "true")
            .parquet("test_spark/test_add")
        )

        data = [row.asDict() for row in df.collect()]

        self.assertIn({"hi": "random_data3", "hello": 3}, data)
        self.assertEqual(df.count(), 3)

    def test_multiple_jobs_same_table(self):
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

        self.assert_concurrent_jobs(1)

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
        folder_path = "test_spark/test_streaming_in"
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        data_in = [
            {
                "hashed_comment_id": "1251",
                "post_id": "123",
                "content": "hello, world!",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
            }
        ]

        with open(os.path.join(folder_path, f"{uuid.uuid4()}.json"), "w") as f:
            json.dump(data_in, f, indent=4)

        sleep(20)

        output_stream_schema = StructType(
            [
                StructField("hashed_comment_id", StringType(), False),
                StructField("post_id", StringType(), False),
                StructField("created_time", TimestampType(), False),
                StructField("platform", StringType(), False),
                StructField("content", StringType(), False),
                StructField("sentiment", StringType(), False),
                StructField("related_topics", ArrayType(StringType(), True), True),
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
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
                "related_topics": ["cleanliness"],
            },
            data,
        )

        self.assertEqual(df.count(), 1)

        self.empty_dir(FakeTable.TEST_STREAMING_IN.value)
        self.empty_dir(FakeTable.TEST_STREAMING_OUT.value)

    def test_streaming_read_2_items_2_files(self):
        folder_path = "test_spark/test_streaming_in"
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        data_in_1 = [
            {
                "hashed_comment_id": "1",
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
            }
        ]

        data_in_2 = [
            {
                "hashed_comment_id": "2",
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
            }
        ]

        with open(os.path.join(folder_path, f"{uuid.uuid4()}.json"), "w") as f:
            json.dump(data_in_1, f, indent=4)
        with open(os.path.join(folder_path, f"{uuid.uuid4()}.json"), "w") as f:
            json.dump(data_in_2, f, indent=4)

        sleep(20)

        output_stream_schema = StructType(
            [
                StructField("hashed_comment_id", StringType(), False),
                StructField("post_id", StringType(), False),
                StructField("created_time", TimestampType(), False),
                StructField("platform", StringType(), False),
                StructField("content", StringType(), False),
                StructField("sentiment", StringType(), False),
                StructField("related_topics", ArrayType(StringType(), True), True),
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
                "hashed_comment_id": "1",
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
                "related_topics": ["cleanliness"],
            },
            data,
        )

        self.assertIn(
            {
                "hashed_comment_id": "2",
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
                "related_topics": ["cleanliness"],
            },
            data,
        )

        self.assertEqual(df.count(), 2)

        self.empty_dir(FakeTable.TEST_STREAMING_IN.value)
        self.empty_dir(FakeTable.TEST_STREAMING_OUT.value)

    def test_streaming_read_32_items_same_file(self):
        folder_path = "test_spark/test_streaming_in"
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        data_in = [
            {
                "hashed_comment_id": "34",
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
            }
        ] * 32

        with open(os.path.join(folder_path, f"{uuid.uuid4()}.json"), "w") as f:
            json.dump(data_in, f, indent=4)

        sleep(20)

        output_stream_schema = StructType(
            [
                StructField("hashed_comment_id", StringType(), False),
                StructField("post_id", StringType(), False),
                StructField("created_time", TimestampType(), False),
                StructField("platform", StringType(), False),
                StructField("content", StringType(), False),
                StructField("sentiment", StringType(), False),
                StructField("related_topics", ArrayType(StringType(), True), True),
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
                "hashed_comment_id": "34",
                "post_id": "123",
                "created_time": "datetime.datetime(2025, 2, 21, 18, 47, 43, tzinfo=datetime.timezone.utc)",
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
                "related_topics": ["cleanliness"],
            },
            data,
        )

        self.assertEqual(df.count(), 32)

        self.empty_dir(FakeTable.TEST_STREAMING_IN.value)
        self.empty_dir(FakeTable.TEST_STREAMING_OUT.value)

    def test_concurrency_multiple_tables(self):
        future_t1 = self.spark.add(FakeTable.TEST_T1, [{"hi": "file1", "hello": 3}])

        future_t2 = self.spark.add(FakeTable.TEST_T2, [{"hi": "file2", "hello": 3}])

        self.assert_concurrent_jobs(2)

        future_t1.result()
        future_t2.result()

        df1 = (
            self.spark.spark.read.option("header", "true")
            .option("inferSchema", "true")
            .parquet(FakeTable.TEST_T1.value)
        )

        df2 = (
            self.spark.spark.read.option("header", "true")
            .option("inferSchema", "true")
            .parquet(FakeTable.TEST_T2.value)
        )

        data_t1 = [row.asDict() for row in df1.collect()]
        data_t2 = [row.asDict() for row in df2.collect()]

        self.assertIn({"hi": "file1", "hello": 3}, data_t1)
        self.assertIn({"hi": "file2", "hello": 3}, data_t2)
        self.assertEqual(df1.count(), 1)
        self.assertEqual(df2.count(), 1)

    def assert_concurrent_jobs(self, num_jobs: int):
        for _ in range(20):
            if (
                len(self.spark.spark.sparkContext.statusTracker().getActiveJobsIds())
                == num_jobs
            ):
                break
            sleep(0.05)
        else:
            self.fail(
                f"Wrong Concurrent Jobs Found({self.spark.spark.sparkContext.statusTracker().getActiveJobsIds()} != {num_jobs})"
            )

    def empty_dir(self, path_to_directory: str):
        for filename in os.listdir(path_to_directory):
            file_path = os.path.join(path_to_directory, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Recursively delete subdirectories
            else:
                os.remove(file_path)  # Delete files

    def tearDown(self):
        for query in self.spark.spark.streams.active:
            query.stop()
        self.spark.spark.stop()

if __name__ == "__main__":
    unittest.main()