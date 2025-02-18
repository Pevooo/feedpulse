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

from src.topics.feedback_topic import FeedbackTopic

# Set up base directory for storing data
base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "database")
)


# Define table locations
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
        topic_detection_batch_function: Callable[
            [list[str]], list[list[FeedbackTopic]]
        ],
    ):
        self.spark = SparkSession.builder.appName("FeedPulse Spark App").getOrCreate()

        self.feedback_classification_batch_function = (
            feedback_classification_batch_function
        )
        self.topic_detection_batch_function = topic_detection_batch_function
        self.executors: dict[SparkTable, ThreadPoolExecutor] = dict()
        self.stream_in = stream_in
        self.stream_out = stream_out

    def start_streaming_job(self):
        if self.stream_in not in self.executors:
            self.executors[self.stream_in] = ThreadPoolExecutor(max_workers=1)
        return self.executors[self.stream_in].submit(self._streaming_worker)

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
        """
        Write job for adding rows to Parquet files.
        We'll set a custom job group/description to track it in Spark UI.
        """
        job_group = f"WriteTo_{table.name}"
        job_description = f"Appending data to {table.value}"
        self.spark.sparkContext.setJobGroup(job_group, job_description)

        # Perform the write job
        self.spark.createDataFrame(row_data).write.mode("append").parquet(table.value)

        # Clear the job group after finishing
        self.spark.sparkContext.setJobGroup("", "")

    def _streaming_worker(self):
        """
        Structured Streaming job that reads JSON files from 'stream_in' directory
        and processes them in micro-batches.
        """
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
            .option("basePath", self.stream_in.value)
            .schema(input_stream_schema)
            .load(self.stream_in.value)
        )

        df.writeStream.queryName("Comments Stream Job").trigger(
            processingTime="5 seconds"
        ).foreachBatch(self.process_data).start()

    def process_data(self, df, epoch_id):
        """
        This method is called on each micro-batch. We collect rows in groups of 32,
        classify sentiment, detect topics, and write the results to 'stream_out'.
        """
        # (Optional) Name the batch for better tracking
        job_group = f"ProcessingEpoch_{epoch_id}"
        job_description = f"Processing micro-batch epoch_id={epoch_id}"
        self.spark.sparkContext.setJobGroup(job_group, job_description)

        # Add a batch_id column to group every 32 rows.
        df = df.withColumn("batch_id", floor(monotonically_increasing_id() / 32))

        grouped_df = df.groupBy("batch_id").agg(
            collect_list(struct(*df.columns)).alias("batch_rows")
        )

        results = []
        for row in grouped_df.collect():
            batch_rows = row.batch_rows
            comments = [r.content for r in batch_rows]

            # Call external classification & topic detection functions
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

                # Convert enum values to strings
                row_dict["related_topics"] = [t.value for t in related_topics]
                results.append(row_dict)

        # Write results to the specified output table
        self.add(self.stream_out, results)

        # Clear the job group after finishing
        self.spark.sparkContext.setJobGroup("", "")
