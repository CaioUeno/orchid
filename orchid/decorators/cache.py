from typing import Any, Callable, Dict, Hashable, Iterable, Union


def cache(max_size: Union[int, None]) -> Callable:
    """
    Decorator to optimize a function call using cache.

    Parameters
    ----------
        max_size : int
            Maximum cache's size.
    """

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
                    if max_size is None or len(_cache) < max_size:
                        _cache[key] = func(*args, **kwargs)

                    else:
                        return func(*args, **kwargs)

                return _cache[key]

        return inner

    return wrapper
