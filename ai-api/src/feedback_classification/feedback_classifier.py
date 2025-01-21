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

    def classify(self, text_batch: list[str]) -> list[Optional[bool]]:
        """
        Classifies the provided text as a complaint, compliment, or neutral and detects if it has a specific topic.

        Args:
            text_batch (list[str]): The text to classify.

        Returns:
            True if the text is positive, False if negative, or None if the text is neutral.
        """

        responses: list[str] = (
            self.model.generate_content(self._generate_prompt(text_batch))
            .lower()
            .split(",")
        )

        impressions: list[Optional[bool]] = []
        for response in responses:
            if "0" in response:
                impressions.append(False)
            elif "1" in response:
                impressions.append(True)
            elif "2" in response:
                impressions.append(None)
        return impressions

    @staticmethod
    def _generate_prompt(text_batch: list[str]) -> Prompt:
        return Prompt(
            instructions=(
                "Classify the given feedbacks as '1' for positive feedback , '0' for negative feedback, or '2'for neutral one for each one"
                "Respond with the specific label only."
            ),
            context=None,
            examples=(
                ("The service was terrible, and I want my money back.", "0"),
                ("I love the new app features.", "1"),
                ("There is a park near my house.", "2"),
                (
                    "The service was terrible, and I want my money back.,"
                    "I love the new app features.,"
                    "There is a park near my house.",
                    "0,1,2",
                ),
            ),
            input_text=",".join(text_batch),
        )
