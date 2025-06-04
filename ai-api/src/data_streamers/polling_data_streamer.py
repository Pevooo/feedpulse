# Deprecated: We now use webhook handlers

import logging
import time
import traceback

from src.concurrency.concurrency_manager import ConcurrencyManager
from src.config.settings import Settings
from src.config.updatable import Updatable
from src.data_streamers.data_streamer import DataStreamer
from src.data.data_manager import DataManager
from src.utlity.util import deprecated


class PollingDataStreamer(DataStreamer, Updatable):
    def __init__(
        self,
        data_manager: DataManager,
        trigger_time: int,
        concurrency_manager: ConcurrencyManager,
    ):
        self.data_manager = data_manager
        self.trigger_time = trigger_time
        self.concurrency_manager = concurrency_manager

    @deprecated
    def start_streaming(self) -> None:
        self.concurrency_manager.submit_job(self.streaming_worker)

    @deprecated
    def streaming_worker(self):
        try:
            self.data_manager.stream_by_polling()
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())

        time.sleep(self.trigger_time)
        self.concurrency_manager.submit_job(self.streaming_worker)

    def update(self) -> None:
        self.trigger_time = Settings.polling_data_streamer_trigger_time
