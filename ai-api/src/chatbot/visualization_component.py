from chatbot_component import ChatBotComponent
from lida import Manager, TextGenerationConfig
from src.reports.custom_text_generator import CustomTextGenerator
from src.models.global_model_provider import GlobalModelProvider
from lida.datamodel import Goal

import pandas as pd


class VisualizationComponent(ChatBotComponent):
    def __init__(self, model_provider: GlobalModelProvider):
        self.text_generator = CustomTextGenerator(
            lambda prompt: model_provider.generate_content(prompt)
        )
        self.lida = Manager(text_gen=self.text_generator)
        self.config = TextGenerationConfig(n=1, temperature=0.5)

    def run(self, input_text, dataset):
        if isinstance(dataset, pd.DataFrame):
            df = dataset
        elif "toPandas" in dir(dataset):
            try:
                df = dataset.toPandas()
            except Exception as e:
                raise ValueError(f"Failed to convert Spark DataFrame: {e}")
        else:
            raise ValueError(
                "Unsupported dataset format. Provide a pandas DataFrame, or Spark DataFrame."
            )

        summary = self.lida.summarize(df, summary_method="default")
        goal = Goal(question=input_text, rationale=input_text, visualization="auto")
        code = self.lida.visualize(summary=summary, goal=goal)
        return code
