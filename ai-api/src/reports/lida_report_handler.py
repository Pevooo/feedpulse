import json
import pandas as pd
from datetime import datetime
import base64
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider
from lida import Manager, TextGenerationConfig

from src.models.custom_text_generator import CustomTextGenerator


from pyspark.sql.functions import col, substring_index
from src.data.data_manager import DataManager
from src.data.spark_table import SparkTable


class LidaReportHandler:
    def __init__(self, data_manager: DataManager, comments_table: SparkTable):
        model_provider = GlobalModelProvider([GoogleModelProvider()])
        self.text_generator = CustomTextGenerator(model_provider)
        self.lida = Manager(text_gen=self.text_generator)
        self.config = TextGenerationConfig(n=1, temperature=0.5)

        self.data_manager = data_manager
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
        filtered_page_data_df = self.data_manager.read(self.comments_table).filter(
            (substring_index(col("post_id"), "_", 1) == page_id)
            & (col("created_time") >= start_date)
            & (col("created_time") <= end_date)
        )  # spark data frame

        filtered_page_data_df = filtered_page_data_df.collect()

        data_as_dict = [row.asDict() for row in filtered_page_data_df]

        pandas_df = pd.DataFrame(data_as_dict)  # pandas data frame

        return pandas_df

    def summarize(self, page_id: str, start_date: datetime, end_date: datetime):
        """
        Generates a summary of the data by calling LIDA's summarize() method.
        """
        data = self.prepare_data(page_id, start_date, end_date)
        return self.lida.summarize(data)

    def goal(self, summary):
        """
        Generates and stores goals based on the summary.
        """
        result = self.lida.goals(summary=summary, n=2, textgen_config=self.config)

        """        print("\n=== Generated Goals ===")
        for idx, goal in enumerate(result):  # Ensure 'goals' key exists
            print(f"Goal {idx}:")
            print("  Question:", goal.question)
            print("  Suggested Visualization:", goal.visualization)
            print("  Rationale:", goal.rationale)
            print("---")
        """
        return result

    def visualize(self, summary, goal, idx):
        """
        Generates visualization code using LIDA's visualize() method based on the data summary.
        The method reuses the first goal from the previously generated goals.
        """

        chart = self.lida.visualize(
            summary=summary,
            textgen_config=self.config,
            library="seaborn",
            goal=goal,
        )

        if "," in chart[0].raster:
            base64_data = chart[0].raster.split(",")[1]
        else:
            base64_data = chart[0].raster

        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_data)

        # Write the image data to a file
        with open(
            rf"D:\GP\graduation-project\ai-api\src\reports\charts\chart{idx+1}.jpg",
            "wb",
        ) as f:
            f.write(image_data)

        return chart[0].code

    def explanation(self, chart_code):
        """
        Generates explanations for the visualization code.
        """

        explanations = self.lida.explain(code=chart_code, textgen_config=self.config)
        print("\nExplaination for chart")
        for explanation in explanations[0]:
            print(f"{explanation['section']}: {explanation['explanation']}\n")

    def refine_chart(self, summary, chart_code, idx):
        """
        Refines the generated visualization chart based on provided instructions.
        """

        instructions = [
            "Generate a feedback analysis report that clearly distinguishes positive and negative feedback. Highlight sentiment trends"
        ]

        refined_chart = self.lida.edit(
            code=chart_code,
            summary=summary,
            instructions=instructions,
            library="seaborn",
            textgen_config=self.config,
        )

        if "," in refined_chart[0].raster:
            base64_data = refined_chart[0].raster.split(",")[1]
        else:
            base64_data = refined_chart[0].raster

        image_data = base64.b64decode(base64_data)

        with open(
            rf"D:\GP\graduation-project\ai-api\src\reports\charts\refined_chart{idx+1}.jpg",
            "wb",
        ) as f:
            f.write(image_data)

        # return refined_chart[0].code

    def generate_report(self, page_id: str, start_date: datetime, end_date: datetime):
        """
        Generates a full report including summary, goals, and visualization.
        """
        report = "--- Report Generated with LIDA ---\n\n"
        summary = self.summarize(page_id, start_date, end_date)
        report += (
            "Data Summary:\n" + json.dumps(summary, indent=2, default=str) + "\n\n"
        )

        goals = self.goal(summary)
        for idx, goal in enumerate(goals):
            report += f"Goal {idx+1}: {goal.question}\n"
            report += f"Rationale: {goal.rationale}\n\n"
            chart_code = self.visualize(summary, goal, idx)
            report += f"Visualization Code (for Goal {idx+1}):\n" + chart_code + "\n"
            # self.explanation(chart_code)
            self.refine_chart(summary, chart_code, idx)

        report += "--- Report Generated with LIDA END ---\n\n"
        print(report)
        return report
