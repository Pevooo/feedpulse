from openai import OpenAI
from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt
from src.models.or_model import ORModel
from src.config.environment import Environment


class ORModelProvider(ModelProvider):
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1", api_key=Environment.or_api_key
        )

    def generate_content(self, prompt: Prompt, model: ORModel = ORModel.DEFAULT) -> str:
        return (
            self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt.to_text()}],
                model=model.value,
            )
            .choices[0]
            .message.content
        )
