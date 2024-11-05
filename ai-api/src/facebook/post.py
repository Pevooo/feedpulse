from datetime import datetime

from src.facebook.comment import Comment


class Post:
    def __init__(
        self, text: str, time_created: datetime, comments: list[Comment]
    ) -> None:
        self.text = text
        self.time_created = time_created
        self.comments = comments

    def __str__(self):
        return f"Facebook Post: {self.text}, Created: {self.time_created}"
