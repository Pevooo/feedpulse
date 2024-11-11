from datetime import datetime
from dataclasses import dataclass

@dataclass
class Comment:
    text: str
    time_created: datetime

    def __str__(self):
        return f"\tFacebook Comment: {self.text}, Created: {self.time_created}"
