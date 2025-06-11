from src.global_model_provider import GlobalModelProvider
from src.prompt import Prompt
from chatbot_component import ChatBotComponent
from chatbot import ChatBot
from sql_component import SqlComponent
from visualization_component import VisualizationComponent
from chat_component import ChatComponent

class Routing(ChatBotComponent):
    def __init__(self, model_provider: GlobalModelProvider):
        self.model_provider = model_provider

    def run(self, input_text, dataset):
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
            examples=[
                (
                    "How many complaints were received about water issues last month?",
                    "2",
                ),
                ("Hello, how are you!", "1"),
                ("Show me a chart of the most common complaint types this year.", "3"),
                ("asdf234@@!!", "4"),
            ],
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        try:
            category = int(response)
        except ValueError:
            category = 4

        if category == 1:
            return ChatComponent().run(input_text, dataset)
        elif category == 2:
            return SqlComponent().run(input_text, dataset)
        elif category == 3:
            return VisualizationComponent().run(input_text, dataset)
        else:
            raise ValueError("Input not understandable")
