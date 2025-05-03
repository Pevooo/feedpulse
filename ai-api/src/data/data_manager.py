import json
import os
import shutil
import tempfile
import uuid
import pandas as pd
from datetime import datetime
from concurrent.futures import Future
from typing import Any, Iterable, Callable
from delta import configure_spark_with_delta_pip
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring_index, split
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
    ArrayType,
)

from src.concurrency.concurrency_manager import ConcurrencyManager
from src.config.settings import Settings
from src.config.updatable import Updatable
from src.data.spark_table import SparkTable
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.topics.feedback_topic import FeedbackTopic
from src.utlity.util import deprecated


class DataManager(Updatable):
    instance: "DataManager"

    INPUT_STREAM_SCHEMA = StructType(
        [
            StructField("comment_id", StringType(), False),
            StructField("post_id", StringType(), False),
            StructField("content", StringType(), False),
            StructField("created_time", TimestampType(), False),
            StructField("platform", StringType(), False),
        ]
    )

    OUTPUT_STREAM_SCHEMA = StructType(
        [
            StructField("comment_id", StringType(), False),
            StructField("post_id", StringType(), False),
            StructField("content", StringType(), False),
            StructField("created_time", TimestampType(), False),  # ISO format string
            StructField("platform", StringType(), False),
            StructField("sentiment", StringType(), False),
            StructField(
                "related_topics", ArrayType(StringType()), False
            ),  # Array of strings
        ]
    )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DataManager, cls).__new__(cls)
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
        pages: SparkTable,
        processing_batch_size: int = 32,
    ):
        self._spark = configure_spark_with_delta_pip(
            SparkSession.builder.appName("FeedPulse")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        ).getOrCreate()

        self.feedback_classification_batch_function = (
            feedback_classification_batch_function
        )

        self.topic_detection_batch_function = topic_detection_batch_function
        self.concurrency_manager = concurrency_manager
        self.stream_in = stream_in
        self.stream_out = stream_out
        self.pages = pages
        self.processing_batch_size = processing_batch_size

    def start_streaming_job(self):
        self._streaming_worker()

    def stream_by_webhook(self, data: list[dict[str, Any]]) -> None:
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.json"

        # Create a temporary file in the system temp directory
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tmp_file:
            json.dump(data, tmp_file, indent=4, ensure_ascii=False)
            temp_path = tmp_file.name  # Get the temporary file path

        # Define the final destination path
        final_path = os.path.join(self.stream_in.value, filename)

        # Move the file to the real directory
        shutil.move(temp_path, final_path)

    @deprecated
    def stream_by_polling(self):
        df = self.read(self.pages)
        if df:
            flattened_df = self._get_flattened_polled_data(df)

            processed_comments = self.read(self.stream_out)
            if processed_comments:
                stream_df = self._get_unique(
                    flattened_df, processed_comments, "comment_id"
                )
                self.add(self.stream_in, stream_df, "json").result()
            else:
                self.add(self.stream_in, flattened_df, "json").result()

    def add(
        self,
        table: SparkTable,
        row_data: Iterable[dict[str, Any]] | pyspark.sql.DataFrame,
        write_format: str = "delta",
        schema: StructType = None,
    ) -> Future:
        return self.concurrency_manager.submit_job(
            self._add_worker, table, row_data, write_format, schema
        )

    def delete(self, table: SparkTable, row_data: str):
        pass

    def read(self, table: SparkTable) -> pyspark.sql.DataFrame | None:
        try:
            return self._spark.read.format("delta").load(table.value)
        except Exception:
            return None

    def modify(self, table: SparkTable, row_data: str):
        pass

    # Modified _add_worker function to reduce Spark-level parallelism for small datasets
    # noinspection PyTypeChecker
    def _add_worker(
        self,
        table: SparkTable,
        row_data: Iterable[dict[str, Any]] | pyspark.sql.DataFrame,
        write_format: str = "delta",
        schema: StructType = None,
    ) -> None:
        if isinstance(row_data, pyspark.sql.DataFrame):
            df = row_data
        else:
            data_list = list(row_data)  # Convert iterable to list for size checking

            if schema:
                df = self._spark.createDataFrame(data_list, schema=schema)
            else:
                df = self._spark.createDataFrame(data_list)

            if (
                len(data_list) < 100
            ):  # For small datasets, reduce the number of partitions to lower Spark-level parallelism
                df = df.coalesce(1)
        df.write.mode("append").format(write_format).save(table.value)

    def _streaming_worker(self):
        os.makedirs(self.stream_in.value, exist_ok=True)
        df = (
            self._spark.readStream.format("json")
            .option("multiLine", True)
            .schema(self.INPUT_STREAM_SCHEMA)
            .load(self.stream_in.value)
        )
        df.writeStream.trigger(processingTime="5 seconds").foreachBatch(
            self.process_data
        ).option(
            "checkpointLocation",
            SparkTable.CHECKPOINT.value,
        ).start()

    def process_data(self, df: pyspark.sql.DataFrame, epoch_id):
        if df.isEmpty():
            return

        # Add a batch_id column to group every 32 rows
        df = df.withColumn(
            "batch_id",
            floor(monotonically_increasing_id() / self.processing_batch_size),
        )
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
        processed_df = self._spark.createDataFrame(
            results, schema=self.OUTPUT_STREAM_SCHEMA
        )

        if len(results) < 100:
            # Reduce parallelism in case of small data to avoid parallelism overhead
            processed_df = processed_df.coalesce(1)

        processed_df = processed_df.withColumn(
            "page_id", split(processed_df["post_id"], "_")[0]
        )
        processed_df.write.format("delta").mode("append").partitionBy("page_id").save(
            self.stream_out.value
        )

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

    @deprecated
    def _get_unique(
        self, new_df: pyspark.sql.DataFrame, old_df: pyspark.sql.DataFrame, on: str
    ) -> pyspark.sql.DataFrame:
        """
        Returns a new dataframe without duplicate rows based on an id.
        """
        return new_df.join(old_df, on=on, how="left_anti")

    @deprecated
    def _get_flattened_polled_data(self, df) -> pyspark.sql.DataFrame:
        def process_page(row):
            try:
                ac_token = row["access_token"]
                platform = row["platform"]

                if platform == "facebook":
                    return FacebookDataProvider(ac_token).get_posts()

            # TODO: Integrate Instagram
            # elif platform == "instagram":
            #     return InstagramDataProvider(ac_token).get_posts()
            except Exception:
                return []

        results_rdd = df.rdd.flatMap(process_page)
        return self._spark.createDataFrame(results_rdd)

    def filter_data(
        self, page_id: str, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Prepare and filter the data.
        Args:
            page_id (str): The id of the page which the report belongs to.
            start_date (datetime): The start date of the data to be included in the report.
            end_date (datetime): The end date of the data to be included in the report.
        Returns:
            pd.DataFrame: The filtered data.
        """
        filtered_page_data_df = (
            self.read(self.stream_out)
            .selectExpr("*")  # start with all columns
            .filter(
                (substring_index(col("post_id"), "_", 1) == page_id)
                & (col("created_time") >= start_date)
                & (col("created_time") <= end_date)
            )
            .drop("post_id", "comment_id", "page_id")
            .toPandas()  # use Arrow here for speed
        )

        filtered_page_data_df["related_topics"] = filtered_page_data_df[
            "related_topics"
        ].apply(lambda x: ", ".join(x))
        return filtered_page_data_df

    def update(self) -> None:
        self.processing_batch_size = Settings.processing_batch_size
