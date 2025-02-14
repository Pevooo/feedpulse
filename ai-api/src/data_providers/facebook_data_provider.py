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
    def get_posts(self) -> tuple[ContextDataUnit, ...]:
        """
        Gets the posts from a Facebook page using the page access token.

        Returns:
            tuple[ContextDataUnit, ...]: A tuple containing all the collected posts as ContextDataUnit objects.
        """
        page_id = self.get_page_id()
        url = f"{FACEBOOK_GRAPH_URL}{page_id}"
        params = {
            "access_token": self.access_token,
            "fields": "posts{comments,message,created_time}",
        }

        data = requests.get(url, params, timeout=3).json()
        posts: list[ContextDataUnit] = []
        for post_data in data.get("posts", {}).get("data", []):
            message: str = post_data.get("message", "")

            time_created: datetime = datetime.strptime(
                post_data["created_time"], DATETIME_FORMAT
            )

            comments: list[FeedbackDataUnit] = (
                [
                    FeedbackDataUnit(
                        comment_data["message"],
                        datetime.strptime(
                            comment_data["created_time"], DATETIME_FORMAT
                        ),
                        tuple(),
                    )
                    for comment_data in post_data.get("comments", {}).get("data", [])
                ]
                if post_data.get("comments")
                else tuple()
            )

            posts.append(ContextDataUnit(message, time_created, tuple(comments)))
        return tuple(posts)
