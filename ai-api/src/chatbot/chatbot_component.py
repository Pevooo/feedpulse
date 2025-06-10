from abc import ABC, abstractmethod

from src.models.model_type import ModelType
from src.models.prompt import Prompt

class ChatBotComponent(ABC):
    """
    An abstract base class representing a chatbot interface.
    """
    
    @abstractmethod
    def run(self, text:str, dataset):
        pass