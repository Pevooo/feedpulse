import csv
import pandas as pd
import constants
from models import BaseModel

class DatasetTestResult:
    def __init__(
            self,
            total_lines: int,
            random_text_success_count: int,
            decieving_text_success_count: int,
            identical_text_success_count: int,
            similar_text_success_count: int,    
        ) -> None:
        # Main attributes
        self.total_lines = total_lines
        self.random_text_success_count = random_text_success_count
        self.decieving_text_success_count = decieving_text_success_count
        self.identical_text_success_count = identical_text_success_count
        self.similar_text_success_count = similar_text_success_count

        # Measured attributes
        self.random_text_success_ratio = self.random_text_success_count / self.total_lines
        self.decieving_text_success_ratio = self.decieving_text_success_count / self.total_lines
        self.identical_text_success_ratio = self.identical_text_success_count / self.total_lines
        self.similar_text_success_ratio = self.similar_text_success_count / self.total_lines

        self.total_success_ratio = (
            self.random_text_success_ratio +
            self.decieving_text_success_ratio +
            self.identical_text_success_ratio +
            self.similar_text_success_ratio
        ) / 4

class DatasetManager:     
    def get_results(self, model: BaseModel) -> list[DatasetTestResult]:
        results: list[DatasetTestResult] = []
        df_dict = {
            "rw": [],
            "dw": [],
            "ir": [],
            "sr": [],
        }

        with open(constants.DATASET_PATH, mode='r', newline='', encoding='ISO-8859-1') as infile:

            self.reader = csv.DictReader(infile)
            total_count = 0

            for row in self.reader:
                total_count += 1
                print(f"Running Predictions on row: {total_count}")
                
                df_dict["rw"].append(
                    model.predict(
                        row["question"],
                        row["answer"],
                        row["random_wrong"],
                    )
                )

                df_dict["dw"].append(
                    model.predict(
                        row["question"],
                        row["answer"],
                        row["decieving_wrong"],
                    )
                )

                df_dict["ir"].append(
                    model.predict(
                        row["question"],
                        row["answer"],
                        row["identical_right"],
                    )
                )

                df_dict["sr"].append(
                    model.predict(
                        row["question"],
                        row["answer"],
                        row["similar_right"],
                    )
                )
        
        df = pd.DataFrame(df_dict)
        for threshhold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            results.append(
                DatasetTestResult(
                    total_count,
                    (df['rw'] < threshhold).sum(),
                    (df['dw'] < threshhold).sum(),
                    (df['ir'] >= threshhold).sum(),
                    (df['sr'] >= threshhold).sum(),
                )
            )

        return results


