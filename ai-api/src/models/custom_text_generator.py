from math import ceil
from typing import Union, List, Dict

from llmx import TextGenerator, TextGenerationConfig, TextGenerationResponse, Message

from src.models.global_model_provider import GlobalModelProvider


class CustomTextGenerator(TextGenerator):
    def __init__(
        self, model_provider: GlobalModelProvider, provider: str = "custom", **kwargs
    ):
        super().__init__(provider=provider, **kwargs)
        self.model_provider = model_provider

    def generate(
        self,
        messages: Union[List[Dict], str],
        config: TextGenerationConfig = TextGenerationConfig(),
        **kwargs
    ) -> TextGenerationResponse:
        messages = self.format_messages(messages)
        response = self.model_provider.generate_content(messages)
        return TextGenerationResponse(
            text=[Message(role="system", content=response)],
            logprobs=[],  # You may need to extract log probabilities from the response if needed
            usage={},
            config={},
        )

    def format_messages(self, messages) -> str:
        prompt = ""
        for message in messages:
            if message["role"] == "system":
                prompt += message["content"] + "\n"
            else:
                prompt += message["role"] + ": " + message["content"] + "\n"

        return prompt

    def count_tokens(self, text) -> int:
        return ceil(len(text) / 4)
