import unittest

from src.control.pipeline_result import PipelineResult
from src.data.data_result import DataResult


class TestPipelineResult(unittest.TestCase):
    def test_append(self):
        pipeline_result = PipelineResult({"topic1, topic2"})

        pipeline_result.append(DataResult(True, ("topic1",)))
        pipeline_result.append(DataResult(False, ("topic2",)))

        self.assertEqual(pipeline_result.items[0], DataResult(True, ("topic1",)))
        self.assertEqual(len(pipeline_result.items), 2)

    def test_extend_same_topics(self):
        pipeline_result1 = PipelineResult({"topic1, topic2"})

        pipeline_result2 = PipelineResult({"topic1, topic2"})

        pipeline_result1.append(DataResult(True, ("topic1",)))
        pipeline_result2.append(DataResult(False, ("topic2",)))
        pipeline_result1.extend(pipeline_result2)

        self.assertEqual(pipeline_result1.items[1], DataResult(False, ("topic2",)))
        self.assertEqual(len(pipeline_result1.items), 2)
        self.assertEqual(len(pipeline_result2.items), 1)

    def text_extend_different_topics(self):
        pipeline_result1 = PipelineResult({"topic1, topic2"})

        pipeline_result2 = PipelineResult({"topic1, topic2, topic3"})

        pipeline_result1.append(DataResult(True, ("topic2",)))
        pipeline_result2.append(DataResult(False, ("topic3",)))

        with self.assertRaises(ValueError):
            pipeline_result1.extend(pipeline_result2)
