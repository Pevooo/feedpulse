import os
import google.generativeai as genai
import model


class GeminiModel(model.Model):
    def __init__(self) -> None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_content(self, text: str) -> str:
        return self.model.generate_content(text).text
