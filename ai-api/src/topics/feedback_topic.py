from enum import Enum


class FeedbackTopic(Enum):
    CLEANLINESS = "cleanliness"
    STAFF = "staff"
    FOOD = "food"
    AMENITIES = "amenities"
    LOCATION = "location"
    WIFI = "wifi"
    PARKING = "parking"
    SECURITY = "security"
    COMFORT = "comfort"
    VALUE_FOR_MONEY = "value_for_money"
    ACCESSIBILITY = "accessibility"
    CHECKIN_PROCESS = "checkin_process"
    CHECKOUT_PROCESS = "checkout_process"
    ROOM_QUALITY = "room_quality"
    MAINTENANCE = "maintenance"
    CUSTOMER_SERVICE = "customer_service"
    ENTERTAINMENT = "entertainment"
    ATMOSPHERE = "atmosphere"
    TEMPERATURE_CONTROL = "temperature_control"
    LIGHTING = "lighting"
    PRIVACY = "privacy"
    NOISE_LEVEL = "noise_level"
    HYGIENE = "hygiene"
    COMMUNICATION = "communication"
    PROFESSIONALISM = "professionalism"
    RELIABILITY = "reliability"
    CHILD_FRIENDLINESS = "child_friendliness"
    PET_FRIENDLINESS = "pet_friendliness"
    PROMOTIONS = "promotions"
    BILLING = "billing"

    @classmethod
    def get_all_topics(cls):
        return list(cls)  # Return all enum members directly
