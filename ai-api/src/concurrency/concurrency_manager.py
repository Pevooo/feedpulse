import logging
import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable


class ConcurrencyManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    def submit_job(self, func: Callable, *args, **kwargs) -> Future:
        future = self.executor.submit(func, *args, **kwargs)
        future.add_done_callback(self.get_complete_callback(traceback.format_exc()))
        return future

    def get_complete_callback(self, tb: str):
        def _on_thread_done(future: Future):
            exception = future.exception()
            if exception:
                logging.error(
                    "Concurrent Task Error: Call Traceback: %s Thread Traceback: %s",
                    tb,
                    traceback.format_exc(),
                )
            else:
                # Logs the result of the task
                logging.info("Concurrent Task Result: %s", future.result())

        return _on_thread_done
