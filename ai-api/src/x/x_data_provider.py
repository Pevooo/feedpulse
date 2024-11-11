import twikit
import time
from random import randint

from src.x.tweet import Tweet


class XDataProvider:
    def __init__(self) -> None:
        self.client = twikit.Client("en-US")

    async def login(self, username: str, email: str, password: str):
        await self.client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password,
        )

    async def get_tweets(self, num_tweets: int, query: str) -> tuple[Tweet]:
        """
        Gets the tweets from X using a given query

        Args:
            num_tweets (int): The number of tweets to get.
            query (str): The keyword to query

        Returns:
            all_tweets (list[Tweet]): A list containing all the collected tweets.
        """
        tweets = await self.client.search_tweet(query, "Latest")
        counts = 0

        all_tweets = []

        for tweet in tweets:
            counts += 1
            all_tweets.append(Tweet(tweet))

            if counts >= num_tweets:
                break

        # Search more tweets
        while counts < num_tweets:
            wait_time = randint(5, 12)
            time.sleep(wait_time)
            more_tweets = await tweets.next()
            for tweet in more_tweets:
                all_tweets.append(Tweet(tweet))
        return all_tweets
