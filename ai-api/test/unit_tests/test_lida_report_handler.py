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
        self.mock_redis_manager = Mock()
        self.report_handler = LidaReportHandler(
            self.mock_data_manager, self.mock_model_provider, self.mock_redis_manager
        )

    def test_compute_metrics(self):
        data = pd.DataFrame(
            {
                "sentiment": ["positive", "negative", "neutral", "positive"],
                "related_topics": ["sports", "politics", "technology", "sports"],
            }
        )

        result = self.report_handler.compute_metrics(data)
        self.assertEqual(
            result,
            {
                "most_freq_sentiment_per_topic": {
                    "politics": "negative",
                    "sports": "positive",
                    "technology": "neutral",
                },
                "most_freq_topic_per_sentiment": {
                    "negative": "politics",
                    "neutral": "technology",
                    "positive": "sports",
                },
                "sentiment_counts": {"negative": 1, "neutral": 1, "positive": 2},
                "top_5_topics": {"politics": 1, "sports": 2, "technology": 1},
                "topic_counts": {"politics": 1, "sports": 2, "technology": 1},
            },
        )

    def test_compute_metrics_multiple_topics(self):
        data = pd.DataFrame(
            {
                "sentiment": ["positive", "negative", "neutral", "positive"],
                "related_topics": [
                    "sports, politics",
                    "politics",
                    "technology",
                    "sports, technology",
                ],
            }
        )

        result = self.report_handler.compute_metrics(data)
        self.assertEqual(
            result,
            {
                "most_freq_sentiment_per_topic": {
                    "politics": "positive",
                    "sports": "positive",
                    "technology": "neutral",
                },
                "most_freq_topic_per_sentiment": {
                    "negative": "politics",
                    "neutral": "technology",
                    "positive": "sports",
                },
                "sentiment_counts": {"negative": 1, "neutral": 1, "positive": 2},
                "top_5_topics": {"politics": 2, "sports": 2, "technology": 2},
                "topic_counts": {"politics": 2, "sports": 2, "technology": 2},
            },
        )

    def test_compute_metrics_with_empty(self):
        empty_data = pd.DataFrame(
            {
                "sentiment": ["positive", "negative", "neutral", "positive"],
                "related_topics": ["", "", "", "sports, technology"],
            }
        )

        result = self.report_handler.compute_metrics(empty_data)

        self.assertEqual(
            result,
            {
                "most_freq_sentiment_per_topic": {
                    "": "positive",
                    "sports": "positive",
                    "technology": "positive",
                },
                "most_freq_topic_per_sentiment": {
                    "negative": "",
                    "neutral": "",
                    "positive": "",
                },
                "sentiment_counts": {"negative": 1, "neutral": 1, "positive": 2},
                "top_5_topics": {"": 3, "sports": 1, "technology": 1},
                "topic_counts": {"": 3, "sports": 1, "technology": 1},
            },
        )

    def test_compute_metrics_empty(self):
        empty_data = pd.DataFrame(
            {
                "sentiment": ["positive", "negative", "neutral", "positive"],
                "related_topics": ["", "", "", ""],
            }
        )

        result = self.report_handler.compute_metrics(empty_data)

        self.assertEqual(
            result,
            {
                "sentiment_counts": {"positive": 2, "negative": 1, "neutral": 1},
                "topic_counts": {"": 4},
                "most_freq_sentiment_per_topic": {"": "positive"},
                "most_freq_topic_per_sentiment": {
                    "negative": "",
                    "neutral": "",
                    "positive": "",
                },
                "top_5_topics": {"": 4},
            },
        )

    def test_generate_report_with_cache(self):
        mock_redis_manager = Mock()
        mock_data_manager = Mock()
        mock_model_provider = Mock()

        report_handler = LidaReportHandler(
            data_manager=mock_data_manager,
            model_provider=mock_model_provider,
            redis_manager=mock_redis_manager,
        )

        dummy_df = pd.DataFrame(
            {
                "sentiment": ["positive", "negative"],
                "related_topics": ["food", "service"],
            }
        )

        mock_redis_manager.get_dataframe.return_value = dummy_df
        report_handler.summarize = Mock(return_value="dummy summary")
        report_handler.goal = Mock(
            return_value=[Goal(question="q1", visualization="v1", rationale="r1")]
        )
        report_handler.visualize = Mock(
            return_value=[
                FakeChartExecutorResponse(Mock(), Mock(), "raster", Mock(), Mock())
            ]
        )
        report_handler.refine_chart = Mock(return_value="refined raster")
        report_handler.compute_metrics = Mock(return_value={"metric": 1})

        result = report_handler.generate_report("123", Mock(), Mock())

        mock_redis_manager.get_dataframe.assert_called_once()
        report_handler.summarize.assert_called_once()
        report_handler.goal.assert_called_once()
        report_handler.visualize.assert_called_once()
        report_handler.compute_metrics.assert_called_once()

        self.assertEqual(result.goals[0], "Goal 1: q1")
        self.assertEqual(result.chart_rasters[0], "raster")
        self.assertEqual(result.metrics, {"metric": 1})

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
        self.report_handler.compute_metrics = Mock(return_value={})

        result = self.report_handler.generate_report(Mock(), Mock(), Mock())

        self.assertEqual(len(result.goals), 1)
        self.assertEqual(len(result.chart_rasters), 1)
        self.assertEqual(result.goals[0], "Goal 1: q1")
        self.assertEqual(result.chart_rasters[0], "raster")
        self.assertEqual(result.metrics, {})
