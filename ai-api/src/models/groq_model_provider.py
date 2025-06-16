from groq import Groq

from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt
from src.models.groq_model import GroqModel
from src.config.environment import Environment


class GroqModelProvider(ModelProvider):
    def __init__(self):
        self.client = Groq(api_key=Environment.groq_token)

    def generate_content(
        self,
        prompt: Prompt,
        model: GroqModel = GroqModel.DEFAULT,
        temperature: float = 1.0,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model.value,
            messages=[{"role": "user", "content": str(prompt)}],
            temperature=temperature,
        )
        return response.choices[0].message.content
