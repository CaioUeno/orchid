from time import sleep
from typing import Any, Callable, Iterable, List

from joblib import Parallel, delayed

from timer import timer


def parallelize(parallelism: int, prefer: str = "processes") -> Callable:
    """
    Parallelize a function using joblib package.
    The function must receive as first positional argument a iterable and then **only** keyword arguments.

    Parameters
    ----------
        parallelism (int) : how many parallel processes/threads to use;
        prefer (str) : argument for joblib Parallel class {`threads`, `processes`}.
    """

    def split(iterable: Iterable, n: int) -> List[Iterable]:
        size = int(len(iterable) / n)
        if len(iterable) % n != 0:
            size += 1

        return [iterable[i : i + size] for i in range(0, len(iterable), size)]

    def wrapper(func: Callable[..., List[Any]]) -> Callable:
        def inner(iterable: Iterable, **kwargs) -> Any:
            return Parallel(n_jobs=parallelism, prefer=prefer)(
                delayed(func)(batch, **kwargs)
                for batch in split(iterable=iterable, n=parallelism)
            )

        return inner

    return wrapper


@timer(logger=None)
@parallelize(parallelism=20)
def dummy_sleeper(items: List[float]) -> List[float]:
    return [sleep(item) for item in items]


dummy_sleeper([1 for _ in range(60)])
