import json
import os
import unittest
import shutil
import datetime
import uuid
from enum import Enum
from time import sleep

import pandas as pd

from src.concurrency.concurrency_manager import ConcurrencyManager
from src.data.data_manager import DataManager
from src.data.spark_table import SparkTable
from src.topics.feedback_topic import FeedbackTopic


class FakeTable(Enum):
    TEST_ADD = "test_spark/test_add"
    TEST_CONCURRENT = "test_spark/test_concurrent"
    TEST_STREAMING_IN = "test_spark/test_streaming_in"
    TEST_STREAMING_OUT = "test_spark/test_streaming_out"
    TEST_T1 = "test_spark/test_t1"
    TEST_T2 = "test_spark/test_t2"
    FILTER_DATE = "test_spark/test_filter_date"
    FILTER_PAGE_ID = "test_spark/test_filter_page_id"


class TestDataManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def fake_classification_function(batch: list[str]) -> list[bool | None]:
            return [None] * len(batch)

        def fake_topic_detection_function(
            batch: list[str],
        ) -> list[list[FeedbackTopic]]:
            return [[FeedbackTopic.CLEANLINESS]] * len(batch)

        cls.data_manager = DataManager(
            FakeTable.TEST_STREAMING_IN,
            FakeTable.TEST_STREAMING_OUT,
            fake_classification_function,
            fake_topic_detection_function,
            ConcurrencyManager(),
            SparkTable.PAGES,
        )

        cls.data_manager.start_streaming_job()

    def test_add(self):
        # Writing random data to test on
        df = self.data_manager._spark.getActiveSession().createDataFrame(
            [{"hi": "random_data", "hello": 2}, {"hi": "random_data2", "hello": 241}]
        )
        df.write.mode("overwrite").format("delta").save("test_spark/test_add")

        future = self.data_manager.add(
            FakeTable.TEST_ADD, [{"hi": "random_data3", "hello": 3}]
        )

        self.assert_concurrent_jobs(1)

        future.result()

        df = (
            self.data_manager._spark.read.option("header", "true")
            .format("delta")
            .load("test_spark/test_add")
        )

        data = [row.asDict() for row in df.collect()]

        self.assertIn({"hi": "random_data3", "hello": 3}, data)
        self.assertEqual(df.count(), 3)

    def test_multiple_jobs_same_table(self):
        # Writing random data to test on
        df = self.data_manager._spark.getActiveSession().createDataFrame(
            [{"hi": "random_data", "hello": 2}, {"hi": "random_data2", "hello": 241}]
        )
        df.write.mode("overwrite").format("delta").save("test_spark/test_concurrent")

        # Adding 6 times so that it's over the number of maximum workers
        futures = [
            self.data_manager.add(FakeTable.TEST_CONCURRENT, [{"hi": "1", "hello": 1}]),
            self.data_manager.add(FakeTable.TEST_CONCURRENT, [{"hi": "2", "hello": 2}]),
            self.data_manager.add(FakeTable.TEST_CONCURRENT, [{"hi": "3", "hello": 3}]),
            self.data_manager.add(FakeTable.TEST_CONCURRENT, [{"hi": "4", "hello": 4}]),
            self.data_manager.add(FakeTable.TEST_CONCURRENT, [{"hi": "5", "hello": 5}]),
            self.data_manager.add(FakeTable.TEST_CONCURRENT, [{"hi": "6", "hello": 6}]),
        ]

        self.assert_concurrent_jobs(5)

        # Wait for all the jobs to complete
        for future in futures:
            future.result()  # This will block until the individual job is done

        df = (
            self.data_manager._spark.read.format("delta")
            .option("inferSchema", "true")
            .load("test_spark/test_concurrent")
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

        # Create an ISO string for JSON serialization.
        created_time_str = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        ).isoformat()

        data_in = [
            {
                "comment_id": "1251",
                "post_id": "123",
                "content": "hello, world!",
                "created_time": created_time_str,
                "platform": "facebook",
            }
        ]

        with open(f"{folder_path}/{uuid.uuid4()}.json", "w") as f:
            json.dump(data_in, f, indent=4)

        sleep(30)

        df = self.data_manager._spark.read.format("delta").load(
            "test_spark/test_streaming_out"
        )

        data = [row.asDict() for row in df.collect()]
        self.assertIn(
            {
                "comment_id": "1251",
                "post_id": "123",
                "created_time": datetime.datetime(2025, 2, 21, 20, 47, 43),
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

        # Create an ISO string for JSON serialization.
        created_time_str = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        ).isoformat()

        data_in_1 = [
            {
                "comment_id": "1",
                "post_id": "123",
                "created_time": created_time_str,
                "platform": "facebook",
                "content": "hello, world!",
            }
        ]

        data_in_2 = [
            {
                "comment_id": "2",
                "post_id": "123",
                "created_time": created_time_str,
                "platform": "facebook",
                "content": "hello, world!",
            }
        ]

        with open(f"{FakeTable.TEST_STREAMING_IN.value}/{uuid.uuid4()}.json", "w") as f:
            json.dump(data_in_1, f, indent=4)
        with open(f"{FakeTable.TEST_STREAMING_IN.value}/{uuid.uuid4()}.json", "w") as f:
            json.dump(data_in_2, f, indent=4)

        sleep(30)

        df = self.data_manager._spark.read.format("delta").load(
            "test_spark/test_streaming_out"
        )

        data = [row.asDict() for row in df.collect()]
        self.assertIn(
            {
                "comment_id": "1",
                "post_id": "123",
                "created_time": datetime.datetime(2025, 2, 21, 20, 47, 43),
                "platform": "facebook",
                "content": "hello, world!",
                "sentiment": "neutral",
                "related_topics": ["cleanliness"],
            },
            data,
        )

        self.assertIn(
            {
                "comment_id": "2",
                "post_id": "123",
                "created_time": datetime.datetime(2025, 2, 21, 20, 47, 43),
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

        # Create an ISO string for JSON serialization.
        created_time_str = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        ).isoformat()

        data_in = [
            {
                "comment_id": "34",
                "post_id": "123",
                "created_time": created_time_str,
                "platform": "facebook",
                "content": "hello, world!",
            }
        ] * 32

        with open(f"{FakeTable.TEST_STREAMING_IN.value}/{uuid.uuid4()}.json", "w") as f:
            json.dump(data_in, f, indent=4)

        sleep(30)

        df = self.data_manager._spark.read.format("delta").load(
            "test_spark/test_streaming_out"
        )

        data = [row.asDict() for row in df.collect()]
        self.assertIn(
            {
                "comment_id": "34",
                "post_id": "123",
                "created_time": datetime.datetime(2025, 2, 21, 20, 47, 43),
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
        future_t1 = self.data_manager.add(
            FakeTable.TEST_T1, [{"hi": "file1", "hello": 3}]
        )

        future_t2 = self.data_manager.add(
            FakeTable.TEST_T2, [{"hi": "file2", "hello": 3}]
        )

        self.assert_concurrent_jobs(2)

        future_t1.result()
        future_t2.result()

        df1 = (
            self.data_manager._spark.read.format("delta")
            .option("inferSchema", "true")
            .load(FakeTable.TEST_T1.value)
        )

        df2 = (
            self.data_manager._spark.read.format("delta")
            .option("inferSchema", "true")
            .load(FakeTable.TEST_T2.value)
        )

        data_t1 = [row.asDict() for row in df1.collect()]
        data_t2 = [row.asDict() for row in df2.collect()]

        self.assertIn({"hi": "file1", "hello": 3}, data_t1)
        self.assertIn({"hi": "file2", "hello": 3}, data_t2)
        self.assertEqual(df1.count(), 1)
        self.assertEqual(df2.count(), 1)

    def test_get_unique(self):
        df1 = self.data_manager._spark.createDataFrame(
            [
                {"comment_id": "123", "content": "hi1"},
                {"comment_id": "456", "content": "hi2"},
                {"comment_id": "789", "content": "hi3"},
            ]
        )

        df2 = self.data_manager._spark.createDataFrame(
            [
                {"comment_id": "123", "content": "fake"},
                {"comment_id": "789", "content": "fake"},
            ]
        )

        df_unique = self.data_manager._get_unique(df1, df2, "comment_id")

        data = [row.asDict() for row in df_unique.collect()]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["content"], "hi2")
        self.assertEqual(data[0]["comment_id"], "456")

    def assert_concurrent_jobs(self, num_jobs: int):
        for _ in range(60):
            if (
                len(
                    self.data_manager._spark.sparkContext.statusTracker().getActiveJobsIds()
                )
                == num_jobs
            ):
                break
            sleep(0.05)
        else:
            self.fail(
                f"Wrong Concurrent Jobs Found({len(self.data_manager._spark.sparkContext.statusTracker().getActiveJobsIds())} != {num_jobs})"
            )

    def empty_dir(self, path_to_directory: str):
        for filename in os.listdir(path_to_directory):
            file_path = os.path.join(path_to_directory, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Recursively delete subdirectories
            else:
                os.remove(file_path)  # Delete files

    def test_filter_exclude_wrong_page_id(self):
        start_time = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        end_time = datetime.datetime(
            2025, 2, 26, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        test_data = self.data_manager._spark.createDataFrame(
            [
                {
                    "post_id": "123_111",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "post_id": "123_112",
                    "created_time": datetime.datetime(
                        2025, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "post_id": "124_111",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ]
        )

        test_data.write.format("delta").save(FakeTable.TEST_STREAMING_OUT.value)

        df = self.data_manager.filter_data("123", start_time, end_time)

        data_as_dict = df.to_dict(orient="records")

        self.assertIn(
            {
                "post_id": "123_112",
                "created_time": datetime.datetime(
                    2025, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                ).isoformat(),
            },
            data_as_dict,
        )
        self.assertIn(
            {
                "post_id": "123_111",
                "created_time": datetime.datetime(
                    2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                ).isoformat(),
            },
            data_as_dict,
        )
        self.assertEqual(len(data_as_dict), 2)

        if os.path.exists(FakeTable.TEST_STREAMING_OUT.value):
            shutil.rmtree(FakeTable.TEST_STREAMING_OUT.value)
            os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)

    def test_filter_exclude_wrong_dates(self):
        start_time = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        end_time = datetime.datetime(
            2025, 2, 26, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        test_data = self.data_manager._spark.createDataFrame(
            [
                {
                    "post_id": "123_111",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "post_id": "123_112",
                    "created_time": datetime.datetime(
                        2026, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "post_id": "123_113",
                    "created_time": datetime.datetime(
                        2021, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ]
        )

        test_data.write.format("delta").save(FakeTable.TEST_STREAMING_OUT.value)

        df = self.data_manager.filter_data("123", start_time, end_time)

        data_as_dict = df.to_dict(orient="records")

        self.assertListEqual(
            data_as_dict,
            [
                {
                    "post_id": "123_111",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ],
        )

        if os.path.exists(FakeTable.TEST_STREAMING_OUT.value):
            shutil.rmtree(FakeTable.TEST_STREAMING_OUT.value)
            os.makedirs(FakeTable.TEST_STREAMING_OUT.value, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        for query in cls.data_manager._spark.streams.active:
            query.stop()
        cls.data_manager._spark.stop()

        if os.path.exists("test_spark"):
            shutil.rmtree("test_spark")
