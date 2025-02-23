import time

from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt


class GlobalModelProvider:
    def __init__(self, providers: list[ModelProvider], retry_delay: float = 60):
        self.providers = providers
        self.retry_delay = retry_delay

    def generate_content(self, prompt: Prompt) -> str:
        for _ in range(3):
            for provider in self.providers:
                try:
                    return provider.generate_content(prompt)
                except Exception:
                    pass
            time.sleep(self.retry_delay)
        raise Exception("No provider available")
