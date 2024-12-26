from typing import Optional

from src.models.model import Model

from src.models.prompt import Prompt


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
        return Prompt(
            instructions="Classify the given text as 'complaint', 'compliment', or 'neutral'. Respond with the specific label only. ",
            context=None,
            examples=(
                ("The service was terrible, and I want my money back.", "complaint"),
                ("I love the new app features.", "compliment"),
                ("There is a park near my house.", "neutral"),
            ),
            input_text=text,
        ).to_text()
