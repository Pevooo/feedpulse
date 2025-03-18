import json

from datetime import datetime

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, substring_index

from src.models.global_model_provider import GlobalModelProvider
from src.models.prompt import Prompt
from src.data.data_manager import DataManager
from src.data.spark_table import SparkTable


class ReportHandler:
    def __init__(
        self,
        provider: GlobalModelProvider,
        spark: DataManager,
        comments_table: SparkTable,
    ):
        self.provider = provider
        self.spark = spark
        self.comments_table = comments_table

    def create(self, page_id: str, start_date: datetime, end_date: datetime) -> str:
        """
        Creates a report from the given result.

        Args:
            page_id (str): The id of the page which the report belongs to.
            start_date (datetime): The start date of the data to be included in the report.
            end_date (datetime): The end date of the data to be included in the report.

        Returns:
            str : contains a report that represent each topic and the number of positive feedbacks and number
            of negative feedbacks.
        """

        filtered_data_df = self._get_filtered_page_data(page_id, start_date, end_date)

        filtered_data = filtered_data_df.collect()
        data_as_dict = [row.asDict() for row in filtered_data]

        return self.provider.generate_content(
            self._generate_prompt(
                json.dumps(data_as_dict, default=lambda date: date.isoformat())
            ),
        )

    def _get_filtered_page_data(
        self, page_id: str, start_date: datetime, end_date: datetime
    ) -> DataFrame:
        return self.spark.read(self.comments_table).filter(
            (substring_index(col("post_id"), "_", 1) == page_id)
            & (col("created_time") >= start_date)
            & (col("created_time") <= end_date)
        )

    @staticmethod
    def _generate_prompt(data: str) -> Prompt:
        return Prompt(
            instructions=(
                """
                Please generate a well-structured report summarizing the positive and negative feedback counts
                for multiple topics based on the provided data.
                The data is in JSON format, where each object represents a comment containing useful information.,

                The report should include:
                1.	A section for each topic with its name.
                2.	The counts of positive and negative feedback.
                3.	A summary line for each topic, like: 'The topic [TOPIC_NAME] received [X] positive and [Y] negative feedback entries.'
                4.	Make the report organized, neat, and easy to read.
                """
            ),
            context=None,
            examples=None,
            input_text=data,
        )
