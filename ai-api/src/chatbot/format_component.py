from typing import Type

from src.chatbot.component import Component
from src.chatbot.query_component import QueryComponent
from src.chatbot.visualization_component import VisualizationComponent
from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt


class FormatComponent(Component):

    def __init__(
        self, model_provider: GlobalModelProvider, target_component: Type[Component]
    ):
        self.model_provider = model_provider
        self.target_component = target_component

    def run(self, input_text, dataset):
        prompt = Prompt(
            instructions=(
                "You are a chatbot that is given the last 5 messages from a chat and based "
                "on the chat you want to output a prompt from your understanding of what the user needs. "
                f"Your prompt would be given to {self._get_target_description()}"
                "Output the precise prompt to the agent. "
                "Very Important note: In the chat there may be other questions before the last one, make sure to understand "
                "what the user wants right now. "
            ),
            context=None,
            examples=self._get_relevant_examples(),
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        return response

    def _get_target_description(self) -> str:
        if self.target_component == QueryComponent:
            return "Query Agent which take the prompt and runs a query on the data. It can't make a visualization. "
        elif self.target_component == VisualizationComponent:
            return "Query Agent which takes the prompt and generated a visualization of the data based on the prompt. "

    def _get_relevant_examples(self) -> tuple[tuple[str, str], ...]:
        if self.target_component == QueryComponent:
            return (
                (
                    "User: Hello\n"
                    "Assistant: Hello, I am your helpful assistant.\n"
                    "User: How many positive comments are there?",
                    "How many positive comments are there?",
                ),
            )
        elif self.target_component == VisualizationComponent:
            return (
                (
                    "User: Generate a chart of sentiments and time\n"
                    "Assistant: Chart generated Successfully\n"
                    "User: Not like this I want it to only have data from 2025",
                    "Generate a chart of sentiments and time considering data from 2025 only",
                ),
            )
