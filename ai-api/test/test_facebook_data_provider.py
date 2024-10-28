import unittest
from unittest.mock import patch, Mock
from src.facebook_data_provider import FacebookDataProvider


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
    def test_get_posts(self, mock_get):
        # Whenever send request is called: return FAKE_API_RESPONSE
        mock_get.return_value.json.return_value = FAKE_API_RESPONSE

        # Pass anything as access token as we don't use it in the test
        data_provider = FacebookDataProvider(Mock())

        posts = data_provider.get_posts(Mock())

        self.assertEqual(
            posts[0].text,
            "hello 2",
        )

        self.assertEqual(
            len(posts[0].comments),
            0,
        )

        self.assertEqual(
            len(posts[1].comments),
            1,
        )
