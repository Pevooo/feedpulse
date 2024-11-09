import unittest

from src.config.feed_pulse_settings import FeedPulseSettings
from src.loaded_models.gemini_model import GeminiModel


class TestFeedPulseSettings(unittest.TestCase):
    def test_change_model(self):
        FeedPulseSettings.feedback_classification_model = (
            None  # Setting it to null to test returning it back to Gemini
        )
        FeedPulseSettings.set_setting("feedback_classification_model", "GeminiModel")
        self.assertEqual(FeedPulseSettings.feedback_classification_model, GeminiModel)

    def test_change_bool(self):
        FeedPulseSettings.set_setting("enable_x_data_collection", "False")
        self.assertEqual(FeedPulseSettings.enable_x_data_collection, False)

    def test_invalid_attribute(self):
        try:
            FeedPulseSettings.set_setting("invalid_attr", "False")
        except Exception as e:
            self.fail(e)

    def test_invalid_model_type(self):
        FeedPulseSettings.feedback_classification_model = GeminiModel
        try:
            FeedPulseSettings.set_setting("feedback_classification_model", "int")
        except Exception as e:
            self.fail(e)

        self.assertEqual(FeedPulseSettings.feedback_classification_model, GeminiModel)

    def test_invalid_bool_value(self):
        FeedPulseSettings.enable_x_data_collection = True
        try:
            FeedPulseSettings.set_setting("enable_x_data_collection", "invalid_value")
        except Exception as e:
            self.fail(e)

        self.assertEqual(FeedPulseSettings.enable_x_data_collection, True)
