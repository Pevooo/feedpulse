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
You are given the latest 5 messages from a chat between a user and an assistant and based on them you should do the following:
You are classifying user questions or statements into four categories based on what they want. You should never choose the wrong number.
Respond with only one number:
1 — General conversation (chit-chat, greetings, opinions, advices about data)
or Irrelevant or unclear text (nonsense, off-topic, or impossible to process)
2 — Query (the user wants a data answer that needs a query on the data or insight from the dataset, even in natural language)
3 — Data visualization (the user is asking for a chart or graph based on data)
""",
            context=None,
            examples=(
                ("User: Hello! How are you today?", "1"),
                ("User: Tell me a joke about social media", "1"),
                ("User: What are the most common complaints related to food?", "2"),
                (
                    "User: What was the overall sentiment about healthcare in October?",
                    "2",
                ),
                ("User: Draw a bar chart of complaints per platform", "3"),
                ("User: I want a line chart showing food sentiment over time", "3"),
                ("User: I miss pizza", "1"),
                ("User: asdf123$@!", "1"),
                (
                    "User: Tell me which topic had the most negative feedback on Facebook",
                    "2",
                ),
                ("User: Plot how sentiment about electricity changed in May", "3"),
                (
                    "User: Hello\n"
                    "Assistant: Hi, how can I help you?\n"
                    "User: How many comments are there\n"
                    "Assistant: 12\n"
                    "User: Nice, how can I increase my engagement?",
                    "1",
                ),
                (
                    "User: Make me a visualization of sentiment and time\n"
                    "Assistant: Chart generated Successfully\n"
                    "User: Hmm nice! How many food related comments are there?\n"
                    "Assistant: 4\n"
                    "User: Nice, I now want a visualization of the topics",
                    "3",
                ),
            ),
            input_text=input_text,
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
