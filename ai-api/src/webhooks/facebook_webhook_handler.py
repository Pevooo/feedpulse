from datetime import datetime, timezone
from typing import Any

import requests

from src.data.data_manager import DataManager
from src.webhooks.webhook_handler import WebhookHandler


FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v22.0/"


class FacebookWebhookHandler(WebhookHandler):
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def handle(self, webhook_data: dict[str, Any]) -> bool:
        """
        Extracts comment details from Facebook webhook JSON and converts the created time to ISO format.

        Args:
            webhook_data (dict): The webhook JSON payload.

        Returns:
            dict: Extracted comment details or None if not a comment event.
        """
        comments = []
        for entry in webhook_data.get("entry", []):  # Loop over multiple entries
            for change in entry.get("changes", []):  # Loop over multiple changes
                value = change.get("value", {})

                # Ensure it's a comment event
                if value.get("item") == "comment":
                    created_time_unix = value.get("created_time")  # Unix timestamp

                    # Convert to ISO 8601 format (UTC)
                    created_time_iso = datetime.fromtimestamp(
                        created_time_unix, tz=timezone.utc
                    ).isoformat()

                    comments.append(
                        {
                            "comment_id": value.get("comment_id"),
                            "content": value.get("message"),
                            "created_time": created_time_iso,  # ISO format
                            "platform": "facebook",
                            "post_id": value.get("post_id"),
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
