class Node:
    def __init__(self, value):
        self.left = None
        self.value = value
        self.right = None

class BSTree:
    def __init__(self, max_node):
        self.root = None
        self.max_node = max_node
        self.n_count = 0
      
    # error handling for insert  
    def ctrl_insert(self, value):
        if self.n_count >= self.max_node:
            raise OverflowError("Your tree is already full!")
        
        self.root = self.insert_node(self.root, value)
        self.n_count += 1
        
    # build tree
    def insert_node(self, node, value):
        if node is None:
            return Node(value)
        
        if value <= node.value:
            node.left = self.insert_node(node.left, value)
        else:
            node.right = self.insert_node(node.right, value)
            
        return node
    
    # LTR (inorder) traversal
    def trav_inorder(self, node, inorder=None):
        if inorder is None:
            inorder = []
        
        if node:
            self.trav_inorder(node.left, inorder)
            inorder.append(node.value)
            self.trav_inorder(node.right, inorder)
        
        return inorder