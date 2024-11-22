"""
A fake tweet used to mock twikit.Tweet, used for simplicity
"""


class FakeTwikitTweet:
    def __init__(self, text, id, created_at_datetime, replies):
        self.text = text
        self.id = id
        self.created_at_datetime = created_at_datetime
        self.replies = replies
