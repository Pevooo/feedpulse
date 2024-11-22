import os


class Environment:
    """
    This class encapsulates all the AI Api environment.
    """

    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    is_production_environment: bool = os.getenv("PROD") is not None

    # X related variables
    x_username: str = os.getenv("X_USERNAME")
    x_email: str = os.getenv("X_EMAIL")
    x_password: str = os.getenv("X_PASSWORD")
