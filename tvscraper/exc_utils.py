import logging
from selenium.common.exceptions import WebDriverException
from .exceptions import RTXStonkException


def handle_sel_exc(f, fargs: list = list(), fkwargs: dict = dict(),
                   exceptions: tuple = (RTXStonkException, WebDriverException),
                   tries: int = 0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            _err = None
            for i in range(tries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    _err = err
                    logging.info(f"catch_sel_exc caught a " +
                                 f"{err.__class__.__name__}. Trying {i + 1} " +
                                 f"more times...")
                    f(*fargs, **fkwargs)
                else:
                    logging.info(f"Function {func.__name__} proceeded error-free")
                    break
            if _err is not None:
                raise _err
        return wrapper
    return decorator
