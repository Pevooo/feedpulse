import os

from enum import Enum

# Define base directory for storing data files
database_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "database")
)


class SparkTable(Enum):
    REPORTS = os.path.join(database_path, "reports")
    INPUT_COMMENTS = os.path.join(database_path, "comments_stream")
    PROCESSED_COMMENTS = os.path.join(database_path, "processed_comments")
    PAGES = os.path.join(
        database_path, "pages"
    )  # including access token, platform, description and page ID
    EXCEPTIONS = os.path.join(database_path, "exceptions")
