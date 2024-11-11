from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Tweet:
    text: str
    id: str
    date: datetime
    replies: tuple["Tweet", ...] = field(default_factory=tuple)
