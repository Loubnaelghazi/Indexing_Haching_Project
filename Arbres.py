import tkinter as tk
from tkinter import ttk
from DataBaseConnection import *

from collections import deque
import random
import os

splits = 0
parent_splits = 0
fusions = 0
parent_fusions = 0


class Node(object):
   

    def __init__(self, parent=None):

        self.keys: list = []
        self.values: list[Node] = []
        self.parent: Node = parent

    def index(self, key):
 
        for i, item in enumerate(self.keys):
            if key < item:
                return i

        return len(self.keys)

    def __getitem__(self, item):
        return self.values[self.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        self.keys[i:i] = [key]
        self.values.pop(i)
        self.values[i:i] = value

    def split(self):
 
        global splits, parent_splits
        splits += 1
        parent_splits += 1

        left = Node(self.parent)

        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid + 1]
        for child in left.values:
            child.parent = left

        key = self.keys[mid]
        self.keys = self.keys[mid + 1:]
        self.values = self.values[mid + 1:]

        return key, [left, self]

    def __delitem__(self, key):
        i = self.index(key)
        del self.values[i]
        if i < len(self.keys):
            del self.keys[i]
        else:
            del self.keys[i - 1]

    def fusion(self):
        global fusions, parent_fusions
        fusions += 1
        parent_fusions += 1

        index = self.parent.index(self.keys[0])
        
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            next_node.keys[0:0] = self.keys + [self.parent.keys[index]]
            for child in self.values:
                child.parent = next_node
            next_node.values[0:0] = self.values
        else: 
            prev: Node = self.parent.values[-2]
            prev.keys += [self.parent.keys[-1]] + self.keys
            for child in self.values:
                child.parent = prev
            prev.values += self.values

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            if len(next_node.keys) > minimum:
                self.keys += [self.parent.keys[index]]

                borrow_node = next_node.values.pop(0)
                borrow_node.parent = self
                self.values += [borrow_node]
                self.parent.keys[index] = next_node.keys.pop(0)
                return True
        elif index != 0:
            prev: Node = self.parent.values[index - 1]
            if len(prev.keys) > minimum:
                self.keys[0:0] = [self.parent.keys[index - 1]]

                borrow_node = prev.values.pop()
                borrow_node.parent = self
                self.values[0:0] = [borrow_node]
                self.parent.keys[index - 1] = prev.keys.pop()
                return True

        return False


class Leaf(Node):
    def __init__(self, parent=None, prev_node=None, next_node=None):

        super(Leaf, self).__init__(parent)
        self.next: Leaf = next_node
        if next_node is not None:
            next_node.prev = self
        self.prev: Leaf = prev_node
        if prev_node is not None:
            prev_node.next = self

    def __getitem__(self, item):
        return self.values[self.keys.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        if key not in self.keys:
            self.keys[i:i] = [key]
            self.values[i:i] = [value]
        else:
            self.values[i - 1] = value

    def split(self):
        global splits
        splits += 1

        left = Leaf(self.parent, self.prev, self)
        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        self.keys: list = self.keys[mid:]
        self.values: list = self.values[mid:]
        return self.keys[0], [left, self]

    def __delitem__(self, key):
        i = self.keys.index(key)
        del self.keys[i]
        del self.values[i]

    def fusion(self):
        global fusions
        fusions += 1

        if self.next is not None and self.next.parent == self.parent:
            self.next.keys[0:0] = self.keys
            self.next.values[0:0] = self.values
        else:
            self.prev.keys += self.keys
            self.prev.values += self.values

        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys) and len(self.next.keys) > minimum:
            self.keys += [self.next.keys.pop(0)]
            self.values += [self.next.values.pop(0)]
            self.parent.keys[index] = self.next.keys[0]
            return True
        elif index != 0 and len(self.prev.keys) > minimum:
            self.keys[0:0] = [self.prev.keys.pop()]
            self.values[0:0] = [self.prev.values.pop()]
            self.parent.keys[index - 1] = self.keys[0]
            return True

        return False


