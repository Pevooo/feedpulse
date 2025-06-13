import pandas as pd

from src.chatbot.routing_component import RoutingComponent
from src.models.global_model_provider import GlobalModelProvider


class Chatbot:
    def __init__(self, model_provider: GlobalModelProvider, dataset: pd.DataFrame):
        self.routing_component = RoutingComponent(model_provider)
        self.dataset = dataset

    def ask(self, question: str) -> tuple[str, int]:
        try:
            return self.routing_component.run(question, self.dataset)
        except RuntimeError:
            return "Chatbot failed to process input. Please try again!", 0
