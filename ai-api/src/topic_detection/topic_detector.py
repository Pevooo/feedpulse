from typing import Iterable, Optional

from src.models.model import Model


class TopicDetector:
    """
    The class responsible for detecting topics of the feedbacks.
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def detect(
        self, text: str, org_topics: Iterable[str], context: Optional[str] = None
    ) -> tuple[str, ...]:
        """
        This Method for detecting matching topics.

        Args:
            text (str): The text to detect.
            org_topics (Iterable[str]): The topics to map to.
            context (Optional[str]): The context to help the mapping process.
        Returns:
            tuple[str, ...]: Contains the list of detected topics.
        """

        response: str = self.model.generate_content(
            self.wrap_text(text, org_topics, context)
        ).lower()
        return tuple(self.extract_topics(response, org_topics))

    def extract_topics(self, response: str, org_topics: Iterable[str]) -> list[str]:
        response = response.split("only respond with relevant topics")[-1].strip()
        detected_topics = [topic for topic in org_topics if topic.lower() in response]
        return detected_topics

    def wrap_text(
        self, text: str, org_topics: Iterable[str], context: Optional[str] = None
    ) -> str:
        # TODO: Use context to generate better results
        return (
            "Identify and list only the relevant topics from the provided list that directly relate to the content in the text.\n"
            f"The list contains: {', '.join(org_topics)}.\n"
            f"And here is the text: '{text}.'"
            "Only respond with relevant topics. If no topics are relevant, respond with 'No relevant topics found.'"
        )
