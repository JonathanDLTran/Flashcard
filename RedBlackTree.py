class RedBlackTree:
    """
    Invariant: Color: Black is True, Red is False
    """
    
    def __init__(self, value, color = True, left = None, right = None):
        self.nodeValue = value
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
        self.binaryInsert(value)
        


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