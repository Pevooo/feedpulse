from abc import ABC, abstractmethod

from src.models.model_type import ModelType
from src.models.prompt import Prompt


class ModelProvider(ABC):
    """
    An abstract base class representing a model / content generation interface.

    This interface defines a contract for implementing classes to provide a
    `generate_content` method, which generates content based on a given text input.
    """

    @abstractmethod
    def generate_content(
        self, prompt: Prompt, model: ModelType = None, temperature: float = None
    ) -> str:
        """
        Generate content based on the provided text input.

        Args:
            prompt (Prompt): The input prompt based on which content is to be generated.
            model (ModelType): The model to generate content with.
            temperature (float): The temperature to use.

        Returns:
            str: The generated content as a str.
        """
        pass
