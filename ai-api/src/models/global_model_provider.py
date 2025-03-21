import time

from src.config.updatable import Updatable
from src.config.settings import Settings
from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt


class GlobalModelProvider(Updatable):
    def __init__(
        self, providers: list[ModelProvider], retry_delay: float = 60, retry_count=3
    ):
        self.providers = providers
        self._retry_delay = retry_delay
        self._retry_count = retry_count

    def generate_content(self, prompt: Prompt) -> str:
        for _ in range(self._retry_count):
            for provider in self.providers:
                try:
                    return provider.generate_content(prompt)
                except Exception:
                    pass
            time.sleep(self._retry_delay)
        raise Exception("No provider available")

    def update(self) -> None:
        self._retry_delay = Settings.global_model_provider_retry_delay
        self._retry_count = Settings.global_model_provider_retry_count
