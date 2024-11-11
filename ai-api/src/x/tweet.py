from datetime import datetime
from dataclasses import dataclass, field
import twikit

@dataclass
class Tweet:
    text: str
    id: str
    date: datetime
    replies: tuple["Tweet", ...] = field(default_factory=tuple)

    def __init__(self, tweet: twikit.Tweet) -> None:
        self.text = tweet.text
        self.id = tweet.id
        self.date = tweet.created_at_datetime
        self.replies = tuple(map(Tweet, tweet.replies)) if tweet.replies else tuple()
