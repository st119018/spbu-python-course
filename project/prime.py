"""This module provides functions for calculating prime numbers.

Functions
---------
prime_generator()

get_prime(func)
"""

from typing import Callable


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

    Raises
    ------
    ValueError
        If k isn't positive

    Returns
    -------
    Function
    """

    def wrapper(k: int = 1):
        if k <= 0:
            raise ValueError("Inappropriate value.")

        gen = prime_generator()
        for _ in range(k - 1):
            next(gen)
        prime = next(gen)
        return prime

    return wrapper
