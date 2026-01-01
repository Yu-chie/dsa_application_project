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
        self.levels = levels                                                     # will get value if correct input
        self.max_node = (2 ** self.levels) - 1
        self.n_count = 0
        
    # build tree
    def create_node(self, value):                                     # create node object
        return Node(value)
    
    def node_child(self, node, value):                                # make left and right child
        if value == ".":
            return None
        
        if node == None:
            return self.create_node(value)
        
        if node.n_left is None:
            node.n_left = self.create_node(value)
        
        elif node.n_right is None:
            node.n_right = self.create_node(value)
            
        else: 
            self.node_child(node.n_left, value)
            self.node_child(node.n_right, value)
        
        return node
    
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
    