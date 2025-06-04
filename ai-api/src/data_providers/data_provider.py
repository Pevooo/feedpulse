# DEPRECATED: We now use webhooks with webhook handlers

from abc import ABC, abstractmethod

from src.utlity.util import deprecated


class DataProvider(ABC):
    """
    an interface for data providers (e.g. Facebook, Instagram, etc.)
    """

    @deprecated
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    @abstractmethod
    def get_posts(self):
        """
        Fetches posts from data provider
        """
        pass
