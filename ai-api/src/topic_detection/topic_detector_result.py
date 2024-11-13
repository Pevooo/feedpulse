from dataclasses import dataclass


@dataclass
class TopicDetectorResult:
    topics: tuple[str, ...]
