import time

from concurrent.futures import ThreadPoolExecutor

from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.data_providers.instagram_data_provider import InstagramDataProvider
from src.data_streamers.data_streamer import DataStreamer
from src.spark.spark import SparkTable


class PollingDataStreamer(DataStreamer):
    def start_streaming(self) -> None:
        with ThreadPoolExecutor(max_workers=1) as executor:
            while True:
                executor.submit(self.streaming_worker).result()
                time.sleep(self.trigger_time)

    def streaming_worker(self):
        def process_page(row):
            ac_token = row["ac_token"]
            platform = row["platform"]

            if platform == "facebook":
                return FacebookDataProvider(ac_token).get_posts()
            elif platform == "instagram":
                return InstagramDataProvider(ac_token).get_posts()

        df = self.spark.read(SparkTable.AC_TOKENS)
        results_rdd = df.rdd.flatMap(process_page)

        if not results_rdd.isEmpty():
            results_df = self.spark.spark.createDataFrame(results_rdd)
        else:
            return

        processed_comments = self.spark.read(SparkTable.PROCESSED_COMMENTS)
        stream_df = results_df.join(
            processed_comments, on="hashed_comment_id", how="left_anti"
        )

        self.spark.add(SparkTable.INPUT_COMMENTS, stream_df, "json")
