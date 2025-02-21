import requests
from datetime import datetime

from src.data.context_data_unit import ContextDataUnit
from src.data.feedback_data_unit import FeedbackDataUnit
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
            "fields": "posts.limit(100){id,message,created_time,comments.limit(100){id,message,created_time,comments.limit(100){id,message,created_time}}}"
        }

        data = requests.get(url, params, timeout=3).json()
        posts: list[dict] = []
        for post_data in data.get("posts", {}).get("data", []):
            #posts
            post_id = post_data.get("id")

            #comments
            for comment_data in post_data.get("comments", {}).get("data", []):
                posts.append({
                    "comment_id": comment_data.get("id"),
                    "post_id": post_id,
                    "message": comment_data.get("message"),
                    "created_time": datetime.strptime(comment_data.get("created_time"), DATETIME_FORMAT),
                    "platform": "facebook"
                })

                #replies
                for reply_data in comment_data.get("comments", {}).get("data", []):
                posts.append({
                    "comment_id": reply_data.get("id"),
                        "post_id": post_id,
                        "message": reply_data.get("message"),
                        "created_time": datetime.strptime(reply_data.get("created_time"), DATETIME_FORMAT),
                        "platform": "facebook"
                })

        return tuple(posts)
