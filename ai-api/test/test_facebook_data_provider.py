import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.data_providers.facebook_data_provider import (
    FacebookDataProvider,
    FACEBOOK_GRAPH_URL,
    DATETIME_FORMAT,
)


class TestFacebookDataProvider(unittest.TestCase):
    def setUp(self):
        # Set up a dummy access token and instance of FacebookDataProvider.
        self.provider = FacebookDataProvider("dummy_access_token")

    @patch("src.data_providers.facebook_data_provider.requests.get")
    def test_get_page_id_success(self, mock_get):
        # Configure the mock to return a response with an 'id'
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "12345"}
        mock_get.return_value = mock_response

        page_id = self.provider.get_page_id()
        self.assertEqual(page_id, "12345")
        # Verify URL and params are correct (optional)
        mock_get.assert_called_with(
            f"{FACEBOOK_GRAPH_URL}me",
            {"access_token": "dummy_access_token"},
            timeout=3,
        )

    @patch("src.data_providers.facebook_data_provider.requests.get")
    def test_get_page_id_error(self, mock_get):
        # Configure the mock to return an error response
        error_message = "Invalid token"
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": {"message": error_message}}
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.provider.get_page_id()
        self.assertIn(error_message, str(context.exception))

    @patch("src.data_providers.facebook_data_provider.requests.get")
    def test_get_posts_success(self, mock_get):
        # Optionally patch get_page_id to avoid making a real request
        self.provider.get_page_id = lambda: "12345"

        # Simulate a posts response with one post, one comment, and one reply
        posts_response = {
            "posts": {
                "data": [
                    {
                        "id": "post1",
                        "message": "Post message",
                        "created_time": "2025-02-21T19:00:00+0000",
                        "comments": {
                            "data": [
                                {
                                    "id": "comment1",
                                    "message": "Comment message",
                                    "created_time": "2025-02-21T19:05:00+0000",
                                    "comments": {  # Replies
                                        "data": [
                                            {
                                                "id": "reply1",
                                                "message": "Reply message",
                                                "created_time": "2025-02-21T19:06:00+0000",
                                            }
                                        ]
                                    },
                                }
                            ]
                        },
                    }
                ]
            }
        }
        # Configure the mock to return the posts_response for the posts call.
        mock_response = MagicMock()
        mock_response.json.return_value = posts_response
        mock_get.return_value = mock_response

        posts = self.provider.get_posts()
        self.assertIsInstance(posts, tuple)
        # There should be 2 items: one for the comment and one for the reply
        self.assertEqual(len(posts), 2)
        # Check that datetime parsing works correctly.
        expected_datetime = datetime.strptime(
            "2025-02-21T19:05:00+0000", DATETIME_FORMAT
        )
        self.assertEqual(posts[0]["created_time"], expected_datetime)
        self.assertEqual(posts[0]["post_id"], "post1")
        self.assertEqual(posts[0]["comment_id"], "comment1")
        self.assertEqual(posts[0]["platform"], "facebook")

    @patch("src.data_providers.facebook_data_provider.requests.get")
    def test_get_posts_comments_and_replies(self, mock_get):
        # Override get_page_id to avoid making a real HTTP call.
        self.provider.get_page_id = lambda: "12345"
        
        # Construct a simulated API response:
        # - One post with two comments:
        #   - The first comment ("comment1") has two replies ("reply1" and "reply2").
        #   - The second comment ("comment2") has no replies.
        posts_response = {
            "posts": {
                "data": [
                    {
                        "id": "post1",
                        "message": "Post message",
                        "created_time": "2025-02-21T19:00:00+0000",
                        "comments": {
                            "data": [
                                {
                                    "id": "comment1",
                                    "message": "Comment message",
                                    "created_time": "2025-02-21T19:05:00+0000",
                                    "comments": {
                                        "data": [
                                            {
                                                "id": "reply1",
                                                "message": "Reply message",
                                                "created_time": "2025-02-21T19:06:00+0000",
                                            },
                                            {
                                                "id": "reply2",
                                                "message": "Second reply message",
                                                "created_time": "2025-02-21T19:07:00+0000",
                                            },
                                        ]
                                    },
                                },
                                {
                                    "id": "comment2",
                                    "message": "Second comment message",
                                    "created_time": "2025-02-21T19:10:00+0000",
                                    "comments": {"data": []}  # No replies.
                                },
                            ]
                        },
                    }
                ]
            }
        }
        
        # Configure the mock for the posts API call.
        mock_response = MagicMock()
        mock_response.json.return_value = posts_response
        mock_get.return_value = mock_response

        # Call the method under test.
        posts = self.provider.get_posts()
        
        # Expect four items: comment1, reply1, reply2, and comment2.
        self.assertEqual(len(posts), 4)
        
        # Verify details for the first comment.
        self.assertEqual(posts[0]["comment_id"], "comment1")
        self.assertEqual(posts[0]["post_id"], "post1")
        self.assertEqual(posts[0]["content"], "Comment message")
        self.assertEqual(
            posts[0]["created_time"],
            datetime.strptime("2025-02-21T19:05:00+0000", DATETIME_FORMAT)
        )
        
        # Verify details for the first reply.
        self.assertEqual(posts[1]["comment_id"], "reply1")
        self.assertEqual(posts[1]["post_id"], "post1")
        self.assertEqual(posts[1]["content"], "Reply message")
        self.assertEqual(
            posts[1]["created_time"],
            datetime.strptime("2025-02-21T19:06:00+0000", DATETIME_FORMAT)
        )
        
        # Verify details for the second reply.
        self.assertEqual(posts[2]["comment_id"], "reply2")
        self.assertEqual(posts[2]["post_id"], "post1")
        self.assertEqual(posts[2]["content"], "Second reply message")
        self.assertEqual(
            posts[2]["created_time"],
            datetime.strptime("2025-02-21T19:07:00+0000", DATETIME_FORMAT)
        )
        
        # Verify details for the second comment.
        self.assertEqual(posts[3]["comment_id"], "comment2")
        self.assertEqual(posts[3]["post_id"], "post1")
        self.assertEqual(posts[3]["content"], "Second comment message")
        self.assertEqual(
            posts[3]["created_time"],
            datetime.strptime("2025-02-21T19:10:00+0000", DATETIME_FORMAT)
        )
