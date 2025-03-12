from enum import Enum

class ORModel(Enum):
    DeepSeek = "deepseek/deepseek-r1-zero:free"
    OpenAi = "openai/gpt-4o"
    DEFAULT = DeepSeek
