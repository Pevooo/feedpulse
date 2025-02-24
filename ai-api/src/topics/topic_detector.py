from typing import Optional

from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt
from src.topics.feedback_topic import FeedbackTopic


class TopicDetector:
    """
    Detects relevant topics from a given text based on a predefined list of topics.
    """

    def __init__(self, model_provider: GlobalModelProvider) -> None:
        self.provider = model_provider

    def detect(
        self,
        text_batch: list[str],
        context: Optional[str] = None,
    ) -> list[list[FeedbackTopic]]:
        """
        Detects topics in the text that match the organization's topics.

        Args:
            text_batch (list[str]): The input text to analyze.
            context (Optional[str]): Additional context for mapping (currently unused).

        Returns:
            list[tuple[str, ...]]: A tuple of detected topics.
        """
        prompt = self._generate_prompt(text_batch, context)
        response = self.provider.generate_content(prompt)
        responses: list[str] = response.lower().replace("\n", "").split("|")
        return self._extract_topics(responses)

    @staticmethod
    def _extract_topics(responses: list[str]) -> list[list[FeedbackTopic]]:
        """
        Extracts relevant topics from the model's response.

        Args:
            responses (list[str]): The model-generated response text.

        Returns:
            list[tuple[FeedbackTopic, ...]]: A list of detected topics.
        """
        results = []
        for response in responses:
            if "none" in response:
                results.append(list())
            else:
                results.append(list(map(FeedbackTopic, response.split(","))))
        return results

    @staticmethod
    def _generate_prompt(
        text_batch: list[str],
        context: Optional[str] = None,
    ) -> Prompt:
        """
        Generates a prompt for the model to detect topics.

        Args:
            text_batch (list[str]): The input text to analyze.
            context (Optional[str]): Additional context for the prompt (currently unused).

        Returns:
            str: The formatted prompt string.
        """
        input_text = ""
        for i, text in enumerate(text_batch):
            input_text += f"\ntext{i}: {text}"
        return Prompt(
            instructions=(
                "Identify and list only the relevant topics from the provided list that "
                f"relate to the content of the text. The topics are: {', '.join(FeedbackTopic.get_all_topics_as_string())}.\n"
                "Only respond with relevant topics. If no topics are relevant, respond with 'NONE'"
                "Don't add a space after or before each topic and do not put anything in the response other than the topics and the separators\n"
                "For each comment that starts with text{n} write the relevant topics, for separating topics use a comma, for separating each text use |"
            ),
            context=context,
            examples=(
                (
                    "I didn't enjoy the food; it was bland and lacked variety.",
                    "food",
                ),
                (
                    "The check-in process was very slow and we had to wait for over an hour.",
                    "customer_service",
                ),
                (
                    "The service was excellent; the staff were always polite, friendly, and eager to help.",
                    "service,communication",
                ),
                (
                    "text{0}: I didn't enjoy the food; it was bland and lacked variety.,"
                    "text{1}: The check-in process was very slow and we had to wait for over an hour.,"
                    "text{2}: The service was excellent; the staff were always polite, friendly, and eager to help.",
                    "food|customer_service|service,communication",
                ),
            ),
            input_text=input_text,
        )
