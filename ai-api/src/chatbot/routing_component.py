from src.chatbot.chat_component import ChatComponent
from src.chatbot.component import Component
from src.chatbot.format_component import FormatComponent
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
        You are an intent classifier.  You receive exactly the last 5 turns of a conversation,
        formatted like this:

        USER: <user message>
        ASSISTANT: <assistant message>
        … (up to 5 alternating lines)

        Your job is to decide **exactly one** of three modes:
        1 — CHAT: general chit‑chat, greetings, casual conversation, opinions/advice about the data.
        2 — QUERY: the user is asking for a data answer or insight that requires querying the dataset.
        3 — VIZ: the user wants a chart or graph based on the data.

        **Respond with ONLY the digit “1”, “2”, or “3” (no extra words, punctuation, or explanation).**
        """,
            examples=(
                # chit‑chat → 1
                (
                    "USER: Hello!\n"
                    "ASSISTANT: Hi there, how can I help?\n"
                    "USER: How’s the weather?\n"
                    "ASSISTANT: It’s sunny today.\n"
                    "USER: Thanks!",
                    "1",
                ),
                # data query → 2
                (
                    "USER: Show me total sales in April.\n"
                    "ASSISTANT: April sales were $12,000.\n"
                    "USER: And how does that compare to March?",
                    "2",
                ),
                # visualization → 3
                (
                    "USER: I’d like a bar chart of monthly users.\n"
                    "ASSISTANT: Generating chart…\n"
                    "USER: Great, can you show it again focusing on desktop users?",
                    "3",
                ),
            ),
            context=input_text,
            input_text="",  # already included in context
        )

        response = self.model_provider.generate_content(prompt).strip()
        component, is_raster = self._choose_component(response)

        if isinstance(component, QueryComponent) or isinstance(
            component, VisualizationComponent
        ):
            input_text = FormatComponent(self.model_provider, component.__class__).run(
                input_text, dataset
            )

        return component.run(input_text, dataset), is_raster

    def _choose_component(self, response):
        try:
            category = int(response)
        except ValueError:
            category = 1

        if category < 1 or category > 3:
            category = 1

        try:
            if category == 1:
                return ChatComponent(self.model_provider), 0
            elif category == 2:
                return QueryComponent(self.model_provider), 0
            elif category == 3:
                return (
                    VisualizationComponent(self.model_provider),
                    1,
                )
        except Exception as e:
            raise RuntimeError(
                f"Component failed to process input. Please try again!: {e}"
            )
