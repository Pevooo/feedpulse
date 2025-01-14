from typing import Iterable, Optional
from src.models.model import Model
from src.models.prompt import Prompt
from src.topics.feedback_topic import FeedbackTopic


class TopicDetector:
    """
    Detects relevant topics from a given text based on a predefined list of topics.
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def detect(
        self,
        text_batch: list[str],
        org_topics: Iterable[FeedbackTopic],
        context: Optional[str] = None,
    ) -> list[tuple[FeedbackTopic, ...]]:
        """
        Detects topics in the text that match the organization's topics.

        Args:
            text_batch (list[str]): The input text to analyze.
            org_topics (Iterable[FeedbackTopic]): The list of topics to map against.
            context (Optional[str]): Additional context for mapping (currently unused).

        Returns:
            list[tuple[str, ...]]: A tuple of detected topics.
        """
        prompt = self._generate_prompt(text_batch, org_topics, context)
        responses: list[str] = (
            self.model.generate_content(prompt).lower().replace("\n", "").split("|")
        )
        return self._extract_topics(responses)

    @staticmethod
    def _extract_topics(responses: list[str]) -> list[tuple[FeedbackTopic, ...]]:
        """
        Extracts relevant topics from the model's response.

        Args:
            responses (list[str]): The model-generated response text.

        Returns:
            list[tuple[FeedbackTopic, ...]]: A list of detected topics.
        """
        results = []
        for response in responses:
            if "no relevant topics found." in response:
                results.append(tuple())
            else:
                results.append(tuple(map(FeedbackTopic, response.split(","))))
        return results

    @staticmethod
    def _generate_prompt(
        text_batch: list[str],
        org_topics: Iterable[FeedbackTopic],
        context: Optional[str] = None,
    ) -> Prompt:
        """
        Generates a prompt for the model to detect topics.

        Args:
            text_batch (list[str]): The input text to analyze.
            org_topics (Iterable[FeedbackTopic]): The list of topics to map against.
            context (Optional[str]): Additional context for the prompt (currently unused).

        Returns:
            str: The formatted prompt string.
        """

        return Prompt(
            instructions=(
                "Identify and list only the relevant topics from the provided list that "
                f"relate to the content of the text. The topics are: {', '.join(topic.value for topic in org_topics)}.\n"
                "Only respond with relevant topics. If no topics are relevant, respond with 'no relevant topics found.'"
                "Don't add a space after or before each topics"
            ),
            context=context,
            examples=(
                (
                    "I didn't enjoy the food; it was bland and lacked variety.",
                    "food quality",
                ),
                (
                    "The check-in process was very slow and we had to wait for over an hour.",
                    "customer service,wait time",
                ),
                (
                    "The service was excellent; the staff were always polite, friendly, and eager to help.",
                    "service",
                ),
                (
                    "I didn't enjoy the food; it was bland and lacked variety.,"
                    "The check-in process was very slow and we had to wait for over an hour.,"
                    "The service was excellent; the staff were always polite, friendly, and eager to help.",
                    "food quality|customer service,wait time|service",
                ),
            ),
            input_text=",".join(text_batch),
        )
