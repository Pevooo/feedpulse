import os
from concurrent.futures import ThreadPoolExecutor, Future

from enum import Enum
from typing import Any, Iterable

from pyspark.sql import SparkSession

"""
# Define schemas
pages_schema = StructType([StructField("page_id", StringType(), False)])

posts_schema = StructType(
    [
        StructField("post_id", StringType(), False),
        StructField("page_id", StringType(), False),
        StructField("content", StringType(), True),
    ]
)

comments_schema = StructType(
    [
        StructField("hashed_comment", StringType(), False),
        StructField("platform", StringType(), False),
        StructField("content", StringType(), False),
        StructField("related_topics", ArrayType(StringType(), True), True),
        StructField("sentiment", StringType(), True),
        StructField("transaction_type", StringType(), True),
        StructField("timestamp", TimestampType(), False),
    ]
)

exceptions_schema = StructType(
    [
        StructField("exception_id", StringType(), False),
        StructField("exception_message", StringType(), True),
        StructField("time", TimestampType(), False),
    ]
)
"""

base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "database")
)


class SparkTable(Enum):
    REPORTS = os.path.join(base_dir, "reports")
    INPUT_COMMENTS = os.path.join(base_dir, "comments_stream")
    PROCESSED_COMMENTS = os.path.join(base_dir, "processed_comments")
    PAGES = os.path.join(base_dir, "pages")
    EXCEPTIONS = os.path.join(base_dir, "exceptions")


class Spark:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Spark, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.spark = SparkSession.builder.appName("session").getOrCreate()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def start_streaming_job(self):
        return self.executor.submit(self._streaming_worker)

    def add(self, table: SparkTable, row_data: Iterable[dict[str, Any]]) -> Future:
        return self.executor.submit(self._add_worker, table, list(row_data))

    def delete(self, table: SparkTable, row_data: str):
        pass

    def query(self, table: SparkTable, row_data: str):
        pass

    def modify(self, table: SparkTable, row_data: str):
        pass

    def _add_worker(
        self, table: SparkTable, row_data: Iterable[dict[str, Any]]
    ) -> None:
        self.spark.createDataFrame(row_data).write.mode("append").parquet(table.value)

    def _streaming_worker(self):
        df = self.spark.readStream.format("json").load(
            os.path.join(base_dir, SparkTable.INPUT_COMMENTS.value)
        )

        # TODO: Some Processing

        (
            df.writeStream.outputMode("append")
            .format("parquet")
            .option("path", os.path.join(base_dir, SparkTable.PROCESSED_COMMENTS.value))
        )
