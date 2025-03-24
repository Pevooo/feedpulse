from enum import Enum


class ORModel(Enum):
    DeepSeek = "deepseek/deepseek-chat-v3-0324:free"
    qwen = "qwen/qwen2.5-vl-72b-instruct:free"
    DEFAULT = DeepSeek
