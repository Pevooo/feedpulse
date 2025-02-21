import requests
from datetime import datetime

from src.data_providers.data_provider import DataProvider
from src.utlity.util import deprecated

FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v21.0/"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class FacebookDataProvider(DataProvider):
    """
    represents a data provider for the Facebook Graph API to fetch facebook data.
    """

    @deprecated
    def get_page_id(self) -> str:
        """
        Retrieves the page ID associated with the provided page access token.

        Returns:
            str: The ID of the page.
        """
        url = f"{FACEBOOK_GRAPH_URL}me"
        params = {"access_token": self.access_token}
        response = requests.get(url, params, timeout=3)
        data = response.json()

        if "error" in data:
            raise Exception(f"Error fetching page ID: {data['error']['message']}")

        return data.get("id")

    @deprecated
    def get_posts(self) -> tuple[dict, ...]:
        """
        Gets the last 100 posts with all of their comments and replies from a Facebook page using the page access token.

        Returns:
            tuple[dict, ...]: A tuple containing all the collected comments and replies as dictionaries.
        """
        page_id = self.get_page_id()
        url = f"{FACEBOOK_GRAPH_URL}{page_id}"
        params = {
            "access_token": self.access_token,
            "fields": "posts.limit(1){id,message,created_time,comments.limit(1){id,message,created_time,comments.limit(1)}}",
        }

        data = requests.get(url, params, timeout=3).json()
        posts: list[dict] = []
        for post_data in data.get("posts", {}).get("data", []):
            # posts
            post_id = post_data.get("id")

            # comments
            comments_edge = post_data.get("comments", {})
            comments = comments_edge.get("data", [])

            if "paging" in comments_edge and "next" in comments_edge["paging"]:
                comments += self.fetch_all_items(comments_edge["paging"]["next"])

            for comment_data in comments:
                posts.append(
                    {
                        "comment_id": comment_data.get("id"),
                        "post_id": post_id,
                        "content": comment_data.get("message"),
                        "created_time": datetime.strptime(
                            comment_data.get("created_time"), DATETIME_FORMAT
                        ),
                        "platform": "facebook",
                    }
                )

                # replies
                if "comments" in comment_data:

                    replies_edge = comment_data.get("comments", {})
                    replies = replies_edge.get("data", [])

                    if "paging" in replies_edge and "next" in replies_edge["paging"]:
                        replies += self.fetch_all_items(replies_edge["paging"]["next"])

                    for reply_data in replies:
                        posts.append(
                            {
                                "comment_id": reply_data.get("id"),
                                "post_id": post_id,
                                "content": reply_data.get("message"),
                                "created_time": datetime.strptime(
                                    reply_data.get("created_time"), DATETIME_FORMAT
                                ),
                                "platform": "facebook",
                            }
                        )

        return tuple(posts)

    def fetch_all_items(self, url: str, params: dict = None) -> list[dict]:
        """Fetch all items by following pagination cursors."""
        items = []
        while url:
            response = requests.get(url, params=params, timeout=3).json()
            items.extend(response.get("data", []))
            # Once the first page is fetched, subsequent requests use the 'next' URL directly.
            url = response.get("paging", {}).get("next")
            params = None  # 'next' already contains all necessary query parameters.
        return items
