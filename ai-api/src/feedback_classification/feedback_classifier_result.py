from dataclasses import dataclass


@dataclass
class FeedbackClassifierResult:
    text_type: str
    has_topic: bool
