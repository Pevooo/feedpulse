import requests

from typing_extensions import deprecated
from src.data_providers.data_provider import DataProvider

FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v21.0/"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class InstagramDataProvider(DataProvider):
    """
    represents a data provider for the Facebook Graph API to fetch instagram data.
    """

    @deprecated
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

    # @deprecated
    # def get_posts(self) -> tuple[ContextDataUnit, ...]:
    #     """
    #     Gets the Instagram posts from the linked Instagram Business Account.
    #
    #     Returns:
    #         tuple[ContextDataUnit, ...]: A tuple containing all the collected posts as ContextDataUnit objects.
    #     """
    #     instagram_account_id = self.get_instagram_account_id()
    #     url = f"{FACEBOOK_GRAPH_URL}{instagram_account_id}/media"
    #     params = {
    #         "access_token": self.access_token,
    #         "fields": "caption,timestamp,comments{username,text,timestamp}",
    #     }
    #
    #     data = requests.get(url, params, timeout=3).json()
    #
    #     posts: list[ContextDataUnit] = []
    #     for post_data in data.get("data", []):
    #         message: str = post_data.get("caption", "")
    #
    #         time_created: datetime = datetime.strptime(
    #             post_data["timestamp"], DATETIME_FORMAT
    #         )
    #
    #         comments: list[FeedbackDataUnit] = (
    #             [
    #                 FeedbackDataUnit(
    #                     comment_data["text"],
    #                     datetime.strptime(comment_data["timestamp"], DATETIME_FORMAT),
    #                     tuple(),
    #                 )
    #                 for comment_data in post_data.get("comments", {}).get("data", [])
    #             ]
    #             if post_data.get("comments")
    #             else tuple()
    #         )
    #
    #         posts.append(ContextDataUnit(message, time_created, tuple(comments)))
    #     return tuple(posts)
