from typing import Type

# Suppressing unused import error as we need all the models to be imported to work properly

from src.models.gemini_model import GeminiModel  # noqa: F401
from src.models.phi_model import PhiModel  # noqa: F401
from src.models.openai_model import OpenAiModel  # noqa: F401


# This class is responsible for managing the setting of the whole app. You can add a setting by adding it in the class
# alongside with its default value and also add it in `BOOLEAN_SETTINGS` if it's a boolean or in `MODEL_SETTINGS` if
# it's a model setting (This is for remote config purposes)


class Settings:
    """
    This class encapsulates all the AI Api configurations.
    """

    BOOLEAN_SETTINGS = {
        "enable_x_data_collection",
        "enable_facebook_data_collection",
    }

    MODEL_SETTINGS = {
        "topic_segmentation_model",
        "report_creation_model",
        "feedback_classification_model",
    }

    # Model-related config
    feedback_classification_model: Type = GeminiModel
    topic_segmentation_model: Type = GeminiModel
    report_creation_model: Type = GeminiModel

    # Features
    # TODO: Bind this settings to the actual product
    enable_x_data_collection: bool = True
    enable_facebook_data_collection: bool = True

    @classmethod
    def get_settings(cls) -> list[dict[str, str]]:
        settings = []
        for setting in cls.BOOLEAN_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "choices": ["true", "false"],
                },
            )

        for setting in cls.MODEL_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting).__name__,
                    "prettyName": " ".join(setting.split("_")).title(),
                    "choices": ["GeminiModel", "PhiModel", "OpenAiModel"],
                }
            )

        return settings

    @classmethod
    def update_settings(cls, settings: dict[str, list[dict[str, str]]]) -> bool:
        updated = True
        for setting in settings["settingsList"]:

            # Set updated to false if there's one or more setting(s) failed to update
            updated &= cls._set_setting(setting["settingName"], setting["settingValue"])

        return updated

    @classmethod
    def _set_setting(cls, setting_name: str, value: str) -> bool:
        if setting_name in cls.BOOLEAN_SETTINGS:
            changed = cls._set_bool_setting(setting_name, value)
            if not changed:
                return False

        elif setting_name in cls.MODEL_SETTINGS:
            model_class = globals().get(value)
            if model_class is None:
                return False  # Model not found
            setattr(cls, setting_name, model_class)
        else:
            return False  # Invalid setting name
        return True

    @classmethod
    def _set_bool_setting(cls, setting_name: str, boolean: str) -> bool:
        if boolean.lower() != "false" and boolean.lower() != "true":
            return False

        if boolean.lower() == "true":
            setattr(cls, setting_name, True)
        elif boolean.lower() == "false":
            setattr(cls, setting_name, False)

        return True
