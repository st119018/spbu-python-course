from project.treap.treap import Treap, Node
import pytest


@pytest.mark.parametrize("key, value", [(1, "1"), (3, 7), (8, [1, 4])])
def test_node(key, value):
    node = Node(key, value)

    assert node.key == key
    assert node.value == value
    assert node.priority <= 100 and node.priority >= 1
    assert node.left is None
    assert node.right is None


def test_treap_setitem():
    # ensure key and value are added
    empty_treap = Treap()
    empty_treap[1] = "a"
    assert empty_treap.root.value == "a"
    assert empty_treap.root.key == 1


@pytest.fixture
def treap():
    # non-empty sample treap
    t = Treap()

    t[1] = "a"
    t[2] = "b"
    t[3] = "c"
    return t


@pytest.mark.parametrize(
    "key, value",
    [
        (1, "a"),
        (2, "b"),
        (3, "c"),
    ],
)
def test_treap_getitem(treap, key, value):
    # ensure values are retrieved correctly
    assert treap[key] == value


@pytest.mark.parametrize(
    "key",
    [
        -1,
        0,
        4,
        5,
    ],
)
def test_treap_getitem_wrong_key(treap, key):
    # error if given key wasn't found in the treap
    with pytest.raises(KeyError):
        treap[key]


@pytest.mark.parametrize(
    "key, value",
    [
        (1, "d"),
        (2, "e"),
        (3, "f"),
    ],
)
def test_treap_setitem_new_value(treap, key, value):
    # set new value to one of existing keys
    treap[key] = value
    assert treap[key] == value


def test_treap_delitem(treap):
    del treap[1]
    with pytest.raises(KeyError):
        treap[1]


def test_treap_delitem_wrong_key(treap):
    with pytest.raises(KeyError):
        # trying to delete non-existing key
        del treap[4]


def test_treap_in(treap):
    for key in range(1, 4):
        assert key in treap


def test_treap_not_in(treap):
    for key in range(4, 10):
        assert key not in treap


def test_treap_len(treap):
    assert len(treap) == 3

    del treap[1]
    assert len(treap) == 2

    del treap[2]
    assert len(treap) == 1

    treap[1] = "d"
    assert len(treap) == 2


def test_treap_iter(treap):
    # iterating through keys in treap
    count = 1
    for k in treap:
        assert k == count
        count += 1


def test_treap_reverse(treap):
    # iterating through keys in treap in reversed order
    count = 3
    for k in reversed(treap):
        assert k == count
        count -= 1


def test_treap_split(treap):
    left_root, right_root = treap.split(treap.root, 2)
    left = Treap(left_root)
    right = Treap(right_root)

    assert len(left) == 1
    assert all(k < 2 for k in left)

    assert len(right) == 2
    assert all(k >= 2 for k in right)


def test_treap_merge(treap):
    left = Treap()
    right = Treap()

    left[1] = "a"
    left[2] = "b"

    right[3] = "c"
    right[4] = "d"

    root = treap.merge(left.root, right.root)
    merged = Treap(root)

    assert len(merged) == 4
    # ensure all keys were added
    assert all(k in merged for k in range(1, 5))


def test_treap_str(treap):
    # ensure that the treap is correctly represented as a string
    s = str(treap)
    assert s == "{1: a, 2: b, 3: c}"
