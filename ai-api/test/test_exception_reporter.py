import unittest
from unittest.mock import Mock, ANY

from src.exception_handling.exception_reporter import ExceptionReporter
from src.spark.spark import SparkTable


class TestExceptionReporter(unittest.TestCase):
    def setUp(self):
        self.mock_spark = Mock()
        self.mock_spark.add = Mock()
        self.exception_reporter = ExceptionReporter(self.mock_spark)

    def test_report_exception(self):
        self.exception_reporter.report(Exception())

        expected_input = [
            {
                "exception_id": ANY,
                "exception_message": str(Exception()),
                "time": ANY,
            }
        ]

        self.mock_spark.add.assert_called_once_with(
            SparkTable.EXCEPTIONS, expected_input
        )
