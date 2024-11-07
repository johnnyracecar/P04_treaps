from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast, Set

from py_treaps.comparable import KT, VT

class TreapNode:

    unused_priorities: Optional[List[int]] = None

    # The maximum priority that a node can have.
    # Access this with TreapNode.MAX_PRIORITY
    MAX_PRIORITY = 65535

    """A key-value node for the TreapMap.

    Please do not modify the attributes below, but feel free to add more.
    You do not need to modify this file to complete the project,
     but you are free to modify it if it makes your implementation simpler.
    Again, do not remove or rename any of the 6 attributes below.

    Attributes:
        key (KT): The key of the node.
        value (VT): The value associated with the key of the node.
        priority (int): The priority of the node.
        parent (TreapNode): The parent of the node.
        left_child (TreapNode): The left child of the node.
        right_child (TreapNode): The right child of the node.
    """

    def __init__(
        self, key: KT, value: VT, parent: Optional[TreapNode] = None
    ):
        self.key: KT = key
        self.value: VT = value
        self.priority: int = self.get_priority()

        self.parent: Optional[TreapNode] = parent
        self.left_child: Optional[TreapNode] = None
        self.right_child: Optional[TreapNode] = None

    def has_left_child(self):
        return self.left_child

    def has_right_child(self):
        return self.right_child
    
    def is_left_child(self):
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        return self.parent and self.parent.right_child == self
    
    def is_root(self):
        return not self.parent
    
    def is_leaf(self):
        return not (self.left_child or self.right_child)
    
    def has_any_children(self):
        return self.left_child or self.right_child
    
    def has_both_children(self):
        return self.left_child and self.right_child
    
    def replace_node_data(self, key, value, priority, left_child, right_child):
        self.key = key
        self.value = value
        self.priority = priority
        self.left_child = left_child
        self.right_child = right_child
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self

    def findMin(self):
        current = self
        while current.has_left_child():
            current = current.left_child
        return current

    def get_priority(self):
        """Generate a new priority for a treap node.
    
        Please do not touch this function, and use it on the creation of a standard treap node.
        You do not need to worry about running out of priorities.

        Returns:
            An unused integer priority.
        """

        if TreapNode.unused_priorities is None:
            TreapNode.unused_priorities = list(range(0, TreapNode.MAX_PRIORITY))
            random.shuffle(TreapNode.unused_priorities)
        return TreapNode.unused_priorities.pop()

#crs5682
