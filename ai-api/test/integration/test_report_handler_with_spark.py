import os
import shutil
import unittest
import datetime

from unittest.mock import Mock
from enum import Enum

from src.reports.report_handler import ReportHandler
from src.spark.spark import Spark


class FakeTable(Enum):
    FILTER_PAGE_ID = "test_report_handler/filter_page_id"
    FILTER_DATE = "test_report_handler/filter_date"


class TestReportHandlerWithSpark(unittest.TestCase):
    def setUp(self):
        self.spark = Spark(Mock(), Mock(), Mock(), Mock())

    def test_filter_exclude_wrong_page_id(self):
        self.report_handler = ReportHandler(
            Mock(), self.spark, FakeTable.FILTER_PAGE_ID
        )
        start_time = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        end_time = datetime.datetime(
            2025, 2, 26, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        test_data = self.spark.spark.createDataFrame(
            [
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2025, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "page_id": "fake_id_2",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ]
        )

        test_data.write.format("delta").save(FakeTable.FILTER_PAGE_ID.value)

        filtered_df = self.report_handler._get_filtered_page_data(
            "fake_id_1", start_time, end_time
        )

        filtered_data = filtered_df.collect()
        data_as_dict = [row.asDict() for row in filtered_data]

        self.assertListEqual(
            data_as_dict,
            [
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2025, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ],
        )

    def test_filter_exclude_wrong_dates(self):
        self.report_handler = ReportHandler(Mock(), self.spark, FakeTable.FILTER_DATE)
        start_time = datetime.datetime(
            2025, 2, 21, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        end_time = datetime.datetime(
            2025, 2, 26, 20, 47, 43, tzinfo=datetime.timezone.utc
        )

        test_data = self.spark.spark.createDataFrame(
            [
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2026, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2021, 2, 23, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ]
        )

        test_data.write.format("delta").save(FakeTable.FILTER_DATE.value)

        filtered_df = self.report_handler._get_filtered_page_data(
            "fake_id_1", start_time, end_time
        )

        filtered_data = filtered_df.collect()
        data_as_dict = [row.asDict() for row in filtered_data]

        self.assertListEqual(
            data_as_dict,
            [
                {
                    "page_id": "fake_id_1",
                    "created_time": datetime.datetime(
                        2025, 2, 24, 20, 47, 43, tzinfo=datetime.timezone.utc
                    ).isoformat(),
                },
            ],
        )

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_report_handler"):
            shutil.rmtree("test_report_handler")
