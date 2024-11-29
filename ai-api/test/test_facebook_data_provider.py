import unittest
import requests
from unittest.mock import patch, Mock
from src.data_providers.facebook_data_provider import FacebookDataProvider
from datetime import datetime


FAKE_API_RESPONSE = {
    "posts": {
        "data": [
            {
                "message": "hello 2",
                "created_time": "2024-10-28T11:06:11+0000",
            },
            {
                "comments": {
                    "data": [
                        {"created_time": "2024-10-28T10:53:26+0000", "message": "test"}
                    ],
                },
                "message": "hello, world!",
                "created_time": "2024-10-24T16:17:02+0000",
            },
        ]
    }
}


class TestFacebookDataProvider(unittest.TestCase):

    @patch("requests.get")
    def test_get_posts_post_message_value(self, mock_get):
        # Whenever `requests.get` is called: return FAKE_API_RESPONSE+
        mock_get.return_value.json.return_value = FAKE_API_RESPONSE

        # Pass anything as access token as we don't use it in the test
        data_provider = FacebookDataProvider(Mock())

        posts = data_provider.get_posts(Mock())

        self.assertEqual(
            posts[0].text,
            "hello 2",
        )

        self.assertEqual(
            posts[1].text,
            "hello, world!",
        )

    @patch("requests.get")
    def test_get_posts_post_comments_list_size(self, mock_get):
        mock_get.return_value.json.return_value = FAKE_API_RESPONSE
        data_provider = FacebookDataProvider(Mock())
        posts = data_provider.get_posts(Mock())

        self.assertEqual(
            len(posts[0].children),
            0,
        )

        self.assertEqual(
            len(posts[1].children),
            1,
        )

    @patch("requests.get")
    def test_get_posts_post_comments_value(self, mock_get):
        mock_get.return_value.json.return_value = FAKE_API_RESPONSE
        data_provider = FacebookDataProvider(Mock())
        posts = data_provider.get_posts(Mock())

        self.assertEqual(
            posts[1].children[0].text,
            "test",
        )

    @patch("requests.get")
    def test_get_posts_post_comments_created_time(self, mock_get):
        mock_get.return_value.json.return_value = FAKE_API_RESPONSE
        data_provider = FacebookDataProvider(Mock())
        posts = data_provider.get_posts(Mock())

        expected_time = datetime.fromisoformat("2024-10-28T10:53:26+00:00")
        self.assertEqual(
            posts[1].children[0].time_created,
            expected_time,
        )

    @patch("requests.get")
    def test_get_posts_timeout_exceeded(self, mock_get):
        def delayed_response(*args, **kwargs):
            import time

            time.sleep(5)  # Delay for 5 seconds
            raise requests.exceptions.Timeout("Request timed out")

        mock_get.side_effect = delayed_response

        # Test the fetch_data function with a timeout of 3 seconds
        with self.assertRaises(requests.exceptions.Timeout):
            FacebookDataProvider(Mock()).get_posts(Mock())
