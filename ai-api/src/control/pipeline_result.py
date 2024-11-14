from collections import defaultdict
from typing import Optional

from src.data.data_result import DataResult


class PipelineResult:
    def __init__(
        self, topics: set[str], results: Optional[list[DataResult]] = None
    ) -> None:
        self.items: list[DataResult] = results if results else []
        self.__topics: set[str] = topics
        self.__topic_counts = defaultdict(int)

    def append(self, data_result: DataResult) -> None:
        self.items.append(data_result)
        for topic in data_result.topics:
            self.__topic_counts[topic] += 1
