"""This module provides functions for calculating rgba vectors.

Functions
---------
rgba_generator()

get_rgba_vector(i)
"""


def rgba_generator():
    """Generator calculate rgba vector.
    r - red; g - green; b - blue; a - alpha.

    Values of r, g, b are between 0 and 255,
    value of a is even and is between 0 and 100.

    Returns
    -------
    Generator
    """
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(101)
        if a % 2 == 0
    )


def get_rgba_vector(i: int = 0):
    """Calculate i-th rgba vector.
    Counting starts with 0.

    Raises
    ------
    ValueError
        If i is negative or exceeds number of vectors.

    Returns
    -------
    Tuple of four integers
    """
    if i < 0 or i > 256 * 256 * 256 * 51:
        raise ValueError("Inappropriate value of i")
    gen = rgba_generator()
    for _ in range(i):
        next(gen)
    return next(gen)
