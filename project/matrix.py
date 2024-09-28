"""This module provides access to matrix operations

Classes
-------
Matrix
"""


class Matrix:
    """Class implements operations with matrices

    Attributes
    ----------
    elements : list
        List of elements of matrix
    rows : int
        Number of rows in matrix
    columns : int
        Number of columns in matrix

    Methods
    -------
    __is_num(args)
        Check if matrix consists of numbers
    __add__(matrix)
        Operator for matrices adding
    __mul__(matrix)
        Operator for matrices multiplying
    transpos()
        Transpose matrix
    """

    def __init__(self, rows: int, columns: int, args: list):
        """Set attributes for object

        Parameters
        ----------
        rows : int
            Number of rows in matrix
        columns : int
            Number of columns in matrix
        elements : list
            List of elements of matrix

        Raises
        ------
        ValueError
            If rows or columns aren't positive
        IndexError
            If size of elements is less than size of matrix or zero
        """
        if rows < 1 or columns < 1:
            raise ValueError("Rows and columns of matrix have to be positive")
        if len(args) == 0:
            raise IndexError("Matrix has no elements")
        if rows * columns != len(args):
            raise IndexError(
                f"Expected {rows * columns} arguments" f" but recieved: {len(args)}"
            )
        self.__is_num(args)
        self.columns = columns
        self.rows = rows
        self.elements = args

    def __is_num(self, args):
        """Check if given list consists of numbers

        Parameters
        ----------
        args : list

        Raises
        ------
        TypeError
            If not numbers are in matrix
        """
        try:
            sum = 0
            for i in range(len(args)):
                sum += args[i]
        except TypeError:
            print("Type error: matrix doesn't consist of numbers")

    def __add__(self, matrix):
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
        if self.rows != matrix.rows and self.columns != matrix.columns:
            raise IndexError("Different size of matrices")
        new_elements = [0] * len(self.elements)
        for i in range(len(self.elements)):
            new_elements.append(self.elements[i] + matrix.elements[i])
        return Matrix(self.rows, self.columns, new_elements)

    def __mul__(self, matrix):
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
        if self.columns != matrix.rows:
            raise IndexError("Matrices can't be multiplied")
        new_elements = [0] * (self.rows * matrix.columns)
        for i in range(self.rows):
            for j in range(matrix.columns):
                for k in range(self.columns):
                    new_elements[i * matrix.columns + j] += (
                        self.elements[i * self.columns + k]
                        * matrix.elements[k * matrix.columns + j]
                    )
        return Matrix(self.rows, matrix.columns, new_elements)

    def transpos(self):
        """Return transposed matrix"""
        el = [0] * (self.rows * self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                el[j * self.rows + i] = self.elements[i * self.columns + j]
        return Matrix(self.columns, self.rows, el)
