from abc import ABC, abstractmethod
from typing import Any


class WebhookHandler(ABC):
    @abstractmethod
    def handle(self, payload: dict[str, Any]) -> bool:
        pass
