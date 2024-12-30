"""
A fake Phi model, it doesn't do anything (used for speeding up tests)
"""

from src.models.model import Model


class FakePhiModel(Model):
    def __init__(self):
        return

    def generate_content(self, text: str, max_new_tokens: int = 15) -> str:
        return ""
