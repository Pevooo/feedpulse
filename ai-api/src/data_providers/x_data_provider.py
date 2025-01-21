import twikit
import time
from random import randint

from src.config.environment import Environment
from src.data.feedback_data_unit import FeedbackDataUnit
from src.utlity.util import deprecated

# DEPRECATED


class XDataProvider:
    """
    represents a data provider for X
    """

    @deprecated
    def __init__(self) -> None:
        self.client = twikit.Client("en-US")
        self.logged_in = False

    @deprecated
    async def login(self):
        await self.client.login(
            auth_info_1=Environment.x_username,
            auth_info_2=Environment.x_email,
            password=Environment.x_password,
        )

        self.logged_in = True

    @deprecated
    async def get_tweets(
        self, num_tweets: int, query: str
    ) -> tuple[FeedbackDataUnit, ...]:
        """
        Gets the tweets from X using a given query

        Args:
            num_tweets (int): The number of tweets to get.
            query (str): The keyword to query

        Returns:
            all_tweets (tuple[MainDataUnit, ...]): A tuple containing all the collected tweets as MainDataUnit objects.
        """

        # If we're not logged in we'll automatically log in
        if not self.logged_in:
            await self.login()

        tweets = await self.client.search_tweet(query, "Latest")
        counts = 0

        all_tweets = []

        if len(tweets) == 0:
            return tuple(all_tweets)

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

            # break if there's no more tweets (this will prevent infinite loops)
            if len(more_tweets) == 0:
                return tuple(all_tweets)

            for tweet in more_tweets:
                all_tweets.append(self.tweet_to_data_unit(tweet))

        return tuple(all_tweets)

    @deprecated
    def tweet_to_data_unit(self, tweet: twikit.Tweet) -> FeedbackDataUnit:
        """
        Converts from a tweet to a MainDataUnit

        Args:
            tweet (twikit.Tweet): The tweet to convert

        Returns:
            The tweet converted to a MainDataUnit
        """
        return FeedbackDataUnit(
            tweet.text,
            tweet.created_at_datetime,
            (
                tuple(map(self.tweet_to_data_unit, tweet.replies))
                if tweet.replies
                else tuple()
            ),
        )
