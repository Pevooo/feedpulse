import unittest
from unittest.mock import Mock

from src.data_streamers.polling_data_streamer import PollingDataStreamer


class TestPollingDataStreamer(unittest.TestCase):
    def setUp(self):
        self.mock_concurrency_manager = Mock()
        self.mock_data_manager = Mock()
        self.streamer = PollingDataStreamer(self.mock_data_manager, Mock(), self.mock_concurrency_manager)

    def test_start_streaming(self):
        self.mock_concurrency_manager.submit_job = Mock()
        self.streamer.start_streaming()
        self.mock_concurrency_manager.submit_job.assert_called_once_with(self.streamer.streaming_worker)
