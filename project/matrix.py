"""This module provides access to matrix operations

Classes
-------
Matrix

Functions
---------
is_matrix(args)
"""

from typing import List


class Matrix:
    """Class implements operations with matrices

    Attributes
    ----------
    elements : List[List[float]]
        List of lists; elements of matrix

    Methods
    -------
    __add__(matrix)
        Operator for matrices adding
    __mul__(matrix)
        Operator for matrices multiplying
    transpos()
        Transpose matrix
    """

    def __init__(self, args: List[List[float]]):
        """Set attributes for object

        Parameters
        ----------
        args : List[List[float]]
            List of lists representing elements of matrix.
            Example of input: [[1, 2], [3, 4]].

        Raises
        ------
        ValueError
            If input is empty
        TypeError
            If type of input is not list of lists
        ValueError
            If lists in input are not same length
        TypeError
            If non-numbers are in matrix
        """
        is_matrix(args)
        self.elements = args

    def __add__(self, matrix: "Matrix"):
        """Add matricies and return new matrix

        Parameters
        ----------
        matrix : Matrix

        Raises
        ------
        TypeError
            If type of parameter isn't Matrix
        IndexError
            If matrices aren't same size
        """
        if type(matrix) != Matrix:
            raise TypeError(f"Incorrect type: {type(matrix)}, " "expected: Matrix.")
        rows = len(self.elements)
        col = len(self.elements[0])
        if rows != len(matrix.elements) or col != len(matrix.elements[0]):
            raise IndexError("Different size of matrices")
        new_elements = []
        for i in range(rows):
            new_row = []
            for j in range(col):
                new_row.append(self.elements[i][j] + matrix.elements[i][j])
            new_elements.append(new_row)
        return Matrix(new_elements)

    def __mul__(self, matrix: "Matrix"):
        """Multiply matrices and return new matrix

        Parameters
        ----------
        matrix : Matrix

        Raises
        ------
        TypeError
            If type of parameter isn't Matrix
        IndexError
            If matrices aren't appropriate size
        """
        if type(matrix) != Matrix:
            raise TypeError(f"Incorrect type: {type(matrix)}, " "expected: Matrix.")
        rows = len(self.elements)
        col = len(self.elements[0])
        if col != len(matrix.elements):
            raise IndexError("Matrices can't be multiplied")
        new_elements = []
        for i in range(rows):
            new_row = [0.0] * len(matrix.elements[0])
            for j in range(len(matrix.elements[0])):
                for k in range(col):
                    new_row[j] += self.elements[i][k] * matrix.elements[k][j]
            new_elements.append(new_row)
        return Matrix(new_elements)

    def transpos(self):
        """Return transposed matrix"""
        new_el = []
        for j in range(len(self.elements[0])):
            new_row = []
            for i in range(len(self.elements)):
                new_row.append(self.elements[i][j])
            new_el.append(new_row)
        return Matrix(new_el)


def is_matrix(args: List[List[float]]):
    """Check if input has form of matrix.

    Parameters
    ----------
    args : List[List[float]]
        List of lists representing elements of matrix.
        Example of input: [[1, 2], [3, 4]].

    Raises
    ------
    ValueError
        If input list is empty
    TypeError
        If type of input is not list of lists
    ValueError
        If empty list in input
    ValueError
        If lists in input are not same length
    TypeError
        If non-numbers are in matrix
    """
    if len(args) == 0:
        raise ValueError("Matrix is empty")
    if not (all(isinstance(row, list) for row in args)):
        raise TypeError("Matrix should be list of lists")
    if not (all(len(row) != 0 for row in args)):
        raise ValueError("Empty row in matrix")
    if not (all(len(args[0]) == len(l) for l in args)):
        raise ValueError("Matrix has rows with different length")
    for row in args:
        if not (all(isinstance(el, (int, float)) for el in row)):
            raise TypeError("Matrix doesn't consist of numbers")
