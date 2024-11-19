from transformers import Pipeline
from typing import Optional


class NLPClassifier:
    """
    a classifier based on sentiment analysis that classifies the feedback by predicting how many stars would this
    feedback gain (1 - 5 starts)
    """

    def __init__(self, classifier: Pipeline):
        self.classifier = classifier

    def __call__(self, text: str) -> Optional[bool]:
        stars = self.extract_stars(self.classifier(text))
        if stars < 3:
            return False
        elif stars > 3:
            return True
        return None

    def extract_stars(self, result: list[dict[str, str]]) -> int:
        return int(result[0]["label"][0])
