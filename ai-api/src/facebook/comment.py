from datetime import datetime


class Comment:
    def __init__(self, text: str, time_created: datetime):
        self.text = text
        self.time_created = time_created

    def __str__(self):
        return f"\tFacebook Comment: {self.text}, Created: {self.time_created}"
