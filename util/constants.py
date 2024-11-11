import os


AI_API_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai-api")
)

WEB_API_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web-api")
)

TWISTER_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "twister")
)

PROJECT_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
