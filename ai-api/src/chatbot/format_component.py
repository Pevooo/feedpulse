from typing import Type

from src.chatbot.component import Component
from src.chatbot.query_component import QueryComponent
from src.chatbot.visualization_component import VisualizationComponent
from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt


class FormatComponent(Component):

    def __init__(self, model_provider: GlobalModelProvider, target_component: Type[Component]):
        self.model_provider = model_provider
        self.target_component = target_component

    def run(self, input_text, dataset):
        prompt = Prompt(
            instructions=(
                "You are a chatbot that is given a chat and based on the chat you want to output a prompt from your understanding of what the user needs. "
                f"Your prompt would be given to {self._get_target_description()}"
                "Output the precise prompt to the agent"
            ),
            context=None,
            examples=(
                (
                    "User: Hello\n"
                    "Assistant: Hello, I am your helpful assistant.\n"
                    "User: How many positive comments are there?",
                    "How many positive comments are there?",
                ),
                (
                    "User: Generate a chart of sentiments and time\n"
                    "Assistant: Chart generated Successfully\n"
                    "User: Not like this I want it to only have data from 2025",
                    "Generate a chart of sentiments and time considering data from 2025 only?",
                )
            ),
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        return response

    def _get_target_description(self):
        if self.target_component == QueryComponent:
            return "Query Agent which take the prompt and runs a query on the data"
        elif self.target_component == VisualizationComponent:
            return "Query Agent which takes the prompt and generated a visualization of the data based on the prompt"
