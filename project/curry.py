"""This module provides decorator for currying and
uncurrying functions.

Functions
---------
curry_explicit(func, arity)
uncurry_explicit(func, arity)
"""

from functools import wraps
from typing import Callable


def curry_explicit(func: Callable, arity: int):
    """Decorator for currying given function.
    Do not support keword arguments.

    Parameters
    ----------
    func : Callable
        Function that currying will be applied to.
    arity : int
        Number of parameters of given function.

    Raises
    ------
    ValueError
        If arity is negative.
    TypeError
        If function takes 0 arguments but argument was given.

    Returns
    -------
    Function"""
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    args = []

    @wraps(func)
    def curry_func(arg=None):
        if arity == 0 and not (arg is None):
            raise TypeError("Arity is 0 but argument was given")
        if arity == 0:
            return func()
        args.append(arg)
        if len(args) == arity:
            return func(*args)
        return lambda next_arg: curry_func(next_arg)

    return curry_func


def uncurry_explicit(func: Callable, arity: int):
    """Decorator for uncurrying given function.
    Do not support keyword arguments.
    Inverse to curry_explicit decorator.

    Parameters
    ----------
    func : Callable
        Curried function that uncurrying will be applied to.
    arity : int
        Number of parameters of given function.

    Raises
    ------
    ValueError
        If arity is negative.
    TypeError
        If number of given arguments isn't equal to arity.

    Returns
    -------
    Function"""
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    @wraps(func)
    def uncurry_func(*args):
        if arity != len(args):
            raise TypeError("Inappropriate number of arguments")

        if arity == 0:
            return func()
        uncurried = func
        for arg in args:
            uncurried = uncurried(arg)

        return uncurried

    return uncurry_func
