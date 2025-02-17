import uuid
from datetime import datetime

from src.spark.spark import Spark, SparkTable


class ExceptionReporter:
    def __init__(self, spark: Spark):
        self.spark = spark
        self.exceptions = []

    def report(self, exception: Exception):
        self.exceptions.append(
            {
                "exception_id": str(uuid.uuid4()),
                "exception_message": str(exception),
                "time": datetime.now().isoformat(),
            }
        )
        if len(self.exceptions) == 50:
            self.spark.add(
                SparkTable.EXCEPTIONS,
                self.exceptions,
            )
            self.exceptions = []
