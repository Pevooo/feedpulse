import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.data_providers.instagram_data_provider import (
    InstagramDataProvider,
    FACEBOOK_GRAPH_URL,
    DATETIME_FORMAT,
)


class TestInstagramDataProvider(unittest.TestCase):
    def setUp(self):
        # Set up a dummy access token and instance of InstagramDataProvider.
        self.provider = InstagramDataProvider("dummy_access_token")

    @patch("src.data_providers.instagram_data_provider.requests.get")
    def test_get_instagram_account_id_success(self, mock_get):
        # Mock successful response with account ID
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [{"instagram_business_account": {"id": "67890"}}]
        }

        mock_get.return_value = mock_response

        account_id = self.provider.get_instagram_account_id()
        self.assertEqual(account_id, "67890")

        mock_get.assert_called_with(
            f"{FACEBOOK_GRAPH_URL}me/accounts",
            {"access_token": "dummy_access_token"},
            timeout=3,
        )

    @patch("src.data_providers.instagram_data_provider.requests.get")
    def test_get_instagram_account_id_error(self, mock_get):
        error_message = "Invalid token"
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": {"message": error_message}}
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.provider.get_instagram_account_id()
        self.assertIn(error_message, str(context.exception))

    @patch("src.data_providers.instagram_data_provider.requests.get")
    def test_get_posts_success(self, mock_get):
        # Mock posts response with comments
        self.provider.get_instagram_account_id = lambda: "67890"
        posts_response = {
            "data": [
                {
                    "id": "post1",
                    "caption": "Post caption",
                    "created_time": "2025-02-21T19:00:00+0000",
                    "comments": {
                        "data": [
                            {
                                "id": "comment1",
                                "caption": "Comment caption",
                                "created_time": "2025-02-21T19:05:00+0000",
                            }
                        ]
                    },
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = posts_response
        mock_get.return_value = mock_response

        posts = self.provider.get_posts()
        self.assertIsInstance(posts, tuple)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["comment_id"], "comment1")
        self.assertEqual(posts[0]["content"], "Comment caption")
        expected_datetime = datetime.strptime(
            "2025-02-21T19:05:00+0000", DATETIME_FORMAT
        )
        self.assertEqual(posts[0]["created_time"], expected_datetime)
        self.assertEqual(posts[0]["platform"], "instagram")
