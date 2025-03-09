import unittest

from src.concurrency.concurrency_manager import ConcurrencyManager
from concurrent.futures import Future


class TestConcurrencyManager(unittest.TestCase):
    def setUp(self):
        self.manager = ConcurrencyManager()

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


unittest.main()
