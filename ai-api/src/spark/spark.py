import os
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum
from typing import Any, Iterable, Callable

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    monotonically_increasing_id,
    collect_list,
    struct,
    floor,
)
from pyspark.sql.types import (
    StructField,
    StructType,
    StringType,
)

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
        StructField("hashed_comment_id", StringType(), False),
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
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Spark, cls).__new__(cls)
        return cls.instance

    def __init__(
        self,
        stream_in: SparkTable,
        stream_out: SparkTable,
        feedback_classification_batch_function: Callable[
            [list[str]], list[bool | None]
        ],
        topic_detection_batch_function: Callable[[list[str]], list[list[str]]],
    ):
        self.spark = SparkSession.builder.appName("session").getOrCreate()
        self.feedback_classification_batch_function = (
            feedback_classification_batch_function
        )
        self.topic_detection_batch_function = topic_detection_batch_function
        self.executors: dict[SparkTable, ThreadPoolExecutor] = dict()
        self.stream_in = stream_in
        self.stream_out = stream_out

    def start_streaming_job(self):
        self._streaming_worker()

    def add(self, table: SparkTable, row_data: Iterable[dict[str, Any]]) -> Future:
        if table not in self.executors:
            self.executors[table] = ThreadPoolExecutor(max_workers=1)

        return self.executors[table].submit(self._add_worker, table, list(row_data))

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
        input_stream_schema = StructType(
            [
                StructField("hashed_comment_id", StringType(), False),
                StructField("platform", StringType(), False),
                StructField("content", StringType(), False),
            ]
        )

        os.makedirs(self.stream_in.value, exist_ok=True)
        df = (
            self.spark.readStream.format("json")
            .option("multiLine", True)
            .schema(input_stream_schema)
            .load(self.stream_in.value)
        )
        df.writeStream.trigger(processingTime="5 seconds").foreachBatch(
            self.process_data
        ).option(
            "checkpointLocation",
            os.path.join(base_dir, "checkpoints/processed_comments"),
        ).start()

    def process_data(self, df, epoch_id):
        # Add a batch_id column to group every 32 rows.
        df = df.withColumn("batch_id", floor(monotonically_increasing_id() / 32))

        grouped_df = df.groupBy("batch_id").agg(
            collect_list(struct(*df.columns)).alias("batch_rows")
        )

        results = []
        for row in grouped_df.collect():
            batch_rows = row.batch_rows
            comments = [r.content for r in batch_rows]
            sentiments = self.feedback_classification_batch_function(comments)
            topics = self.topic_detection_batch_function(comments)
            for original_row, sentiment, related_topics in zip(
                batch_rows, sentiments, topics
            ):
                row_dict = original_row.asDict()
                del row_dict["batch_id"]

                if sentiment is None:
                    row_dict["sentiment"] = "neutral"
                elif sentiment:
                    row_dict["sentiment"] = "positive"
                else:
                    row_dict["sentiment"] = "negative"

                row_dict["related_topics"] = related_topics.copy()
                results.append(row_dict)

        self.add(self.stream_out, results)
