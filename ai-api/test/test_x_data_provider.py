import unittest
from datetime import datetime
from unittest.mock import patch, Mock

import twikit

from src.x.tweet import Tweet
from src.x.x_data_provider import XDataProvider


class FakeTwikitTweets:
    def __init__(self, tweets):
        self.tweets = tweets

    def __iter__(self):
        return self.tweets.__iter__()

    async def next(self):
        return []


class FakeTwikitTweet:
    def __init__(self, text, id, created_at_datetime, replies):
        self.text = text
        self.id = id
        self.created_at_datetime = created_at_datetime
        self.replies = replies


class TestXDataProvider(unittest.IsolatedAsyncioTestCase):

    @patch.object(twikit.Client, "search_tweet")
    async def test_get_tweets_content_no_replies(self, mock_search_tweet):
        mock_search_tweet.return_value = FakeTwikitTweets(
            [
                FakeTwikitTweet("hello", "1", datetime.now(), []),
                FakeTwikitTweet("helloo", "2", datetime.now(), []),
            ]
        )

        data_provider = XDataProvider()
        tweets: list[Tweet] = await data_provider.get_tweets(2, Mock())

        self.assertEqual(tweets[0].text, "hello")
        self.assertEqual(tweets[1].text, "helloo")

    @patch.object(twikit.Client, "search_tweet")
    async def test_get_tweets_size_no_replies(self, mock_search_tweet):
        mock_search_tweet.return_value = FakeTwikitTweets(
            [
                FakeTwikitTweet("hello", "1", datetime.now(), []),
                FakeTwikitTweet("helloo", "2", datetime.now(), []),
            ]
        )

        data_provider = XDataProvider()
        tweets: list[Tweet] = await data_provider.get_tweets(1, Mock())

        self.assertEqual(1, len(tweets))

    @patch.object(twikit.Client, "search_tweet")
    async def test_get_tweets_size(self, mock_search_tweet):
        mock_search_tweet.return_value = FakeTwikitTweets(
            [
                FakeTwikitTweet(
                    "hello",
                    "1",
                    datetime.now(),
                    [FakeTwikitTweet("reply", "7", datetime.now(), [])],
                ),
                FakeTwikitTweet("helloo", "2", datetime.now(), []),
            ]
        )

        data_provider = XDataProvider()
        tweets: list[Tweet] = await data_provider.get_tweets(2, Mock())

        self.assertEqual(2, len(tweets))

    @patch.object(twikit.Client, "search_tweet")
    async def test_get_tweets_content(self, mock_search_tweet):
        mock_search_tweet.return_value = FakeTwikitTweets(
            [
                FakeTwikitTweet(
                    "hello",
                    "1",
                    datetime.now(),
                    [FakeTwikitTweet("reply", "7", datetime.now(), [])],
                ),
                FakeTwikitTweet("helloo", "2", datetime.now(), []),
            ]
        )

        data_provider = XDataProvider()
        tweets: list[Tweet] = await data_provider.get_tweets(2, Mock())

        self.assertEqual("hello", tweets[0].text)
        self.assertEqual("reply", tweets[0].replies[0].text)

    @patch.object(twikit.Client, "search_tweet")
    async def test_get_tweets_replies_size(self, mock_search_tweet):
        mock_search_tweet.return_value = FakeTwikitTweets(
            [
                FakeTwikitTweet(
                    "hello",
                    "1",
                    datetime.now(),
                    [
                        FakeTwikitTweet("reply", "7", datetime.now(), []),
                        FakeTwikitTweet("reply", "7", datetime.now(), []),
                    ],
                ),
                FakeTwikitTweet("helloo", "2", datetime.now(), []),
            ]
        )

        data_provider = XDataProvider()
        tweets: list[Tweet] = await data_provider.get_tweets(2, Mock())

        self.assertEqual(2, len(tweets[0].replies))
        self.assertEqual(0, len(tweets[1].replies))


if __name__ == "__main__":
    unittest.main()
