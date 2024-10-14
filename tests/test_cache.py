from project.cache import cache_results
from typing import List


def test_cache():
    @cache_results(2)
    def add(x: int, y: int):
        return x + y

    assert add(3, 6) == 9
    assert add(2, 9) == 11
    assert add(8, 4) == 12


def test_cache_with_count():
    count = [0]

    @cache_results(2)
    def add_with_count(x: int, y: int):
        count[0] += 1
        return x + y

    f = add_with_count
    assert f(1, 2) == 3
    assert count[0] == 1  # calculate

    assert f(3, 4) == 7
    assert count[0] == 2  # calculate

    assert f(1, 2) == 3
    assert count[0] == 2  # take from cache

    assert f(5, 7) == 12
    assert count[0] == 3  # calculate

    assert f(3, 4) == 7
    assert count[0] == 4  # calculate


def test_cache_built_in():
    divmod_cache = cache_results(1)(divmod)

    assert divmod_cache(7, 3) == (2, 1)
    assert divmod_cache(8, 2) == (4, 0)
    assert divmod_cache(8, 2) == (4, 0)


def test_cache_non_hashable():
    count = [0]

    @cache_results(2)
    def addl_with_count(l: List[int]):
        count[0] += 1
        return sum(l)

    f = addl_with_count
    assert f([1, 2]) == 3
    assert count[0] == 1  # calculate

    assert f([6, 3, 1]) == 10
    assert count[0] == 2  # calculate

    assert f([1, 2]) == 3
    assert count[0] == 2  # take from cache

    assert f([2, 8, 4]) == 14
    assert count[0] == 3  # calculate

    assert f([6, 3, 1]) == 10
    assert count[0] == 4  # calculate
