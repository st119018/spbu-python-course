"""This module provides decorator that caches results of
function execution.

Functions
---------
cache_results(cache_size)"""

from functools import wraps
from typing import Callable
from collections import OrderedDict


def cache_results(cache_size: int = 0):
    """Decorator for caching function results.
    Keep finite number of last input arguments and corresponding results.

    Parameters
    ----------
    cache_size : int
        Number of last results to keep.

    Returns
    -------
    Function
    """

    def decorator(func: Callable):
        cache = OrderedDict()

        @wraps(func)
        def caching(*args, **kwargs):
            key = (tuple(args), hash(tuple(sorted(kwargs.items()))))
            if key in cache:
                cache.move_to_end(key)
                return cache[key]

            result = func(*args, **kwargs)
            if cache_size > 0:
                if len(cache) >= cache_size:
                    oldest_key = next(iter(cache))
                    del cache[oldest_key]
                cache[key] = result
            return result

        return caching

    return decorator