class BPlusTree(object):
 
    root: Node

    def __init__(self, maximum=4):
        self.root = Leaf()
        self.maximum: int = maximum if maximum > 2 else 2
        self.minimum: int = self.maximum // 2
        self.depth = 0

    def find(self, key) -> Leaf:

        node = self.root
        # Traverse tree until leaf node is reached.
        while type(node) is not Leaf:
            node = node[key]

        return node

    def __getitem__(self, item):
        return self.find(item)[item]

    def query(self, key):

        leaf = self.find(key)
        return leaf[key] if key in leaf.keys else None

    def change(self, key, value):

        leaf = self.find(key)
        if key not in leaf.keys:
            return False, leaf
        else:
            leaf[key] = value
            return True, leaf

    def __setitem__(self, key, value, leaf=None):
 
        if leaf is None:
            leaf = self.find(key)
        leaf[key] = value
        if len(leaf.keys) > self.maximum:
            self.insert_index(*leaf.split())

    def insert(self, key, value):
       
        leaf = self.find(key)
        if key in leaf.keys:
            return False, leaf
        else:
            self.__setitem__(key, value, leaf)
            return True, leaf

    def insert_index(self, key, values: list[Node]):
       
        parent = values[1].parent
        if parent is None:
            values[0].parent = values[1].parent = self.root = Node()
            self.depth += 1
            self.root.keys = [key]
            self.root.values = values
            return

        parent[key] = values

        if len(parent.keys) > self.maximum:
            self.insert_index(*parent.split())


    def delete(self, key, node: Node = None):
        if node is None:
            node = self.find(key)
        del node[key]

        if len(node.keys) < self.minimum:
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.values) > 0:
                    self.root = self.root.values[0]
                    self.root.parent = None
                    self.depth -= 1
                return

            elif not node.borrow_key(self.minimum):
                node.fusion()
                self.delete(key, node.parent)
        

    def show(self, node=None, file=None, _prefix="", _last=True):
        """Prints the keys at each level."""
        if node is None:
            node = self.root
        print(_prefix, "`- " if _last else "|- ", node.keys, sep="", file=file)
        _prefix += "   " if _last else "|  "

        if type(node) is Node:

            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.show(child, file, _prefix, _last)

    def output(self):
        return splits, parent_splits, fusions, parent_fusions, self.depth

    def readfile(self, reader):
        i = 0
        for i, line in enumerate(reader):
            s = line.decode().split(maxsplit=1)
            self[s[0]] = s[1]
            if i % 1000 == 0:
                print('Insert ' + str(i) + 'items')
        return i + 1

    def leftmost_leaf(self) -> Leaf:
        node = self.root
        while type(node) is not Leaf:
            node = node.values[0]
        return node



import graphviz

def to_dot(self):
    dot = graphviz.Digraph()

    if not self.root.keys:
        dot.node("empty", label="L'arbre est vide.")
        return dot.source  

    queue = deque([self.root])

    level_positions = {}

    while queue:
        current_level = []
        next_level = []

        while queue:
            node = queue.popleft()
            node_id = str(id(node))

            current_level.append((node_id, node))

            if not isinstance(node, Leaf):
                for child in node.values:
                    child_id = str(id(child))
                    dot.edge(node_id, child_id)
                    next_level.append(child)

       
        level_positions[len(level_positions)] = current_level

        queue.extend(next_level)

    
    for level, nodes in level_positions.items():
        with dot.subgraph() as subgraph:
            subgraph.attr(rank='same')  
            for i, (node_id, node) in enumerate(nodes):
                if isinstance(node, Leaf):
                  
                    leaf_label = ", ".join(map(str, node.keys))
                    if i == 0:  
                        subgraph.node(node_id, label=leaf_label, shape='box', width='0.1')
                    else:
                        subgraph.node(node_id, label=leaf_label, shape='box')
                else:

                    internal_label = ", ".join(map(str, node.keys))
                    subgraph.node(node_id, label=internal_label)

   
    for nodes in level_positions.values():
        leaf_nodes = [node_id for node_id, node in nodes if isinstance(node, Leaf)]
        for i in range(len(leaf_nodes) - 1):
            dot.edge(leaf_nodes[i], leaf_nodes[i + 1], dir='both', arrowhead='vee')

    return dot.source  


def demo():
    bplustree = BPlusTree()
    connection = database_connection()
    print(fetch_year_from_database(connection))
    random_list = fetch_year_from_database(connection)
    for i in random_list:
        bplustree[i] = 'test' + str(i)
        print('Insert ' + str(i))
        bplustree.show
    
    dot_code = to_dot(bplustree)

    with open("bplustree.dot", "w") as f:
        f.write(dot_code)

    os.system("dot -Tpng bplustree.dot -o bplustree.png")

    
   
def generating_arbre():
    bplustree = BPlusTree()
    connection = database_connection()
    print(fetch_year_from_database(connection))
    random_list = fetch_year_from_database(connection)
    for i in random_list:
        bplustree[i] = 'test' + str(i)
        print('Insert ' + str(i))
        bplustree.show
    
    dot_code = to_dot(bplustree)

    with open("bplustree.dot", "w") as f:
        f.write(dot_code)

    os.system("dot -Tpng bplustree.dot -o bplustree.png")

def insert_item_arbre(title , author,year , genre):
  
    connection = database_connection()
    insert_book(connection, title, author, year, genre)
    generating_arbre()

def delete_arbre(delete_entry):
    year = delete_entry
    connection = database_connection()
    delete_book_year(connection, year)
    generating_arbre()