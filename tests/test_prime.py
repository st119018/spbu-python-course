import pytest
from project.prime import get_prime, prime_generator


@pytest.mark.parametrize("k, prime", [(1, 2), (5, 11), (6, 13)])
def test_prime_get_prime(k, prime):
    @get_prime
    def func(a, b):
        pass

    assert func(k) == prime


def test_prime_get_prime_negative_index():
    @get_prime
    def func(a, b):
        pass

    with pytest.raises(ValueError):
        func(-1)


@pytest.mark.parametrize("k, prime", [(1, 2), (2, 3), (20, 71)])
def test_prime_generator(k, prime):
    gen = prime_generator()
    for _ in range(k - 1):
        next(gen)
    assert next(gen) == prime
