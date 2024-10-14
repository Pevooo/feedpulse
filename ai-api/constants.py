import os


# Always use environment variables when working with credentials
class Credential:
    GEMINI_API_KEY: str = os.environ['GEMINI_API_KEY']
