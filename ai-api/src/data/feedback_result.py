from dataclasses import dataclass


@dataclass
class FeedbackResult:
    """
    a result of the pipeline for single data unit
    """

    impression: bool
    topics: tuple[str, ...]
