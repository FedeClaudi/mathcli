from pathlib import Path
import os
from loguru import logger

cache_dir = Path(os.path.join(os.path.expanduser("~"), ".mathcli"))
cache_dir.mkdir(exist_ok=True)

logger.debug(f"Cache directory: {cache_dir}")


def to_cache(result):
    with open(cache_dir / "last.txt", "w") as out:
        out.write(result)
        logger.debug(f"CACHED RESULT {result}")


def load_last():
    with open(cache_dir / "last.txt", "r") as f:
        last = f.read()
        logger.debug(f"LOADED CACHED RESULT {last}")
    return last


def cache_expression(func):
    """
        Decorator for functions that accept an expression
        string as argument and return a string or number as result.
        The decorator handles:
            - if the expression string is 'last' it loads the last cached expression
            - if the inner functin's output is an expression, it caches it
    """

    def cache(*args, **kwargs):
        # check if loading from cache
        args = list(args)
        if args[0] == "last":
            args[0] = load_last()

        # carry out the function
        result = func(*args, **kwargs)

        # cache result
        if isinstance(result, str):
            to_cache(result)

        return result

    return cache
