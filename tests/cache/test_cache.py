from time import sleep, time
from typing import List

from orchid.decorators import cache


class TestCache:
    function_time = 3
    tol = 0.005

    def test_no_max_size(self):
        # define a dummy function and decorate it
        @cache(max_size=None)
        def dummy(param: int):
            sleep(self.function_time)
            return param

        # call function once
        dummy(1)

        # call it again and check time spent
        start = time()
        dummy(1)
        elapsed = time() - start

        assert elapsed <= self.tol

    def test_full_cache(self):
        # define a dummy function and decorate it
        @cache(max_size=3)
        def dummy(param: int):
            sleep(self.function_time)
            return param

        # fill cache
        dummy(-1)
        dummy(3)
        dummy(4)

        # call it again (new param value) and check time spent
        start = time()
        dummy(0)
        elapsed = time() - start

        assert abs(elapsed - self.function_time) <= self.tol

    def test_no_hashable_params(self):
        # define a dummy function and decorate it
        @cache(max_size=None)
        def dummy(param: List[int]):
            sleep(self.function_time)
            return param

        # call function once
        dummy([1, 2, 3])

        # call it again and check time spent
        start = time()
        dummy([1, 2, 3])
        elapsed = time() - start

        assert abs(elapsed - self.function_time) <= self.tol
