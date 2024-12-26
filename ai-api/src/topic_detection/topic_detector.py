from typing import Iterable, Optional
from src.models.model import Model
from src.models.prompt import Prompt

class TopicDetector:
    """
    Detects relevant topics from a given text based on a predefined list of topics.
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def detect(
        self, text: str, org_topics: Iterable[str], context: Optional[str] = None
    ) -> tuple[str, ...]:
        """
        Detects topics in the text that match the organization's topics.

        Args:
            text (str): The input text to analyze.
            org_topics (Iterable[str]): The list of topics to map against.
            context (Optional[str]): Additional context for mapping (currently unused).

        Returns:
            tuple[str, ...]: A tuple of detected topics.
        """
        prompt = self._generate_prompt(text, org_topics, context)
        response = self.model.generate_content(prompt).lower()
        return tuple(self._extract_topics(response, org_topics))

    def _extract_topics(self, response: str, org_topics: Iterable[str]) -> list[str]:
        """
        Extracts relevant topics from the model's response.

        Args:
            response (str): The model-generated response text.
            org_topics (Iterable[str]): The list of topics to map against.

        Returns:
            list[str]: A list of detected topics.
        """
        relevant_section = response.split("only respond with relevant topics")[
            -1
        ].strip()
        return [topic for topic in org_topics if topic.lower() in relevant_section]

    def _generate_prompt(
        self, text: str, org_topics: Iterable[str], context: Optional[str] = None
    ) -> str:
        """
        Generates a prompt for the model to detect topics.

        Args:
            text (str): The input text to analyze.
            org_topics (Iterable[str]): The list of topics to map against.
            context (Optional[str]): Additional context for the prompt (currently unused).

        Returns:
            str: The formatted prompt string.
        """
        return Prompt(
            instructions=(
                "Identify and list only the relevant topics from the provided list that "
                f"relate to the content of the text. The topics are: {', '.join(org_topics)}.\n"
                "Only respond with relevant topics. If no topics are relevant, respond with 'No relevant topics found.'"
            ),
            context=None,
            examples=( 
                ("I didn't enjoy the food; it was bland and lacked variety.", "Relevant topics: food quality"),
                ("The check-in process was very slow and we had to wait for over an hour.", "Relevant topics: customer service, wait time"),
                ("The service was excellent; the staff were always polite, friendly, and eager to help.", "Relevant topics: service"),        
            ),
            input_text=text,
        ).to_text()
