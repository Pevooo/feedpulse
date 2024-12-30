import unittest

from src.config.environment import Environment
from src.models.gemini_model import GeminiModel


class TestGeminiModel(unittest.TestCase):
    def test_connection(self):
        try:
            GeminiModel()
        except Exception as e:
            self.fail(f"Connection Failed: {e}")

    def test_env_variable(self):
        self.assertIsNotNone(Environment.gemini_api_key)
