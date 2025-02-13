from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType,
    ArrayType,
)

spark = SparkSession

df = spark.readStream.fomrat("json").load("ai-api/src/coming-data")


writer = (
    df.writeStream.outputMode("append")
    .format("parquet")
    .option("path", "ai-api/src/data_sink")
)
