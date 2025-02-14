from transformers import Pipeline


class FeedbackClassifier:
    """
    a classifier based on sentiment analysis that classifies the feedback by predicting if it's positive, negative or neutral
    """

    def __init__(self, classifier: Pipeline):
        self.classifier = classifier

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
