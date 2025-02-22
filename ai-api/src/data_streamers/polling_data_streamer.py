import time

from concurrent.futures import ThreadPoolExecutor

import pyspark

from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.data_streamers.data_streamer import DataStreamer
from src.spark.spark import SparkTable


class PollingDataStreamer(DataStreamer):
    def start_streaming(self) -> None:
        with ThreadPoolExecutor(max_workers=1) as executor:
            while True:
                executor.submit(self.streaming_worker).result()
                time.sleep(self.trigger_time)

    def process_page(self, row):
        ac_token = row["ac_token"]
        platform = row["platform"]

        if platform == "facebook":
            return FacebookDataProvider(ac_token).get_posts()

        # TODO: Integrate Instagram
        # elif platform == "instagram":
        #     return InstagramDataProvider(ac_token).get_posts()

    def streaming_worker(self):
        df = self.spark.read(SparkTable.AC_TOKENS)

        flattened_df = self._get_flattened(df)

        processed_comments = self.spark.read(SparkTable.PROCESSED_COMMENTS)
        stream_df = self._get_unique(flattened_df, processed_comments)

        self.spark.add(SparkTable.INPUT_COMMENTS, stream_df, "json").result()

    def _get_flattened(self, df) -> pyspark.sql.DataFrame:
        results_rdd = df.rdd.flatMap(self.process_page)
        return self.spark.spark.createDataFrame(results_rdd)

    def _get_unique(self, new_df, old_df) -> pyspark.sql.DataFrame:
        return new_df.join(old_df, on="hashed_comment_id", how="left_anti")
