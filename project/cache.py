"""This module provides decorator that caches results of
function execution.

Functions
---------
get_hash(arg)

cache_results(cache_size)"""

from functools import wraps
from typing import Callable, Any
from collections import OrderedDict
import hashlib
import json


def get_hash(arg: Any) -> str:
    """Return hash value of arg."""
    json_str = json.dumps(arg, sort_keys=True, ensure_ascii=False).encode("utf8")
    return hashlib.sha256(json_str).hexdigest()


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
        cache: OrderedDict[str, str] = OrderedDict()

        @wraps(func)
        def caching(*args, **kwargs):
            key = get_hash(args), get_hash(kwargs)
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
