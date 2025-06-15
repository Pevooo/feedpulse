import time

from src.config.updatable import Updatable
from src.config.settings import Settings
from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt
from src.utlity.util import log


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
                    response = provider.generate_content(prompt)
                    log(f"MODEL API REQUEST USING {provider.__class__.__name__}: {response}")
                except Exception:
                    log(f"MODEL API REQUEST FAILED USING {provider.__class__.__name__}: {response}", level="error")
            time.sleep(self._retry_delay)
        raise Exception("No provider available")

    def update(self) -> None:
        self._retry_delay = Settings.global_model_provider_retry_delay
        self._retry_count = Settings.global_model_provider_retry_count
