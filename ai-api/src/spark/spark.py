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

# Define base directory for storing data files
base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "database")
)


# Enum for managing Spark tables
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
        # Define schema for input streaming data
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
        # Add a batch_id column to group every 32 rows
        df = df.withColumn("batch_id", floor(monotonically_increasing_id() / 32))

        grouped_df = df.groupBy("batch_id").agg(
            collect_list(struct(*df.columns)).alias("batch_rows")
        )

        results = []

        # Process each batch concurrently
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.process_batch, row.batch_rows)
                for row in grouped_df.collect()
            ]

            # Collect results from each processed batch
            for future in futures:
                results.extend(future.result())

        # Store processed data in Spark table
        self.add(self.stream_out, results)

    def process_batch(self, batch_rows):

        comments = [r.content for r in batch_rows]

        # Execute sentiment analysis and topic detection concurrently
        with ThreadPoolExecutor() as executor:
            sentiment_future = executor.submit(
                self.feedback_classification_batch_function, comments
            )
            topics_future = executor.submit(
                self.topic_detection_batch_function, comments
            )

            sentiments = sentiment_future.result()
            topics = topics_future.result()

        batch_results = []
        for original_row, sentiment, related_topics in zip(
            batch_rows, sentiments, topics
        ):
            row_dict = original_row.asDict()
            del row_dict["batch_id"]

            # Convert sentiment to text format
            row_dict["sentiment"] = (
                "neutral"
                if sentiment is None
                else "positive" if sentiment else "negative"
            )

            row_dict["related_topics"] = related_topics.copy()
            batch_results.append(row_dict)

        return batch_results
