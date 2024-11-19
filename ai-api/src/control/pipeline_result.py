from src.data.data_result import DataResult


class PipelineResult:
    """
    Represents the result of a pipeline. (determining the impression and detecting the topics of data)
    """

    def __init__(self, topics: set[str]) -> None:
        self.items: list[DataResult] = []
        self.topics: set[str] = topics
        self.topic_counts = {}
        for topic in topics:
            self.topic_counts[topic] = {False: 0, True: 0}

    def append(self, data_result: DataResult) -> None:
        self.items.append(data_result)
        for topic in data_result.topics:
            if data_result.impression:
                self.topic_counts[topic][True] += 1
            else:
                self.topic_counts[topic][False] += 1

    def extend(self, data_results: "PipelineResult") -> None:
        if data_results.topics != self.topics:
            raise ValueError("Both results should have the same topics")

        self.items.extend(data_results.items)
        for data_result in data_results.items:
            for topic in data_result.topics:
                if data_result.impression:
                    self.topic_counts[topic][True] += 1
                else:
                    self.topic_counts[topic][False] += 1
