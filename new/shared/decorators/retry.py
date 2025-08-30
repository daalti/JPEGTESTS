import functools
import time
from selenium.common.exceptions import WebDriverException # type: ignore[import]

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except WebDriverException as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
                    print(f"Intento {attempt + 1} falló, reintentando...")
            return None
        return wrapper
    return decorator