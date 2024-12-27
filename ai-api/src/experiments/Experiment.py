"""
This file is not meant to be executed/used locally, but rather use this file through colab
"""

import os
import pickle as pk
from google.colab import drive
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import Trainer
from transformers import TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


class Experiment:

    def __init__(
        self,
        dataset_filename: str,
        model_name: str,
        num_labels: int,
        learning_rate=2e-5,
        epochs=1,
        batch_size=16,
        load_best_model_at_end=True,
        weight_decay=0.01,
    ):
        drive.mount("/content/drive")

        if model_name in os.listdir("models"):
            model_name = os.path.join("models", model_name)

        dataset = pk.load(open(f"datasets/{dataset_filename}", "rb"))

        encoded_data = dataset.map(
            lambda examples: tokenizer(
                examples["text"], padding="max_length", truncation=True
            ),
            batched=True,
        )

        model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        training_args = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=learning_rate,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            logging_dir="./logs",
            logging_steps=10,
            save_total_limit=2,
            load_best_model_at_end=load_best_model_at_end,
            report_to="none",
            weight_decay=weight_decay,  # Add weight decay
        )
        self.trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=encoded_data["Train"],
            eval_dataset=encoded_data["Test"],
            tokenizer=tokenizer,
            compute_metrics=self.__compute_metrics,
        )

    def run(self):
        self.trainer.train()

    def __compute_metrics(self, pred):
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, preds, average="weighted"
        )
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}
