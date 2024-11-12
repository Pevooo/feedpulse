"""
Fake Twikit Tweets, fakes the collection of tweets to mock the `next` method and return nothing and
it's compatible with `FakeTwikitTweets`.
"""


class FakeTwikitTweets:
    def __init__(self, tweets):
        self.tweets = tweets

    def __iter__(self):
        return self.tweets.__iter__()

    async def next(self):
        return []
