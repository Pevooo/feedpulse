import os


class FeedPulseEnvironment:
    """This class encapsulates all the AI Api environment."""

    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    is_production_environment: bool = os.getenv("PROD") is not None
