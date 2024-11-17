from typing import Iterable, Optional

from src.topic_detection.topic_detector_result import TopicDetectorResult
from src.loaded_models.model import Model


class TopicDetector:
    def __init__(self, model: Model) -> None:
        self.model = model

    def __call__(
        self, text: str, org_topics: Iterable[str], context: Optional[str] = None
    ) -> TopicDetectorResult:
        """
        This Method for detecting matching topics.

        Args:
            text (str): The text to detect.
            org_topics (Iterable[str]): The topics to map to.
            context (Optional[str]): The context to help the mapping process.
        Returns:
            TopicDetectorResult: Contains the list of detected topics.
        """

        response: str = self.model.generate_content(
            self.wrap_text(text, org_topics, context)
        ).lower()
        topics = self.extract_topics(response, org_topics)
        return TopicDetectorResult(topics)

    def extract_topics(
        self, response: str, org_topics: Iterable[str]
    ) -> tuple[str, ...]:
        response = response.split("only respond with relevant topics")[-1].strip()
        detected_topics = [topic for topic in org_topics if topic in response]
        return tuple(detected_topics)

    def wrap_text(
        self, text: str, org_topics: Iterable[str], context: Optional[str] = None
    ) -> str:
        # TODO: Use context tp generate better results
        return (
            "Identify and list only the relevant topics from the provided list that directly relate to the content in the text.\n"
            f"The list contains: {', '.join(org_topics)}.\n"
            f"And here is the text: '{text}.'"
            "Only respond with relevant topics. If no topics are relevant, respond with 'No relevant topics found.'"
        )
