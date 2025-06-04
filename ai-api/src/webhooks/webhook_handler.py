from abc import ABC, abstractmethod
from typing import Any


class WebhookHandler(ABC):
    @abstractmethod
    def handle(self, webhook_data: dict[str, Any]) -> bool:
        """
        Handles webhook data.

        Args:
            webhook_data (dict): The webhook JSON payload.

        Returns:
            dict: Extracted comment details or None if not a comment event.
        """
        pass

    @abstractmethod
    def register(self, page_id: str, access_token: str) -> bool:
        """
        Registers a page for feed webhooks given an access token.

        Args:
            page_id (str): The id of the page.
            access_token (str): The access token that belongs to the page.

        Returns:
            bool: True if registration was successful otherwise False.
        """
        pass
