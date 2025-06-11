import pandas as pd

from src.chatbot.routing_component import Routing
from src.models.global_model_provider import GlobalModelProvider


class Chatbot:
    def __init__(self, model_provider: GlobalModelProvider, dataset: pd.DataFrame):
        self.routing_component = Routing(model_provider)
        self.dataset = dataset

    def ask(self, question: str) -> str:
        return self.routing_component.run(question, self.dataset)
