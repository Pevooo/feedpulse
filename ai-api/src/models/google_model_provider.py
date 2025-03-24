import google.generativeai as genai

from src.models.google_model import GoogleModel
from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt
from src.config.environment import Environment


class GoogleModelProvider(ModelProvider):
    def __init__(self):
        genai.configure(api_key=Environment.gemini_api_key)

    def generate_content(
        self, prompt: Prompt, model: GoogleModel = GoogleModel.DEFAULT
    ) -> str:
        return genai.GenerativeModel(model.value).generate_content(str(prompt)).text
