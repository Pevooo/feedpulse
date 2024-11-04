import requests
from datetime import datetime

from src.facebook.comment import Comment
from src.facebook.post import Post

FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v21.0/"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class FacebookDataProvider:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    def get_posts(self, page_id: str) -> list[Post]:
        """
        Gets the posts from Facebook page using a page id

        Args:
            page_id (str): The id of the intended page.

        Returns:
            posts (list[Post]): A list containing all the collected posts.
        """
        url = f"{FACEBOOK_GRAPH_URL}{page_id}"
        params = {
            "access_token": self.access_token,
            "fields": "posts{comments,message,created_time}",
        }

        data = requests.get(url, params).json()

        posts: list[Post] = []
        for post_data in data["posts"]["data"]:
            message: str = post_data["message"]

            time_created: datetime = datetime.strptime(
                post_data["created_time"], DATETIME_FORMAT
            )

            comments: list[Comment] = (
                [
                    Comment(
                        comment_data["message"],
                        datetime.strptime(
                            comment_data["created_time"], DATETIME_FORMAT
                        ),
                    )
                    for comment_data in post_data["comments"]["data"]
                ]
                if post_data.get("comments")
                else []
            )

            posts.append(Post(message, time_created, comments))
        return posts
