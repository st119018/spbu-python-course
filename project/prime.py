"""This module provides functions for calculating prime numbers.

Functions
---------
prime_generator()

get_prime(func)
"""

from typing import Callable
from functools import wraps


def prime_generator():
    """Generator of prime numbers.

    Returns
    -------
    Integer
    """
    n = 2
    while True:
        if all(n % i != 0 for i in range(2, int(n**0.5) + 1)):
            yield n
        n += 1


def get_prime(func: Callable):
    """Decorator returns function that calculate k-th prime number.
    Counting starts with 1.

    Parameters
    ----------
    func : Callable
        Generator of prime numbers

    Raises
    ------
    ValueError
        If k isn't positive

    Returns
    -------
    Function
    """
    gen = func()
    last = [0]

    @wraps(func)
    def wrapper(k: int = 1):
        """Returns k-th prime number in increasing sequence.
        Counting starts with 1.
        """
        if k <= 0 or k <= last[0]:
            raise ValueError("Inappropriate value.")

        k -= last[0]
        last[0] += k

        for _ in range(k - 1):
            next(gen)
        prime = next(gen)

        return prime

    return wrapper
