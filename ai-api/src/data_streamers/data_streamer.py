from abc import ABC, abstractmethod

from src.spark.spark import SparkTable


class DataStreamer(ABC):
    def __init__(self, trigger_time: int, streaming_dir: SparkTable):
        self.trigger_time = trigger_time
        self.streaming_dir = streaming_dir

    @abstractmethod
    def stream(self):
        pass