import google.generativeai as genai
from src.models.model import Model
from src.config.environment import Environment
from src.models.prompt import Prompt


class GeminiModel(Model):
    """
    The Google Gemini model
    """

    def __init__(self) -> None:
        genai.configure(api_key=Environment.gemini_api_key)
        self.__model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_content(self, prompt: Prompt) -> str:
        return self.__model.generate_content(str(prompt)).text
