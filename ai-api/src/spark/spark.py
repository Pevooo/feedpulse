import os
from concurrent.futures import Future
from typing import Any, Iterable, Callable
from delta import configure_spark_with_delta_pip
import pyspark
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
    TimestampType,
)

from src.concurrency.concurrency_manager import ConcurrencyManager
from src.spark.spark_table import SparkTable
from src.topics.feedback_topic import FeedbackTopic


class Spark:
    instance: "Spark"

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
        concurrency_manager: ConcurrencyManager,
    ):
        self.spark = configure_spark_with_delta_pip(
            SparkSession.builder.appName("FeedPulse")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
        ).getOrCreate()

        self.feedback_classification_batch_function = (
            feedback_classification_batch_function
        )

        self.topic_detection_batch_function = topic_detection_batch_function
        self.concurrency_manager = concurrency_manager
        self.stream_in = stream_in
        self.stream_out = stream_out

    def start_streaming_job(self):
        self._streaming_worker()

    def add(
        self,
        table: SparkTable,
        row_data: Iterable[dict[str, Any]] | pyspark.sql.DataFrame,
        write_format: str = "delta",
    ) -> Future:
        return self.concurrency_manager.submit_job(
            self._add_worker, table, row_data, write_format
        )

    def delete(self, table: SparkTable, row_data: str):
        pass

    def read(self, table: SparkTable) -> pyspark.sql.DataFrame | None:
        try:
            return self.spark.read.format("delta").load(table.value)
        except Exception:
            return None


    def update(
        self,
        table: SparkTable,
        condition_column: str,
        condition_value: Any,
        updates: dict[str, Any],
    ):
        df = self.read(table)
        if df is None:
            return

        updates_expr = ", ".join(
            [f"target.{col} = '{val}'" for col, val in updates.items()]
        )

        query = f"""
            MERGE INTO delta.`{table.value}` AS target
            USING (SELECT * FROM delta.`{table.value}` WHERE {condition_column} = '{condition_value}') AS source
            ON target.{condition_column} = source.{condition_column}
            WHEN MATCHED THEN
            UPDATE SET {updates_expr}
        """

        try:
            self.spark.sql(query)
            print(f"Update successful on {table.value}")
        except Exception as e:
            print(f"Error updating {table.value}: {str(e)}")

    # Modified _add_worker function to reduce Spark-level parallelism for small datasets
    def _add_worker(
        self,
        table: SparkTable,
        row_data: Iterable[dict[str, Any]] | pyspark.sql.DataFrame,
        write_format: str = "delta",
    ) -> None:
        if isinstance(row_data, pyspark.sql.DataFrame):
            df = row_data
        else:
            data_list = list(row_data)  # Convert iterable to list for size checking
            df = self.spark.createDataFrame(data_list)
            if (
                len(data_list) < 100
            ):  # For small datasets, reduce the number of partitions to lower Spark-level parallelism
                df = df.coalesce(1)
        df.write.mode("append").format(write_format).save(table.value)

    def _streaming_worker(self):
        # Define schema for input streaming data
        input_stream_schema = StructType(
            [
                StructField("comment_id", StringType(), False),
                StructField("post_id", StringType(), False),
                StructField("content", StringType(), False),
                StructField("created_time", TimestampType(), False),
                StructField("platform", StringType(), False),
            ]
        )

        os.makedirs(self.stream_in.value, exist_ok=True)
        df = (
            self.spark.readStream.format("json")
            .option("multiLine", False)
            .schema(input_stream_schema)
            .load(self.stream_in.value)
        )
        df.writeStream.trigger(processingTime="5 seconds").foreachBatch(
            self.process_data
        ).start()

    def process_data(self, df: pyspark.sql.DataFrame, epoch_id):
        if df.isEmpty():
            return

        # Add a batch_id column to group every 32 rows
        df = df.withColumn("batch_id", floor(monotonically_increasing_id() / 32))
        grouped_df = df.groupBy("batch_id").agg(
            collect_list(struct(*df.columns)).alias("batch_rows")
        )

        results = []

        # Process each batch concurrently
        grouped_data = grouped_df.collect()

        futures = [
            self.concurrency_manager.submit_job(self.process_batch, row.batch_rows)
            for row in grouped_data
        ]

        # Collect results from each processed batch
        for future in futures:
            results.extend(future.result())
        # Store processed data in Spark table
        self.add(self.stream_out, results)

    def process_batch(self, batch_rows):
        comments = [r.content for r in batch_rows]
        # Execute sentiment analysis and topic detection concurrently

        sentiment_future = self.concurrency_manager.submit_job(
            self.feedback_classification_batch_function, comments
        )
        topics_future = self.concurrency_manager.submit_job(
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

            row_dict["related_topics"] = [t.value for t in related_topics]
            batch_results.append(row_dict)

        return batch_results
