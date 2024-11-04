from typing import Type

from src.loaded_models.gemini_model import GeminiModel


class FeedPulseSettings:
    """This class encapsulates all the AI Api configurations."""

    # Model-related config
    feedback_classification_model: Type = GeminiModel
    topic_filtration_model: Type = GeminiModel
    topic_segmentation_model: Type = GeminiModel
    report_creation_model: Type = GeminiModel
