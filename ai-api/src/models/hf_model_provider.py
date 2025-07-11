from huggingface_hub import InferenceClient
from src.models.hf_model import HFModel
from src.models.model_provider import ModelProvider
from src.models.prompt import Prompt
from src.config.environment import Environment


class HFModelProvider(ModelProvider):
    def __init__(self):
        self.client = InferenceClient(token=Environment.hf_token)

    def generate_content(
        self, prompt: Prompt, model: HFModel = HFModel.DEFAULT, temperature: float = 1.0
    ) -> str:
        return self.client.text_generation(
            prompt=prompt.to_text(),
            model=model.value,
            temperature=temperature,
        )
