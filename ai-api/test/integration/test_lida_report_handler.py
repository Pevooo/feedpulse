import json
from datetime import datetime, timezone
from pyspark.sql.functions import col, substring_index

# Import LIDA components and Spark dependencies.
from src.spark.spark import Spark
from src.spark.spark_table import SparkTable
from lida import Manager, llm, TextGenerationConfig
from src.models.prompt import Prompt
from src.concurrency.concurrency_manager import ConcurrencyManager
from src.reports.lida_report_handler import LidaReportHandler

from unittest.mock import Mock, MagicMock

# --- Setup Rich Dummy Data for Summarization and Visualization ---
# Each row now includes content and engagement metrics.
dummy_data = [
    {
        "post_id": "123_111",
        "created_time": datetime(2025, 2, 24, 20, 47, 43, tzinfo=timezone.utc),
        "content": "I really enjoyed this post—it was insightful and detailed.",
        "likes": 10,
        "comments": 2,
    },
    {
        "post_id": "123_112",
        "created_time": datetime(2025, 2, 23, 20, 47, 43, tzinfo=timezone.utc),
        "content": "The post was okay, but I expected more examples and clarity.",
        "likes": 5,
        "comments": 1,
    },
    {
        "post_id": "124_111",
        "created_time": datetime(2025, 2, 24, 20, 47, 43, tzinfo=timezone.utc),
        "content": "Not impressed; it lacked detail and missed some important insights.",
        "likes": 2,
        "comments": 0,
    },
]

# Create a dummy DataFrame-like object using MagicMock.
dummy_dataframe = MagicMock()
# When filter() is called, simply return dummy_dataframe (simulate chaining).
dummy_dataframe.filter.return_value = dummy_dataframe
# When collect() is called, return dummy rows; each row simulates asDict() returning a dictionary.
dummy_dataframe.collect.return_value = [
    MagicMock(asDict=lambda d=row: row) for row in dummy_data
]

# Create a dummy SparkTable instance (using MagicMock for interface).
dummy_spark_table = MagicMock(spec=SparkTable)

# Create a dummy Spark instance and patch its read() method to return our dummy_dataframe.
dummy_concurrency_manager = ConcurrencyManager()
spark = Spark(Mock(), Mock(), Mock(), Mock(), dummy_concurrency_manager)
spark.read = MagicMock(return_value=dummy_dataframe)

# --- Instantiate the LIDA Report Handler ---
# Note: LidaReportHandler expects a SparkTable instance as the second argument.
handler = LidaReportHandler(spark, dummy_spark_table)

# Define filter parameters as datetime objects.
page_id_filter = "123"
start_date = datetime(2025, 2, 21, 20, 47, 43, tzinfo=timezone.utc)
end_date = datetime(2025, 2, 26, 20, 47, 43, tzinfo=timezone.utc)

# --- Test prepare_data() ---
# This method filters rows based on the prefix of post_id and the created_time range.
filtered_data = handler.prepare_data(page_id_filter, start_date, end_date)
print("Filtered Data:")
print(json.dumps(filtered_data, default=str, indent=2))

# --- Test generate_report() ---
# This method internally calls summarize(), goals(), visualize(), etc.
# The richer dummy data now allows LIDA to generate a summary and visualization code.
report = handler.generate_report(page_id_filter, start_date, end_date)
print("\nFinal Report:")
print(report)
