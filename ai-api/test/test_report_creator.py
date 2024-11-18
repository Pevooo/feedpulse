import json
import unittest
from unittest.mock import Mock

from src.loaded_models.model import Model
from src.reports.report_creator import ReportCreator

FAKE_TOPIC_COUNTS = json.dumps(
    {
        "cleanliness": {True: 2, False: 1},
        "food": {True: 0, False: 4},
    }
)


class TestReportCreator(unittest.TestCase):
    def setUp(self):
        self.report_creator = ReportCreator(Mock(spec=Model))

    def test_wrap_text(self):
        self.assertEqual(
            self.report_creator.wrap_text(FAKE_TOPIC_COUNTS),
            f"""
            Please generate a well-structured report summarizing the positive and negative feedback counts
            for multiple topics based on the provided data.
            The data is in JSON format, where each key represents a topic name,
            and its value is another dictionary containing the counts of 'positive_feedback' and 'negative_feedback' for that topic.

            Here is the data in JSON format:

           {FAKE_TOPIC_COUNTS}

            The report should include:
            1.	A section for each topic with its name.
            2.	The counts of positive and negative feedback.
            3.	A summary line for each topic, like: 'The topic [TOPIC_NAME] received [X] positive and [Y] negative feedback entries.'
            4.	Make the report organized, neat, and easy to read.
            """,
        )
