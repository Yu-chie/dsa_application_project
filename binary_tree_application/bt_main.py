import tkinter as tk
                
# class to make nodes
class Node:
    def __init__(self, data):
        self.n_left = None
        self.n_val = data
        self.n_right = None

# class to make the tree - connections of nodes
class Tree:
    def __init__(self, levels):
        if not isinstance(levels, int):                                          # checks if user input is correct
            raise TypeError("Enter a valid number between 1 to 5 only")
        if levels < 1 or levels > 5:
            raise ValueError("Enter a valid number between 1 to 5 only")
        
        self.levels = levels                                                     # will get value if correct input
        
    # build tree
    def create_node(self, value):                                     # create node object
        return Node(value)
    
    def node_child(self, node, value):
        if node == None:
            return self.create_node(value)
        
        

# class for determining tree traversals
class Traversal:
    pass

# class for tkinter implementation
class BTMaker:
    pass

# if __name__ == "__main__":
    