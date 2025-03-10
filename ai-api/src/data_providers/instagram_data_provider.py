import requests
from datetime import datetime

from src.data_providers.data_provider import DataProvider

FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v21.0/"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class InstagramDataProvider(DataProvider):
    """
    represents a data provider for the Facebook Graph API to fetch instagram data.
    """

    def get_instagram_account_id(self) -> str:
        """
        Retrieves the Instagram Business Account ID linked to the Facebook page.

        Returns:
            str: The Instagram Business Account ID.
        """
        url = f"{FACEBOOK_GRAPH_URL}me/accounts"
        params = {"access_token": self.access_token}
        response = requests.get(url, params, timeout=3)
        data = response.json()

        if "error" in data:
            raise Exception(f"Error fetching page data: {data['error']['message']}")

        # Look for the Instagram Business Account
        for page in data.get("data", []):
            if "instagram_business_account" in page:
                return page["instagram_business_account"]["id"]

        raise Exception("No Instagram Business Account linked to this page.")

    def get_posts(self) -> tuple[dict, ...]:
        """
        Gets the Instagram posts from the linked Instagram Business Account along with
        all of their comments and replies.

         Returns:
             tuple[dict, ...]: A tuple containing all the collected comments and replies as dictionaries.
        """
        instagram_account_id = self.get_instagram_account_id()
        url = f"{FACEBOOK_GRAPH_URL}{instagram_account_id}/media"
        params = {
            "access_token": self.access_token,
            "fields": "posts.limit(100){id,caption,created_time,comments.limit(100){id,username,text,created_time,replies.limit(100){id,username,text,created_time}}",
        }

        data = requests.get(url, params, timeout=3).json()

        posts: list[dict] = []
        for post_data in data.get("data", []):
            post_id = post_data.get("id")

            # comments
            comments_edge = post_data.get("comments", {})
            comments = comments_edge.get("data", [])

            if "paging" in comments_edge and "next" in comments_edge["paging"]:
                comments += self.next(comments_edge["paging"]["next"])

            for comment_data in comments:
                posts.append(
                    {
                        "comment_id": comment_data.get("id"),
                        "post_id": post_id,
                        "content": comment_data.get("caption"),
                        "created_time": datetime.strptime(
                            comment_data.get("created_time"), DATETIME_FORMAT
                        ),
                        "platform": "instagram",
                    }
                )

                # replies
                if "replies" in comments:

                    replies_edge = comment_data.get("replies", {})
                    replies = replies_edge.get("data", [])

                    if "paging" in replies_edge and "next" in replies_edge["paging"]:
                        replies += self.next(replies_edge["paging"]["next"])

                    for reply_data in replies:
                        posts.append(
                            {
                                "comment_id": reply_data.get("id"),
                                "post_id": post_id,
                                "content": reply_data.get("caption"),
                                "created_time": datetime.strptime(
                                    comment_data.get("created_time"), DATETIME_FORMAT
                                ),
                                "platform": "instagram",
                            }
                        )

        return tuple(posts)

    def next(self, url: str) -> list[dict]:
        """Fetch all items by following pagination cursors."""
        items = []
        while url:
            response = requests.get(url, params=None, timeout=3).json()
            items.extend(response.get("data", []))
            # Once the first page is fetched, subsequent requests use the 'next' URL directly.
            url = response.get("paging", {}).get("next")
        return items
