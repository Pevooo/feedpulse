import os
from typing import Type

from pydantic_settings import BaseSettings

from models.gemini_model import GeminiModel


class FeedPulseSettings(BaseSettings):
    """This class encapsulates all the AI Api configurations."""

    # Model-related config
    feedback_classification_model: Type = GeminiModel
    topic_filtration_model: Type = GeminiModel
    topic_segmentation_model: Type = GeminiModel
    report_creation_model: Type = GeminiModel

    # Environment
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    is_production_environment: bool = os.getenv("PROD") is not None
