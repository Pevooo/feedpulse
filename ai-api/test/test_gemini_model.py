import unittest

from src.loaded_models.gemini_model import GeminiModel


class TestGeminiModel(unittest.TestCase):
    def test_connection(self):
        try:
            GeminiModel()
        except Exception as e:
            self.fail(f"Connection Failed: {e}")

    def test_str_return_type(self):
        model = GeminiModel()

        result = model.generate_content("hi")
        self.assertEqual(type(result), str)
