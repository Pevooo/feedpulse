import time
from tabulate import tabulate


def main():

    tests = [
        ("Spark Read 1,000 Rows", _exec_time(spark_read_1k)),
        ("Spark Read 1,000,000 Rows", _exec_time(spark_read_1m)),
    ]

    # Generate Markdown table
    performance_table = tabulate(
        tests, headers=["Component", "Execution Time (s)"], tablefmt="github"
    )
    with open("performance_report.md", "w") as f:
        f.write("## 🏎️ Performance Report\n\n")
        f.write(performance_table)
        f.write("\n")


def _exec_time(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)  # Should be synchronous
    end = time.perf_counter()
    return end - start


def spark_read_1k():
    time.sleep(1.2)


def spark_read_1m():
    time.sleep(0.5)


if __name__ == "__main__":
    main()
