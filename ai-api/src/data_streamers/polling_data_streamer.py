import logging
import time

import pyspark

from src.concurrency.concurrency_manager import ConcurrencyManager
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.data_streamers.data_streamer import DataStreamer
from src.spark.spark import SparkTable, Spark


class PollingDataStreamer(DataStreamer):
    def __init__(
        self,
        spark: Spark,
        trigger_time: int,
        streaming_in: SparkTable,
        streaming_out: SparkTable,
        pages_dir: SparkTable,
        concurrency_manager: ConcurrencyManager,
    ):
        self.spark = spark
        self.trigger_time = trigger_time
        self.streaming_in = streaming_in
        self.streaming_out = streaming_out
        self.pages_dir = pages_dir
        self.concurrency_manager = concurrency_manager

    def start_streaming(self) -> None:
        self.concurrency_manager.submit_job(self.streaming_worker)

    def streaming_worker(self):
        df = self.spark.read(self.pages_dir)
        if df:
            flattened_df = self._get_flattened(df)

            processed_comments = self.spark.read(self.streaming_out)
            if processed_comments:
                stream_df = self._get_unique(flattened_df, processed_comments)
                self.spark.add(self.streaming_in, stream_df, "json").result()
            else:
                self.spark.add(self.streaming_in, flattened_df, "json").result()

        time.sleep(self.trigger_time)
        self.concurrency_manager.submit_job(self.streaming_worker)

    def _get_flattened(self, df) -> pyspark.sql.DataFrame:
        def process_page(row):
            logging.error(f"Hi {row}")
            try:
                ac_token = row["access_token"]
                platform = row["platform"]

                if platform == "facebook":
                    return FacebookDataProvider(ac_token).get_posts()

            # TODO: Integrate Instagram
            # elif platform == "instagram":
            #     return InstagramDataProvider(ac_token).get_posts()
            except Exception:
                logging.error(f"Error getting posts from {row}")
                return []

        results_rdd = df.rdd.flatMap(process_page)
        return self.spark.spark.createDataFrame(results_rdd)

    def _get_unique(self, new_df, old_df) -> pyspark.sql.DataFrame:
        return new_df.join(old_df, on="comment_id", how="left_anti")
