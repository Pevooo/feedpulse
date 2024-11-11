from datetime import datetime
from dataclasses import dataclass
from src.facebook.comment import Comment

@dataclass
class Post:
    text: str
    time_created: datetime
    comments: tuple[Comment]

    def __str__(self):
        return f"Facebook Post: {self.text}, Created: {self.time_created}"
