from time import sleep, time
from typing import List

from orchid.decorators import parallelize


class TestParallelize:
    function_time = 3
    tol = 0.5

    def test_two_parallel_processes(self):
        @parallelize(parallelism=2, prefer="processes")
        def dummy_sleeper(items: List[float]) -> List[float]:
            return [sleep(item) for item in items]

        start = time()
        dummy_sleeper([1, 1, 1, 1, 1, 1])
        elapsed = time() - start

        assert abs(elapsed - 3) <= self.tol

    def test_one_per_item(self):
        @parallelize(parallelism=6, prefer="processes")
        def dummy_sleeper(items: List[float]) -> List[float]:
            return [sleep(item) for item in items]

        start = time()
        dummy_sleeper([1, 1, 1, 1, 1, 1])
        elapsed = time() - start

        assert abs(elapsed - 1) <= self.tol

    def test_one_thread(self):
        @parallelize(parallelism=1, prefer="threads")
        def dummy_sleeper(items: List[float]) -> List[float]:
            return [sleep(item) for item in items]

        start = time()
        dummy_sleeper([1, 1, 1, 1, 1, 1])
        elapsed = time() - start

        assert abs(elapsed - 6) <= self.tol
