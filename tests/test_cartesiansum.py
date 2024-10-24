import pytest
from project.cartesian_sum import cartesian_product_sum


@pytest.mark.parametrize(
    "num, total_sum", [([0], 0), ([1], 2), ([1, 1], 8), ([1, -1], 0), ([1, 1, 1], 18)]
)
def test_cartesian_product_sum(num, total_sum):
    assert cartesian_product_sum(num) == total_sum


def test_cartesian_product_sum_empty_input():
    with pytest.raises(ValueError):
        cartesian_product_sum([])
