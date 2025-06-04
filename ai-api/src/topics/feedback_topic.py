from enum import Enum


class FeedbackTopic(Enum):
    """
    This enum includes all the topics we use in feedback classification
    """
    CLEANLINESS = "cleanliness"
    STAFF = "staff"
    FOOD = "food"
    AMENITIES = "amenities"
    LOCATION = "location"
    WIFI = "wifi"
    ACCESSIBILITY = "accessibility"
    PRIVACY = "privacy"
    SECURITY = "security"
    COMFORT = "comfort"
    VALUE_FOR_MONEY = "value_for_money"
    CUSTOMER_SERVICE = "customer_service"
    NOISE_LEVEL = "noise_level"
    HYGIENE = "hygiene"
    COMMUNICATION = "communication"
    PROFESSIONALISM = "professionalism"
    RELIABILITY = "reliability"
    BILLING = "billing"

    @classmethod
    def get_all_topics(cls) -> list["FeedbackTopic"]:
        return list(cls)  # Return all enum members directly

    @classmethod
    def get_all_topics_as_string(cls) -> list[str]:
        return [topic.value for topic in cls]
