from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").getOrCreate()

df = spark.readStream.format("json").load("ai-api/src/coming-data")


writer = (
    df.writeStream.outputMode("append")
    .format("parquet")
    .option("path", "ai-api/src/data_sink")
)
