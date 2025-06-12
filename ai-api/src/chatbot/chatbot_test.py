import base64

import pandas as pd

from src.chatbot.chatbot import Chatbot
from src.models.global_model_provider import GlobalModelProvider
from src.models.google_model_provider import GoogleModelProvider

dataset = {
    "comment_id": [1, 2, 3, 4, 5],
    "user_name": ["Alice", "Bob", "Charlie", "Daisy", "Eli"],
    "comment_text": [
        "Love this!",
        "Could be better",
        "Amazing work team!",
        "Not what I expected...",
        "So helpful, thank you!",
    ],
    "timestamp": pd.to_datetime(
        [
            "2025-06-10 10:12",
            "2025-06-10 11:45",
            "2025-06-10 13:05",
            "2025-06-10 15:20",
            "2025-06-10 16:00",
        ]
    ),
    "likes": [10, 2, 8, 1, 5],
    "sentiment": ["positive", "neutral", "positive", "negative", "positive"],
}

df = pd.DataFrame(dataset)

chatbot = Chatbot(GlobalModelProvider([GoogleModelProvider()]), df)


while True:
    response, is_raster = chatbot.ask(input("Enter your question: "))
    if is_raster:
        with open(r"C:\Users\pevod\Desktop\plot.png", "wb") as f:
            f.write(base64.b64decode(response))
        print("Image saved")
    else:
        print(response)
