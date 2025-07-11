import pandas as pd
from pandasai import SmartDataframe

from src.chatbot.component import Component
from pandasai.llm.base import LLM

from src.config.settings import Settings
from src.models.global_model_provider import GlobalModelProvider


class QueryComponent(Component):
    class CustomLLM(LLM):
        def __init__(self, model_provider: GlobalModelProvider, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.model_provider = model_provider

        @property
        def type(self) -> str:
            return "custom"

        def call(self, prompt: str, context=None) -> str:
            return self.model_provider.generate_content(
                prompt, Settings.query_component_temperature_x10 / 10
            ).strip()

    def __init__(self, model_provider):
        self.model_provider = model_provider

    def run(self, input_text, dataset: pd.DataFrame) -> str:
        llm = QueryComponent.CustomLLM(self.model_provider)
        sdf = SmartDataframe(dataset, config={"llm": llm})
        response = str(sdf.chat(self._wrap_prompt(input_text)))
        if "error" in response.lower():
            raise ValueError("Problem encountered")
        return response

    def _wrap_prompt(self, prompt: str) -> str:
        return (
            "The dataset includes the comments data of a facebook page, alongside with their sentiments and related topics."
            f"Content column contains comments data. I don't want a visualization. Never Send a path. "
            f"Wrap the response in a natural language sentence. Question: {prompt}"
        )
