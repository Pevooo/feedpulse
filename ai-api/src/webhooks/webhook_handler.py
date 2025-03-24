from abc import ABC, abstractmethod
from typing import Any


class WebhookHandler(ABC):
    @abstractmethod
    def handle(self, webhook_data: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def register(self, page_id: str, access_token: str) -> bool:
        pass