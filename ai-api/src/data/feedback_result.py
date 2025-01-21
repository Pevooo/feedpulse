from dataclasses import dataclass

from src.topics.feedback_topic import FeedbackTopic


@dataclass
class FeedbackResult:
    """
    a result of the pipeline for single data unit
    """

    impression: bool
    topics: tuple[FeedbackTopic, ...]
