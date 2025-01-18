from typing import Type

# Suppressing unused import error as we need all the models to be imported to work properly

from src.models.gemini_model import GeminiModel  # noqa: F401
from src.models.phi_model import PhiModel  # noqa: F401
from src.models.openai_model import OpenAiModel  # noqa: F401


# This class is responsible for managing the setting of the whole app. You can add a setting by adding it in the class
# alongside with its default value and also add it in `BOOLEAN_SETTINGS` if it's a boolean or in `MODEL_SETTINGS` if
# it's a model setting (This is for remote config purposes)

_ALL_MODELS = [
    "GeminiModel",
    "PhiModel",
    "OpenAiModel",
]

_OFFLINE_MODELS = [
    "PhiModel",
]

_ONLINE_MODELS = [
    "OpenAiModel",
    "GeminiModel",
]

class Settings:
    """
    This class encapsulates all the AI Api configurations.
    """

    BOOLEAN_SETTINGS = {
        "enable_facebook_data_collection",
        "enable_instagram_data_collection",
    }

    MODEL_SETTINGS = {
        "topic_segmentation_model": _ALL_MODELS,
        "report_creation_model": _ALL_MODELS,
        "feedback_classification_model": _ALL_MODELS,
    }

    NUMBER_SETTINGS = {
        "processing_batch_size": [1, 2, 4, 8, 16],
    }

    # Model-related config
    feedback_classification_model: Type = GeminiModel
    topic_segmentation_model: Type = GeminiModel
    report_creation_model: Type = GeminiModel

    # Features
    enable_facebook_data_collection: bool = True
    enable_instagram_data_collection: bool = True

    processing_batch_size: int = 1

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            return super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(
            self,
            # Model-related config
            feedback_classification_model: Type = GeminiModel,
            topic_segmentation_model: Type = GeminiModel,
            report_creation_model: Type = GeminiModel,

            # Features config
            enable_facebook_data_collection: bool = True,
            enable_instagram_data_collection: bool = True,

            # Processing config
            processing_batch_size: int = 1,
    ):
        if self.__class__._instance is None:
            self.feedback_classification_model = feedback_classification_model
            self.topic_segmentation_model = topic_segmentation_model
            self.report_creation_model = report_creation_model
            self.enable_facebook_data_collection = enable_facebook_data_collection
            self.enable_instagram_data_collection = enable_instagram_data_collection
            self.processing_batch_size = processing_batch_size

    @classmethod
    def get_settings(cls) -> list[dict[str, str]]:
        settings = []
        for setting in cls.BOOLEAN_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "bool",
                    "choices": ["true", "false"],
                },
            )

        for setting in cls.MODEL_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting).__name__,
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "enum",
                    "choices": cls.MODEL_SETTINGS[setting],
                }
            )

        for setting in cls.NUMBER_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "int",
                    "choices": cls.NUMBER_SETTINGS[setting],
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
        changed = False
        if setting_name in cls.BOOLEAN_SETTINGS:
            changed = cls._set_bool_setting(setting_name, value)
        elif setting_name in cls.MODEL_SETTINGS:
            changed = cls._set_model_setting(setting_name, value)
        elif setting_name in cls.NUMBER_SETTINGS:
            changed = cls._set_int_setting(setting_name, value)
        return changed

    @classmethod
    def _set_model_setting(cls, setting_name: str, value: str) -> bool:
        model_class = globals().get(value)
        if model_class is None:
            return False  # Model not found
        setattr(cls, setting_name, model_class)
        return True

    @classmethod
    def _set_int_setting(cls, setting_name: str, value: str) -> bool:
        try:
            value = int(value)
        except ValueError:
            return False

        if value not in cls.NUMBER_SETTINGS[setting_name]:
            return False
        setattr(cls, setting_name, value)
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
