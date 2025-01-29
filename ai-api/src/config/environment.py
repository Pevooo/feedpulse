import os


class Environment:
    """
    This class encapsulates all the AI Api environment.
    """

    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    groqcloud_api_key: str = "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"
    is_production_environment: bool = os.getenv("PROD") is not None
    hf_token: str = os.getenv("HF_TOKEN")

    # X related variables
    x_username: str = os.getenv("X_USERNAME")
    x_email: str = os.getenv("X_EMAIL")
    x_password: str = os.getenv("X_PASSWORD")
