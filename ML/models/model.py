import joblib

class Model:
    def __init__(self):
        self.name = self.__class__.__name__

    @staticmethod
    def load(name: str):
        return joblib.load(f"{name}.joblib")

    def save(self) -> None:
        joblib.dump(self, f"{self.name}.joblib")

    def predict(self, question: str, answer: str, candidate_answer: str) -> bool:
        raise NotImplementedError
    
    def train():
        raise NotImplementedError
    
