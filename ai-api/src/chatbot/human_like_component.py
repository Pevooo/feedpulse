from src.chatbot.component import Component
from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt


class HumanlikeComponent(Component):

    def __init__(self, model_provider: GlobalModelProvider):
        self.model_provider = model_provider

    def run(self, input_text, dataset):
        prompt = Prompt(
            instructions="You will be given some text make the text more human like. Just give me the human like version only.",
            context=None,
            examples=None,
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        return response
