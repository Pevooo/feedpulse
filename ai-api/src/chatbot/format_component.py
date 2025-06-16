from typing import Type

from src.chatbot.component import Component
from src.chatbot.query_component import QueryComponent
from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt
from src.utlity.util import log


class FormatComponent(Component):
    """
    Takes the last 5 messages of the chat (already formatted as a USER/ASSISTANT text block)
    and distills exactly what the user wants next into a single concise instruction.
    Used to normalize inputs to QueryComponent or VisualizationComponent.
    """

    def __init__(
        self, model_provider: GlobalModelProvider, target_component: Type[Component]
    ):
        self.model_provider = model_provider
        self.target_component = target_component

    def run(self, input_text: str, dataset) -> str:
        # input_text: a string with 5 turns of USER/ASSISTANT lines

        # Determine task description based on target component
        if self.target_component == QueryComponent:
            target_desc = "a data query"
        else:
            target_desc = "a data visualization"

        instructions = (
            "You are a prompt extractor.\n"
            "Given exactly five turns of USER/ASSISTANT dialogue, output one concise sentence describing "
            f"what the user wants next for {target_desc}.\n"
            "Respond with ONLY that single sentence."
        )

        prompt = Prompt(
            instructions=instructions,
            context=None,
            examples=self._get_relevant_examples(),
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()
        log(f"RESPONSE FROM FORMAT COMPONENT: {response}")
        return response

    def _get_relevant_examples(self) -> tuple[tuple[str, str], ...]:
        if self.target_component == QueryComponent:
            return (
                (
                    "USER: What’s total sales in Q1?\n"
                    "ASSISTANT: $50k\n"
                    "USER: And by region?\n"
                    "ASSISTANT: North: $20k, South: $30k\n"
                    "USER: Now compare to Q2",
                    "Compare total sales by region between Q1 and Q2",
                ),
            )
        else:
            return (
                (
                    "USER: Show me a line chart of daily users.\n"
                    "ASSISTANT: [chart]\n"
                    "USER: Focus only on desktop users.\n"
                    "ASSISTANT: Done.\n"
                    "USER: Add a rolling average",
                    "Generate a line chart of daily desktop users with rolling average",
                ),
            )
