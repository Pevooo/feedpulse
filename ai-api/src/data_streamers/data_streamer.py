from abc import ABC, abstractmethod

from src.spark.spark import SparkTable, Spark


class DataStreamer(ABC):
    def __init__(self, spark: Spark, trigger_time: int, streaming_dir: SparkTable):
        self.spark = spark
        self.trigger_time = trigger_time
        self.streaming_dir = streaming_dir

    @abstractmethod
    def streaming_worker(self):
        pass

    @abstractmethod
    def start_streaming(self):
        pass
