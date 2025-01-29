from src.config.environment import Environment
from src.models.model import Model
from src.models.prompt import Prompt
from groq import Groq


class Llama33_70BVersatileModel(Model):
    def __init__(self):
        self.client = Groq(api_key=Environment.groqcloud_api_key)

    def generate_content(self, prompt: Prompt) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt.get_system_msg()},
                {"role": "user", "content": prompt.input_text},
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response_text = ""
        for chunk in response:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content

        return response_text
