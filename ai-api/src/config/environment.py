import os


class Environment:
    """
    This class encapsulates all the AI Api environment.
    """

    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    facebook_graph_api_webhook_verify_token = os.getenv(
        "FACEBOOK_GRAPH_API_VERIFY_TOKEN"
    )
    is_production_environment: bool = os.getenv("PROD") is not None
