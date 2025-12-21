import tkinter as tk

# for user input of node levels and other inputs
def user_input():
    levels = input("Preferred Binary Tree Level: ")
    
    
    if levels == 1:
        print("You have 1 node")
        
    elif levels == 2:
        print("You have 3 nodes")

    elif levels == 3:
        print("You have 7 nodes")
    
    elif levels == 4:
        print("You have 15 nodes")
    
    elif levels == 5:
        print("You have 31 nodes")        

# class to make nodes
class Node:
    def __init__(self, value):
        self.n_left = None
        self.n_val = value
        self.n_right = None

# class to make the tree - connections of nodes
class Tree:
    pass

# class for determining tree traversals
class Traversal:
    pass

# class for tkinter implementation
class BTMaker:
    pass