import unittest

from unittest.mock import Mock, MagicMock
from src.concurrency.concurrency_manager import ConcurrencyManager
from concurrent.futures import Future


class TestConcurrencyManager(unittest.TestCase):
    def setUp(self):
        mock = Mock()
        self.manager = ConcurrencyManager(mock)

    def test_submit_job_valid_params(self):
        def add(a, b):
            return a + b

        future = self.manager.submit_job(add, 2, 5)

        self.assertEqual(future.result(), 7)

    def test_submit_job_invalid_params(self):
        def add(a, b):
            return a + b

        with self.assertRaises(TypeError):
            self.manager.submit_job(add, 2).result()

    def test_submit_job_raise_exception(self):
        def raise_exc():
            raise Exception("I am an exception")

        with self.assertRaises(Exception):
            self.manager.submit_job(raise_exc).result()

    def test_on_thread_done_exception(self):
        mock_reporter = MagicMock()
        self.manager.exception_reporter = mock_reporter

        future = Future()
        future.set_exception(RuntimeError("Test Exception"))

        self.manager._on_thread_done(future)

        mock_reporter.report.assert_called_once()
        called_exception = mock_reporter.report.call_args[0][0]
        self.assertIsInstance(called_exception, RuntimeError)
        self.assertEqual(str(called_exception), "Test Exception")
