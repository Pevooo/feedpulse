from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def generate_content(self, text: str):
        pass
