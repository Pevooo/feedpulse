import json
import pandas as pd
from datetime import datetime

from src.models.hf_model_provider import HFModelProvider  # using our custom HF provider
from src.spark.spark import Spark
from src.spark.spark_table import SparkTable
from lida import Manager, TextGenerationConfig

# from pyspark.sql import DataFrame
from pyspark.sql.functions import col, substring_index
from src.spark.spark import Spark
from src.spark.spark_table import SparkTable
from lida import Manager, llm, TextGenerationConfig


class LidaReportHandler:
    def __init__(self, spark: Spark, comments_table: SparkTable):
        # Instead of HFTextGenerator, we instantiate our HFModelProvider.
        model_provider = HFModelProvider()
        self.lida = Manager(model_provider)
        self.config = TextGenerationConfig(n=1, temperature=0.5)
        self.summary = None
        self.chart_code = None
        self.goals = None

        self.spark = spark
        self.comments_table = comments_table

    def prepare_data(
        self, page_id: str, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Prepare and filter the data.
        Args:
            page_id (str): The id of the page which the report belongs to.
            start_date (datetime): The start date of the data to be included in the report.
            end_date (datetime): The end date of the data to be included in the report.
        Returns:
            pd.DataFrame: The filtered data.
        """
        filtered_page_data_df = self.spark.read(self.comments_table).filter(
            (substring_index(col("post_id"), "_", 1) == page_id)
            & (col("created_time") >= start_date)
            & (col("created_time") <= end_date)
        )  # spark data frame

        pandas_df = filtered_page_data_df.toPandas()  # pandas data frame

        df = pd.DataFrame(pandas_df)
        return df

    def summarize(self, page_id: str, start_date: datetime, end_date: datetime):
        """
        Generates a summary of the data by calling LIDA's summarize() method.
        """
        data = self.prepare_data(page_id, start_date, end_date)
        self.summary = self.lida.summarize(data)
        return self.summary

    def goal(self):
        """
        Generates and stores goals based on the summary.
        """
        if self.summary is None:
            raise ValueError("No summary available. Please run summarize() first.")

        self.goals = self.lida.goals(self.summary, n=2, textgen_config=self.config)
        print("\n=== Generated Goals ===")
        for idx, goal in enumerate(self.goals):
            print(f"Goal {idx}:")
            print("  Question:", goal.question)
            print("  Suggested Visualization:", goal.visualization)
            print("  Rationale:", goal.rationale)
            print("---")
        return self.goals

    def visualize(self):
        """
        Generates visualization code using LIDA's visualize() method based on the data summary.
        The method reuses the first goal from the previously generated goals.
        """
        if self.summary is None:
            raise ValueError("No summary available. Please run summarize() first.")
        if self.goals is None:
            self.goal()
        chart = self.lida.visualize(
            summary=self.summary,
            textgen_config=self.config,
            library="seaborn",
            goal=self.goals[0],
        )

        print("Generated Visualization Code:")
        print(chart.code)
        self.chart_code = chart.code
        return chart.code

    def explanation(self):
        """
        Generates explanations for the visualization code.
        """
        if self.chart_code is None:
            self.visualize()
        explanations = self.lida.explain(
            code=self.chart_code, textgen_config=self.config
        )
        print("\n=== Chart Explanation ===")
        for explanation in explanations[0]:
            print(f"{explanation['section']}: {explanation['explanation']}")

    def refine_chart(self):
        """
        Refines the generated visualization chart based on provided instructions.
        """
        if self.summary is None:
            raise ValueError("No summary available. Please run summarize() first.")
        if self.chart_code is None:
            self.visualize()

        instructions = ["Change the title to 'Report: Positive vs Negative Feedback'"]

        refined_chart = self.lida.edit(
            code=self.chart_code,
            summary=self.summary,
            instructions=instructions,
            library="seaborn",
            textgen_config=self.config,
        )

        return refined_chart

    def generate_report(self, page_id: str, start_date: datetime, end_date: datetime):
        """
        Generates a full report including summary, goals, and visualization.
        """
        summary = self.summarize(page_id, start_date, end_date)
        report = f"--- Report Generated with LIDA ---\n\n"
        report += (
            "Data Summary:\n" + json.dumps(summary, indent=2, default=str) + "\n\n"
        )
        print("Summary complete.")
        print(report)

        goals = self.goal()
        for idx, goal in enumerate(goals):
            report += f"Goal {idx+1}: {goal.question}\n"
            report += f"Rationale: {goal.rationale}\n\n"

        chart_code = self.visualize()
        report += "Visualization Code (for Goal 1):\n" + chart_code + "\n"

        print("\n=== Final Report ===")
        print(report)
        return report
