"""This module provides access to vector operations

Classes
-------
Vector
"""

from math import acos


class Vector:
    """Class implements operations with vectors.

    Attributes
    ----------
    coord : list
        Coordinates of vector

    Methods
    -------
    __is_num(args)
        Check if vector has coordinates and they are numbers
    length()
        Calculate length of vector
    dim()
        Calculate dimension of vector
    scalar_product(vect)
        Calculate scalar product of vectors
    angle(vect)
        Calculate angle between vectors
    """

    def __init__(self, args: list):
        """Set attribute for object.

        Parameters
        ----------
        args : list
            List of coordinates of vector
        """
        self.__is_num(args)
        self.coord = args

    def __is_num(self, args: list):
        """Check if given list isn't empty and consists of numbers.

        Parameters
        ----------
        args : list

        Raises
        ------
        IndexError
            If not numbers are in the given list or
            given list is empty
        """
        if len(args) == 0:
            raise IndexError("Vector has no coordinates")
        try:
            sum = 0
            for i in range(len(args)):
                sum += args[i]
        except IndexError:
            print("Index error: vector doesn't consist of numbers")

    def length(self) -> float:
        """Return length of vector."""
        l = 0
        for x in self.coord:
            l += x**2
        return l**0.5

    def dim(self):
        """Return dimension of vector."""
        return len(self.coord)

    def scalar_product(self, vect):
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

    def angle(self, vect) -> float:
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
        try:
            cos = self.scalar_product(vect) / (self.length() * vect.length())
        except ZeroDivisionError:
            print("Division error: division by zero")
        return acos(cos)
