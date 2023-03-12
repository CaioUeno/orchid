from time import sleep
from typing import Any, Callable, Dict, Hashable, Iterable


def cache(max_size: int) -> Callable:
    """ """

    def check_params(args: Iterable[Any], kwargs: Dict[str, Any]) -> bool:
        for arg in args:
            if not isinstance(arg, Hashable):
                return True

        for item in kwargs.items():
            if not isinstance(item, Hashable):
                return True

        return False

    def hash_params(args: Iterable[Hashable], kwargs: Dict[str, Hashable]) -> bool:
        keys = list(args)
        keys.extend([item for item in kwargs.items()])

        for _, value in kwargs:
            keys.append(value)

        return hash(tuple(keys))

    def wrapper(func: Callable[..., Any]) -> Callable:
        _cache = {}

        def inner(*args, **kwargs) -> Any:
            has_unhashable = check_params(args, kwargs)

            if has_unhashable:
                return func(*args, **kwargs)

            else:
                key = hash_params(args, kwargs)

                if key not in _cache:
                    if len(_cache) == max_size:
                        return func(*args, **kwargs)
                    else:
                        _cache[key] = func(*args, **kwargs)

                return _cache[key]

        return inner

    return wrapper


# @timer(level=None)
# @cache(max_size=1)
# def dummy_sleeper(seconds: int):
#     sleep(seconds)
#     return seconds


# dummy_sleeper(5)
# dummy_sleeper(5)
# dummy_sleeper(3)
# dummy_sleeper(3)
