from datetime import datetime
from dataclasses import dataclass


@dataclass
class Comment:
    text: str
    time_created: datetime
