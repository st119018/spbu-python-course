"""This module provides test for vector operations"""

import pytest
from project.vector import Vector


def test_init():
    v1 = Vector([4, 5.4, 8])
    v2 = Vector([1])
    assert v1.coord == [4, 5.4, 8]
    assert v2.coord == [1]


def test_init_empty_vector():
    with pytest.raises(IndexError):
        Vector([])


def test_init_wrong_input_type():
    with pytest.raises(TypeError):
        Vector([1, 2, "r"])


def test_length():
    v1 = Vector([3, 4])
    v2 = Vector([2, 1])
    assert v1.length() == 5
    assert v2.length() == pytest.approx(2.2, 0.1)


def test_zero_length():
    v = Vector([0, 0])
    assert v.length() == 0


def test_dim():
    v1 = Vector([3])
    v2 = Vector([7, 0, 0, 4, 5, 1])
    assert v1.dim() == 1
    assert v2.dim() == 6


def test_scalar_product():
    v1 = Vector([1, -1])
    v2 = Vector([0.5, 1])
    assert v1.scalar_product(v2) == -0.5


def test_scalar_product_zero():
    v1 = Vector([3, 4])
    v2 = Vector([0, 0])
    assert v1.scalar_product(v2) == 0


def test_scalar_product_wrong_input_type():
    v = Vector([8, 3.8, 6])
    with pytest.raises(TypeError):
        v.scalar_product(3)


def test_scalar_product_diff_size():
    v1 = Vector([8, 4])
    v2 = Vector([1, 2, 3, 4])
    with pytest.raises(IndexError):
        v1.scalar_product(v2)


def test_angle():
    v1 = Vector([2, 5])
    v2 = Vector([3, 0])
    assert v1.angle(v2) == pytest.approx(1.2, 0.1)
    with pytest.raises(TypeError):
        v1.scalar_product(4.5)


def test_angle_zero_length():
    v1 = Vector([7, 5, 8])
    v2 = Vector([0, 0, 0])
    with pytest.raises(ZeroDivisionError):
        v1.angle(v2)


def test_angle_wrong_input_type():
    v = Vector([1, 1, 1])
    with pytest.raises(TypeError):
        v.scalar_product(4.5)
