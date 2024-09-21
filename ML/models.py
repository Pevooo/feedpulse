import joblib
import constants
import os

class BaseModel:
    def __init__(self):
        self.name = self.__class__.__name__

    @classmethod
    def load(cls) -> 'BaseModel':
        return joblib.load(os.path.join(constants.MODELS_PATH, f"{cls.__name__}.joblib"))

    def save(self) -> None:
        joblib.dump(self, os.path.join(constants.MODELS_PATH, f"{self.name}.joblib"))

    def predict(self, question: str, answer: str, candidate_answer: str) -> float:
        raise NotImplementedError
    
    def train(self):
        raise NotImplementedError
    
class SBert(BaseModel):
    def train(self):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def predict(self, question: str, answer: str, candidate_answer: str) -> str:
        from sentence_transformers import util

        answer_embeddings = self.model.encode(answer, convert_to_tensor=True)
        candidate_answer_embeddings = self.model.encode(candidate_answer, convert_to_tensor=True)

        cosine_similarity = util.pytorch_cos_sim(answer_embeddings, candidate_answer_embeddings)

        return cosine_similarity