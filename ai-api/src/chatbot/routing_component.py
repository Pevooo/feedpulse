from src.chatbot.chat_component import ChatComponent
from src.chatbot.component import Component
from src.chatbot.query_component import QueryComponent
from src.chatbot.visualization_component import VisualizationComponent
from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt


class RoutingComponent(Component):
    def __init__(self, model_provider: GlobalModelProvider):
        self.model_provider = model_provider

    def run(self, input_text, dataset) -> tuple[str, int]:
        prompt = Prompt(
            instructions="""
            You will be given a statement. Classify it into one of the following contexts by responding with only the corresponding number:
            1 — General conversation
            2 — SQL query
            3 — Data visualization
            4 — Irrelevant or not understandable

            Please respond with only one number (1, 2, 3, or 4).
            """,
            context=None,
            examples=(
                (
                    "How many complaints were received about water issues last month?",
                    "2",
                ),
                ("Hello, how are you!", "1"),
                ("Show me a chart of the most common complaint types this year.", "3"),
                ("asdf234@@!!", "4"),
            ),
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        try:
            category = int(response)
        except ValueError:
            category = 4

        if category == 1:
            return ChatComponent(self.model_provider).run(input_text, dataset), 0
        elif category == 2:
            return QueryComponent(self.model_provider).run(input_text, dataset), 1
        elif category == 3:
            return (
                VisualizationComponent(self.model_provider).run(input_text, dataset),
                0,
            )
        else:
            raise ValueError("Input not understandable")
