from transformers import pipeline


class NLPFeedbackClassifier:
    """
    a classifier based on sentiment analysis that classifies the feedback by predicting if it positive, negative or neutral
    """

    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis"
        )

    def _get_sentiments(self, texts: list[str]):
        return self.classifier(texts)

    def classify(self, texts: list[str]) -> list[bool | None]:
        results = self._get_sentiments(texts)
        bool_list: list[bool | None] = [
            (
                True
                if result["label"] in ["Positive", "Very Positive"]
                else False if result["label"] in ["Negative", "Very Negative"] else None
            )
            for result in results
        ]
        return bool_list
