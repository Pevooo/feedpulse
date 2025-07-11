from datetime import datetime
import pandas as pd

from src.redis.redis_manager import RedisManager
from src.reports.report import Report
from src.reports.custom_text_generator import CustomTextGenerator
from src.models.global_model_provider import GlobalModelProvider
from src.data.data_manager import DataManager
from lida import Manager, TextGenerationConfig


class LidaReportHandler:
    def __init__(
        self,
        data_manager: DataManager,
        model_provider: GlobalModelProvider,
        redis_manager: RedisManager,
    ):
        self.text_generator = CustomTextGenerator(
            lambda prompt: model_provider.generate_content(prompt)
        )
        self.lida = Manager(text_gen=self.text_generator)
        self.config = TextGenerationConfig(n=1, temperature=0.5)
        self.redis_manager = redis_manager
        self.data_manager = data_manager

    def summarize(self, data: pd.DataFrame):
        """
        Generates a summary of the data by calling LIDA's summarize() method.
        """

        if data.empty:
            return None

        return self.lida.summarize(data)

    def compute_metrics(self, df: pd.DataFrame) -> dict:
        metrics = {}

        if "sentiment" in df.columns:
            metrics["sentiment_counts"] = df["sentiment"].value_counts().to_dict()

        if "related_topics" in df.columns:
            # Step 1: EXPLODE properly: make sure every (sentiment, topic) pair is separated
            df_exploded = df.assign(
                related_topic=df["related_topics"].str.split(",")
            ).explode("related_topic")

            # Step 2: Strip spaces
            df_exploded["related_topic"] = df_exploded["related_topic"].str.strip()

            # Step 3: Now safely compute
            metrics["topic_counts"] = (
                df_exploded["related_topic"].value_counts().to_dict()
            )

            # Step 4: Most frequent sentiment per topic
            metrics["most_freq_sentiment_per_topic"] = (
                df_exploded.groupby("related_topic")["sentiment"]
                .agg(lambda x: x.value_counts().idxmax())
                .to_dict()
            )

            # Step 5: Most frequent topic per sentiment
            metrics["most_freq_topic_per_sentiment"] = (
                df_exploded.groupby("sentiment")["related_topic"]
                .agg(lambda x: x.value_counts().idxmax())
                .to_dict()
            )

            # Step 6: Top 5 topics
            metrics["top_5_topics"] = (
                df_exploded["related_topic"].value_counts().head(5).to_dict()
            )

        return metrics

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
        charts = self.lida.visualize(
            summary=summary,
            textgen_config=self.config,
            library="seaborn",
            goal=goal,
        )

        return charts

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

    def generate_report(
        self, page_id: str, start_date: datetime, end_date: datetime
    ) -> Report:
        """
        Generates a full report including summary, goals, and visualization.
        """

        # Check for cached data
        data = self.redis_manager.get_dataframe(str(start_date), str(end_date), page_id)
        if data is None:
            data = self.data_manager.filter_data(page_id, start_date, end_date)

            # Cache Data
            self.redis_manager.cache_dataframe(
                str(start_date), str(end_date), page_id, data
            )

        summary = self.summarize(data)
        if summary is None:
            return None

        metrics = self.compute_metrics(data)

        report = Report()
        report.metrics = metrics
        goals = self.goal(summary)
        for idx, goal in enumerate(goals):
            report.goals.append(f"Goal {idx+1}: {goal.question}")
            charts_code = self.visualize(summary, goal)
            for chart_code in charts_code:
                report.chart_rasters.append(chart_code.raster)

        return report
