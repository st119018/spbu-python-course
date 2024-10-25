import pytest
from project.decorators.smart_args import Evaluated, Isolated, smart_args


def test_smart_args_Evaluated():
    with pytest.raises(ValueError):
        Evaluated(lambda x: x)


def test_smart_args_isol():
    @smart_args
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    no_mutable = {"a": 10}

    assert check_isolation(d=no_mutable) == {"a": 0}
    assert no_mutable == {"a": 10}


def test_smart_args_eval():
    count = [0]

    def get_count():
        count[0] += 1
        return count[0]

    @smart_args
    def check_evaluation(*, x=get_count(), y=Evaluated(get_count)):
        return (x, y)

    assert check_evaluation() == (1, 2)
    assert count[0] == 2  # call get_count for x and y
    assert check_evaluation() == (1, 3)
    assert count[0] == 3  # call get_count for y
    assert check_evaluation(y=150) == (1, 150)
    assert count[0] == 3  # don't call get_count


def test_smart_args_isol_positional_argument():
    @smart_args
    def increment(l=Isolated()):
        for el in l:
            el += 1
        return l

    with pytest.raises(AssertionError):
        increment(Isolated())


def test_smart_args_eval_positional_argument():
    @smart_args
    def add(a, b):
        return a + b

    with pytest.raises(AssertionError):
        add(Evaluated(lambda: 1), 4)


def test_smart_args_eval_isol_combination():
    @smart_args
    def add(*, a, b=Evaluated(Isolated)):
        return a + b

    with pytest.raises(ValueError):
        add(a=1)
    with pytest.raises(ValueError):
        add(a=1, b=3)


def test_smart_args_isol_without_argument():
    @smart_args
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    with pytest.raises(ValueError):
        check_isolation()


def test_smart_args_eval_isol_together():
    count = [0]

    def get_count():
        count[0] += 1
        return count[0]

    @smart_args
    def check_isol_eval(*, x=Isolated(), y=Evaluated(get_count)):
        x["a"] = 0
        return (x, y)

    no_mutable = {"a": 10}

    assert check_isol_eval(x=no_mutable) == ({"a": 0}, 1)
    assert check_isol_eval(x=no_mutable) == ({"a": 0}, 2)
    assert no_mutable == {"a": 10}
