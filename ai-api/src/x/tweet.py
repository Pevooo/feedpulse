from datetime import datetime

import twikit


class Tweet:
    def __init__(self, tweet: twikit.Tweet) -> None:
        self.text: str = tweet.text
        self.id: str = tweet.id
        self.date: datetime = tweet.created_at_datetime
        self.replies: list[Tweet] = (
            list(map(Tweet, tweet.replies)) if tweet.replies else []
        )
