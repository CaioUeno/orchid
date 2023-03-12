import logging
from time import sleep, time
from orchid import timer
from unittest.mock import Mock


class TestTimer:
    tol = 0.01

    def test_timer_simple(self):
        @timer(logger=None)
        def dummy_sleeper(seconds: int) -> None:
            sleep(seconds)

        seconds = 3
        start = time()
        _ = dummy_sleeper(seconds)
        elapsed = time() - start

        assert abs((elapsed / seconds) - 1) <= self.tol
