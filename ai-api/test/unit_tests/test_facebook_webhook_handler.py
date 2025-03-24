import unittest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from src.data.data_manager import DataManager
from src.webhooks.facebook_webhook_handler import FacebookWebhookHandler


class TestFacebookWebhookHandler(unittest.TestCase):
    def setUp(self):
        self.mock_data_manager = MagicMock(spec=DataManager)
        self.handler = FacebookWebhookHandler(data_manager=self.mock_data_manager)

    def test_valid_comment_event(self):
        webhook_data = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "item": "comment",
                                "comment_id": "comment_1",
                                "message": "Test comment",
                                "created_time": 1742667604,
                                "post_id": "post_1",
                            }
                        }
                    ]
                }
            ],
            "object": "page",
        }
        expected_iso_time = datetime.fromtimestamp(
            1742667604, tz=timezone.utc
        ).isoformat()
        result = self.handler.handle(webhook_data)
        self.assertTrue(result)
        self.mock_data_manager.stream_by_webhook.assert_called_once_with(
            [
                {
                    "comment_id": "comment_1",
                    "content": "Test comment",
                    "created_time": expected_iso_time,
                    "platform": "facebook",
                    "post_id": "post_1",
                }
            ]
        )

    def test_non_comment_event(self):
        webhook_data = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "item": "post",
                                "comment_id": "comment_1",
                                "message": "Not a comment",
                                "created_time": 1742667604,
                                "post_id": "post_1",
                            }
                        }
                    ]
                }
            ],
            "object": "page",
        }
        result = self.handler.handle(webhook_data)
        self.assertTrue(result)
        self.mock_data_manager.stream_by_webhook.assert_called_once_with([])
