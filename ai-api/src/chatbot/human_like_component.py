from src.chatbot.component import Component
from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt


class HumanlikeComponent(Component):

    def __init__(self, model_provider: GlobalModelProvider):
        self.model_provider = model_provider

    def run(self, input_text, dataset):
        prompt = Prompt(
            instructions=(
                "You are a chatbot that is given some text in the prompt to make the text more human like."
                "Just give me the human like version only without any additional information."
            ),
            context=None,
            examples=None,
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        return response
