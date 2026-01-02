# class to make nodes
class Node:
    def __init__(self, value, empty_node=False):
        self.value = value
        self.empty_node = empty_node

# class to make the tree - connections of nodes
class Tree:
    def __init__(self, levels):
        self.levels = levels                                                     # will get value if correct input
        self.max_node = (2 ** self.levels) - 1
        self.node = [None] * self.max_node
        self.n_count = 0
        
        # queue for index that can accept input
        self.valid_queue = [0]
        
    # build tree
    def insert_node(self, value):
        if not self.valid_queue:
            raise OverflowError("Your tree is already full")
        
        index = self.valid_queue.pop(0)
        
        # for empty node
        if value == "." or value == "":
            self.node[index] = Node("", empty_node=True)
            return
        
        self.node[index] = Node(value)
            
        n_left = 2 * index + 1
        n_right = 2 * index + 2
        
        if n_left < self.max_node:
            self.valid_queue.append(n_left)
        if n_right < self.max_node:
            self.valid_queue.append(n_right)
    
    # for traversing preorder (TLR)
    def trav_preorder(self, index=0, preorder=None):
        if preorder is None:
            preorder = []
            
        if index >= len(self.node):
            return preorder
        
        node = self.node[index]
        if node is None or node.empty_node:
            return preorder
        
        preorder.append(node.value)
        self.trav_preorder(2 * index + 1, preorder)
        self.trav_preorder(2 * index + 2, preorder)
        
        return preorder
        
    # for traversing inorder (LTR)
    def trav_inorder(self, index=0, inorder=None):
        if inorder is None:
            inorder = []
            
        if index >= len(self.node):
            return inorder
        
        node = self.node[index]
        if node is None or node.empty_node:
            return inorder
        
        self.trav_preorder(2 * index + 1, inorder)
        inorder.append(node.value)
        self.trav_preorder(2 * index + 2, inorder)
        
        return inorder
    
    # for traversing postorder (LRT)
    def trav_postorder(self, index=0, postorder=None):
        if postorder is None:
            postorder = []
            
        if index >= len(self.node):
            return postorder
        
        node = self.node[index]
        if node is None or node.empty_node:
            return postorder
        
        self.trav_postorder(2 * index + 1, postorder)
        self.trav_postorder(2 * index + 2, postorder)
        postorder.append(node.value)
        
        return postorder