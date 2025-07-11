from lida import Manager, TextGenerationConfig
from src.chatbot.component import Component
from src.config.settings import Settings
from src.reports.custom_text_generator import CustomTextGenerator
from src.models.global_model_provider import GlobalModelProvider
from lida.datamodel import Goal
import pandas as pd


class VisualizationComponent(Component):
    def __init__(self, model_provider: GlobalModelProvider):
        self.text_generator = CustomTextGenerator(
            lambda prompt: model_provider.generate_content(
                prompt, Settings.visualization_component_temperature_x10 / 10
            ).strip(),
        )
        self.lida = Manager(text_gen=self.text_generator)
        self.config = TextGenerationConfig(n=1, temperature=0.5)

    def run(self, input_text: str, dataset: pd.DataFrame) -> str:
        summary = self.lida.summarize(dataset, summary_method="default")
        goal = Goal(
            question=input_text,
            rationale="Generate a relevant chart based on the question. It may be a question or a command",
            visualization="auto",
        )
        charts = self.lida.visualize(summary=summary, goal=goal)
        return charts[0].raster
