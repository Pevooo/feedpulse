from dataclasses import dataclass


@dataclass
class TopicDetectorResult:
    """
    The result of a topic detection task.
    """

    topics: tuple[str, ...]
