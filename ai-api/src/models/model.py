from abc import ABC, abstractmethod

from src.models.prompt import Prompt


class Model(ABC):
    """
    An abstract base class representing a model / content generation interface.

    This interface defines a contract for implementing classes to provide a
    `generate_content` method, which generates content based on a given text input.
    """

    @abstractmethod
    def generate_content(self, prompt: Prompt) -> str:
        """
        Generate content based on the provided text input.

        Args:
            prompt (Prompt): The input prompt based on which content is to be generated.

        Returns:
            str: The generated content as a str.
        """
        pass
