import json

from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt
from src.utlity.util import deprecated


class ReportHandler:
    def __init__(self, provider: GlobalModelProvider):
        self.provider = provider

    @deprecated
    def create(self, result) -> str:
        """
        Creates a report from the given result.

        Args:
            result (PipelineResult): The result of the pipeline.

        Returns:
            str : contains a report that represent each topic and the number of positive feedbacks and number
            of negative feedbacks.
        """

        topic_counts = json.dumps(result.topic_counts)
        return self.provider.generate_content(self._generate_prompt(topic_counts))

    @staticmethod
    @deprecated
    def _generate_prompt(topic_counts: str) -> Prompt:
        return Prompt(
            instructions=(
                """
                Please generate a well-structured report summarizing the positive and negative feedback counts
                for multiple topics based on the provided data.
                The data is in JSON format, where each key represents a topic name,
                and its value is another dictionary containing the counts of 'positive_feedback' and 'negative_feedback' for that topic.

                Here is the data in JSON format:

                The report should include:
                1.	A section for each topic with its name.
                2.	The counts of positive and negative feedback.
                3.	A summary line for each topic, like: 'The topic [TOPIC_NAME] received [X] positive and [Y] negative feedback entries.'
                4.	Make the report organized, neat, and easy to read.
                """
            ),
            context=None,
            examples=None,
            input_text=topic_counts,
        )
