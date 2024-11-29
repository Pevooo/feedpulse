from typing import Optional

from src.models.model import Model


class FeedbackClassifier:
    """
    The class responsible for performing feedback classification.
    (e.g. determining if a feedback is positive, negative or neutral)
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def classify(self, text: str) -> Optional[bool]:
        """
        Classifies the provided text as a complaint, compliment, or neutral and detects if it has a specific topic.

        Args:
            text (str): The text to classify.

        Returns:
            True if the text is positive, False if negative, or None if the text is neutral.
        """

        response: str = self.model.generate_content(self._generate_prompt(text)).lower()
        impression: Optional[bool] = None
        if "complaint" in response:
            impression = False
        elif "compliment" in response:
            impression = True

        return impression

    def _generate_prompt(self, text: str) -> str:
        return (
            f"You will be provided with a text. Respond as follows:\n"
            f"Is it a complaint, a compliment, or neutral? Answer only with 'complaint', 'compliment', or 'neutral'.\n\n"
            f'Here is the text: "{text}".'
        )
