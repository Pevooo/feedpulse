# Deprecated: We now use webhook handlers

from abc import ABC, abstractmethod


class DataStreamer(ABC):
    @abstractmethod
    def streaming_worker(self):
        pass

    @abstractmethod
    def start_streaming(self):
        pass
