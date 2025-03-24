from datetime import datetime, timezone
from typing import Any

import requests

from src.data.data_manager import DataManager
from src.webhooks.webhook_handler import WebhookHandler


FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v22.0/"


class InstagramWebhookHandler(WebhookHandler):
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def handle(self, webhook_data: dict[str, Any]) -> bool:
        comments = []
        for entry in webhook_data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                comments.append(
                    {
                        "comment_id": value.get("id"),
                        "content": value.get("text"),
                        "created_time": datetime.now(timezone.utc).isoformat(),
                        "platform": "instagram",
                        "post_id": value.get("parent_id"),
                    }
                )

        self.data_manager.stream_by_webhook(comments)
        return True

    def register(self, page_id: str, access_token: str) -> bool:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        data = {"subscribed_fields": ["feed"]}

        response = requests.post(
            f"{FACEBOOK_GRAPH_URL}{page_id}/subscribed_apps", headers=headers, json=data
        )
        return response.ok
