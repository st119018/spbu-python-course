import pytest
from project.prime import get_prime, prime_generator


@pytest.mark.parametrize(
    "k, prime", [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11), (6, 13), (7, 17)]
)
def test_prime_evenly_increasing_sequence(k, prime):
    @get_prime
    def gen():
        return prime_generator()

    assert gen(k) == prime


@pytest.mark.parametrize(
    "k, prime", [(1, 2), (2, 3), (5, 11), (20, 71), (21, 73), (27, 103)]
)
def test_prime_unevenly_increasing_sequence(k, prime):
    @get_prime
    def gen():
        return prime_generator()

    assert gen(k) == prime


def test_prime_invalid_index():
    @get_prime
    def gen():
        return prime_generator()

    with pytest.raises(ValueError):
        gen(-1)

    assert gen(4) == 7
    with pytest.raises(ValueError):
        gen(3)  # got 4-th prime number before


def test_prime_generator():
    gen = prime_generator()
    gen_primes = [next(gen) for _ in range(7)]
    primes = [2, 3, 5, 7, 11, 13, 17]
    assert gen_primes == primes
