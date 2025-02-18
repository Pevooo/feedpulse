from abc import ABC, abstractmethod


class DataStreamer(ABC):
    """
    an interface for data streamers (e.g. Facebook, Instagram, etc.)
    """

    @abstractmethod
    def stream(self, payload: dict) -> None:
        """
        Takes the webhook request and streams it to the streaming path
        """
        pass
