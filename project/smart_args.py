"""This module provides decorator that depending on arguments of passed
function copies/calculates them.

Classes
-------
Evaluated

Isolated

Functions
---------
smart_args(func)
"""

from typing import Callable
from functools import wraps
import inspect
import copy


class Evaluated:
    """Class-flag for evaluating.
    If it is passed as default value of parameter then after applying smart_args
    decorator given function is evaluated every time.

    Attributes
    ----------
    func : Callable
        Function with no arguments. Returns some value.
    """

    def __init__(self, func: Callable):
        if not callable(func) or inspect.signature(func).parameters:
            raise ValueError("Evaluated requires a function with no arguments")
        self.func = func


class Isolated:
    """Fictitious class-flag."""

    pass


def smart_args(func: Callable):
    """Decorator for analyzing default values of function keyword arguments.
    Copy and/or calculate default values before executing function.

    Evaluated(func_without_args) - calculate default value before
    execution of function. func_without_args takes no argument and
    returns some value.

    Isolated - fictitious value; argument must be passed but it is
    copied (deep copy).

    Parameters
    ----------
    func : Callable
        Function which arguments will be copied/calculated.

    Raises
    ------
    AssertionError
        If Evaluated or Isolated is passed as arguments.
    ValueError
        If Isolated is passed as argument to Evaluated.
        If default value is Isolated but argument wasn't passed.

    Returns
    -------
    Function
    """
    signature = inspect.signature(func)
    params = signature.parameters

    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if Evaluated or Isolated is passed as argument
        assert all(not isinstance(arg, (Evaluated, Isolated)) for arg in args)
        assert all(not isinstance(kwargs[key], (Evaluated, Isolated)) for key in kwargs)

        new_kwargs = {}
        for name, param in params.items():
            if name in kwargs and not isinstance(param.default, Isolated):
                new_kwargs[name] = kwargs[name]

            else:
                if isinstance(param.default, Evaluated):
                    d_value = param.default.func
                    if isinstance(d_value, Isolated):
                        raise ValueError(
                            "Isolated was passed as argument to Evaluated."
                        )
                    new_kwargs[name] = d_value()
                if isinstance(param.default, Isolated):
                    if name in kwargs:
                        new_kwargs[name] = copy.deepcopy(kwargs[name])
                    else:
                        raise ValueError(f"Argument '{name}' must be provided")
        return func(*args, **new_kwargs)

    return wrapper
