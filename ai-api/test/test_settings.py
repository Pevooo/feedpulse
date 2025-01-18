import unittest

from src.config.settings import Settings
from src.models.gemini_model import GeminiModel
from src.models.phi_model import PhiModel


class TestFeedPulseSettings(unittest.TestCase):
    def test_change_model(self):
        Settings.feedback_classification_model = PhiModel
        Settings._set_setting("feedback_classification_model", "GeminiModel")
        self.assertEqual(Settings.feedback_classification_model, GeminiModel)

    def test_change_bool(self):
        Settings._set_setting("enable_facebook_data_collection", "False")
        self.assertEqual(Settings.enable_facebook_data_collection, False)

    def test_invalid_attribute(self):
        try:
            Settings._set_setting("invalid_attr", "False")
        except Exception as e:
            self.fail(e)

    def test_invalid_model_type(self):
        Settings.feedback_classification_model = GeminiModel
        try:
            Settings._set_setting("feedback_classification_model", "int")
        except Exception as e:
            self.fail(e)

        self.assertEqual(Settings.feedback_classification_model, GeminiModel)

    def test_invalid_bool_value(self):
        Settings.enable_x_data_collection = True
        try:
            Settings._set_setting("enable_facebook_data_collection", "invalid_value")
        except Exception as e:
            self.fail(e)

        self.assertEqual(Settings.enable_x_data_collection, True)

    def test_get_settings_model_setting(self):
        Settings.report_creation_model = PhiModel
        settings = Settings.get_settings()
        self.assertIn(
            {
                "settingName": "report_creation_model",
                "settingValue": "PhiModel",
                "prettyName": "Report Creation Model",
                "type": "enum",
                "choices": ["GeminiModel", "PhiModel", "OpenAiModel"],
            },
            settings,
        )

    def test_get_settings_bool_setting(self):
        Settings.enable_facebook_data_collection = True
        settings = Settings.get_settings()
        self.assertIn(
            {
                "settingName": "enable_facebook_data_collection",
                "settingValue": True,
                "prettyName": "Enable Facebook Data Collection",
                "type": "bool",
                "choices": ["true", "false"],
            },
            settings,
        )

    def test_get_settings_int_setting(self):
        Settings.processing_batch_size = 1
        settings = Settings.get_settings()
        self.assertIn(
            {
                "settingName": "processing_batch_size",
                "settingValue": 1,
                "prettyName": "Processing Batch Size",
                "type": "int",
                "choices": [1, 2, 4, 8, 16],
            },
            settings,
        )

    def test_update_bool_setting(self):
        Settings.enable_facebook_data_collection = True

        json = {
            "settingsList": [
                {"settingName": "enable_facebook_data_collection", "settingValue": "False"}
            ]
        }

        updated = Settings.update_settings(json)

        self.assertEqual(Settings.enable_facebook_data_collection, False)
        self.assertTrue(updated)

    def test_update_model_setting(self):
        Settings.report_creation_model = GeminiModel

        json = {
            "settingsList": [
                {"settingName": "report_creation_model", "settingValue": "PhiModel"}
            ]
        }

        updated = Settings.update_settings(json)

        self.assertEqual(Settings.report_creation_model, PhiModel)
        self.assertTrue(updated)

    def test_update_int_setting(self):
        Settings.processing_batch_size = 0
        json = {
            "settingsList": [
                {"settingName": "processing_batch_size", "settingValue": "4"}
            ]
        }

        updated = Settings.update_settings(json)

        self.assertEqual(Settings.processing_batch_size, 4)
        self.assertTrue(updated)

    def test_update_model_invalid_bool_setting(self):
        Settings.enable_facebook_data_collection = False

        json = {
            "settingsList": [
                {
                    "settingName": "enable_facebook_data_collection",
                    "settingValue": "invalid_value",
                }
            ]
        }

        updated = Settings.update_settings(json)

        self.assertEqual(Settings.enable_facebook_data_collection, False)
        self.assertFalse(updated)

    def test_update_model_invalid_model_setting(self):
        Settings.report_creation_model = GeminiModel

        json = {
            "settingsList": [
                {
                    "settingName": "report_creation_model",
                    "settingValue": "invalid_model",
                }
            ]
        }

        updated = Settings.update_settings(json)

        self.assertEqual(Settings.report_creation_model, GeminiModel)
        self.assertFalse(updated)

    def test_update_model_invalid_int_setting(self):
        Settings.processing_batch_size = 2

        json = {
            "settingsList": [
                {
                    "settingName": "processing_batch_size",
                    "settingValue": "100",
                }
            ]
        }

        updated = Settings.update_settings(json)

        self.assertEqual(Settings.processing_batch_size, 2)
        self.assertFalse(updated)
