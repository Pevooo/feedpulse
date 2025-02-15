import os
import unittest
import shutil

from enum import Enum

from src.spark.spark import Spark


class FakeTable(Enum):
    TEST_ADD = "test_spark/test_add"
    TEST_CONCURRENT = "test_spark/test_concurrent"


class TestSpark(unittest.TestCase):
    def setUp(self):
        self.spark = Spark()

    def test_singleton(self):
        new_spark = Spark()
        self.assertIs(new_spark, Spark())

    def test_add(self):
        # Writing random data to test on
        df = self.spark.spark.getActiveSession().createDataFrame(
            [{"hi": "random_data", "hello": 2}, {"hi": "random_data2", "hello": 241}]
        )
        df.write.option("header", "true").parquet("test_spark/test_add")

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
        # Writing random data to test on
        df = self.spark.spark.getActiveSession().createDataFrame(
            [{"hi": "random_data", "hello": 2}, {"hi": "random_data2", "hello": 241}]
        )
        df.write.option("header", "true").parquet("test_spark/test_concurrent")

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

    def tearDown(self):
        if os.path.exists("test_spark"):
            shutil.rmtree("test_spark")
