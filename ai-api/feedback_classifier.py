import os
import google.generativeai as genai


class FeedbackClassifierResult:
    def __init__(self, text_type, has_topic) -> None:
        self.text_type = text_type
        self.has_topic = has_topic


class FeedbackClassifier:
    def __init__(self) -> None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def __call__(self, text: str) -> FeedbackClassifierResult:
        """
        "It returns whether it's a complaint or a compliment, and if it has topic
        """

        response: str = self.model.generate_content(self.wrap_text(text)).text.lower()
        text_type = "neutral"
        if "complaint" in response:
            text_type = "complaint"

        elif "compliment" in response:
            text_type = "compliment"

        # default assumption if topic isn't clear or there is no topic
        has_topic = False
        if "yes" in response:
            has_topic = True

        return FeedbackClassifierResult(text_type, has_topic)

    def wrap_text(self, text: str) -> str:
        return (
            f"You will be provided with a text. Respond in two parts as follows:\n"
            f"1. Is it a complaint, a compliment, or neutral? Answer with 'complaint', 'compliment', or 'neutral'.\n"
            f"2. Does the complaint or compliment have a specific topic? Answer with 'yes' or 'no'.\n\n"
            f'Here is the text: "{text}".'
        )
