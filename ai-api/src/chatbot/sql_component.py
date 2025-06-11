from src.chatbot.component import Component


class SqlComponent(Component):
    def __init__(self, model_provider):
        self.model_provider = model_provider

    def run(self, input_text, dataset):
        pass
