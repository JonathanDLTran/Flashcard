
class RedBlackTree:
    """
    Color Invariant: Color: Black is True, Red is False
    Class Invariant: The top node of every red back tree is always black,
    moreover, there are never two white nodes in a row. Finally, the number
    of black nodes from the root to ANY leaf is always the same
    """
    
    def __init__(self, value, color = True, parent = None, left = None, right = None):
        self.nodeValue = value
        self.parentNode = parent
        self.leftTree = left
        self.rightTree = right
        self.nodeColor = color
        
    def addLeftTree(self, left):
        self.leftTree = left
        
    def addRightTree(self, right):
        self.rightTree = right
        
    def binaryInsert(self, value):
        topValue = self.nodeValue
        if value < topValue:
            leftNode = self.leftTree
            if leftNode == None:
                newRB = RedBlackTree(value)
                self.leftTree = newRB
            else:
                leftNode.binaryInsert(value)
        else:
            rightNode = self.rightTree
            if rightNode == None:
                newRB = RedBlackTree(value)
                self.rightTree = newRB
            else:
                rightNode.binaryInsert(value)         
    

    def redBlackInsert(self, value):
        #TODO : implement algorithm
        self.binaryInsert(value)
        
        
    
    def determineChild(self, node, child):
        """
        True if right node is the child, False if left node is the child
        Requires: Child is one of either the left or right subtrees of node
        Requires: Node and Child are not None, and node is a parent node of child
        """
        return node.rightTree.nodeValue == child
        
        
    def left_rotate(self, centerNode):
        """
        Performs a left rotation around the central node 
        """
        parent = centerNode.parentNode
        direction = self.determineChild(parent, centerNode)
        right = centerNode.rightTree
        left = centerNode.leftTree
        rightL = right.leftTree
        
        
        if direction:
            parent.rightTree = right
            right.leftTree = left
            
            
            
        
        
        

    def right_rotate(self):
        pass

        


rb = RedBlackTree(0)
assert rb.nodeValue == 0
left = RedBlackTree(1)
rb.addLeftTree(left)
assert rb.leftTree == left
right = RedBlackTree(-1)
rb.addRightTree(right)
assert rb.rightTree == right

rb = RedBlackTree(10)
rb.binaryInsert(7) 
assert rb.leftTree.nodeValue == 7
rb.binaryInsert(12)
assert rb.rightTree.nodeValue == 12
rb.binaryInsert(14)
assert rb.rightTree.rightTree.nodeValue == 14