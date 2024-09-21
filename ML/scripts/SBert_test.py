from dataset import DatasetManager, DatasetTestResult
from models import SBert

model = SBert()
model.train()
model.save()
manager = DatasetManager()
model = SBert.load()
results: list[DatasetTestResult] = manager.get_results(model)

for result in results:
    print(result.decieving_text_success_ratio, result.identical_text_success_ratio, result.random_text_success_ratio, result.similar_text_success_ratio)
