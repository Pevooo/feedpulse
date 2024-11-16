import unittest

from src.config.feed_pulse_environment import FeedPulseEnvironment
from src.loaded_models.gemini_model import GeminiModel


class TestGeminiModel(unittest.TestCase):
    def test_connection(self):
        try:
            GeminiModel()
        except Exception as e:
            self.fail(f"Connection Failed: {e}")

    def test_env_variable(self):
        self.assertIsNotNone(FeedPulseEnvironment.gemini_api_key)
