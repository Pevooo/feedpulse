from abc import ABC, abstractmethod


class ChatBotComponent(ABC):
    """
    An abstract base class representing a chatbot interface.
    """

    @abstractmethod
    def run(self, input_text: str, dataset):
        pass
