from transformers import pipeline
from typing import Optional


class NLPClassifier:
    """
    a classifier based on sentiment analysis that classifies the feedback by predicting how many stars would this
    feedback gain (1 - 5 starts)
    """

    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
        )

    def __call__(self, text: str) -> Optional[bool]:
        result = int(self.classifier(text)[0]["label"[0]])
        if result < 3:
            return False
        elif result > 3:
            return True
        return None
