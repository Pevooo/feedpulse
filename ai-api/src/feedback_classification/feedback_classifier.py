from src.feedback_classification.feedback_classifier_result import (
    FeedbackClassifierResult,
)
from src.loaded_models.model import Model


class FeedbackClassifier:
    """
    The class responsible for performing feedback classification. (e.g. determining if a feedback is
    positive, negative or neutral)
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def __call__(self, text: str) -> FeedbackClassifierResult:
        """
        Classifies the provided text as a complaint, compliment, or neutral and detects if it has a specific topic.

        Args:
            text (str): The text to classify.

        Returns:
            FeedbackClassifierResult: An instance of FeedbackClassifierResult with the classification
            results if the classification.
        """

        response: str = self.model.generate_content(self.wrap_text(text)).lower()
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
