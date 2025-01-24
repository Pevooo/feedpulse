from src.config.environment import Environment
from src.models.model import Model
from src.models.prompt import Prompt
from huggingface_hub import InferenceClient

class HFQwen72BModel(Model):
    def __init__(self):
        self.client = InferenceClient(api_key=Environment.hf_token)

    def generate_content(self, prompt: Prompt) -> str:
        messages = [
            {
                "role": "system",
                "content": prompt.get_system_msg()
            },
            {
                "role": "user",
                "content": prompt.input_text
            }
        ]

        response = self.client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            max_tokens=2048,
            stream=True
        )

        response_text = ""
        for chunk in response:
            response_text += chunk.choices[0].delta.content

        return response_text