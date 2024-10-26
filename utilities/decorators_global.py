from typing import Callable
from datetime import datetime


def execution_time_decorator(in_seconds: bool = False,
                             note: str = None,
                             exec_time_logging: bool = False) -> Callable:

    def decorator(func: Callable):
        if not exec_time_logging:
            return func

        def wrapper(*args, **kwargs):
            start_time_point = datetime.now()
            result = func(*args, **kwargs)
            finish_time_point = datetime.now()

            time_delta = (finish_time_point - start_time_point).total_seconds()

            if in_seconds:
                time_delta = round(time_delta, 3)
                units = "seconds"
            else:
                time_delta = int(time_delta * 1e6)
                units = "microseconds"

            note_text = f"[{note}]" if note else None
            text = ("#" * 20 + f"  EXECUTION TIME {note_text}: "
                               f"{time_delta} {units}  " + "#" * 20)

            print(f"\n{'#' * len(text)}\n"
                  f"{text}\n"
                  f"{'#' * len(text)}\n")

            return result
        return wrapper
    return decorator
