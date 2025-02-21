import time
import os
from unittest.mock import Mock

from tabulate import tabulate
from enum import Enum
from pathlib import Path

from src.spark.spark import Spark

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class FakeTable(Enum):
    K = os.path.join(BASE_DIR, "performance_test", "K")
    M = os.path.join(BASE_DIR, "performance_test", "M")


def main():

    spark = Spark(
        Mock(), Mock(), Mock(), Mock()
    )  # Just create the instance so that we can use it later without the creation overhead

    tests = [
        # Writes before read so we can read the pre-written data
        ("Spark Write 1k Rows", _exec_time(spark_write_1k, spark)),
        ("Spark Read 1k Rows", _exec_time(spark_read_1k, spark)),
        ("Spark Size of 1k Rows", _get_folder_size(FakeTable.K.value)),
        ("Spark Write 1M Rows", _exec_time(spark_write_1m, spark)),
        ("Spark Read 1M Rows", _exec_time(spark_read_1m, spark)),
        ("Spark Size of 1M Rows", _get_folder_size(FakeTable.M.value)),
    ]

    # Generate Markdown table
    performance_table = tabulate(
        tests, headers=["Component", "Value"], tablefmt="github"
    )

    save_path = os.path.join(BASE_DIR, "performance_report.md")

    with open(save_path, "w") as f:
        f.write("## 🏎️ Performance Report\n\n")
        f.write(performance_table)
        f.write("\n")


def _exec_time(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)  # Should be synchronous
    end = time.perf_counter()
    return f"{end - start}s"


def _get_folder_size(folder_path):
    return f"{sum(f.stat().st_size for f in Path(folder_path).rglob("*"))}b"


def spark_read_1m(spark):
    spark.spark.read.parquet(FakeTable.M.value).collect()


def spark_write_1k(spark: Spark):
    spark.add(
        FakeTable.K,
        [
            {"col1": "val1", "col2": "val2"},
        ]
        * 1_000,
    ).result()


def spark_read_1k(spark: Spark):
    spark.spark.read.parquet(FakeTable.K.value).collect()


def spark_write_1m(spark: Spark):
    spark.add(
        FakeTable.M,
        [
            {"col1": "val1", "col2": "val2"},
        ]
        * 1_000_000,
    ).result()


if __name__ == "__main__":
    main()
