import logging
from datetime import timedelta
from time import perf_counter
from typing import Any, Callable


def timer(logger: logging.Logger = None, level: str = "INFO") -> Callable:
    """
    Calculate function's run time.

    Parameters
    ----------
        logger (logging.Logger) : logger object to log the run time as a message;
        level (str) : logger level to use when logger parameter is given.
    """

    def wrapper(func: Callable[..., Any]) -> Callable:
        def inner(*args, **kwargs) -> Any:
            start = perf_counter()
            r = func(*args, **kwargs)
            end = perf_counter()
            run_time = end - start

            # remove microseconds
            message = str(timedelta(seconds=run_time)).split(".")[0]

            if logger is None:
                print(message)
            else:
                logger.log(getattr(logging, level), message)

            return r

        return inner

    return wrapper
