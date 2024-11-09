from collections.abc import MutableMapping
from typing import Any, Optional, Tuple, Generator
import random


class Node:
    """Class implements node of treap

    Attributes
    ----------
    key : int
        Key of node
    value : Any
        Value of node
    priority : int
        Priority of node
    left : Optional[Node]
        Left child of node
    right : Optional[Node]
        Right child of node
    """

    def __init__(self, key: int, value: Any, priority: Optional[int] = None):
        """Set attributes

        priority is chosen randomly if not given

        Parameters
        ----------
        key : int
            Key of node
        value : Any
            Value of node
        priority : int
            Priority of node
        """
        self.key: int = key
        self.value: Any = value
        self.priority: int = (
            priority if priority is not None else random.randint(1, 100)
        )
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class Treap(MutableMapping):
    """Class implements treap data structure that combines binary tree and heap

    Attributes
    ----------
    root : Optional[Node]
        Root of treap

    Methods
    -------
    split(node, key)
        Split treap into two subtrees
    merge(left_node, right_node)
        Merge two treaps into one
    __setitem__(key, value)
        Add new key and value or change value of existing key to the treap
    _rotate_left(node)
        Rotate treap to left
    _rotate_right(node)
        Rotate treap to right
    _insert(node, key, value)
        Insert new key and value or change value of existing key
    _find(node, key)
        Return value of the given key
    __getitem__(key)
        Get value of the given key inn the treap
    __delitem__(key)
        Delete given key and its value from the treap
    _delete(node, key)
        Delete given key and its value
    __iter__()
        Return iterator of keys in the treap
    _inorder_traversal(node)
        Iterate through keys in ascending order
    __reverse__()
        Return reverse iterator of keys in the treap
    _reverse_inorder_traversal(node)
        Iterate through keys in descending order
    __len__()
        Return number of nodes in the treap
    _size(node)
        Return number of nodes
    __contains__(key)
       Return True if the given key is in the treap
    __str__()
       Return keys and values of nodes as a string
    """

    def __init__(self, root: Optional[Node] = None):
        """Initialize new treap with the given root

        Parameters
        ----------
        root : Optional[Node]
            Root of treap
        """
        self.root: Optional[Node] = root

    def split(
        self, node: Optional[Node], key: int
    ) -> Tuple[Optional[Node], Optional[Node]]:
        """Split the treap with the given root into two subtrees

        Left subtree consists of nodes with keys less then the given key

        Right subtree consists of nodes with keys greater or equal to the given key

        Parameters
        ----------
        node : Optional[Node]
            Root of the treap to split
        key : int
            Key of node at which the treap is split

        Return
        ------
            Tuple[Optional[Node], Optional[Node]]
        """
        if node is None:
            return None, None
        elif key > node.key:
            left, right = self.split(node.right, key)
            node.right = left
            return node, right
        else:
            left, right = self.split(node.left, key)
            node.left = right
            return left, node

    def merge(
        self, left_node: Optional[Node], right_node: Optional[Node]
    ) -> Optional[Node]:
        """Merge two treaps with the given roots into one treap and return its root

        Left subtree of merged treap consists of nodes with keys less than keys of right subtree

        Parameters
        ----------
        left_node : Optional[Node]
            Root of left treap
        right_node : Optional[Node]
            Root of right treap

        Return
        ------
            Optional[Node]
        """
        if right_node is None:
            return left_node
        if left_node is None:
            return right_node
        elif left_node.priority > right_node.priority:
            left_node.right = self.merge(left_node.right, right_node)
            return left_node
        else:
            right_node.left = self.merge(left_node, right_node.left)
            return right_node

    def __setitem__(self, key: int, value: Any) -> None:
        """Add new node with key and value to the treap or set new value of existing key

        Parameters
        ----------
        key : int
            Key of new or existing node
        value : Any
            Value to add or change existing value

        Return
        ------
            None
        """
        self.root = self._insert(self.root, key, value)

    def _rotate_left(self, node: Node) -> Node:
        """Rotate treap with the given root to left

        Right child of the given root becomes the root

        Parameters
        ----------
        node : Node
            Root of the treap to rotate

        Return
        ------
            Node
        """
        if node.right is None:
            return node
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _rotate_right(self, node: Node) -> Node:
        """Rotate treap with the given root to right

        Left child of the given root becomes the root

        Parameters
        ----------
        node : Node
            Root of the treap to rotate

        Return
        ------
            Node
        """
        if node.left is None:
            return node
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _insert(self, node: Optional[Node], key: int, value: Any) -> Node:
        """Insert new key and value or change value of existing key

        in the treap with the given root

        Parameters
        ----------
        node : Optional[Node]
            Root of treap
        key : int
            New or existing key
        value: Any
            Value of key

        Return
        ------
            Node
        """
        if not node:
            return Node(key, value)
        if key == node.key:
            node.value = value
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, key, value)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)
        return node

    def _find(self, node: Optional[Node], key: int) -> Any:
        """Return value of the given key or None if key wasn't found

        in the treap with the given root

        Parameters
        ----------
        node : Optional[Node]
            Root of treap in which key is searched
        key : int
            Key to search

        Return
        ------
            Any
        """
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def __getitem__(self, key: int) -> Any:
        """Get value of the given key in the treap

        Parameters
        ----------
        key : int
            Key of value

        Raises
        ------
        KeyError
            If key was not found

        Return
        ------
            Any
        """
        value = self._find(self.root, key)
        if value is None:
            raise KeyError(f"Key {key} not found")
        return value

    def __delitem__(self, key: int) -> None:
        """Delete node with the given key from the treap

        Parameters
        ----------
        key : int
            Key of node to delete

        Raises
        ------
        KeyError
            If key was not found

        Return
            None
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[Node], key: int) -> Optional[Node]:
        """Delete node with the given key from the treap with the given root

        Parameters
        ----------
        node : Optional[Node]
            Root of treap to delete key from
        key : int
            Key of node to delete

        Raises
        ------
        KeyError
            If key was not found

        Return
            Optional[Node]
        """
        if node is None:
            raise KeyError(f"Key {key} not found")
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            node = self.merge(node.left, node.right)
        return node

    def __iter__(self) -> Generator[int, Any, None]:
        """Return in order traversal iterator of keys in the treap

        Yields
        ------
            int
        """
        yield from self._inorder_traversal(self.root)

    def _inorder_traversal(self, node: Optional[Node]) -> Generator[int, Any, None]:
        """Iterate through keys of the treap with the given root
        in ascending order

        Parameters
        ----------
        node : Optional[Node]
            Root of the treap to iterate over

        Yields
        ------
            int
        """
        if node is not None:
            yield from self._inorder_traversal(node.left)
            yield node.key
            yield from self._inorder_traversal(node.right)

    def __reversed__(self) -> Generator[int, Any, None]:
        """Return reverse in order traversal iterator of keys in the treap

        Yields
        ------
            int
        """
        yield from self._reverse_inorder_traversal(self.root)

    def _reverse_inorder_traversal(
        self, node: Optional[Node]
    ) -> Generator[int, Any, None]:
        """Iterate through keys of the treap with the given root
        in descending order

        Parameters
        ----------
        node : Optional[Node]
            Root of the treap to iterate over

        Yields
        ------
            int
        """
        if node is not None:
            yield from self._reverse_inorder_traversal(node.right)
            yield node.key
            yield from self._reverse_inorder_traversal(node.left)

    def __len__(self) -> int:
        """Return number of nodes in the treap

        Return
        ------
            int
        """
        return self._size(self.root)

    def _size(self, node: Optional[Node]) -> int:
        """Return number of nodes in the treap with the given root

        Parameters
        ----------
        node : Optional[Node]
            Root of the treap

        Return
        ------
            int
        """
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def __contains__(self, key: Any) -> bool:
        """Return True if the given key is in the treap

        Parameters
        ----------
        key : int
            Key to search for in the treap

        Return
        ------
            bool
        """
        return self._find(self.root, key) is not None

    def __str__(self) -> str:
        """Return keys and values of nodes in the treap as a string"""
        treap_str = "{"
        for key in self:
            treap_str += f"{key}: {self[key]}, "
        return treap_str[:-2] + "}"
