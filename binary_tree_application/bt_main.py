import tkinter as tk

# for user input of node levels and other inputs
def user_input():
    try:
        levels = int(input("Preferred Binary Tree Level (1-5): "))
        
        if levels < 1 or levels > 5:
            raise ValueError
        
    except ValueError: 
        print("Please enter a valid number between 1 to 5.")
    
    else:
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

if __name__ == "__main__":
    user_input()