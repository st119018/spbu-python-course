"""This module provides access to vector operations

Classes
-------
Vector
"""

from math import acos
from typing import List, Union


class Vector:
    """Class implements operations with vectors.

    Attributes
    ----------
    coord : list
        Coordinates of vector

    Methods
    -------
    length()
        Calculate length of vector
    dim()
        Calculate dimension of vector
    scalar_product(vect)
        Calculate scalar product of vectors
    angle(vect)
        Calculate angle between vectors
    """

    def __init__(self, args: List[Union[int, float]]):
        """Set attribute for object.

        Parameters
        ----------
        args : List[Union[int, float]]
            List of coordinates of vector

        Raises
        ------
        IndexError
            If given list is empty
        TypeError
            If not numbers are in the given list
        """
        if len(args) == 0:
            raise IndexError("Vector has no coordinates")
        if not (all([isinstance(item, (int, float)) for item in args])):
            raise TypeError("Vector doesn't consist of numbers")
        self.coord = args

    def length(self) -> float:
        """Return length of vector."""
        l = 0
        for x in self.coord:
            l += x**2
        return l**0.5

    def dim(self):
        """Return dimension of vector."""
        return len(self.coord)

    def scalar_product(self, vect: "Vector"):
        """Return scalar product of vectors.

        Parameters
        ----------
        vect : Vector

        Raises
        ------
        TypeError
            If type of parameter isn't Vector
        IndexError
            If vectors have different dimensions
        """
        if type(vect) != Vector:
            raise TypeError(f"Incorrect type: {type(vect)}, " "expected: Vector.")
        if self.dim() == vect.dim():
            sum = 0
            for i in range(self.dim()):
                sum += self.coord[i] * vect.coord[i]
            return sum
        else:
            raise IndexError("Different dimensions of vectors")

    def angle(self, vect: "Vector") -> float:
        """Return angle between vectors in radians.
        The result is between 0 and pi.

        Parameters
        ----------
        vect : Vector

        Raises
        ------
        TypeError
            If type of given vect isn't Vector
        ZeroDivisionError
            If length one of vectors is zero
        """
        if type(vect) != Vector:
            raise TypeError(f"Incorrect type: {type(vect)}, " "expected: Vector.")
        if self.length() * vect.length() == 0.0:
            raise ZeroDivisionError("Division by zero")
        cos = self.scalar_product(vect) / (self.length() * vect.length())
        return acos(cos)
