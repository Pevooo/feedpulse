class ComplaintFilter:
    def __init__(self) -> None:
        import os
        import google.generativeai as genai 

        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def __call__(self, text: str) -> bool:
        """
        Returns true if the text is a complaint
        """

        response: str = self.model.generate_content(self.wrap_text(text)).text
        return "yes" in response.lower()

    def wrap_text(self, text: str) -> str:
        return f"You will be provided with some text and you have to tell if it's a complaint or not using only one word (YES or NO).\nHere is the text: \"{text}\"."
