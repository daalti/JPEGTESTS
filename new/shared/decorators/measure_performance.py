from typing import Callable
from functools import wraps
import time

def measure_performance(operation_name: str):
    """Decorator to measure and log operation performance."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            self._logger.debug(f"Starting {operation_name}")
            try:
                result = func(self, *args, **kwargs)
                elapsed = time.time() - start_time
                self._logger.info(f"{operation_name} completed in {elapsed:.2f}s")
                self._performance_metrics[operation_name] = elapsed
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                self._logger.error(f"{operation_name} failed after {elapsed:.2f}s: {e}")
                raise
        return wrapper
    return decorator
