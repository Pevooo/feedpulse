from enum import Enum
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType,
    ArrayType,
)

# Define schemas
pages_schema = StructType([StructField("page_id", StringType(), False)])

posts_schema = StructType(
    [
        StructField("post_id", StringType(), False),
        StructField("page_id", StringType(), False),
        StructField("content", StringType(), True),
    ]
)

comments_schema = StructType(
    [
        StructField("hashed_comment", StringType(), False),
        StructField("platform", StringType(), False),
        StructField("content", StringType(), False),
        StructField("related_topics", ArrayType(StringType(), True), True),
        StructField("sentiment", StringType(), True),
        StructField("transaction_type", StringType(), True),
        StructField("timestamp", TimestampType(), False),
    ]
)

exceptions_schema = StructType(
    [
        StructField("exception_id", StringType(), False),
        StructField("exception_message", StringType(), True),
        StructField("time", TimestampType(), False),
    ]
)


class SparkTable(Enum):
    REPORTS = "reports"
    INPUT_COMMENTS = "input_comments"
    PROCESSED_COMMENTS = "processed_comments"
    PAGES = "pages"


class Spark:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Spark, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.spark = SparkSession.builder.appName("session").getOrCreate()

    def add(self, table: SparkTable, row_data: str):
        pass

    def delete(self, table: SparkTable, row_data: str):
        pass

    def query(self, table: SparkTable, row_data: str):
        pass

    def modify(self, table: SparkTable, row_data: str):
        pass


spark_instance = Spark()
