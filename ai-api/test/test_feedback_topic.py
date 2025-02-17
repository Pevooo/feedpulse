import unittest

from src.topics.feedback_topic import FeedbackTopic


class TestFeedbackTopic(unittest.TestCase):
    def setUp(self):
        self.enum_list = [
            FeedbackTopic.CLEANLINESS,
            FeedbackTopic.STAFF,
            FeedbackTopic.FOOD,
            FeedbackTopic.AMENITIES,
            FeedbackTopic.LOCATION,
            FeedbackTopic.WIFI,
            FeedbackTopic.SECURITY,
            FeedbackTopic.COMFORT,
            FeedbackTopic.VALUE_FOR_MONEY,
            FeedbackTopic.ACCESSIBILITY,
            FeedbackTopic.CUSTOMER_SERVICE,
            FeedbackTopic.PRIVACY,
            FeedbackTopic.NOISE_LEVEL,
            FeedbackTopic.HYGIENE,
            FeedbackTopic.COMMUNICATION,
            FeedbackTopic.PROFESSIONALISM,
            FeedbackTopic.RELIABILITY,
            FeedbackTopic.BILLING,
        ]

        self.str_list = [
            "cleanliness",
            "staff",
            "food",
            "amenities",
            "location",
            "wifi",
            "security",
            "comfort",
            "value_for_money",
            "accessibility",
            "customer_service",
            "privacy",
            "noise_level",
            "hygiene",
            "communication",
            "professionalism",
            "reliability",
            "billing",
        ]

    def test_get_all_topics(self):
        self.assertListEqual(
            FeedbackTopic.get_all_topics(),
            self.enum_list,
        )

    def test_get_all_topics_as_string(self):
        self.assertListEqual(
            FeedbackTopic.get_all_topics_as_string(),
            self.str_list,
        )
