class ComplaintFilter:
    def __init__(self) -> None:
        import os
        import google.generativeai as genai

        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def __call__(self, text: str) -> dict[str, bool]:
        """
        Returns a dictionary indicating if the text is a complaint and if it has a topic
        """

        response: str = self.model.generate_content(self.wrap_text(text)).text.lower()

        is_complaint = "yes" in response

        if "has a topic" in response:
            has_topic = True
        else:
            # default assumption if topic isn't clear or there is no topic
            has_topic = False

        return {
            "is_complaint": is_complaint,
            "has_topic": has_topic
        }

    def wrap_text(self, text: str) -> str:
        return (
            f"You will be provided with a text. Respond in two parts as follows:\n"
            f"1. Is it a complaint? Answer with 'yes' or 'no'.\n"
            f"2. Does the complaint have a specific topic? Answer with 'has a topic' or 'no topic'.\n\n"
            f"Here is the text: \"{text}\"."
        )
