import time

from concurrent.futures import ThreadPoolExecutor

import pyspark

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
    ):
        self.spark = spark
        self.trigger_time = trigger_time
        self.streaming_in = streaming_in
        self.streaming_out = streaming_out
        self.pages_dir = pages_dir
        self.executor = ThreadPoolExecutor(max_workers=1)

    def start_streaming(self) -> None:
        self.executor.submit(self.streaming_worker)

    def process_page(self, row):
        ac_token = row["ac_token"]
        platform = row["platform"]

        if platform == "facebook":
            return FacebookDataProvider(ac_token).get_posts()

        # TODO: Integrate Instagram
        # elif platform == "instagram":
        #     return InstagramDataProvider(ac_token).get_posts()

    def streaming_worker(self):
        df = self.spark.read(self.pages_dir)

        flattened_df = self._get_flattened(df)

        processed_comments = self.spark.read(self.streaming_out)
        if processed_comments:
            stream_df = self._get_unique(flattened_df, processed_comments)
            self.spark.add(self.streaming_in, stream_df, "json").result()
        else:
            self.spark.add(self.streaming_in, flattened_df, "json").result()

        time.sleep(self.trigger_time)
        self.executor.submit(self.streaming_worker)

    def _get_flattened(self, df) -> pyspark.sql.DataFrame:
        results_rdd = df.rdd.flatMap(self.process_page)
        return self.spark.spark.createDataFrame(results_rdd)

    def _get_unique(self, new_df, old_df) -> pyspark.sql.DataFrame:
        return new_df.join(old_df, on="comment_id", how="left_anti")
