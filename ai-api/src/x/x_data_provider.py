import twikit
import time
from random import randint

from src.data.main_data_unit import MainDataUnit


class XDataProvider:
    def __init__(self) -> None:
        self.client = twikit.Client("en-US")

    async def login(self, username: str, email: str, password: str):
        await self.client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password,
        )

    async def get_tweets(self, num_tweets: int, query: str) -> tuple[MainDataUnit, ...]:
        """
        Gets the tweets from X using a given query

        Args:
            num_tweets (int): The number of tweets to get.
            query (str): The keyword to query

        Returns:
            all_tweets (tuple[MainDataUnit, ...]): A tuple containing all the collected tweets as MainDataUnit objects.
        """
        tweets = await self.client.search_tweet(query, "Latest")
        counts = 0

        all_tweets = []

        for tweet in tweets:
            counts += 1
            all_tweets.append(self.tweet_to_data_unit(tweet))

            if counts >= num_tweets:
                break

        # Search more tweets
        while counts < num_tweets:
            wait_time = randint(5, 12)
            time.sleep(wait_time)
            more_tweets = await tweets.next()
            for tweet in more_tweets:
                all_tweets.append(self.tweet_to_data_unit(tweet))
        return tuple(all_tweets)

    def tweet_to_data_unit(self, tweet: twikit.Tweet) -> MainDataUnit:
        """
        Converts from a tweet to a MainDataUnit

        Args:
            tweet (twikit.Tweet): The tweet to convert

        Returns:
            The tweet converted to a MainDataUnit
        """
        return MainDataUnit(
            tweet.text,
            tweet.created_at_datetime,
            (
                tuple(map(self.tweet_to_data_unit, tweet.replies))
                if tweet.replies
                else tuple()
            ),
        )
