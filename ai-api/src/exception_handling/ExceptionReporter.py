import uuid
from datetime import datetime

from src.spark.spark import Spark, SparkTable


class ExceptionReporter:
    def __init__(self, spark: Spark):
        self.spark = spark

    def report(self, exception: Exception):
        self.spark.add(
            SparkTable.EXCEPTIONS,
            [
                {
                    "exception_id": uuid.uuid4(),
                    "exception_message": str(exception),
                    "time": datetime.now().isoformat(),
                }
            ],
        )
