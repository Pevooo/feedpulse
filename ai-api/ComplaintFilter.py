class ComplaintFilterResult:
    def __init__(self, type, has_topic) -> None:
        self.type = type
        self.has_topic = has_topic


class ComplaintFilter:

    def __init__(self) -> None:
        import os
        import google.generativeai as genai

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def __call__(self, text: str) -> ComplaintFilterResult:

        """
        Returns a ComplaintFilterResult indicating if the text is a complaint and if it has a topic
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

        return ComplaintFilterResult(text_type, has_topic)

    def wrap_text(self, text: str) -> str:
        return (
            f"You will be provided with a text. Respond in two parts as follows:\n"
            f"1. Is it a complaint, a compliment, or neutral? Answer with 'complaint', 'compliment', or 'neutral'.\n"
            f"2. Does the complaint or compliment have a specific topic? Answer with 'yes' or 'no'.\n\n"
            f'Here is the text: "{text}".'
        )
