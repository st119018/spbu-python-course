"""This module provides test for matrix operations"""

import pytest
from project.matrix import Matrix


def test_add():
    m1 = Matrix(2, 2, [1, -1, 1, 0])
    m2 = Matrix(2, 2, [1.1, 1, 1, 0])
    m3 = Matrix(1, 2, [1, 1])
    m4 = m1 + m2
    assert m4.elements == [2.1, 0, 2, 0]
    with pytest.raises(TypeError):
        m1 + 7
    with pytest.raises(IndexError):
        m1 + m3


def test_mul():
    m1 = Matrix(1, 2, [1, 1])
    m2 = Matrix(2, 2, [1, 1, 1, 0])
    assert (m1 * m2).elements == [2, 1]
    with pytest.raises(TypeError):
        m1 * 6
    with pytest.raises(IndexError):
        m2 * m1


def test_transpos():
    m = Matrix(2, 2, [1, 2, 3, 4])
    assert m.transpos().elements == [1, 3, 2, 4]
