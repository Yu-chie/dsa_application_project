import tkinter as tk
                
# class to make nodes
class Node:
    def __init__(self, value):
        self.value = value

# class to make the tree - connections of nodes
class Tree:
    def __init__(self, levels):
        self.levels = levels                                                     # will get value if correct input
        self.max_node = (2 ** self.levels) - 1
        self.node = [None] * self.max_node
        self.n_count = 0
        
    # build tree
    def insert_node(self, value):
        if self.n_count >= self.max_node:
            raise OverflowError("Your tree is already full")
        
        self.node[self.n_count] = Node(value)
        self.n_count += 1
    
    # for traversing preorder (TLR)
    def trav_preorder(self, root):
        if root is not None:
            print(root.n_val)
            self.trav_preorder(root.n_left)
            self.trav_preorder(root.n_right)
        
    # for traversing inorder (LTR)
    def trav_inorder(self, root):
        if root is not None:
            self.trav_inorder(root.n_left)
            print(root.n_val)
            self.trav_inorder(root.n_right)
    
    # for traversing postorder (LRT)
    def trav_postorder(self, root):
        if root is not None:
            self.trav_postorder(root.n_left)
            self.trav_postorder(root.n_right)
            print(root.n_val)

# class for tkinter implementation
class BTMaker:
    pass

# if __name__ == "__main__":
    