import unittest
from dataclasses import dataclass
from typing import Optional, Union, Dict
from unittest.mock import Mock
import pandas as pd
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

        self.report_handler.compute_metrics = Mock(return_value={})

    def test_compute_metrics(self):
        data = pd.DataFrame(
            {
                "sentiment": ["positive", "negative", "neutral", "positive"],
                "related_topics": ["sports", "politics", "technology", "sports"],
            }
        )

        result = self.report_handler.compute_metrics(data)
        print(result)

    def test_compute_metrics_multiple_topics(self):
        # DataFrame with multiple topics in one cell
        data = pd.DataFrame({
            'sentiment': ['positive', 'negative', 'neutral', 'positive'],
            'related_topics': ['sports, politics', 'politics', 'technology', 'sports, technology']
        })

        result = self.report_handler.compute_metrics(data)
        print(result)
        self.assertIsNotNone(result)
    
    def test_compute_metrics_with_empty(self):
        # Test with an empty DataFrame
        empty_data = pd.DataFrame({
            'sentiment': ['positive', 'negative', 'neutral', 'positive'],
            'related_topics': ['', '', '', 'sports, technology']
        })

        result = self.report_handler.compute_metrics(empty_data)

        # Example: assert the result is empty or zeros
        # Adjust based on your expected behavior
        print(result)
        self.assertIsNotNone(result)
        self.assertEqual(len(result),0) 

    def test_compute_metrics_empty(self):
        # Test with an empty DataFrame
        empty_data = pd.DataFrame({
            'sentiment': ['positive', 'negative', 'neutral', 'positive'],
            'related_topics': ['', '', '', '']
        })

        result = self.report_handler.compute_metrics(empty_data)

        # Example: assert the result is empty or zeros
        # Adjust based on your expected behavior
        print(result)
        self.assertIsNotNone(result)
        self.assertEqual(len(result),0) 

    def test_generate_report(self):
        self.report_handler.summarize = Mock(return_value="dummy summary")
        self.report_handler.goal = Mock(
            return_value=[Goal(question="q1", visualization="v1", rationale="r1")]
        )

        self.report_handler.visualize = Mock(
            return_value=[
                FakeChartExecutorResponse(Mock(), Mock(), "raster", Mock(), Mock())
            ]
        )

        self.report_handler.refine_chart = Mock(return_value="refined raster")

        result = self.report_handler.generate_report(Mock(), Mock(), Mock())

        self.assertEqual(len(result.goals), 1)
        self.assertEqual(len(result.chart_rasters), 1)

        self.assertEqual(result.goals[0], "Goal 1: q1")
        self.assertEqual(result.chart_rasters[0], "raster")
        self.assertEqual(result.metrics, {})
