from datetime import datetime

from src.reports.report import Report
from src.reports.custom_text_generator import CustomTextGenerator
from src.models.global_model_provider import GlobalModelProvider
from src.models.model_provider import ModelProvider
from src.data.data_manager import DataManager

from lida import Manager, TextGenerationConfig


class LidaReportHandler:
    def __init__(self, data_manager: DataManager, model_providers: list[ModelProvider]):
        model_provider = GlobalModelProvider(model_providers)
        self.text_generator = CustomTextGenerator(model_provider)
        self.lida = Manager(text_gen=self.text_generator)
        self.config = TextGenerationConfig(n=1, temperature=0.5)

        self.data_manager = data_manager

    def summarize(self, page_id: str, start_date: datetime, end_date: datetime):
        """
        Generates a summary of the data by calling LIDA's summarize() method.
        """
        data = self.data_manager.filter_data(page_id, start_date, end_date)
        return self.lida.summarize(data)

    def goal(self, summary):
        """
        Generates and stores goals based on the summary.
        """
        return self.lida.goals(summary=summary, n=2, textgen_config=self.config)

    def visualize(self, summary, goal):
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

        return chart[0]

    def refine_chart(self, summary, chart_code):
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

        return refined_chart[0].raster

    def generate_report(self, page_id: str, start_date: datetime, end_date: datetime):
        """
        Generates a full report including summary, goals, and visualization.
        """
        summary = self.summarize(page_id, start_date, end_date)

        report = Report()
        goals = self.goal(summary)
        for idx, goal in enumerate(goals):
            report.goals.append(f"Goal {idx+1}: {goal.question}")
            chart_code = self.visualize(summary, goal)
            report.chart_raster.append(chart_code.raster)
            report.refined_chart_raster.append(
                self.refine_chart(summary, chart_code.code)
            )

        return report
