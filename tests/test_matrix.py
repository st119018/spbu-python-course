"""This module provides test for matrix operations"""

import pytest
from project.matrix import Matrix


def test_init():
    m = Matrix([[-1.1, 8, 4.8], [0, 0, 0]])
    assert m.elements == [[-1.1, 8, 4.8], [0, 0, 0]]


def test_init_empty_matrix():
    with pytest.raises(ValueError):
        Matrix([])


def test_init_empty_row():
    with pytest.raises(ValueError):
        Matrix([[], [4], [5]])
    with pytest.raises(ValueError):
        Matrix([[]])


def test_init_wrong_input_type():
    with pytest.raises(TypeError):
        Matrix([[1], 1, [6]])
    with pytest.raises(TypeError):
        Matrix([1])


def test_init_diff_row_legnth():
    with pytest.raises(ValueError):
        Matrix([[1, 2], [1, 2, 3]])


def test_init_non_numbers_in_row():
    with pytest.raises(TypeError):
        Matrix([[1, 2, "3"], [1, 2, 3]])
    with pytest.raises(TypeError):
        Matrix([["3"]])


def test_add():
    m1 = Matrix([[1, -1], [1, 0]])
    m2 = Matrix([[1, 1], [1, 0]])
    m3 = m1 + m2
    assert m3.elements == [[2, 0], [2, 0]]


def test_add_small():
    m1 = Matrix([[1]])
    m2 = Matrix([[2]])
    m3 = m1 + m2
    assert m3.elements == [[3]]


def test_add_not_matrix():
    m = Matrix([[1], [1]])
    with pytest.raises(TypeError):
        m + 7
    with pytest.raises(TypeError):
        m + "123"


def test_add_diff_size():
    m1 = Matrix([[1, 2, 3], [1, 2, 3]])
    m2 = Matrix([[1, 2], [1, 2]])
    with pytest.raises(IndexError):
        m1 + m2


def test_mul():
    m1 = Matrix([[1, 1]])
    m2 = Matrix([[1, 1], [1, 0]])
    m3 = m1 * m2
    assert m3.elements == [[2, 1]]


def test_mul_small():
    m1 = Matrix([[3]])
    m2 = Matrix([[-4]])
    m3 = m1 * m2
    assert m3.elements == [[-12]]


def test_mul_zero():
    m1 = Matrix([[0, 0]])
    m2 = Matrix([[4, 9], [56, 46]])
    m3 = m1 * m2
    assert m3.elements == [[0, 0]]


def test_mul_not_matrix():
    m = Matrix([[5, 3]])
    with pytest.raises(TypeError):
        m * 6
    with pytest.raises(TypeError):
        m * "5"


def test_mul_wrong_size():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2]])
    with pytest.raises(IndexError):
        m1 * m2


def test_transpos():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6, 7]])
    assert m1.transpos().elements == [[1, 3], [2, 4]]
    assert m2.transpos().elements == [[5], [6], [7]]


def test_transpos_small():
    m = Matrix([[3]])
    assert m.transpos().elements == [[3]]
