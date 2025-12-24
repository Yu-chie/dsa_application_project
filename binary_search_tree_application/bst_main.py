import tkinter as tk
import random

class Node:
    def __init__(self, data):
        self.n_left = None
        self.n_val = data
        self.n_right = None

class BSTree:
    def __init__(self, countnode):
        if not isinstance(countnode, int):
            raise TypeError("Enter a valid number between 10 to 30 only")
        if countnode < 10 or countnode > 30:
            raise ValueError("Enter a valid number between 10 to 30 only")
        
        self.countnode = countnode
    
    def create_node(self, value):
        return Node(value)
    
    def node_child(self, node, value):
        if node == None:
            return self.create_node(value)
        
        if value <= node.n_val:                                    # duplicates will automatically be on the left child (as per sir)
            node.n_left = self.node_child(node.n_left, value)
        else:
            node.n_right = self.node_child(node.n_right, value)
        
        return node

class BSTMaker:
    pass

# if __name__ == "__main__":