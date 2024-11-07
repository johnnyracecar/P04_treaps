from py_treaps.treap_map import TreapMap
from py_treaps.treap_node import TreapNode

import pytest
from typing import Any

# This file includes some starter test cases that you can use
# as a template to test your code and write your own test cases.
# You should write more tests; passing the following tests is
# NOT sufficient to guarantee that your code works.
# For example, there is no test for join(). You should write some.
# Be sure to read the test cases carefully.

def test_split_boundaries() -> None:
    """Test split on boundary conditions."""

    treap = TreapMap[int, str]()
    for i in range(10):
        treap.insert(i, str(i))
    
    # Split at smallest key
    split_result = treap.split(0)
    assert split_result[0].count_nodes() == 0
    assert split_result[1].count_nodes() == 10

    # Split at largest key
    treap = TreapMap[int, str]()
    for i in range(10):
        treap.insert(i, str(i))
    split_result = treap.split(9)
    assert split_result[0].count_nodes() == 9
    assert split_result[1].count_nodes() == 1

    # Split on non-existent key
    treap = TreapMap[int, str]()
    for i in range(10):
        treap.insert(i, str(i))
    print("treap")
    print(treap)
    split_result = treap.split(5.5)
    assert split_result[0].count_nodes() == 6
    assert split_result[1].count_nodes() == 4


def test_remove_varied_nodes() -> None:
    print("I AM HERE IN REMOVE VARIED NODES")
    """Test remove functionality for nodes with different child configurations."""

    treap = TreapMap[int, str]()
    for i in range(10):
        treap.insert(i, str(i))

    print("*********")
    print("treap")
    print(treap)
    print()
    #assert False, "Forcing failure to view print output"

    # Remove leaf node
    assert treap.remove(9) == "9"
    assert not treap.lookup(9)

    # Remove node with only left child
    assert treap.remove(7) == "7"
    assert not treap.lookup(7)

    # Remove node with only right child
    assert treap.remove(0) == "0"
    assert not treap.lookup(0)

    # Remove node with two children
    assert treap.remove(5) == "5"
    assert not treap.lookup(5)


def test_join_non_overlapping() -> None:
    """Test joining two treaps with non-overlapping key ranges."""

    left_treap = TreapMap[int, str]()
    right_treap = TreapMap[int, str]()

    for i in range(5):
        left_treap.insert(i, str(i))
    for i in range(5, 10):
        right_treap.insert(i, str(i))

    left_treap.join(right_treap)

    # Check all keys are in the joined treap
    for i in range(10):
        assert left_treap.lookup(i) == str(i)

    # Ensure original treap structure is not broken
    assert left_treap.get_root_node() is not None


def test_lookup_varied_keys() -> None:
    """Test lookup on present and absent keys."""

    treap = TreapMap[int, str]()
    for i in range(5):
        treap.insert(i, str(i))

    # Existing keys
    for i in range(5):
        assert treap.lookup(i) == str(i)

    # Non-existing keys
    assert not treap.lookup(6)
    assert not treap.lookup(-1)




def test_complex_join():
    # Setup
    treap1 = TreapMap()
    treap2 = TreapMap()
    treap1.insert(10, "A")
    treap1.insert(5, "B")
    treap1.insert(15, "C")
    treap2.insert(32, "D")
    treap2.insert(20, "E")
    treap2.insert(74, "F")

    # Perform join in-place on treap1
    treap1.join(treap2)

    # Verification
    expected_keys = [5, 10, 15, 20, 32, 74]
    assert sorted([key for key in treap1]) == expected_keys
    assert all(treap1.lookup(key) is not None for key in expected_keys)

def test_insert_with_priority_conflict():
    # Setup
    treap = TreapMap()
    treap.insert(10, "A")
    treap.insert(5, "B")
    treap.insert(15, "C")
    
    # Insert node and manually adjust its priority to simulate a conflict
    treap.insert(8, "HighPriority")
    high_priority_node = treap.recursive_lookup(8, treap.get_root_node())
    high_priority_node.priority = 100000  # Set high priority
    treap.priority_reorder(high_priority_node)

    # Verification
    assert treap.get_root_node().key == 8
    assert all(treap.lookup(key) is not None for key in [5, 8, 10, 15])

def test_remove_with_multiple_percolations():
    # Setup
    treap = TreapMap()
    treap.insert(10, "A")
    treap.insert(5, "B")
    treap.insert(15, "C")
    treap.insert(7, "D")
    treap.insert(3, "E")

    # Perform remove
    removed_value = treap.remove(5)
    
    # Verification
    assert removed_value == "B"
    assert treap.lookup(5) is None
    assert sorted([key for key in treap]) == [3, 7, 10, 15]

def test_split_with_overlapping_keys():
    # Setup
    treap = TreapMap()
    treap.insert(10, "A")
    treap.insert(5, "B")
    treap.insert(15, "C")
    treap.insert(7, "D")
    treap.insert(3, "E")

    # Split around key 7
    left_treap, right_treap = treap.split(7)
    
    # Verification
    assert sorted([key for key in left_treap]) == [3, 5]
    assert sorted([key for key in right_treap]) == [7, 10, 15]

def test_iterator_validation():
    # Setup
    treap = TreapMap()
    treap.insert(10, "A")
    treap.insert(5, "B")
    treap.insert(15, "C")
    treap.insert(3, "D")
    treap.insert(7, "E")

    # Test iterator
    sorted_keys = [3, 5, 7, 10, 15]
    assert list(treap) == sorted_keys

def test_recursive_boundary_join_and_insert():
    # Setup
    treap1 = TreapMap()
    treap2 = TreapMap()
    treap1.insert(10, "Root1")
    treap1.insert(5, "LChild")
    treap2.insert(15, "Root2")
    treap2.insert(20, "RChild")

    # Perform join in-place on treap1
    treap1.join(treap2)

    # Verification
    expected_keys = [5, 10, 15, 20]
    assert sorted([key for key in treap1]) == expected_keys
    assert all(treap1.lookup(key) is not None for key in expected_keys)

def test_split_followed_by_remove():
    # Setup
    treap = TreapMap()
    treap.insert(10, "A")
    treap.insert(5, "B")
    treap.insert(15, "C")
    treap.insert(7, "D")

    # Split and then remove
    left_treap, right_treap = treap.split(7)
    removed_value = right_treap.remove(15)

    # Verification
    assert removed_value == "C"
    assert right_treap.lookup(15) is None
    assert sorted([key for key in left_treap]) == [5]
    assert sorted([key for key in right_treap]) == [7, 10]


import sys

def test_treap_structure():
    treap = TreapMap()
    treap.insert(10, "ten")
    treap.insert(2, "two")
    treap.insert(12, "twelve")
    treap.insert(7, "seven")
    treap.insert(5, "five")
    print(str(treap))  # This will output if the test "fails"
    assert False, "Forcing failure to view print output"


