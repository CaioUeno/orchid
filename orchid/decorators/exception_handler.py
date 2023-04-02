from typing import Any, Callable, Dict, List


def exception_handler(
    exception: Exception,
    callback: Callable,
    callback_args: List[Any] = [],
    callback_kwargs: Dict[str, Any] = {},
    intercept_exception: bool = False,
    exception_return: Any = None,
) -> Callable:
    """
    Decorator to handle an exception. When the exception is raised, a callback function is called.
    Positional and keyword arguments can be passed. Also, it is possible to intercept the error itself
    to the callback function as the `first` positional argument. It defines a value to be returned
    in case of the exception is raised.

    Parameters
    ----------
        exception : Exception
            The exception the handle if raised;
        callback : Callable

        callback_args : List[Any]
            List of positional arguments to pass to the callback function;
        callback_kwargs : Dict[str, Any]
            Dictionary mapping keyword arguments to pass to the callback function;
        intercept_exception : bool
            Whether to pass exception as the first positional param to the callback;
        exception_return : Any
            Value to return in case of an exception.
    """

    def wrapper(func: Callable[..., Any]) -> Callable:
        def inner(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if e.__class__ != exception:
                    raise e

                if intercept_exception:
                    positional_args = [e] + callback_args
                else:
                    positional_args = callback_args

                # execute function
                callback(*positional_args, **callback_kwargs)

                return exception_return

        return inner

    return wrapper
