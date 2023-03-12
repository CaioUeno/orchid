from typing import Any, Callable, Dict, List, Tuple, Union


def exception_handler(
    handlers: List[
        Dict[
            Exception,
            Tuple[Callable, Union[List[Any], None], Union[Dict[str, Any], None]],
        ]
    ],
    exception_return: Any = None,
) -> Callable:
    """
    Decorator to handle exceptions. When a known exception is raised, a list of functions is called.
    Undefined exceptions (that are not present in the `handlers` parameter) are raised normally.

    Parameters
    ----------
        handlers (List[Dict]): It maps exceptions to a list of functions along with their positional and keyword arguments;
        exception_return (Any) : value to return in case of an exception.
    """

    def wrapper(func: Callable[..., Any]) -> Callable:
        def inner(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if e.__class__ not in set(handlers.keys()):
                    raise e

                # iterate over functions to call
                for f, exc_args, exc_kwargs in handlers[e.__class__]:
                    # replace Nones by list/dict
                    exc_args = [] if exc_args is None else exc_args
                    exc_kwargs = {} if exc_kwargs is None else exc_kwargs

                    # execute function
                    f(*exc_args, **exc_kwargs)

                return exception_return

        return inner

    return wrapper


# HANDLERS = {
#     ValueError: [
#         (print, ["value error handled"], None),
#     ],
#     TypeError: [(print, ["type error detected B)"], None)],
# }


# @exception_handler(handlers=HANDLERS)
# def unknown_exception():
#     raise Exception("This exception class is *not* in handlers")


# @exception_handler(
#     handlers=HANDLERS,
#     exception_return="unsuccessful call :(",
# )
# def value_error_exception():
#     raise ValueError("Value not supported.")


# @exception_handler(
#     handlers=HANDLERS,
#     exception_return="unsuccessful call :(",
# )
# def type_error_exception():
#     raise TypeError("Type not supported.")


# print(value_error_exception())
# print(type_error_exception())
# print(unknown_exception())
