import openai
from src.models.model import Model
from src.config.environment import Environment


class OpenAiModel(Model):
    """
    The OpenAI GPT4o-mini model
    """

    def __init__(self) -> None:
        openai.api_key = Environment.openai_api_key

    def generate_content(self, text: str):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": text},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
