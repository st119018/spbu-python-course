"""This module provides test for vector operations"""

import pytest
from project.vector import Vector


def test_length():
    v1 = Vector([3, 4])
    v2 = Vector([0, 0])
    v3 = Vector([1, -1, -1, 1])
    assert v1.length() == 5
    assert v2.length() == 0
    assert v3.length() == 2


def test_scalar_product():
    v1 = Vector([3, 4])
    v2 = Vector([0, 0])
    v3 = Vector([1, -1, -1])
    v4 = Vector([0.5, 1, 0])
    assert v1.scalar_product(v2) == 0
    assert v3.scalar_product(v4) == -0.5
    with pytest.raises(IndexError):
        v1.scalar_product(v2)
    with pytest.raises(TypeError):
        v1.scalar_product(3)


def test_angle():
    v1 = Vector([3, 4])
    v2 = Vector([0, 0])
    v3 = Vector([2, 5])
    v4 = Vector([3, 0])
    assert v3.angle(v4) == pytest.approx(1.2, 0.1)
    with pytest.raises(ZeroDivisionError):
        v1.angle(v2)
    with pytest.raises(TypeError):
        v1.scalar_product(4.5)
