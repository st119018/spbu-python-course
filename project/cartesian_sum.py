"""This module provides functions for calculating sum of Cartesian product of integer set

Functions
---------
product_sum(product)

cartesian_product_sum(num)
"""
import itertools
from typing import List
from concurrent.futures import ProcessPoolExecutor


def product_sum(product: List[int]) -> int:
    """Return sum of elements in product"""
    return sum(product)


def cartesian_product_sum(num: List[int]) -> int:
    """Return sum of Cartesian product of num

    Parameters
    ----------
    num : List[int]
        List of integers to compute Cartesian product

    Raises
    ------
    ValueError
        If num is empty
    """
    if len(num) == 0:
        raise ValueError("num is empty.")

    product = itertools.product(num, repeat=2)

    with ProcessPoolExecutor() as executor:
        partial_sum = list(executor.map(product_sum, product))

    return sum(partial_sum)
