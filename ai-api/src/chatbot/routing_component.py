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
You are classifying user questions or statements into four categories based on what they want.
Respond with only one number:
1 — General conversation (chit-chat, greetings, opinions not related to data)
2 — Query (the user wants a data answer or insight from the dataset, even in natural language)
3 — Data visualization (the user is asking for a chart or graph based on data)
4 — Irrelevant or unclear (nonsense, off-topic, or impossible to process)
Here are some examples:
""",
            context=None,
            examples=(
                ("Hello! How are you today?", "1"),
                ("Tell me a joke about social media", "1"),
                ("What are the most common complaints related to food?", "2"),
                ("What was the overall sentiment about healthcare in October?", "2"),
                ("Draw a bar chart of complaints per platform", "3"),
                ("I want a line chart showing food sentiment over time", "3"),
                ("I miss pizza", "1"),
                ("asdf123$@!", "4"),
                ("Tell me which topic had the most negative feedback on Facebook", "2"),
                ("Plot how sentiment about electricity changed in May", "3"),
            ),
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        try:
            category = int(response)
        except ValueError:
            category = 4

        try:
            if category == 1:
                return ChatComponent(self.model_provider).run(input_text, dataset), 0
            elif category == 2:
                return QueryComponent(self.model_provider).run(input_text, dataset), 0
            elif category == 3:
                return (
                    VisualizationComponent(self.model_provider).run(
                        input_text, dataset
                    ),
                    1,
                )
            else:
                raise ValueError("Input not understandable")
        except Exception as e:
            raise RuntimeError(
                f"Component failed to process input. Please try again!: {e}"
            )
