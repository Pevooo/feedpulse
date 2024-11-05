import google.generativeai as genai
import src.loaded_models.model as model
from src.config.feed_pulse_environment import FeedPulseEnvironment


class GeminiModel(model.Model):
    def __init__(self) -> None:
        genai.configure(api_key=FeedPulseEnvironment.gemini_api_key)
        self.__model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_content(self, text: str) -> str:
        return self.__model.generate_content(text).text
