import pandas as pd
from pandasai import SmartDataframe

from src.chatbot.component import Component
from pandasai.llm.base import LLM

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
            return self.model_provider.generate_content(prompt)

    def __init__(self, model_provider):
        self.model_provider = model_provider

    def run(self, input_text, dataset: pd.DataFrame):
        llm = QueryComponent.CustomLLM(self.model_provider)
        sdf = SmartDataframe(dataset, config={"llm": llm})
        return sdf.chat(input_text)
