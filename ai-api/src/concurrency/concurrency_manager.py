import logging
import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable


class ConcurrencyManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    def submit_job(self, func: Callable, *args, **kwargs) -> Future:
        future = self.executor.submit(func, *args, **kwargs)
        future.add_done_callback(self._on_thread_done)
        return future

    def _on_thread_done(self, future: Future):
        exception = future.exception()
        if exception:
            logging.error("Concurrent Task Error: %s", exception)
            logging.error(traceback.format_exc())
        else:
            logging.info("Concurrent Task Result: %s", future.result())
