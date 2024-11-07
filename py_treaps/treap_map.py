from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast

from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size
    
    def __len__(self):
        return self.size
    


    def get_root_node(self) -> Optional[TreapNode]:
        return self.root

    def lookup(self, key: KT) -> Optional[VT]:
        if self.root:
            found_node = self.recursive_lookup(key, self.root)
            if found_node:
                return found_node.value
            else:
                return None

    def recursive_lookup(self, key: KT, current_node: TreapNode) -> Optional[TreapNode]:
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self.recursive_lookup(key, current_node.left_child)
        else:
            return self.recursive_lookup(key, current_node.right_child)
        
    def __getitem__(self, key: KT) -> Optional[VT]:
        return self.lookup(key)
    
    def __contains__(self, key: KT) -> bool:
        if self.recursive_lookup(key, self.root):
            return True
        else:
            return False



    def insert(self, key: KT, value: VT) -> None:
        if self.root:
            #print("DIVING IN FROM insert")
            new_node = self.recursive_insert(key, value, self.root)
            self.priority_reorder(new_node)
        else:
            new_node = TreapNode(key, value)
            #print("FIRST NODE: ", new_node.key, new_node.value, new_node.priority)
            self.root = new_node
        self.size += 1

        

    def recursive_insert(self, key: KT, value: VT, current_node: TreapNode) -> Optional[TreapNode]:
        #print(f"Inserting node with key: {key}, current_node.key: {current_node.key}")
        if key < current_node.key:
            if current_node.has_left_child() is not None:
                #print("Current Node has left child:", current_node.key, current_node.priority, current_node.left_child.key)
                #print("INTO RECURSION*")
                return self.recursive_insert(key, value, current_node.left_child)
            else:
                #print("I AM HERE 3")
                current_node.left_child = TreapNode(key, value, parent = current_node)
                return current_node.left_child
        elif key > current_node.key:
            if current_node.has_right_child() is not None:
                #print("Current Node has right child:", current_node.key, current_node.priority, current_node.right_child.key)
                #print("INTO RECURSION+")
                return self.recursive_insert(key, value, current_node.right_child)
            else:
                #print("I AM HERE 2")
                current_node.right_child = TreapNode(key, value, parent = current_node)
                return current_node.right_child
        else:
            #print("I AM HERE")
            current_node.value = value
            return current_node

    def priority_reorder(self, current_node: TreapNode):

        while current_node.parent and current_node.priority > current_node.parent.priority:

            #print(f"Before Rotation | Node: {current_node.key}, Priority: {current_node.priority}")
            #print(f"Before Rotation | Parent Node: {current_node.parent.key}, Priority: {current_node.parent.priority}")

            parent_is_lc = False
            parent_is_rc = False

            parent_node = current_node.parent
            if parent_node.is_root():
                grandparent_node = None
            else: 
                grandparent_node = parent_node.parent
                if parent_node.is_left_child():
                    parent_is_lc = True

            # rotate right
            if current_node.is_left_child():
                #print("ROTATE RIGHT")
                if current_node.right_child is not None:
                    child_node = current_node.right_child
                    parent_node.left_child = child_node
                    child_node.parent = parent_node
                else:
                    parent_node.left_child = None
                current_node.right_child = parent_node
                parent_node.parent = current_node
                if grandparent_node is not None:
                    current_node.parent = grandparent_node
                    if parent_is_lc:
                       grandparent_node.left_child = current_node
                    else:
                       grandparent_node.right_child = current_node
                else:
                    self.root = current_node
                    current_node.parent = None
           
            # rotate left
            else:
                #print("ROTATE LEFT")
                if current_node.left_child is not None:
                    child_node = current_node.left_child
                    parent_node.right_child = child_node
                    child_node.parent = parent_node
                else:
                    parent_node.right_child = None
                current_node.left_child = parent_node
                parent_node.parent = current_node
                if grandparent_node is not None:
                    current_node.parent = grandparent_node
                    if parent_is_lc:
                       grandparent_node.left_child = current_node
                    else:
                       grandparent_node.right_child = current_node
                else:
                    self.root = current_node
                    current_node.parent = None

            #print(f"After Rotation | New Parent: {self.root.key if self.root else None}")
            #print(f"Left Child of New Root: {self.root.left_child.key if self.root.left_child else None}")
            #print(f"Right Child of New Root: {self.root.right_child.key if self.root.right_child else None}")
        
        #if current_node.parent:
            #print("priority_reorder | BOTTOM OF LOOP:", current_node.parent.key, current_node.parent.priority)
        #else:
            #print("priority_reorder | BOTTOM OF LOOP: Root node reached")
        #print("priority_reorder | BOTTOM OF LOOP | current_node.key, current_node.priority")
        #print("priority_reorder | BOTTOM OF LOOP: ", current_node.key, current_node.priority)



    def remove(self, key: KT) -> Optional[VT]:
        if self.size > 1:
            node_to_remove = self.recursive_lookup(key, self.root)
            if node_to_remove:
               self.reorder_to_remove(node_to_remove)
               self.size -= 1
            else:
               return None
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else: 
            return None
        #print("*** Node to remove value: ", node_to_remove.value)
        return node_to_remove.value
        
  
    def reorder_to_remove(self, current_node: TreapNode) -> None:
            
        while not current_node.is_leaf():

            #print("reorder_to_remove | current_node.key: ", current_node.key)
																														
            current_is_lc = False
            current_is_rc = False
 
            if current_node.is_root():
                parent_node = None
            else: 
                parent_node = current_node.parent
                if current_node.is_left_child():
                    current_is_lc = True
						  
            if current_node.has_both_children():
                if current_node.left_child.priority > current_node.right_child.priority:  
                    #print("ROTATE RIGHT")
                    child_node = current_node.left_child           # DEFINE CHILD
                    if child_node.right_child is not None:
                        grandchild_node = child_node.right_child
                        current_node.left_child = grandchild_node   # DEFINE GRANDCHILD
                        grandchild_node.parent = current_node
                    else:
                        current_node.left_child = None
                    child_node.right_child = current_node
                    current_node.parent = child_node			   
                    if parent_node is not None:
                        child_node.parent = parent_node
                        if current_is_lc:
                           parent_node.left_child = child_node
                        else:
                           parent_node.right_child = child_node						   
                    else:
                        self.root = child_node
                        child_node.parent = None					   

                else: 
                    #print("ROTATE LEFT")
                    child_node = current_node.right_child            # DEFINE CHILD
                    if child_node.left_child is not None:
                        grandchild_node = child_node.left_child      # DEFINE GRANDCHILD
                        current_node.right_child = grandchild_node
                        grandchild_node.parent = current_node
                    else:
                        current_node.right_child = None
                    child_node.left_child = current_node
                    current_node.parent = child_node			   
                    if parent_node is not None:
                        child_node.parent = parent_node
                        if current_is_lc:
                           parent_node.left_child = child_node
                        else:
                           parent_node.right_child = child_node						   
                    else:
                        self.root = child_node
                        child_node.parent = None		
 
            else:

                if current_node.has_left_child():
                    #print("ROTATE RIGHT")
                    child_node = current_node.left_child            # DEFINE CHILD
                    if child_node.right_child is not None:
                        grandchild_node = child_node.right_child
                        current_node.left_child = grandchild_node   # DEFINE GRANDCHILD
                        grandchild_node.parent = current_node
                    else:
                        current_node.left_child = None
                    child_node.right_child = current_node
                    current_node.parent = child_node			   
                    if parent_node is not None:
                        child_node.parent = parent_node
                        if current_is_lc:
                           parent_node.left_child = child_node
                        else:
                           parent_node.right_child = child_node						   
                    else:
                        self.root = child_node
                        child_node.parent = None	

                else:
                    #print("ROTATE LEFT")
                    child_node = current_node.right_child            # DEFINE CHILD
                    if child_node.left_child is not None:
                        grandchild_node = child_node.left_child      # DEFINE GRANDCHILD
                        current_node.right_child = grandchild_node
                        grandchild_node.parent = current_node
                    else:
                        current_node.right_child = None
                    child_node.left_child = current_node
                    current_node.parent = child_node			   
                    if parent_node is not None:
                        child_node.parent = parent_node
                        if current_is_lc:
                           parent_node.left_child = child_node
                        else:
                           parent_node.right_child = child_node						   
                    else:
                        self.root = child_node
                        child_node.parent = None	

        # current node is now a leaf; remove current node
        if current_node == current_node.parent.left_child:
            current_node.parent.left_child = None
        else:																		 
            current_node.parent.right_child = None
																							


    def split(self, threshold: KT) -> List[Treap[KT, VT]]:

        # Check if threshold key already exists in treap
        dummy_threshold_node = False
        threshold_node = self.recursive_lookup(threshold, self.root)
        #print(f"Splitting at threshold key: {threshold}")

        if threshold_node is None:
            dummy_threshold_node = True
            threshold_node = self.split_insert(threshold, None)
        else:
            threshold_node.priority = TreapNode.MAX_PRIORITY 
            self.priority_reorder(threshold_node)
        
        left_treap = TreapMap()
        right_treap = TreapMap()

        left_treap.root = threshold_node.left_child
        if dummy_threshold_node == False: 
            right_treap.root = threshold_node
        elif dummy_threshold_node == True: 
            right_treap.root = threshold_node.right_child
        left_treap.size = left_treap.count_nodes()
        right_treap.size = right_treap.count_nodes()

        #print("right_treap")
        #print(right_treap)
        #print("left_treap")
        #print(left_treap)

        #print("left treap count nodes")
        #print(left_treap.count_nodes())

        #print("right treap count nodes")
        #print(right_treap.count_nodes())

        threshold_node.left_child = None
        
        #print(f"Left treap root: {left_treap.root.key if left_treap.root else None}")
        #print(f"Right treap root: {right_treap.root.key if right_treap.root else None}")
        #print(f"Threshold node left child after split: {threshold_node.left_child.key}")
        #print(f"Threshold node right child after split: {threshold_node.right_child.key}")

        return [left_treap, right_treap]


    def split_insert(self, key: KT, value: None) -> TreapNode:
        if self.root:
            threshold_node = self.recursive_insert(key, value, self.root)
        else:
            threshold_node = TreapNode(key, value)
            self.root = threshold_node
        self.size =+ 1

        threshold_node.priority = TreapNode.MAX_PRIORITY

        self.priority_reorder(threshold_node)
        #print(f"After priority_reorder | threshold_node.key: {threshold_node.key}")
        #print(f"Left child key (should be left subheap root): {threshold_node.left_child.key if threshold_node.left_child else None}")
        #print(f"Right child key (should be right subheap root): {threshold_node.right_child.key if threshold_node.right_child else None}")

        return threshold_node


    def join(self, _other: Treap[KT, VT]) -> None:

        # Check if first treap is empty
        if self.root is None:
            # If first treap is empty, return the other treap
            self.root = _other.root
            self.size = _other.size
            return
        # Check if second treap is empty
        if _other.root is None:
            # If second treap is empty, return the first treap
            return
        
        # Create dummy root for joined treap
        dummy_root = TreapNode(key='dummy', value=None)
        dummy_root.priority = TreapNode.MAX_PRIORITY
        # Determine the dummy root's left child and right child
        if self.root.key < _other.root.key:
            dummy_root.left_child = self.root
            dummy_root.right_child = _other.root
        else:
            dummy_root.left_child = _other.root
            dummy_root.right_child = self.root   

        # Make dummy root the parent of the two treaps to be joined
        self.root.parent = dummy_root
        _other.root.parent = dummy_root

        self.root = dummy_root
        self.remove(key='dummy')

        self.size += _other.size

  
    
    def meld(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError
    def difference(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError
    def balance_factor(self) -> float: # KARMA
        raise AttributeError

    
    def __str__(self) -> str:
        # Handle empty treap case
        if not self.root:
            return "Empty Treap"

        # Inner recursive function to help format each node
        def display(node: TreapNode, depth: int = 0, max_depth: int = 10) -> str:
            if not node:
                return ""
        
            # Format current node's info: key, value, and priority
            node_info = f"{' ' * depth * 2}- (Key: {node.key}, Value: {node.value}, Priority: {node.priority})\n"
        
            # Recursively format the left and right children
            left_info = display(node.left_child, depth + 1) if node.left_child else f"{' ' * (depth + 1) * 2}- None\n"
            right_info = display(node.right_child, depth + 1) if node.right_child else f"{' ' * (depth + 1) * 2}- None\n"
        
            return node_info + left_info + right_info
    
        # Generate the display string for the entire treap
        return display(self.root)




    def __iter__(self) -> typing.Iterator[KT]:
        # empty case
        if self.root is None:
            return
        else:
            yield from self.traverse(self.root)

    def traverse(self, current_node: TreapNode) -> typing.Iterator[KT]:
        # Traverse through left subtreap
        if current_node.left_child is not None:
            #print(f"In traverse: Checking left child is not None (key value =): {current_node.left_child.key}")
            yield from self.traverse(current_node.left_child)
        # yield current node key (root key)
        yield current_node.key
        # Traverse through right subtreap
        if current_node.right_child is not None:
            #print(f"In traverse: Checking right child is not None (key value =): {current_node.right_child.key}")
            yield from self.traverse(current_node.right_child)
    
    def count_nodes(self) -> int:
        # Using the iterator directly to count nodes
        return sum(1 for _ in self.__iter__())
    

    #crs5682


    
