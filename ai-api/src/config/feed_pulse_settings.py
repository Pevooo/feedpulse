from typing import Type

from src.loaded_models.gemini_model import GeminiModel


class FeedPulseSettings:
    """This class encapsulates all the AI Api configurations."""

    __BOOLEAN_SETTINGS = {"enable_x_data_collection", "enable_facebook_data_collection"}
    __MODEL_SETTINGS = {
        "topic_filtration_model",
        "topic_segmentation_model",
        "report_creation_model",
        "feedback_classification_model",
    }

    # Model-related config
    feedback_classification_model: Type = GeminiModel
    topic_filtration_model: Type = GeminiModel
    topic_segmentation_model: Type = GeminiModel
    report_creation_model: Type = GeminiModel

    # Features
    # TODO: Bind this settings to the actual product
    enable_x_data_collection: bool = True
    enable_facebook_data_collection: bool = True

    @classmethod
    def set_setting(cls, setting_name: str, value: str) -> bool:
        if setting_name in cls.__BOOLEAN_SETTINGS:
            changed = cls.__set_bool_setting(setting_name, value)
            if not changed:
                return False

        elif setting_name in cls.__MODEL_SETTINGS:
            model_class = globals().get(value)
            if model_class is None:
                return False  # Model not found
            setattr(cls, setting_name, model_class)
        else:
            return False  # Invalid setting name
        return True

    @classmethod
    def __set_bool_setting(cls, setting_name: str, boolean: str) -> bool:

        if boolean.lower() != "false" and boolean.lower() != "true":
            return False

        if boolean.lower() == "true":
            setattr(cls, setting_name, True)
        elif boolean.lower() == "false":
            setattr(cls, setting_name, False)

        return True
