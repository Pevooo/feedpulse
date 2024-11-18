import unittest

from src.config.feed_pulse_settings import FeedPulseSettings
from src.loaded_models.gemini_model import GeminiModel
from src.loaded_models.phi_model import PhiModel


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

    def test_get_settings_model_setting(self):
        FeedPulseSettings.report_creation_model = PhiModel
        settings = FeedPulseSettings.get_settings()
        self.assertIn(
            {
                "settingName": "report_creation_model",
                "settingValue": "PhiModel",
                "prettyName": "Report Creation Model",
                "choices": ["GeminiModel", "PhiModel"],
            },
            settings,
        )

    def test_get_settings_bool_setting(self):
        FeedPulseSettings.enable_x_data_collection = True
        settings = FeedPulseSettings.get_settings()
        self.assertIn(
            {
                "settingName": "enable_x_data_collection",
                "settingValue": True,
                "prettyName": "Enable X Data Collection",
                "choices": ["true", "false"],
            },
            settings,
        )

    def test_update_bool_setting(self):
        FeedPulseSettings.enable_x_data_collection = True

        json = {
            "settingsList": [
                {"settingName": "enable_x_data_collection", "settingValue": "False"}
            ]
        }

        updated = FeedPulseSettings.update_settings(json)

        self.assertEqual(FeedPulseSettings.enable_x_data_collection, False)
        self.assertTrue(updated)

    def test_update_model_setting(self):
        FeedPulseSettings.report_creation_model = GeminiModel

        json = {
            "settingsList": [
                {"settingName": "report_creation_model", "settingValue": "PhiModel"}
            ]
        }

        updated = FeedPulseSettings.update_settings(json)

        self.assertEqual(FeedPulseSettings.report_creation_model, PhiModel)
        self.assertTrue(updated)

    def test_update_model_invalid_bool_setting(self):
        FeedPulseSettings.enable_x_data_collection = False

        json = {
            "settingsList": [
                {
                    "settingName": "enable_x_data_collection",
                    "settingValue": "invalid_value",
                }
            ]
        }

        updated = FeedPulseSettings.update_settings(json)

        self.assertEqual(FeedPulseSettings.enable_x_data_collection, False)
        self.assertFalse(updated)

    def test_update_model_invalid_model_setting(self):
        FeedPulseSettings.report_creation_model = GeminiModel

        json = {
            "settingsList": [
                {
                    "settingName": "report_creation_model",
                    "settingValue": "invalid_model",
                }
            ]
        }

        updated = FeedPulseSettings.update_settings(json)

        self.assertEqual(FeedPulseSettings.report_creation_model, GeminiModel)
        self.assertFalse(updated)
