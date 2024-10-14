import pytest
from project.rgba import get_rgba_vector, rgba_generator


@pytest.mark.parametrize(
    "index, vector",
    [
        (0, (0, 0, 0, 0)),
        (50, (0, 0, 0, 100)),
        (51, (0, 0, 1, 0)),
    ],
)
def test_rgba_vector(index, vector):
    rgba = get_rgba_vector(index)
    assert vector == rgba


def test_rgba_vector_negative_index():
    with pytest.raises(ValueError):
        get_rgba_vector(-1)


@pytest.mark.parametrize(
    "index, vector",
    [
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 2)),
        (50, (0, 0, 0, 100)),
        (51 * 256, (0, 1, 0, 0)),
    ],
)
def test_rgba_generator(index, vector):
    gen = rgba_generator()
    for _ in range(index):
        next(gen)
    assert next(gen) == vector
