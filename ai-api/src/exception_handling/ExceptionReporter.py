import traceback
from datetime import datetime
from pyspark.sql import SparkSession
import pandas as pd


class ExceptionReporter:
    def __init__(self, hdfs_path="hdfs://localhost:9000/logs/exception_logs.parquet"):
        self.hdfs_path = hdfs_path
        self.logs = []
        self.spark = SparkSession.builder.appName("ExceptionReporter").getOrCreate()

    def report(self, exception: Exception, **metadata):
        self._log_exception(exception, **metadata)
        self._save_to_hdfs()

    def _log_exception(self, exception: Exception, **metadata):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "stack_trace": traceback.format_exc(),
            "metadata": str(metadata),
        }
        self.logs.append(log_entry)

    def _save_to_hdfs(self):
        # Convert logs to PySpark DataFrame
        spark_df = self.spark.createDataFrame(self.logs)

        # Write the DataFrame to Parquet in HDFS
        spark_df.write.mode("append").parquet(self.hdfs_path)

        # Clear the logs after saving to avoid duplicates
        self.logs.clear()
