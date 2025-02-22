from src.data_streamers.data_streamer import DataStreamer


class PollingDataStreamer(DataStreamer):
    def stream(self):
        # Should fetch all pages found in the database
        # Should create a data provider for each page
        # Should use get_posts method
        # Should only stream the new data (save new data to `streaming_dir`)
        # Should run this job every `trigger_time` seconds (or minutes)
        pass