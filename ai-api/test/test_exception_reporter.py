import unittest
from unittest.mock import Mock, ANY

from src.exception_handling.exception_reporter import ExceptionReporter
from src.spark.spark import SparkTable


class TestExceptionReporter(unittest.TestCase):
    def setUp(self):
        self.mock_spark = Mock()
        self.mock_spark.add = Mock()
        self.exception_reporter = ExceptionReporter(self.mock_spark)

    def test_one_report_exception(self):
        self.exception_reporter.report(Exception())

        expected_input = [
            {
                "exception_id": ANY,
                "exception_message": str(Exception()),
                "time": ANY,
            }
        ]

        self.mock_spark.add.assert_not_called()

        self.assertEqual(len(self.exception_reporter.exceptions), 1)


    def test_50_report_exceptions(self):
        for _ in range(50):
            self.exception_reporter.report(Exception())

        expected_input = [
            {
                "exception_id": ANY,
                "exception_message": str(Exception()),
                "time": ANY,
            }
        ]*50
        
        self.mock_spark.add.assert_called_once_with(
            SparkTable.EXCEPTIONS, expected_input
        )

        self.assertEqual(len(self.exception_reporter.exceptions), 0)


    def test_more_than_50_report_exceptions(self):
        for _ in range(51):
            self.exception_reporter.report(Exception("Test Exception"))

        expected_input = [
            {
                "exception_id": ANY,
                "exception_message": "Test Exception",
                "time": ANY,
            }
        ] * 50  
        self.mock_spark.add.assert_called_once_with(
            SparkTable.EXCEPTIONS, expected_input
        )

        self.assertEqual(len(self.exception_reporter.exceptions), 1)
