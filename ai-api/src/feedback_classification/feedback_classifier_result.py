from dataclasses import dataclass


@dataclass
class FeedbackClassifierResult:
    """
    represents the result of a feedback classification
    """

    text_type: str
    has_topic: bool
