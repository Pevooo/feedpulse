from datetime import datetime
import pandas as pd
from src.reports.report import Report
from src.reports.custom_text_generator import CustomTextGenerator
from src.models.global_model_provider import GlobalModelProvider
from src.data.data_manager import DataManager
from lida import Manager, TextGenerationConfig


class LidaReportHandler:
    def __init__(self, data_manager: DataManager, model_provider: GlobalModelProvider):
        self.text_generator = CustomTextGenerator(
            lambda prompt: model_provider.generate_content(prompt)
        )
        self.lida = Manager(text_gen=self.text_generator)
        self.config = TextGenerationConfig(n=1, temperature=0.5)

        self.data_manager = data_manager

    def summarize(self, data: pd.DataFrame):
        """
        Generates a summary of the data by calling LIDA's summarize() method.
        """

        if data.empty:
            return None

        return self.lida.summarize(data)

    def compute_metrics(self, df: pd.DataFrame) -> dict:
        """
        Compute metrics for 'sentiment' and 'related_topic' columns, handling comma-separated topics:
        - sentiment_counts: count of each sentiment label
        - topic_counts: count of each individual topic
        - most_freq_sentiment_per_topic: sentiment that appears most for each topic
        - most_freq_topic_per_sentiment: topic that appears most for each sentiment
        - top_5_topics: overall top 5 topics
        """
        metrics = {}
        if "sentiment" in df.columns:
            metrics["sentiment_counts"] = df["sentiment"].value_counts().to_dict()

        if "related_topics" in df.columns:
            exploded_topics = df["related_topics"].str.split(",")
            exploded_topics = exploded_topics.explode().str.strip()
            metrics["topic_counts"] = exploded_topics.value_counts().to_dict()

            if "sentiment" in df.columns:

                df_exploded = df.copy()
                df_exploded = df_exploded.assign(
                    related_topic=df_exploded["related_topics"]
                    .str.split(",")
                    .explode()
                    .str.strip()
                )

                per_topic = (
                    df_exploded.groupby("related_topics")["sentiment"]
                    .agg(lambda x: x.value_counts().idxmax())
                    .to_dict()
                )
                metrics["most_freq_sentiment_per_topic"] = per_topic
                per_sentiment = (
                    df_exploded.groupby("sentiment")["related_topics"]
                    .agg(lambda x: x.value_counts().idxmax())
                    .to_dict()
                )
                metrics["most_freq_topic_per_sentiment"] = per_sentiment

            metrics["top_5_topics"] = exploded_topics.value_counts().head(5).to_dict()

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
        data = self.data_manager.filter_data(page_id, start_date, end_date)
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
