from datetime import datetime

import twikit
import time
from random import randint


class Tweet:
    def __init__(self, tweet: twikit.Tweet) -> None:
        self.text: str = tweet.text
        self.id: str = tweet.id
        self.user: str = tweet.user.name
        self.date: datetime = tweet.created_at_datetime
        self.replies: list[Tweet] = (
            list(map(Tweet, tweet.replies)) if tweet.replies else None
        )


class XDataProvider:
    def __init__(self) -> None:
        self.client = twikit.Client("en-US")

    async def login(self, username: str, email: str, password: str):
        await self.client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password,
        )

    async def get_tweets(self, num_tweets: int, query: str) -> list[twikit.Tweet]:

        tweets = await self.client.search_tweet(query, "Latest")
        counts = 0

        all_tweets = []

        for tweet in tweets:
            counts += 1
            all_tweets.append(Tweet(tweet))

        # Search more tweets
        while counts < num_tweets:
            wait_time = randint(5, 12)
            time.sleep(wait_time)
            more_tweets = await tweets.next()
            for tweet in more_tweets:
                all_tweets.append(Tweet(tweet))
        return all_tweets
