import pytest
from project.generator.prime import get_prime, prime_generator

# without parametrize
def test_prime_evenly_increasing_sequence():
    @get_prime
    def gen():
        return prime_generator()

    generated_primes = [gen(k) for k in range(1, 10)]
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]

    assert generated_primes == primes


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


@get_prime
def gen():
    return prime_generator()


# using parametrize
@pytest.mark.parametrize(
    "k, prime", [(1, 2), (2, 3), (2, 3), (20, 71), (20, 71), (27, 103)]
)
def test_prime_unevenly_increasing_sequence(k, prime):

    assert gen(k) == prime
