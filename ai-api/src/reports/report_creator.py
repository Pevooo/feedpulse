import json
from typing import Iterable, Optional

from src.control.pipeline_result import PipelineResult
from src.loaded_models.model import Model


class ReportCreator:
    def __init__(self, model: Model) -> None:
        self.model = model

    def create(self, result: PipelineResult) -> str:
        topic_counts = json.dumps(result.topic_counts)
        """
        This Method is for creating reborts.

        Args:
            topic_counts (str): The counts of positive and negative feedbacks on each topic
        
        Returns:
            str : contains a report that represent each topic and the number of positive feedbacks and number of negative feedbacks.
        """

        response: str = self.model.generate_content(self.wrap_text(result)).lower()

    def wrap_text(topic_counts) -> str:
        return f"""
            Please generate a well-structured report summarizing the positive and negative feedback counts
            for multiple topics based on the provided data.
            The data is in JSON format, where each key represents a topic name, 
            and its value is another dictionary containing the counts of 'positive_feedback' and 'negative_feedback' for that topic.

            Here is the data in JSON format:

           {topic_counts}

           The report should include:
	       1.	A section for each topic with its name.
	       2.	The counts of positive and negative feedback.
	       3.	A summary line for each topic, like: 'The topic [TOPIC_NAME] received [X] positive and [Y] negative feedback entries.'
	       4.	Make the report organized, neat, and easy to read.
           """
