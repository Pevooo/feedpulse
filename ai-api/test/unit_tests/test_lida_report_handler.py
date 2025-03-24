import unittest
from dataclasses import dataclass
from typing import Optional, Union, Dict
from unittest.mock import Mock

from lida.datamodel import Goal

from src.reports.lida_report_handler import LidaReportHandler


@dataclass
class FakeChartExecutorResponse:
    spec: Optional[Union[str, Dict]]
    status: bool
    raster: Optional[str]
    code: str
    library: str
    error: Optional[Dict] = None


class TestLidaReportHandler(unittest.TestCase):
    def setUp(self):
        self.mock_data_manager = Mock()
        self.mock_model_provider = Mock()
        self.report_handler = LidaReportHandler(
            self.mock_data_manager, self.mock_model_provider
        )

    def test_generate_report(self):
        self.report_handler.summarize = Mock()
        self.report_handler.goal = Mock(
            return_value=[Goal(question="q1", visualization="v1", rationale="r1")]
        )

        self.report_handler.visualize = Mock(
            return_value=FakeChartExecutorResponse(
                Mock(), Mock(), "raster", Mock(), Mock()
            )
        )

        self.report_handler.refine_chart = Mock(return_value="refined raster")

        result = self.report_handler.generate_report(Mock(), Mock(), Mock())

        self.assertEqual(len(result.goals), 1)
        self.assertEqual(len(result.chart_rasters), 1)

        self.assertEqual(result.goals[0], "Goal 1: q1")
        self.assertEqual(result.chart_rasters[0], "raster")
