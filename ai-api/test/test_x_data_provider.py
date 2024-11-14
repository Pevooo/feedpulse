import unittest
from datetime import datetime
from unittest.mock import patch, Mock

import twikit

from src.x.x_data_provider import XDataProvider
from fake_twikit_tweet import FakeTwikitTweet
from fake_twikit_tweets import FakeTwikitTweets


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
        tweets = await data_provider.get_tweets(2, Mock())

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
        tweets = await data_provider.get_tweets(1, Mock())

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
        tweets = await data_provider.get_tweets(2, Mock())

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
        tweets = await data_provider.get_tweets(2, Mock())

        self.assertEqual("hello", tweets[0].text)
        self.assertEqual("reply", tweets[0].children[0].text)

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
        tweets = await data_provider.get_tweets(2, Mock())

        self.assertEqual(2, len(tweets[0].children))
        self.assertEqual(0, len(tweets[1].children))
